__author__ = 'murnko'
from pre import *
from math import *
import copy

def pss(n, lam):
    return ((lam**n)/factorial(n))*exp(-lam)

def psslepszy(mean, threshold, iters=1000):
    result = []
    p = exp(-mean)
    i = 0
    remaning = 1
    while p > threshold and i < iters:
        p *= mean
        p /= i + 1
        result.append(p)
        remaning-=p
        i += 1
    result[-1]+=remaning
    return result

def cars_movement(parkrent, parkback):
    cars = {}
    for i in range(len(parkrent)):
        for j in range(len(parkback)):
            (prob, est) = cars.get(i - j, (0, []))
            est.append((parkrent[i] * parkback[j], i))
            cars[i - j] = (prob + parkrent[i] * parkback[j], est)
    result = {}
    for (change, (prob, returns)) in cars.items():
        sum_prob = 0
        est = 0
        for (rent_prob, cars_change) in returns:
            sum_prob += rent_prob
            est += rent_prob * cars_change
        result[change] = (prob, est / sum_prob)
    return result


def printer(matrix):
    for i in range(21):
        for j in range(21):
            print("{:2d} ".format(matrix[i][j]), end='')
        print()


def printer_f(matrix):
    for i in range(21):
        for j in range(21):
            print("{:2f} ".format(matrix[i][j]), end='')
        print()

def printer_dict(matrix):
    for i in range(21):
        for j in range(21):
            print("{:2d} ".format(matrix[(i, j)]), end='')
        print()

M = 21
values = [[0 for x in range(M)] for x in range(M)]
# values_tmp = [[0 for x in range(M)] for x in range(M)]
# policy = [[0 for x in range(M)] for x in range(M)]
act = {}
new_policy = [[0 for x in range(M)] for x in range(M)]
Actions = [x for x in range(-5, 6)]
# reward = [[0 for x in range(M)] for x in range(M)]
reward = {}


park1rent = []  # 3
park2rent = []  # 4
park1back = []  # 3
park2back = []  # 2

for x in range(13):
    pr = pss(x, 2)
    park2back.append(pr)
    pr = pss(x, 3)
    park1back.append(pr)
    park1rent.append(pr)
    pr = pss(x, 4)
    park2rent.append(pr)

#tutaj sensownie redukuje liczbę stanów
#park1rent = psslepszy(3, 000.5)
#park2rent = psslepszy(4, 000.5)
#park1back = psslepszy(3, 000.5)
#park2back = psslepszy(2, 000.5)

cars1 = cars_movement(park1rent, park1back)
cars2 = cars_movement(park2rent, park2back)
suma = 0
print(cars1)
print(cars2)
przejscia = {}
mozliwe_stany = {}
suma = 0
z = 0
for x in range(M):
    for y in range(M):

        #print((x, y))
        przejscia[(x, y)] = []
        for (zmiana1, (prob1, rent1)) in cars1.items():
            for (zmiana2, (prob2, rent2)) in cars2.items():

                if prob1*prob2 < 0.00001:
                    continue
                else:
                    stan1probabilistyczny = 0 if x-zmiana1 < 0 else 20 if x-zmiana1 > 20 else x-zmiana1
                    stan2probabilistyczny = 0 if y-zmiana2 < 0 else 20 if y-zmiana2 > 20 else y-zmiana2
                    zwrotprobabilstyczny = min(x, rent1)*100 + min(y, rent2)*100
                    z += 1
                    for a in Actions:
                        if a > stan1probabilistyczny or -a > stan2probabilistyczny:
                                continue
                        else:
                            zwrotrzeczywisty = zwrotprobabilstyczny - abs(a)*20
                            stan1poakcji = min(stan1probabilistyczny - a, 20)
                            stan2poakcji = min(stan2probabilistyczny + a, 20)
                            przejscia[(x, y)].append((a, zwrotrzeczywisty, prob1*prob2, (stan1poakcji, stan2poakcji)))


for (state, args) in przejscia.items():
    for (a, zwrot, prob, przejscie) in args:
        reward[(state, a, przejscie)] = zwrot
        if not (state in act):
            act[state] = []
        act[state].append(a)
        if not ((state, a) in mozliwe_stany):
            mozliwe_stany[(state, a)] = []
        mozliwe_stany[(state, a)].append((przejscie, prob))

policy = dict([(state, 0) for state in przejscia.keys()])
new_policy = dict([(state, 0) for state in przejscia.keys()])
values = dict([(state, 0) for state in przejscia.keys()])




z = 0
iterate = 1
while iterate == 1:
    z += 1
    policy = copy.deepcopy(new_policy)
#ewaluacja
    #printer_dict(values)
    new_values = {}
    k = 0
    for xy in przejscia.keys():
        value_tmp = 0
        a = policy[xy]
        for (przejscie, prob) in mozliwe_stany[(xy, a)]:
            k += 1
            value_tmp += prob * (reward[(xy, a, przejscie)] + values[przejscie])
        new_values[xy] = 0.9 * value_tmp
    values = copy.deepcopy(new_values)


#iteracja
    for xy in przejscia.keys():
        values_actions = []
        for a in act[xy]:
            values_tmp = 0
            for (przejscie, prob) in mozliwe_stany[(xy, a)]:
                values_tmp += prob * (reward[(xy, a, przejscie)] + values[przejscie])
            values_actions.append(values_tmp)
        s = max(values_actions)
        for i, j in enumerate(values_actions):
            if j == s:
                new_policy[xy] = act[xy][i]
    print("iterajca " + str(z) + "\n")
    printer_dict(new_policy)
    diff = 0
    iterate = 0
    for i in policy:
        if not (policy[i] == new_policy[i]):
            diff += 1
            iterate = 1
    print(diff)
    if iterate == 0:
        break