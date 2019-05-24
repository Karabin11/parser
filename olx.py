import requests
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def  get_html(url, useragent=None, proxy=None):
    try:
        r = requests.get(url, headers=useragent, proxies=proxy)
    except requests.ConnectionError:
        return
    return r.text

def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_count = soup.find('div', class_='pager rel clr')
    return int(pages_count.find_all('a')[-2].text)

def get_page_links(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='content').find_all('tr', class_='wrap')  # ('div', class_='space rel')
    links = []
    for div in divs:
        a = div.find('div', class_="space rel").find('a').get('href')
        links.append(a)
    return links
def get_page_data(link, us_ag):
    options = Options()
    options.headless = True
    options.add_argument(us_ag)
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    print(link)
    try:
        button_cookie = driver.find_element_by_xpath('//*[@id="cookiesBar"]/button')
        button_cookie.click()
    except:
        print('Неможливо знайти елемент: button_cookes!!!')
    try:
        button = driver.find_element_by_xpath('//*[@id="contact_methods"]/li[2]/div')
        button.click()
        sleep(uniform(1,2))
    except:
        print('Не вказаний')
    try:
        tels = driver.find_elements_by_xpath('//*[@id="contact_methods"]/li[2]/div/strong')
        for tel in tels:
            print(tel.text)
    except:
        tels = []
    try:
        title = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[2]/h1').text
        print(title)
    except:
        title = ''
    try:
        price = driver.find_elements_by_xpath('//*[@id="offeractions"]/div[1]/strong').text
        print(price)
    except:
        price = ''
    try:
        loc = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[2]/div[1]/a/strong').text
        print(loc)
    except:
        loc = ''
    try:
        td = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[2]/div[1]/em').text
        print(td)
    except:
        td = ''
    try:
        mod = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[3]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/strong/a').text
        print(mod)
    except:
        mod = ""
    try:
        syst = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[3]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/strong/a').text
        print(syst)
    except:
        syst = ''
    try:
        siz = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[3]/table/tbody/tr[3]/td[1]/table/tbody/tr/td/strong/a').text
        print(siz)
    except:
        siz = ''
    try:
        state = driver.find_element_by_xpath('//*[@id="offerdescription"]/div[3]/table/tbody/tr[3]/td[2]/table/tbody/tr/td/strong/a').text
        print(state)
    except:
        state = ''
    try:
        info = driver.find_element_by_xpath('//*[@id="textContent"]').text
        print(info)
    except:
        info = ''
    driver.quit()





def main():
    start = datetime.now()
    useragents = open('user-agents-utf-8.txt').read().split('\n')
    proxies = open('proxylist-http').read().split('\n')
    base_url = 'https://www.olx.ua/uk/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/apple/q-iphone-xs-max/?search%5Bfilter_enum_mobile_phone_diagonal%5D%5B0%5D=3&search%5Bfilter_enum_mobile_phone_diagonal%5D%5B1%5D=4&search%5Bfilter_enum_mobile_phone_diagonal%5D%5B2%5D=5&search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bprivate_business%5D=private'
    useragent = {'User-Agent': choice(useragents)}
    proxy = {'http': 'http//' + choice(proxies)}
    all_links = []
    pages = get_page_count(get_html(base_url, useragent, proxy))
    print(pages)
    for page in range(1, pages + 1):
        useragent = {'User-Agent': choice(useragents)}
        proxy = {'http': 'http//' + choice(proxies)}
        page_url = base_url + '&page=' + str(page)
        page_html = get_html(page_url, useragent, proxy)
        page_links = get_page_links(page_html)
        for i in page_links:
            if i not in all_links:
                all_links.append(i)
            # print(i)
    print(len(all_links))
    print('...START SELENIUM...')
    for link in all_links[35:40]:
        start_page = datetime.now()
        print('№ ' + str(all_links.index(link)+1))
        us_ag = 'user-agent=' + choice(useragents)
        data = get_page_data(link, us_ag)
        finish_page = datetime.now()
        t = finish_page - start_page
        print('time page: ' + str(t))
        print('------------------------------------')
    finish = datetime.now()
    total =finish - start
    print('Total time:' + str(total))









if __name__ == '__main__':
    main()