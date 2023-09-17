import requests
from bs4 import BeautifulSoup
import re
import PIL.Image
from brisque import BRISQUE

obj = BRISQUE(url=False)

path = '/Users/kangbeenko/Desktop/GitHub_Repository/dangmoog-ai/original-scaled-image.jpg'
img = PIL.Image.open(path)



product = '농구공'
alpha = round(obj.score(img)/100, 3)

# 웹 페이지의 URL 설정
url = f'https://web.joongna.com/search-price/{product}?'

response = requests.post(url)

# 응답 받은 HTML을 파싱
soup = BeautifulSoup(response.text, 'html.parser')

mean_price_div = soup.find('div', class_='graphTitle')
lower_price_span = soup.find('span', {'class': 'text-blue-500'})

mean_price = mean_price_div.find('p').text.strip()
lower_price = lower_price_span.find('span', {'class': 'font-bold'}).text.strip()

mean_price = re.findall(r'\d+', mean_price)
lower_price = re.findall(r'\d+', lower_price)

mean_price = int(''.join(mean_price))
lower_price = int(''.join(lower_price))

# price algorithm - will be modified
result = (1-alpha) * mean_price + alpha * lower_price
result = int(round(result, -1))

print(result)
