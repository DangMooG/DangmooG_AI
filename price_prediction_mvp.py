import requests
from bs4 import BeautifulSoup
import re

product = '농구공'

# 웹 페이지의 URL 설정
url = f'https://web.joongna.com/search-price/{product}?'

response = requests.post(url)

# 응답 받은 HTML을 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 시세금액을 포함하는 div 요소를 찾기
div_with_price = soup.find('div', class_='graphTitle')

# 시세금액 텍스트 추출
price = div_with_price.find('p').text.strip()
numbers = re.findall(r'\d+', price)

# 추출된 숫자를 하나의 문자열로 합치고 정수로 변환
result = int(''.join(numbers))

print(result)
