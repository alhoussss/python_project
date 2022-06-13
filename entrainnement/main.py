age_int = 0
def demander_age():
    global age_int
    while age_int == 0:
        age_str = input("quel est votre age ? ")
        print(" ")
        try:
             age_int = int(age_str)
        except:
             print("ERREUR:vous devez entrer un nombre pour l'age")




#function demander le nom
def demande_nom():
    nom = input("quel est votre nom ? ")
    while nom == "" :
        nom = input("quel est votre nom ? ")
    return nom

reponse_nom = demande_nom()

# function demander l'age

demander_age()

print("je m'appelle " + reponse_nom + ".")
print(" ")
print("j'ai " + str(age_int) +"ans.")
print("l'an prochain j'aurai " + str(age_int+1) + "ans")



"""
# commentaire 1H03
n = 0

while n < 10:
    print("valeur de n : " + str(n))
    n = n + 1
"""

