import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class Funk_SVD(object):
    def __init__(self, path, USER_NUM, ITEM_NUM, FACTOR):
        super(Funk_SVD, self).__init__()
        self.path = path
        self.USER_NUM = USER_NUM
        self.ITEM_NUM = ITEM_NUM
        self.FACTOR = FACTOR
        self.init_model()

    def load_data(self, flag='train', sep=' ', random_state=0, size=0.8):
        np.random.seed(random_state)
        f = open('data/test_translate.data')
        for index, line in enumerate(f):
            if index == 0:
                continue
            rand_num = np.random.rand()
            if flag == 'train':
                if rand_num < size:
                    try:
                        u, i, r, t = line.strip('\r\n').split(sep)
                    except:
                        continue
                    if r == '':
                        continue
                    yield (int(u) - 1, int(i) - 1, float(r))
            else:
                if rand_num >= size:

                    try:
                        u, i, r, t = line.strip('\r\n').split(sep)
                    except:
                        continue

                    if r == '':
                        continue

                    yield (int(u) - 1, int(i) - 1, float(r))

    def init_model(self):
        self.P = np.random.rand(self.USER_NUM, self.FACTOR) / (self.FACTOR ** 0.5)
        self.Q = np.random.rand(self.ITEM_NUM, self.FACTOR) / (self.FACTOR ** 0.5)


    def train(self, epochs=4, theta=1e-4, alpha=0.0018, beta=0.01):  # 500
        old_e = 0.0
        self.cost_of_epoch = []
        for epoch in range(epochs):  # SGD
            print("current epoch is {}".format(epoch))
            current_e = 0.0
            train_data = self.load_data(flag='train')  # reload the train data every iteration(generator)
            for index, d in enumerate(train_data):
                u, i, r = d
                pr = np.dot(self.P[u], self.Q[i])
                err = r - pr
                current_e += pow(err, 2)  # loss term
                self.P[u] += alpha * (err * self.Q[i] - beta * self.P[u])
                self.Q[i] += alpha * (err * self.P[u] - beta * self.Q[i])

                current_e += (beta / 2) * (sum(pow(self.P[u], 2)) + sum(pow(self.Q[i], 2)))  # 正则项
            self.cost_of_epoch.append(current_e)
            print('cost is {}'.format(current_e))
            if abs(current_e - old_e) < theta:
                break
            old_e = current_e
            alpha *= 0.9

    def predict_rating(self, user_id, item_id):
        pr = np.dot(self.P[user_id], self.Q[item_id])
        return pr

    def recommand_list(self, user, k = 5):
        user_id = user - 1
        user_items = {}
        for item_id in range(self.ITEM_NUM):
            user_had_look = {}
            user_had_look = self.user_had_look_in_train()
            if item_id in user_had_look[user]:
                continue
            pr = self.predict_rating(user_id, item_id)
            user_items[item_id] = pr
        items = sorted(user_items.items(), key=lambda x: x[1], reverse=True)[:k]
        return items

    def user_had_look_in_train(self):
        user_had_look = {}
        train_data = self.load_data(flag='train')
        for index, d in enumerate(train_data):
            u, i, r = d
            user_had_look.setdefault(u, {})
            user_had_look[u][i] = r
        return user_had_look

    def test_rmse(self):
        rmse = .0
        num = 0
        test_data = self.load_data(flag='test')
        for index, d in enumerate(test_data):
            num = index + 1
            u, i, r = d
            pr = np.dot(self.P[u], self.Q[i])
            rmse += pow((r - pr), 2)
        rmse = (rmse / num) ** 0.5
        return rmse

    def show(self):
        nums = range(len(self.cost_of_epoch))
        plt.plot(nums, self.cost_of_epoch, label='cost value')
        plt.xlabel('# of epoch')
        plt.ylabel('cost')
        plt.legend()
        plt.show()
        pass

    def save_model(self):
        data_dict = {'P': self.P, 'Q': self.Q}
        f = open('funk-svd.pkl', 'wb')
        pickle.dump(data_dict, f)
        pass

    def read_model(self):
        f = open('funk-svd.pkl', 'rb')
        model = pickle.load(f)
        self.P = model['P']
        self.Q = model['Q']
        pass


def transf(game_items):
    f = open('data/game.data', encoding='UTF-8')
    game_list = {}
    game_list_recommand = {}
    for line in f:
        (game, num) = line.split(' ')
        num = num.split('\n')
        game_list.setdefault(num[0], game)
    sum = 0
    for i in game_items:
        game_list_recommand.setdefault(game_list[str(game_items[sum][0])], game_items[sum][1])
        sum += 1
    return game_list_recommand

def trans_to_num(user_name):
    f = open('data/user.data', encoding='UTF-8')
    for line in f:
        (u, num) = line.split(' ')
        num = num.split('\n')
        if user_name == u:
            return num[0]

def main():
    start = time.time()
    print("training model...")
    mf = Funk_SVD('data/test_translate.data', 87459, 501, 10)  # path,user_num,item_num,factor
    mf.train()
    mf.save_model()
    rmse = mf.test_rmse()
    print("rmse:", rmse)
    print("Model training completed!")
    print("please input the people who you what to recommand game to him/she:")
    while 1:
        a = input()
        a = int(trans_to_num(a))
        if a:
            break
        else:
            print("con't find that user,please try again:")
    print("generating recommand list,please wait...")
    game_items = mf.recommand_list(a)
    game_items = transf(game_items)
    table = PrettyTable(["game","predic_rating"])
    for i in game_items.keys():
        table.add_row([str(i),str(game_items[i])])
    print(table)
    end = time.time()
    cost = end - start
    print("timecost: " + str(cost) + " second")
