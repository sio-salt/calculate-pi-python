#
# Arbitrary precision calculator by Kato Yo (last update : Mon Mar 27 19:07:07 JST 2023)
# How to use  -->  python (this script)
#
#




# import sys
import Basic_arithmetic_int as Int
import pdb

#pdb.set_trace()




#最初の桁は符号の予定,プラスなら+,マイナスなら-
def str_to_list(nums):
    sign = nums[0]
    if remove_sign(nums)[0] == '.':
        nums.insert(0,'0')
    if sign not in ['+','-']: sign = '+'
    point_index = find_exponent(nums)   #numlistの形は['+-', 指数部(整数部=0), 小数部, 小数部, ...] の形にこの関数中で行う。
    numlist = [ int(n) for n in remove_sign_point(nums) ]
    if point_index <= 0: del numlist[:1-point_index]
    numlist.insert(0,point_index)
    numlist.insert(0,sign)
    return numlist


def remove_sign_point(nums):
    sign = nums[0]
    if '.' in nums:
        if sign in ['+', '-']:
            return nums.lstrip('+-').replace('.','')
        else:
            return nums.replace('.','')
    else:
        if sign in ['+', '-']:
            return nums.lstrip('+-')
        else:
            return nums


def remove_sign(nums):
    sign = nums[0]
    if sign in ['+', '-']:
        return nums.lstrip('+-')
    else:
        return nums


def find_exponent(nums):
    #pdb.set_trace()
    sign = nums[0]
    if '.' in nums:
        if sign in ['+','-']:
            point_index = nums.lstrip('+-').index('.')
            if point_index == 1:
                while remove_sign_point(nums)[1 - point_index] == '0': point_index -= 1
        else:
            point_index = nums.index('.')
            if point_index == 1:
                while remove_sign_point(nums)[1 - point_index] == '0': point_index -= 1
    else:
        if sign in ['+','-']:
            point_index = len(nums.lstrip('+-'))
        else:
            point_index = len(nums)

    return point_index
            

#def list_to_str(numlist):
#    #pdb.set_trace()
#    sign = numlist[0]
#    expo = numlist[1]
#    numlist.insert(3 + expo,'.')
#    if expo == 0:
#        numlst.insert(2,0)
#    del numlist[1]
#    nums = ''
#    if sign == '+':
#        del numlist[0]
#    for i in range(len(numlist)):
#        nums += str(numlist[i])
#    return nums


def addition(numlist_a, numlist_b):
    #pdb.set_trace()
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    aexpo = numlist_a[1]
    bexpo = numlist_b[1]
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
    del numlist_a[0:2]
    del numlist_b[0:2]
    upper_digit = numlist_a[0:(abs(aexpo - bexpo))] if aexpo > bexpo else numlist_b[0:(abs(aexpo - bexpo))]
    a_decimal = len(numlist_a[0:]) - aexpo
    b_decimal = len(numlist_b[0:]) - bexpo
    lower_digit = numlist_a[b_decimal + aexpo:] if a_decimal > b_decimal else numlist_b[a_decimal + bexpo:]
    if aexpo > bexpo:
        del numlist_a[0:(abs(aexpo - bexpo))]
    else:
        del numlist_b[0:(abs(aexpo - bexpo))]
    if a_decimal > b_decimal:
        del numlist_a[b_decimal + aexpo:]
    else:
        del numlist_b[a_decimal + bexpo:]
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
    maxexpo = max(aexpo,bexpo)
    numlist_ans = upper_digit + numlist_ans + lower_digit
    numlist_ans.insert(0,maxexpo)
    numlist_ans.insert(0,sign)
    return carry_updown(numlist_ans)


def subtraction(numlist_a, numlist_b):
    #pdb.set_trace()
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    aexpo = numlist_a[1]
    bexpo = numlist_b[1]
    compa = comparison(numlist_a, numlist_b)
    #compa = Int.comparison(['+']+numlist_a, ['+']+numlist_b)
    if asign == '+' and bsign == '-':
        numlist_b[0] = '+'
        return addition(numlist_a, numlist_b)
    elif asign == '-' and bsign == '+':
        numlist_b[0] = '-'
        return addition(numlist_a, numlist_b)
    elif compa == 0:
        return ['+',1,0]
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
        exit('error in subtraction :  something went wrong...')
    
    del numlist_a[0:2]
    del numlist_b[0:2]
    Na_decimal = len(numlist_a) - aexpo
    Nb_decimal = len(numlist_b) - bexpo
    Na_int = aexpo if aexpo > 0 else 1
    Nb_int = bexpo if bexpo > 0 else 1 

    max_expo = max(aexpo, bexpo)
    max_decimal = max(Na_decimal,Nb_decimal)
    N = max_expo + max_decimal
    diff_expo = aexpo - bexpo
    diff_decimal = Na_decimal - Nb_decimal
    if diff_expo > 0:
        numlist_b = [0] * diff_expo + numlist_b
    elif diff_expo < 0:
        numlist_a[:0] = [0] * abs(diff_expo)
    else:
        pass

    if diff_decimal > 0:
        numlist_b += [0] * diff_decimal
    elif diff_decimal < 0:
        numlist_a += [0] * abs(diff_decimal)
    else:
        pass

    numlist_ans = []
    for i in range(N):
        numlist_ans.append(numlist_a[i] - numlist_b[i])
    numlist_ans.insert(0,max_expo)
    numlist_ans.insert(0,sign)
    return carry_updown(numlist_ans)


def carry_updown(numlist):  # 繰り上げ繰り下げのとき最上位桁が負になることがないように注意する。
    #pdb.set_trace()
    sign = numlist[0]
    expo = numlist[1]
    del numlist[0:2]
    len_original = len(numlist)

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
        numlist.insert(0,K)
        numlist[1] -= K * 10

    while len(numlist) > 1 and numlist[0] == 0: #最上位桁の要素数減らし
        del numlist[0]
        expo -= 1

    if len(numlist) - len_original == 1:
        expo += 1
    else:
        pass
        # exit('error in carry_updown : something went wrong')
    numlist.insert(0, expo)
    numlist.insert(0, sign)
    return numlist


def significant_digits(numlist,exp):  # 符号と指数は取り除き済みのlistのみOK
    if exp >= 0:
        return len(numlist)
    elif exp < 0:
        return len(numlist) 
    else:
        exit("something went wrong in significant_digits")


def cut_carry_up_down(numlist, signum): # 符号と指数を含んだlistをinputとする。
    if len(numlist) <= signum + 2:
        exit("ERROR in cut_carry_up_down : index out of range")

    sign = numlist[0]
    expo = numlist[1]

    if sign == '+':
        if numlist[signum] >= 5:
            numlist[signum - 1] += 1
            return numlist[:signum + 2]
        elif numlist[signum] < 5:
            return numlist[:signum + 2]
    elif sign == '-':
        if numlist[signum] >= 5:
            return numlist[:signum + 2]
        elif numlist[signum] < 5:
            numlist[signum - 1] += 1
            return numlist[:signum + 2]
    else:
        exit("ERROR in 0.3235 : something went wrong")



def multiplication(numlist_a, numlist_b):
    #pdb.set_trace()
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    aexpo = numlist_a[1]
    bexpo = numlist_b[1]
    if asign == '+' and bsign == '+' or asign == '-' and bsign == '-':
        sign = '+'
    elif asign == '+' and bsign == '-' or asign == '-' and bsign == '+':
        sign = '-'
    del numlist_a[0:2]
    del numlist_b[0:2]

    Na = len(numlist_a)
    Nb = len(numlist_b)
    numlist_ans = [0] * (Na + Nb - 1)
    signum = min(Na, Nb)
    for i in range(Na):
        for j in range(Nb):
            numlist_ans[i+j] += numlist_a[i] * numlist_b[j]

    expo = len(numlist_ans) - ((Na - aexpo) + (Nb - bexpo))
    numlist_ans.insert(0,expo)
    numlist_ans.insert(0,sign)
    ans = carry_updown(numlist_ans)
    #return cut_carry_up_down(ans, signum)  # 有効数字を気にする場合はこっちのreturnをonにする。
    return ans


def check_zero(numlist):
    for i in numlist[2:]:
        if i != 0:
            return 1
    return 0


def comparison(numlist_a, numlist_b):
    #pdb.set_trace()
    if check_zero(numlist_a) == 0 and check_zero(numlist_b) == 0: return 0
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
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

    aexpo = numlist_a[1]
    bexpo = numlist_b[1]
    del numlist_a[0:2]
    del numlist_b[0:2]
    sign_reverse = 1

    if sign == '+':
        pass
    elif sign == '-':
        sign_reverse = -1
    else:
        exit('error in comparison')

    def back_original():
        numlist_a.insert(0,aexpo)
        numlist_a.insert(0,asign)
        numlist_b.insert(0,bexpo)
        numlist_b.insert(0,bsign)

    if aexpo > bexpo:
        back_original()
        return +1 * sign_reverse 
    elif aexpo < bexpo:
        back_original()
        return -1 * sign_reverse
    else:
        pass

    # Na_int = len(numlist_a[:aexpo]) if aexpo > 0 else 0
    # Nb_int = len(numlist_b[:bexpo]) if bexpo > 0 else 0 
    # for i in range(Na_int):
    #     if numlist_a[0] == 0:
    #         del numlist_a[0]
    #     else:
    #         break
    # for i in range(Nb_int):
    #     if numlist_b == 0:
    #         del numlist_b[0]
    #     else:
    #         break

    Na_int = aexpo if aexpo > 0 else 0
    Nb_int = bexpo if bexpo > 0 else 0 
    if Na_int == Nb_int and Na_int > 0:
        for i in range(Na_int):
            if numlist_a[i] > numlist_b[i]:
                back_original()
                return +1 * sign_reverse
            elif numlist_a[i] < numlist_b[i]:
                back_original()
                return -1 * sign_reverse
    Na_decimal = len(numlist_a[Na_int:])
    Nb_decimal = len(numlist_b[Nb_int:])
    min_decimal = min(Na_decimal,Nb_decimal)
    for i in range(Na_int, Na_int + min_decimal):
        if numlist_a[i] > numlist_b[i]:
            back_original()
            return +1 * sign_reverse
        elif numlist_a[i] < numlist_b[i]:
            back_original()
            return -1 * sign_reverse
    if Na_decimal > Nb_decimal:
        back_original()
        return +1 * sign_reverse
    elif Na_decimal < Nb_decimal:
        back_original()
        return -1 * sign_reverse
    else:
        return 0
        

def devision(numlist_a, numlist_b):
    #pdb.set_trace()
    if check_zero(numlist_b) == 0:
        exit('!! devision by zero is not allowed !!')
    elif check_zero(numlist_a) == 0:
        return ['+',1,0]
    sign = ''
    asign = numlist_a[0]
    bsign = numlist_b[0]
    aexpo = numlist_a[1]
    bexpo = numlist_b[1]
    if asign == '+' and bsign == '+' or asign == '-' and bsign == '-':
        sign = '+'
    elif asign == '+' and bsign == '-' or asign == '-' and bsign == '+':
        sign = '-'
    del numlist_a[0:2]
    del numlist_b[0:2]

    Na = len(numlist_a)
    Nb = len(numlist_b)
    point_shift = (Nb - bexpo) - (Na - aexpo)
    #ans_decimal = point_shift + min(Na - aexpo,Nb - bexpo) + 1  #有効数字の桁数の少ない方に合わせる。四捨五入用に＋1桁。
    signum = min(Na, Nb) + 1  #有効数字の桁数の少ない方に合わせる。四捨五入用に＋1桁。
    if Na > Nb:
        for i in range(2):
            if Int.comparison(['+']+numlist_a[:Nb + i],['+']+numlist_b) >= 0:
                ans_int = Na - (Nb + i) + 1
                break
    elif Na <= Nb:
        for i in range(2):
            if Int.comparison(['+']+numlist_a+[0]*(Nb - Na + i),['+']+numlist_b) >= 0:
                ans_int = Na - (Nb + i) + 1
                break

    #else:
    #    if comparison(numlist_a[:Nb],numlist_b) >= 0:
    #        ans_int = 1

    ## ステップ1　:　Dは a / b の商の桁数
    #D_int = Na - Nb
    #digi_diff = numlist_a[:Nb] # aの上位Nb桁
    #if Int.comparison(['+']+digi_diff, ['+']+numlist_b) >= 0: # aとbの大小でD_intが変わる。
    #    D_int = Na - Nb + 1
    ## ステップ2　：　a / b の筆算のアルゴリズム
    #if D_int == 0:
    #    return [0] # 商がゼロ

    if ans_int >= 1:
        remain = numlist_a[:(Na-ans_int+1)] 
    else:
        remain = numlist_a + [0] * (-ans_int+1)
    numlist_ans = [0] * (signum)
    #if D_int != ans_int: exit('D_int != ans_int') # for debug
    for i in range(signum):
        numlist_ans[i] = 9
        for j in range(1,10):
            x = Int.multiplication(['+']+numlist_b, ['+']+[j])
            if Int.comparison(x, ['+']+remain) == 1:
                numlist_ans[i] = j - 1
                break
            
        tmp = Int.multiplication(['+']+numlist_b, ['+']+[numlist_ans[i]])
        remain = Int.subtraction(['+']+remain, tmp)
        del remain[0] #delete sign
        if i < ans_int - 1:
            remain.append(numlist_a[Na - ans_int + 1 + i]) #[]を忘れるとnotiterableになる。
            if remain[0] == 0:
                del remain[0]
        elif ans_int - 1 <= i < signum - 1:
            remain.append(0)
            if remain[0] == 0:
                del remain[0]

    ans_expo = ans_int + point_shift
    numlist_ans.insert(0,ans_expo)
    numlist_ans.insert(0,sign)
    return round_off(numlist_ans,ans_expo-len(numlist_ans[2:])+1)
    #return numlist_ans


def round_off(numlist,round_digit):  #例:  入力が (['+',3, 3,5,2,7,6], -1) なら出力は、 (['+',3, 3,5,2,8])
    expo = numlist[1]
    digit = 2 + expo - round_digit
    try:
        if 9 >= numlist[digit] >= 5:
            numlist[digit-1] += 1
            del numlist[digit]
            return numlist
        elif 4 >= numlist[digit] >= 0:
            del numlist[digit]
            return numlist
        else:
            exit('ERROR in round_off')
    except IndexError as err:
        print(err)


#def back_original():
#    numlist_a.insert(0,aexpo)
#    numlist_a.insert(0,asign)
#    numlist_b.insert(0,bexpo)
#    numlist_b.insert(0,bsign)


def interaction():
    numinp1 = '' 
    numinp2 = '' 
    while True: 
        numinp1 = input('input a first number >>>  ')
        if type(numinp1) is str:
            numinp1 = numinp1.strip()
            break
    while True:
        numinp2 = input('input a second number >>>  ')
        if type(numinp2) is str:
            numinp2 = numinp2.strip()
            break
    print('what operation do you want?')
    while True:
        which = input('1: addition,  2: subtraction,  3: multiplication,  4: devision >>>  ')
        if which in ['1','2','3','4','5']:
            break
        else:
            print('only 1, 2, 3 or 4')
    inplist1 = str_to_list(numinp1)
    inplist2 = str_to_list(numinp2)
    if which == '1':
        show(addition(inplist1,inplist2))
    elif which == '2':
        show(subtraction(inplist1,inplist2))
    elif which == '3':
        show(multiplication(inplist1,inplist2))
    elif which == '4':
        show(devision(inplist1,inplist2))
    elif which == '5':
        print(comparison(inplist1,inplist2))
    else :
      print('ERROR : something went wrong...')


def show(numlist):
    #pdb.set_trace()
    if check_zero(numlist) == 0:
        numlist[0] = '+'
        numlist[1] = 1
    sign = numlist[0]
    expo = numlist[1]
    if expo > 0 and expo == len(numlist[2:]):
        pass
    elif expo > 0:
        numlist.insert(2 + expo,'.')
    elif expo <= 0:
        numlist.insert(2,'.')
        numlist[:2] += [0]
        numlist[:3+1] += [0] * abs(expo)
    del numlist[1]
    if sign == '+':
        del numlist[0]
    print(''.join(list(map(str, numlist))))




# num1 = '999'
# num2 = '-150.3'
# num3 = '-0.000379'
# num4 = '-0.003791'
# testlist1 = [97,45,2,3,67,3,3,74,51]
# testlist2 = [0,0,1,2,3,4,5,6,7,8,9]
# testfloat1 = ['+',2,23,3,5,54,2]   # +0.33542*10^5 = +33542
# testfloat2 = ['-',3,1,7,2,1,9]   # -0.27219*10^3 = -272.19
# testfloat3 = ['-',-1,5]
# testfloat4 = ['-', 1, 2, 4]
# testfloat5 = ['+', 1, 3, 5, 5]

#numlist1 = str_to_list(num1)
#numlist2 = str_to_list(num2)
#numlist3 = str_to_list(num3)
#numlist4 = str_to_list(num4)


# print(numlist1, numlist2, numlist3, numlist4)
# print(testfloat4,testfloat5)
# print(devision(testfloat4,testfloat5))
# print(round_off(['+',0,6,7],-1))
# show(subtraction(testfloat4,testfloat5))
# print(testfloat1)
# print(subtraction(numlist1, numlist2))
# print(carry_updown(testfloat1))
# print(numlist2)
# print(numlist3,numlist4)
# print((numlist3,numlist4))
# print(subtraction(numlist1, numlist2))
# print(multiplication(numlist1, numlist2))
# print(comparison(numlist3,numlist4))
# print(comparison([0,0,0,0,0,1,2],[1,2]))
# print(numlist1, numlist2, numlist3)
# print(list_to_str(numlist1), list_to_str(numlist2))
# print(comparison([1,2],[1,1]))
# print(tj)
# print(devision(numlist1, numlist2))
# print(numlist4)
# print(check_zero(['-',3,0,0,0,0]))
#print(str_to_list(input('input number')))

if __name__ == '__main__':
    interaction() 



