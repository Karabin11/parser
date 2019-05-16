import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
import urllib.error
'''
Не парсить!!!
'''
def get_html(url, headers):
    try:
        s = requests.Session()
        r = s.get(url, headers=headers)
    except requests.ConnectionError:
        return
    if r.status_code < 400:
        print('--------------------------------------------------------------------')
        print(r.status_code)
        print(r.text)
        return r.text
def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_count = soup.find('div', class_='pager rel clr')
    print(int(pages_count.find_all('a')[-2].text))
    return int(pages_count.find_all('a')[-2].text)

def get_page_links(html):
    soup = BeautifulSoup(html, 'lxml')
    print('--------------------------------------------------------------------')
    # print(soup)
    divs = soup.find('div', class_='content').find_all('tr', class_='wrap')#('div', class_='space rel')
    print('--------------------------------------------------------------------')
    print(divs[0])
    links = []
    for div in divs:
        a = div.find('div', class_="space rel").find('a').get('href')
        links.append(a)
    return links
def parse_advert(html):
    pass



def main():
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.84'
               }
    base_url = 'https://www.olx.ua/uk/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/apple/q-iphone-xs-max/?search%5Bfilter_enum_mobile_phone_diagonal%5D%5B0%5D=3&search%5Bfilter_enum_mobile_phone_diagonal%5D%5B1%5D=4&search%5Bfilter_enum_mobile_phone_diagonal%5D%5B2%5D=5&search%5Bfilter_enum_mobile_phone_diagonal%5D%5B3%5D=6&search%5Bprivate_business%5D=private&search%5Border%5D=filter_float_price%3Aasc'

    num_of_pages = get_page_count(get_html(base_url, headers))
    all_links = []
    for page in range(1, num_of_pages + 1):
        page_url = base_url + '&page=' + str(page)
        page_links = get_page_links(get_html(page_url, headers))
        for i in page_links:
            all_links.append(i)
    print(len(all_links))
    print(all_links[:5])


    # print(pages_count, page_url)




if __name__ == '__main__':
    main()