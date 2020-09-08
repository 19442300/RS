import rs
import funksvd
if __name__=="__main__":
    sum = 0
    while 1:
        if sum == 0:
            print("Welcome to the recommand system(7630_project)!")
            print("This system has the following 4 function:")
            print("1.Quick recommend(user-base-Lagrange)")
            print("2.Recommendation by predictive scoring(funksvd)")
            print("3.Analyze the type of game the player likes")
            print("4.Analysis of player preferences by game type - by year")
        print("Please select the function you want or exit：")
        sum += 1
        flag = input()
        if flag == '1':
            rs.main()
        elif flag == '2':
            funksvd.main()
        elif flag == '3':
            print("暂未开发！")
        elif flag == '4':
            print("暂未开发！")
        else:
            break



