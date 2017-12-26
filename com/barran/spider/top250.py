# encoding=utf-8
import codecs
from collections import namedtuple
from bs4 import BeautifulSoup
import requests

__author__ = 'tanwei'

top_250_url = 'http://movie.douban.com/top250'

Movie = namedtuple('Movie', ['rank', 'name', 'rating_num'])


def get_page(request_url=top_250_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(request_url, headers=headers).content
    # print(data)
    return data


def parse_content(content, rank_num=1):
    soup = BeautifulSoup(content, "lxml")
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_data_list = []
    for li in movie_list_soup.find_all("li"):
        detail = li.find('div', attrs={'class': 'hd'})
        movie_name = li.find('span', attrs={'class': 'title'}).getText()
        vote = li.find('span', attrs={'class': 'rating_num'}).getText()
        print(rank_num, movie_name, vote)
        movie_data_list.append(Movie(rank_num, movie_name, vote))
        rank_num += 1

    # find next page
    next_url = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_url:
        return movie_data_list, top_250_url + next_url['href']
    else:
        return movie_data_list, None


if __name__ == "__main__":
    url = top_250_url
    rank = 1
    while url:
        data = get_page(url)
        if data:
            movie_list, url = parse_content(data, rank)
            # 'b'表示二进制,'rw'表示读写,'a'表示追加
            # 判断文件是否存在  os.path.isfile("movies")
            if rank == 1:
                write_args = 'wb'
            else:
                write_args = 'a'
            with codecs.open("movies", write_args, encoding='utf-8') as fp:
                for movie in movie_list:
                    fp.write('%d  %s  %s\n' % (movie.rank, movie.name, movie.rating_num))
                    rank += 1