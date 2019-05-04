import urllib.request
from bs4 import BeautifulSoup

base_url = 'http://moviestape.net/katalog_filmiv/'


def get_html(url):
    res = urllib.request.urlopen(url)
    return res.read()


def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    cross_page = soup.find('div', class_='navigation')
    # print (int (cross_page.find_all ('a')[-2].text))
    return int(cross_page.find_all('a')[-2].text)


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    div1 = soup.find('div', class_='left')
    div2 = div1.find_all('div', class_='bnewmovie')

    films = []
    for n in div2:
        film = n.find('p', class_='title').text
        rate = n.find('li', class_='current-rating').text
        year = n.find('div', class_='ycc').text[0:4]
        produce = n.find('div', class_='ycc').text[5:].replace ('\xa0', '')
        films.append({'Фільм': film, 'рік': int(year), 'країна': produce, 'Рейтинг': rate + ' відсотків'})
    # for f in films:
    # print (films)
    return films


def main():
    # i = 0
    # for  f in parse(get_html('http://moviestape.net/katalog_filmiv/')):
    #     i += 1
    #     print(i,f)
    # print(parse(get_html('http://moviestape.net/katalog_filmiv/')))
    # print(get_page_count(get_html('http://moviestape.net/katalog_filmiv/')))
    progects = []

    page_count = get_page_count(get_html(base_url))
    for page in range(1, page_count -229):
        # print (base_url + 'page/%d' % page)
        progects.extend(parse(get_html(base_url + 'page/%d/' % page)))

    for progect in progects:
        print(progect)


if __name__ == '__main__':
    main ()
