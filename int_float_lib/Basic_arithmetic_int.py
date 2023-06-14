import math
import copy
import sys
import pdb
# pdb.set_trace()



#最初の桁は符号の予定,プラスなら0,マイナスなら-
def str_to_list(nums):
    numlist = []
    sign = nums[0]
    # a = 0
    if sign == '-':
        pass
    elif sign == '+':
        pass
    else:
        sign = '+'
    for n in nums.lstrip('+-'):
        numlist += [int(n)]  #[int()]を消すとnumlistに'数字'で保存される。[]を忘れるとエラーになる。
    numlist.insert(0,sign)
    return numlist


def list_to_str(numlist):
    nums = ''
    for i in range(len(numlist)):
        nums += str(numlist[i])
    return nums


def addition(numlist_a, numlist_b):
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    if asign == '+' and bsign == '-':
        numlist_b[0] = '+'
        return subtraction(numlist_a,numlist_b)
    elif asign == '-' and bsign == '+':
        numlist_b[0] = '-'
        return subtraction(numlist_a,numlist_b)
    elif asign == '+':
        sign = '+'
    elif bsign == '-':
        sign = '-'
    else:
        exit('error in addition function')
    del numlist_a[0]
    del numlist_b[0]
    N = max(len(numlist_a), len(numlist_b))
    diff = len(numlist_a) - len(numlist_b)
    if diff > 0:
        numlist_b = [0] * diff + numlist_b
    elif diff < 0:
        numlist_a[:0] = [0] * abs(diff)
    else:
        pass
    numlist_ans = []
    for i in range(N):
        numlist_ans.append((int(numlist_a[i]) + int(numlist_b[i])))
    numlist_ans.insert(0,sign)
    return carry_updown(numlist_ans)


def subtraction(numlist_a, numlist_b):
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    compa = comparison(numlist_a, numlist_b)
    if asign == '+' and bsign == '-':
        numlist_b[0] = '+'
        return addition(numlist_a, numlist_b)
    elif asign == '-' and bsign == '+':
        numlist_b[0] = '-'
        return addition(numlist_a, numlist_b)
    elif compa == 0:
        return [0]
    elif compa > 0:
        sign = '+'
        if asign == '-':
            temp = numlist_a
            numlist_a = numlist_b
            numlist_b = temp
        else:
            pass
    elif compa < 0:
        sign = '-'
        if asign == '+':
            temp = numlist_a
            numlist_a = numlist_b
            numlist_b = temp
        else:
            pass
    else:
        exit('error in subtraction :  something went wrong')
    
    del numlist_a[0]
    del numlist_b[0]
    N = max(len(numlist_a), len(numlist_b))
    diff = len(numlist_a) - len(numlist_b)
    if diff > 0:
        numlist_b = [0] * diff + numlist_b
    elif diff < 0:
        numlist_a[:0] = [0] * abs(diff)
    else:
        pass
    numlist_ans = []
    for i in range(N):
        numlist_ans.append((int(numlist_a[i]) - int(numlist_b[i]))) 
    numlist_ans.insert(0,sign)
    return carry_updown(numlist_ans)


def carry_updown(numlist):
    sign = numlist[0]
    del numlist[0]
    N = len(numlist)
    for i in range(N-1,0,-1):
        if numlist[i] >= 10: #carry up
            K = numlist[i] // 10
            numlist[i] -= K * 10
            numlist[i-1] += K
        elif numlist[i] < 0: #carry down 結局桁上がりも下がりも同じアルゴリズム
            K = numlist[i] // 10
            numlist[i] -= K * 10
            numlist[i-1] += K
        else:
            pass

    while numlist[0] >= 10: #最上位桁の要素数増やし
        K = numlist[0] // 10
        numlist = [0] + numlist
        numlist[1] -= K * 10
        numlist[0] += K

    while len(numlist) > 1 and numlist[0] == 0: #最上位桁の要素数減らし
        del numlist[0]

    numlist.insert(0, sign)

    return numlist


def multiplication(numlist_a, numlist_b):
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    if asign == '+' and bsign == '+' or asign == '-' and bsign == '-':
        sign = '+'
    elif asign == '+' and bsign == '-' or asign == '-' and bsign == '+':
        sign = '-'
    del numlist_a[0]
    del numlist_b[0]

    Na = len(numlist_a)
    Nb = len(numlist_b)
    numlist_ans = [0] * (Na + Nb - 1)
    for i in range(Na):
        for j in range(Nb):
            numlist_ans[i+j] += numlist_a[i] * numlist_b[j]

    numlist_ans.insert(0,sign)
    return carry_updown(numlist_ans)


def comparison(numlist_a, numlist_b):
    asign = numlist_a[0]
    bsign = numlist_b[0]
    sign = ''
    if asign == '+' and bsign == '-':
        return +1
    elif asign == '-' and bsign == '+':
        return -1
    elif asign not in ['+','-'] or bsign not in ['+','-']:
        exit('error in comparison : sign missing')
    elif asign == '+':
        sign = '+'
    elif asign == '-':
        sign = '-'

    del numlist_a[0]
    del numlist_b[0]
    sign_reverse = 1

    if sign == '+':
        pass
    elif sign == '-':
        sign_reverse = -1
    else:
        exit('error in comparison')

    Na = len(numlist_a)
    Nb = len(numlist_b)
    for i in range(Na):
        if numlist_a[0] == 0:
            del numlist_a[0]
        else:
            break
    for i in range(Nb):
        if numlist_b[0] == 0:
            del numlist_b[0]
        else:
            break
    Na = len(numlist_a)
    Nb = len(numlist_b)
    if Na > Nb:
        numlist_a.insert(0,sign)
        numlist_b.insert(0,sign)
        return +1 * sign_reverse
    elif Na < Nb:
        numlist_a.insert(0,sign)
        numlist_b.insert(0,sign)
        return -1 * sign_reverse
    if Na == Nb:
        for i in range(Na):
            if numlist_a[i] > numlist_b[i]:
                numlist_a.insert(0,sign)
                numlist_b.insert(0,sign)
                return +1 * sign_reverse
            elif numlist_a[i] < numlist_b[i]:
                numlist_a.insert(0,sign)
                numlist_b.insert(0,sign)
                return -1 * sign_reverse
            else:
                pass
    return 0


def devision(numlist_a, numlist_b):
    # pdb.set_trace()
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    if asign == '+' and bsign == '+' or asign == '-' and bsign == '-':
        sign = '+'
    elif asign == '+' and bsign == '-' or asign == '-' and bsign == '+':
        sign = '-'
    del numlist_a[0]
    del numlist_b[0]

    if comparison(['+']+numlist_a, ['+']+numlist_b) < 0:
        remain = numlist_b
        return [0]
    else:
        Na = len(numlist_a)
        Nb = len(numlist_b)

        # ステップ1　:　Dは a / b の商の桁数
        D = Na - Nb
        digi_diff = numlist_a[:Nb] # aの上位Nb桁
        if comparison(['+']+digi_diff, ['+']+numlist_b) >= 0: # aとbの大小でDが変わる。
            D = Na - Nb + 1
        # ステップ2　：　a / b の筆算のアルゴリズム
        if D == 0:
            return [0] # 商がゼロ
        remain = numlist_a[:(Na-D+1)]
        numlist_ans = [0] * D
        for i in range(D):
            numlist_ans[i] = 9
            for j in range(1,10,1):
                x = multiplication(['+']+numlist_b, ['+']+[j])
                del x[0]
                if comparison(['+']+x, ['+']+remain) == 1:
                    numlist_ans[i] = j - 1
                    break
                
            tmp = multiplication(['+']+numlist_b, ['+']+[numlist_ans[i]])
            remain = subtraction(['+']+remain, tmp)
            del remain[0] #delete sign
            if i < D-1:
                remain += [numlist_a[Na-D+1+i]] #[]を忘れるとnotiterableになる。
                if remain[0] == 0:
                    del remain[0]
        numlist_ans.insert(0,sign)
        return numlist_ans        


def interaction():
    numinp1 = 0 
    numinp2 = 0 
    while True: 
        numinp1 = input('input a first integer >>>  ')
        if type(numinp1) is str:
            break
    while True:
        numinp2 = input('input a second integer >>>  ')
        if type(numinp2) is str:
            break
    print('what operation do you want?')
    while True:
        which = input('1: addition,  2: subtraction,  3: multiplication,  4: devision >>>  ')
        if which in ['1','2','3','4']:
            break
        else:
            print('only 1, 2, 3 or 4')
    inplist1 = str_to_list(numinp1)
    inplist2 = str_to_list(numinp2)
    if which == '1':
        print(list_to_str(addition(inplist1,inplist2)))
    elif which == '2':
        print(list_to_str(subtraction(inplist1,inplist2)))
    elif which == '3':
        print(list_to_str(multiplication(inplist1,inplist2)))
    elif which == '4':
        print(list_to_str(devision(inplist1,inplist2)))
    else :
        print('ERROR : something went wrong...')


def show(numlist):
    numlist = carry_updown(numlist)
    if numlist[0] == '+':
        del numlist[0]
    print(list_to_str(numlist))



# num1 = '99999'
# num2 = '2'
# num3 = '-35184572379'
# testlist1 = [97,45,2,3,67,3,3,74,51]
# testlist2 = [0,0,1,2,3,4,5,6,7,8,9]
# 
# numlist1 = str_to_list(num1)
# numlist2 = str_to_list(num2)
# numlist3 = str_to_list(num3)

# show(addition(numlist1,numlist2))
# print(subtraction(numlist1, numlist2))
# print(multiplication(numlist1, numlist2))
# print(comparison(numlist3,numlist3))
# print(comparison([0,0,0,0,0,1,2],[1,2]))
# print(numlist1, numlist2, numlist3)
# print(list_to_str(numlist1), list_to_str(numlist2))
# print(comparison([1,2],[1,1]))
# print(tj)
# print(devision(numlist1, numlist2))
# show(testlist2)

if __name__ == '__main__':
    interaction()



