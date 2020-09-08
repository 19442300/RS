import numpy as np
import prettytable as pt
import math

def load_data():
    f = open('data/ini.data', encoding='UTF-8')
    user_list = {}
    for line in f:
        try:
            (user, game, rating, time) = line.split('\t')
        except:
            print("1")
            continue
        try:
            rating = int(rating)
        except:
            continue
        user_list.setdefault(user, {})
        user_list[user][game] = int(rating)
    return user_list
def calculate(user):
    list = load_data()
    user_diff = {}
    for games in list[user]:
        for people in list.keys():
            user_diff.setdefault(people,{})
            for item in list[people]:
                if item == games:
                    diff = math.sqrt(pow(list[user][games] - list[people][item],2))
                    user_diff[people][item] = diff
    return user_diff
def people_rating(user):
    user_diff = calculate(user)
    rating = {}
    sum = 0
    for people in user_diff.keys():
        rating.setdefault(people, {})
        a = 0
        b = 0
        for score in user_diff[people].values():
            a += score
            b += 1
        if a == b == 0:
            continue
        rating[people] = float(1/(1+(a/b)))
    return rating
def top_list(user):
    list = people_rating(user)
    items = list.items()
    top = []
    for v in items:
        if v[1] == {}:
            continue
        top.append([v[1], v[0]])
    top.sort(reverse=True)
    return top[0:10]
def find_rec(user,iter):
    rec_list = top_list(user)
    first = rec_list[iter][1]
    second = rec_list[iter+1][1]
    all_list = load_data()
    rs_list = []
    final_list = []
    for k, v in all_list[first].items():#k->key,v->value
        if k not in all_list[user].keys() and v >= 9:
            rs_list.append(k)
    for k, v in all_list[second].items():
        if k not in all_list[user].keys() and v >= 9:
            if exists(k, rs_list) == 1:
                final_list.append(k)
    if final_list:
        return final_list
    elif rs_list:
        return rs_list
    else:
        print("iteration:" + str(iter))
        a = find_rec(user, iter+1)
        return a

def exists(x,list):
    flag = 0
    for i in list:
        if i == x:
            flag = 1
    return flag

def test_data():
    test_data_file_name = 'data/test.data'
    with open(test_data_file_name, "a+") as f:
        f.writelines(contant)
        f.writelines("\n")


def main():
    print('Loading,Please wait.......')
    print("please input the people who you what to recommand to him/she:" + '\n')
    user = input()
    a = find_rec(user,1)
    if a:
        print(a)


