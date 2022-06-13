
texte = str(input("ecrire votre nom: "))

def accro(chaine):
    mots = chaine.split()
    accro = ''
    for i in mots:
        accro = accro + str(i[0]).upper()
    return accro

resultat = accro(texte)
print(f"voici l'acronyme de votre nom: {resultat}")