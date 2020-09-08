# -*- coding:utf-8 -*-
# author:Administrator
# datetime:2020/4/8 17:12
# software: PyCharm
# function : None

from urllib import request

from http.client import IncompleteRead
import hashlib
import urllib
import random
import json

from bs4 import BeautifulSoup
import numpy as np
from lxml import etree
import time
import re


class games(object):
    def __init__(self):
        self.game_name = ""
        self.game_device = ""
        self.date = ''
        self.genre = ''
        self.game_score = 0
        self.users = []
        self.users_score = []


from urllib import error


def getHtml(url):
    time.sleep(5)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url, headers=headers)
    try:
        content = request.urlopen(req).read()
    except error.URLError as e:
        print(e.reason)
        time.sleep(10)
        getHtml(url)
    except error.HTTPError as e:
        print(e.reason, e.code, e.headers)
        time.sleep(10)
        getHtml(url)
    except IncompleteRead as e:
        content = e.partial
        content = content.decode('UTF-8')
        if content is None:
            getHtml(url)
        else:
            return content
    except :
        getHtml(url)
    else:
        if content.decode("UTF-8") is None:
            getHtml(url)
        # print(content.decode("UTF-8"))
        else:
            return content.decode("UTF-8")


def getContent(content):

    soup = BeautifulSoup(content, 'lxml')
    urls = soup.find_all(name='div', attrs={'class': 'basic_stat product_title'})
    links = []
    for url in urls:
        link = url.find_all(name='a', href=True)
        links.append(link[0]['href'])
    scores = soup.find_all(name='li', attrs={'class': 'stat product_avguserscore'})
    s = []
    for score in scores:
        pattern = re.compile(r'">(.*?)</span>', re.S)  # 查找数字
        result1 = pattern.findall(str(score).strip("\n"), 50, len(str(score)))
        # print(str(score).strip("\n"), result1[1])
        if result1[1] == 'tbd':
            s.append(str(0))
        else:
            s.append(result1[1])
        # print(s)
    return links, s


def get_date(html, game):
    base_html = "https://www.metacritic.com"
    #print(base_html + html)
    content = getHtml(base_html + html)
    while content is None:
        content = getHtml(base_html + html)
    soup = BeautifulSoup(content, 'lxml')
    data = soup.find_all(name='li', attrs={'class': 'summary_detail release_data'})
    game.date = data[0].find_all(name='span', attrs={'class': 'data'})[0].get_text().replace(',', ' ')
    #data = soup.find_all(name='li', attrs={'class': 'summary_detail product_genre'})
    data = soup.find_all(name='li', attrs={'class': 'summary_detail product_genre'})
    atter = data[0].find_all(name='span', attrs={'class': 'data'})
    string = ''
    for a in atter:
        string += a.get_text() + '- '
    game.genre = string[:-1]


def get_games(html, game):
    base_html = "https://www.metacritic.com/"
    words = html.split("/")
    # print(words)
    game.game_device = words[2]
    game.game_name = words[3].replace("-", "  ")
    content = getHtml(base_html + html + "/user-reviews")
    while content is None:
        content = getHtml(base_html + html + "/user-reviews")
    soup = BeautifulSoup(content, 'lxml')
    last_page = soup.find_all(name='li', attrs={'class': 'page last_page'})
    # print(last_page)
    if len(last_page) > 0:
        pattern = re.compile(r'>(\d+)</a></li>', re.S)  # 查找数字
        #print(last_page)
        result1 = pattern.findall(str(last_page[0]).strip("\n"), 20, len(str(last_page[0])))
        #print(result1)
        nu = result1[0]
        #print(nu)
    users = soup.find_all(name='div', attrs={'class': 'name'})

    for user in users:
        # print(user)
        con = user.find_all(name='a', href=True)
        if len(con) > 0:
            #print(con[0]['href'].split('/')[2])
            game.users.append(con[0]['href'].split('/')[2])
        else:
            con = user.find_all(name='span')
            #print(con)
            game.users.append(con[0].get_text())
    # print(game.users)
    scores = soup.find_all(name='div', attrs={'class': 'review_grade'})

    for score in scores[:-3]:
        pattern = re.compile(r'>(.*?)</div>', re.S)  # 查找数字
        result1 = pattern.findall(str(score), 30, len(str(score)))
        game.users_score.append(result1)
        # print(result1)
    if len(last_page) > 0:
        for i in range(1, int(nu)):
            print("Subpage:"+str(i))
            content = getHtml(base_html + html + "/user-reviews?page=" + str(i))
            while content is None:
                #print(content)
                print(base_html + html + "/user-reviews?page=" + str(i))
                content = getHtml(base_html + html + "/user-reviews?page=" + str(i))
            soup = BeautifulSoup(content, 'lxml')
            users = soup.find_all(name='div', attrs={'class': 'name'})
            for user in users:
                con = user.find_all(name='a', href=True)
                if len(con) > 0:
                    #print(con[0]['href'].split('/')[2])
                    game.users.append(con[0]['href'].split('/')[2])
                else:
                    con = user.find_all(name='span')
                    game.users.append(con[0].get_text())
            # print(game.users)
            scores = soup.find_all(name='div', attrs={'class': 'review_grade'})

            for score in scores[:-3]:
                pattern = re.compile(r'>(.*?)</div>', re.S)  # 查找数字
                result1 = pattern.findall(str(score), 30, len(str(score)))
                game.users_score.append(result1)
                # print(result1)


game_list = []


def main():
    for n in range(173):  # 173 70
        n += 7
        #print(n)
        html = getHtml(
            "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&page=" + str(n))
        while html is None:
            html = getHtml(
                "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&page=" + str(n))

        sublinks, score = getContent(html)
        #print(len(sublinks), '\n', len(score))
        #print(sublinks, score)
        score = score
        for index, link in enumerate(sublinks[:-8]):
            g = games()
            # time.sleep(3)
            print("page:",n,"index:", index)
            g.game_score = np.array(score)[index]
            # print(score, index)

            game = g
            words = link.split("/")
            # print(words)
            game.game_device = words[2]
            game.game_name = words[3].replace("-", "  ")
            get_date(link, game)
            print(game.game_name+" Start!\n")
            if game.game_score == 0:
                f = open("./all_games_re.csv", 'a', encoding='UTF-8')
                string = str(game.game_name) + ',' + \
                         str(game.game_device) + ',' + str(game.date) + ',' + \
                         str(game.genre) + ',' + str(game.game_score) + "\n"
                #print(string)
                f.write(string)
                f.close()
            else:
                get_games(link, g)
                #print(len(game.users), len(game.users_score))
                if len(game.users) != len(game.users_score):
                    numbers = min(len(game.users_score),len(game.users))
                else:
                    numbers = len(game.users)
                if len(game.users) == 0:
                    f = open("./all_games_re.csv", 'a', encoding='UTF-8')
                    string = str(game.game_name) + ',' + \
                             str(game.game_device) + ',' + str(game.date) + ',' + \
                             str(game.genre) + ',' + str(game.game_score) + "\n"
                    #print(string)
                    f.write(string)
                    f.close()
                else:
                    for i in range(numbers):
                        f = open("./all_games_re.csv", 'a', encoding='UTF-8')

                        string = str(game.game_name) + ',' + \
                                 str(game.game_device) + ',' + str(game.date)  + ',' + str(game.genre) +','\
                                 + str(game.game_score) + ',' + str(game.users[i]) \
                                 + ',' + str(game.users_score[i][0]) + '\n'
                        #print(string)
                        f.write(string)
                        f.close()
            print(g.game_name+"Finished!\n")


if __name__ == '__main__':
    main()
