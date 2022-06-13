import random

password=int(input("entrer la longueur de votre mot de passe  "))
a="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\'()*+,-./:;<=>?@[\]^_`{|}~ tx0c"
separator="".join(random.sample(a,password))
print(separator)
