import math

a=float(input("Enter number a:"))
b=float(input("Enter number b:"))
operation=input("+,-,/,*,^,%:")
if operation=="+":
    print(a+b)
elif operation=="-":
    print(a-b)
elif operation=="*":
    print(a*b)
elif operation=="/":
    print(a/b)
elif operation=="^":
    print(math.pow(a, b))
elif operation=="%":
    print(a%b)
else:
    print("illegal opperand")