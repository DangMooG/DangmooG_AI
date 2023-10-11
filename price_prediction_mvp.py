import requests
from bs4 import BeautifulSoup
import re
import PIL.Image
from brisque import BRISQUE

def get_brisque_score(img_path):
    obj = BRISQUE(url=False)
    alpha = round(obj.score(img_path)/100, 3)
    return alpha

def scrapp_joogna(product_name):
    url = f'https://web.joongna.com/search-price/{product_name}?'

    response = requests.post(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        trend_price_div = soup.find('div', class_='graphTitle')
        lower_price_span = soup.find('span', {'class': 'text-blue-500'})    

        trend_price = trend_price_div.find('p').text.strip()
        lower_price = lower_price_span.find('span', {'class': 'font-bold'}).text.strip()

        trend_price = re.findall(r'\d+', trend_price)
        lower_price = re.findall(r'\d+', lower_price)

        lower_price = int(''.join(lower_price))
        trend_price = int(''.join(trend_price))
        trend_price = min(int(round(trend_price, -1)), int(1.5*lower_price))
        return trend_price, lower_price
    except:
        return False
    
def get_rec_price(upper, lower, alpha) -> int:
    recommend_price = (1-alpha) * upper + alpha * lower
    return int(round(recommend_price, -1))

def get_results_list(upper, recommend, lower) -> list:
    results = set([upper, recommend, lower])
    results = sorted(list(results))
    return list(results)

    
"""
if __name__ == '__main__':
    path = './original-scaled-image.jpg'
    img = PIL.Image.open(path)

    product = input()
    alpha = get_brisque_score(img)
    trend_price, lower_price = scrapp_joogna(product)
    recommend_price = get_rec_price(trend_price, lower_price, alpha)
    results = get_results_list(trend_price, recommend_price, lower_price)
    print(results)
"""