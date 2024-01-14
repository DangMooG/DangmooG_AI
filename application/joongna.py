import re
import requests
from bs4 import BeautifulSoup

def scrap_joogna_price(product_name):
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
        return 0, 0