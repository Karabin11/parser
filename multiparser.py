from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
import urllib.error
from multiprocessing import Pool
# from urllib.request import urlopen
url = 'http://moviestape.net/katalog_filmiv/'
def get_html(url):
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        return
    if r.status_code < 400:
        return r.text
        # r = requests.get(url)
        # # print(r.text)
        # return r.text
def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    cross_page = soup.find('div', class_='navigation')
    # print (int (cross_page.find_all ('a')[-2].text))
    return int(cross_page.find_all('a')[-2].text)

def parse_link(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='left').find_all('div', class_='bnewmovie')
    links = []
    for div in divs:
        a = div.find('p', class_='title').find('a').get('href')
        links.append(a)
    return links

def parse_film(html):
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='f-box2')
    try:
        name = div.find('h1').text.strip().replace('\u2032', '').replace('/', '')
    except:
        name = ''
    try:
        name_eng = div.find('h3').text.strip().replace('\u2032', '')
    except:
        name_eng = ''
    try:
        content = div.find('div', class_='f-content2').text.replace('\n', '').replace('\u2032', '')
    except:
        content = ''
    try:
        rating = div.find('div', class_='f-content2_r').text.replace('\xa0', '') .replace('\n', '').replace('\u2032','')
    except:
        rating = ''
    try:
        script = div.find('div', class_='f-content2_s').text.strip().replace('\u2032', '')
    except:
        script = ''
    try:
        img_post = div.find('div', class_='f-poster2').find('img').get('src')
    except:
        img_post = ''
    try:
        imgs = div.find('div', class_='f-content2_ss').find_all('img')
    except:
        imgs =[]

    film = {'Назва фільму': name,
            'Назва(англ.)': name_eng,
            'Виробник': content,
            'Рейтинг': rating[15:],
            'Зміст': script,
            'poster': img_post,
            'screens': imgs
            }
    return film
# def clean_data(text):#----------------------- чистка#
#     return text.strip().replace('\u2032', '').replace('\n', '').replace('/', '').replace('\xa0', '')\


def write_csv(film):
    with open('test#1\my_parser.csv', 'a', newline="", encoding="utf-8") as f:  # E:\Testpython\PythonLabs\
        writer = csv.writer(f)
        writer.writerow(
            (film['Назва фільму'],
             film['Назва(англ.)'],
             film['Виробник'],
             film['Рейтинг'],
             film['Зміст']))
    url_img_post = 'http://moviestape.net' + film['poster']
    try:
        urllib.request.urlretrieve(url_img_post, "test#1\№" +'_'
                                                 + film['Назва фільму'].replace(':', '_').replace('(', '_')
                                                 .replace(')', '').replace('?', '_').rstrip()
                                                 + '_poster.jpg')
    except urllib.error.HTTPError:
        print('. Poster not found!!!')  # '№' + str(all_links.index(link)+1) + #<<<
    for i, img in enumerate(film['screens']):
        url_img = 'http://moviestape.net' + img.get('src')
        try:
            urllib.request.urlretrieve(url_img, "test#1\№" +'_'
                                       + film['Назва фільму'].replace(':', '_').replace('(', '_').replace(')', '')
                                       .replace('?', '_').rstrip()
                                       + '_screen_'+str(i + 1)+'.jpg')
        except urllib.error.HTTPError:
            pass
        except urllib.error.URLError:
            pass
def make_all(link):
    html = get_html(link)
    film = parse_film(html)
    write_csv(film)

def main():
    start = datetime.now()
    global all_links
    global link
    all_links = []
    page_count = get_page_count(get_html(url))
    for page in range(1, page_count + 1):
        links = parse_link(get_html(url + 'page/%d/' % page))
        for link in links:
            all_links.append(link)

    # for link in all_links:
    #     html = get_html(link)
    #     film = parse_film(html)
    #     write_csv(film)
    with Pool(40) as p:
        p.map(make_all, all_links)
    finish = datetime.now()
    total = finish - start
    print(total)


if __name__ == '__main__':
    main()
