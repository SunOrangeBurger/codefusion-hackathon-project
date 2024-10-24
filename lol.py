import math
n=int(input("num:"))
str_n=len(n)
sum=[]
need=len(str_n)-1
for i in range(len(str_n)):
    n_sub=n/math.pow(10, need)
    sum.append(n_sub)
    need-=need
    
