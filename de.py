import random

while True:
    a=int(input("cliquer sur un button "))
    if a==0:
        print("Au revoir")
        break
    elif a==1:
        print(random.randint(1,6))
    else:
        print("je n'ai pas compris")
1