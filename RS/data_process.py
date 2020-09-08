import pandas as pd
def load_user():
    f = open('data/u1.data', encoding='UTF-8')
    user_list = {}
    sum = 0
    for line in f:
        (user, movie, rating, ts) = line.split('\t')
        try:
            if user_list[user]:
                continue
        except:
            sum += 1
            user_list.setdefault(user, sum)
        if rating == '':
            continue
    return user_list

def load_game():
    f = open('data/u1.data', encoding='UTF-8')
    game_list = {}
    sum = 0
    for line in f:
        (user, game, rating, ts) = line.split('\t')
        try:
            if game_list[game]:
                continue
        except:
            sum += 1
            game_list.setdefault(game, sum)
        if rating == '':
            continue
    return game_list

def translate_data(user_list,game_list):
    fp = open('data/u1.data', encoding='UTF-8')
    test_data_file_name = 'data/test_translate.data'
    with open(test_data_file_name,'w') as w:
        for line in fp:
            try:
                (user, game, rating, ts) = line.split('\t')
            except:
                continue
            try:
                rating = int(rating)
            except:
                print(line)
                continue
            user = user_list[user]
            game = game_list[game]

            line = str(user) + ' ' + str(game) + ' ' + str(rating) + ' ' + str(ts) +'\n'
            w.writelines(line)

def v_output():
    fp = open('data/test_translate.data')
    for line in fp:
        print(line)
        (user, movie, rating, ts) = line.split(' ')
        print(user)

def del_null():
    f1 = pd.read_excel('all_games_re_fix.xlsx')
    f1 = f1.dropna()
    f1.to_csv('test_translate.csv')

def query_user_game():
    a = load_user()
    print(len(a.keys()))
    b = load_game()
    print(len(b.keys()))

def data_cleaning():
    del_null()
def create_dic(a,b):
    with open('data/user.data','w', encoding='UTF-8') as w:
        sum = 0
        for line in a:
            sum += 1
            w.writelines(line+' '+str(sum)+'\n')
    with open('data/game.data','w', encoding='UTF-8') as w:
        sum = 0
        for line in b:
            sum += 1
            w.writelines(line+' '+str(sum)+'\n')

def word_to_num():
    a = load_user()
    b = load_game()
    translate_data(a, b)
    create_dic(a,b)

def transf():
    f = open('data/game.data', encoding='UTF-8')
    game_list = {}
    for line in f:
        (game, num) = line.split(' ')
        num = num.split('\n')
        game_list.setdefault(num[0], game)
    print(type(game_list['52']))



if __name__=="__main__":
    a = load_game()
    print(len(a.keys()))
