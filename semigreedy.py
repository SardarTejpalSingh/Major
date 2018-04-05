from random import *
import re

f = open("data.txt", "r")

n = int(f.readline().strip())
print(n)
ar = list(map(int, f.readline().strip().split("  ")))
ar = ar[:len(ar)]
#print(ar)

c = int(f.readline().strip())

#print(c)
main_list = []
for i in range(n-1):
    
    temp_list = list(map(int, f.readline().strip().split()))
    main_list.append(temp_list)


i = 0
l=0

#print(len(main_list[1]))


min_risk = 10000000000000000
while i<1000:
    j, risk = 0, 0
    summ = 0
    r = randint(2, 93)
    i += 1
    risk += ar[r-2]
    summ = ar[r-2] + summ
    while(risk < c and j<n):
        num = ar[j]
        #print(j)
        if ar[j] == ar[r-2]:
            j += 1
            num = ar[j]
        j += 1
        summ += num
        risk += num
        if i>j and j<n:
            risk += main_list[r-2][j]
        elif j<n:
            risk += main_list[j][r-2]
    if(risk < min_risk):
        min_risk = risk
        l = summ
print(min_risk)