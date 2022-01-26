import json

import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
def get_links(url):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    list_url_blocks = soup.find_all('div', class_='overlay')
    list_urls = []
    for item in list_url_blocks:
        list_urls.append(f'https://xn--e1ako1a.xn--p1ai{item.findNext().get("href")}')
    with open('list_urls.txt', 'w' ) as file:
        for element in list_urls:
            file.write(f"{element}\n")


def get_data():
    with open('list_urls.txt') as file:
        list_urls = [url.strip() for url in file.readlines()]
    print(list_urls)
    result = []
    with open('nmo.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['section', 'titele', 'duration', 'price', 'cat_students', 'url'])
    for item in tqdm(list_urls):
        response = requests.get(url=item, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            section = soup.find('div', class_='breadcrumbs_block').find_all('a')[2].get('title').strip()
        except:
            section = None
            print(f'section_ERROR at {item}')
        try:
            title = soup.find('h1').text
        except:
            title = None
            print(f'title_ERROR at {item}')

        try:
            duration = soup.find_all('span', class_='big')[0].text.strip()
        except:
            duration = None
            print(f'duration_ERROR at {item}')
        try:
            price = soup.find_all('span', class_='big')[2].text.strip()
        except:
            price = soup.find_all('span', class_='big')[1].text.strip()
        try:
            cat_students = soup.find('table', class_='services-table-def').find_all('p')[1].text.strip().replace('\xa0', '')
        except:
            cat_students = None
            print(f'cat_students_ERROR at {item}')
        url = item
        # print(section)
        # print(title)
        # print(duration)
        # print(price)
        # print(cat_students)
        # print(url)
        curs = {
            'section':section,
            'title':title,
            'duration':duration,
            'price':price,
            'cat_students':cat_students,
            'url':url
        }
        with open('nmo.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([section, title, duration, price, cat_students, url])
        result.append(curs)


    with open('nom.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)











def main():
    # get_links(url='https://xn--e1ako1a.xn--p1ai/uslugi/nmo/')
    get_data()

if __name__ == '__main__':
    main()