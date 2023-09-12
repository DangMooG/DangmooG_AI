import requests
from bs4 import BeautifulSoup
import csv

def scrap_category(url, number):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        target_link = soup.find('a', {'href': f'/search?category={number}'})

        if target_link:
            link_text = target_link.text
            return link_text
        else:
            return None
    else:
        return response.status_code

if __name__ == '__main__':
    url = 'https://web.joongna.com'
    csv_filename = './category_joongna.csv'
    for i in range(101, 262):
        text = scrap_category(url, i)
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([text]) 
