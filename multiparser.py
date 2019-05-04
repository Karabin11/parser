import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import urllib.request
import urllib.error

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
    # print(links)
    return links


def parse_film(html):
    # html = clean_data(html)#---------------- чистка
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
        content = div.find('div', class_='f-content2') \
            .text.replace('\n', '').replace('\u2032', '')
    except:
        content = ''
    try:
        rating = div.find('div', class_='f-content2_r') \
            .text.replace('\xa0', '') \
            .replace('\n', '').replace('\u2032',
                                       '')
    except:
        rating = ''
    try:
        script = div.find('div', class_='f-content2_s').text.strip().replace('\u2032', '')
    except:
        script = ''

    img_post = div.find('div', class_='f-poster2').find('img').get('src')
    url_img_post = 'http://moviestape.net' + img_post
    try:
        urllib.request.urlretrieve(url_img_post, "test#1\№" + str(n) + '_' +
                                   name.replace(':', '_')
                                   .replace('(', '_').replace(')', '')
                                   .replace('?', '_').rstrip() +
                                   '_poster.jpg')
    except urllib.error.HTTPError:
        print('№' + str(n) + '. Poster not found!!!')
    imgs = div.find('div', class_='f-content2_ss').find_all('img')
    for i, img in enumerate(imgs):
        url_img = 'http://moviestape.net' + img.get('src')

        try:
            urllib.request.urlretrieve(url_img, "test#1\№" + str(n) + '_' +
                                       name.replace(':', '_')
                                       .replace('(', '_').replace(')', '')
                                       .replace('?', '_').rstrip() +
                                       '_screen_' + str(i + 1) + '.jpg')
        except urllib.error.HTTPError:
            pass
        except urllib.error.URLError:
            pass

    film = {'Назва фільму': name,
            'Назва(англ.)': name_eng,
            'Виробник': content,
            'Рейтинг': rating[15:],
            'Зміст': script}
    # print(film)
    # name, name_engl, content, rating[15:], descript
    return film
# def clean_data(text):#----------------------- чистка#
#     return text.replace('\u2032', '')#------- чистка#

def write_csv(film):
    with open('test#1\my_parser.csv', 'a', newline="", encoding="utf-8") as f:  # E:\Testpython\PythonLabs\
        writer = csv.writer(f)
        writer.writerow(
            (film['Назва фільму'],
             film['Назва(англ.)'],
             film['Виробник'],
             film['Рейтинг'],
             film['Зміст']))


def main():
    global n
    n = 1
    all_links = []
    page_count = get_page_count(get_html(url))
    for page in range(1,2):# page_count + 1):
        links = parse_link(get_html(url + 'page/%d/' % page))
        for link in links:
            all_links.append(link)

    for num, link in enumerate(all_links):
        html = get_html(link)
        film = parse_film(html)
        n += 1
        # print('№' + str(num + 1) + '.', film['Назва фільму'])
        write_csv(film)
        # with Pool as p:
        #     p.map(make_all, all_links)


if __name__ == '__main__':
    main()
