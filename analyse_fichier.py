import re

def rec_liste(chaine):
    """permet de verifier si une chaine de caractere est
    au format liste"""

    expr_reguliere = r"^\[\s*(\S+\s*,\s*)*\S+\s*\]$"
    return bool(re.match(expr_reguliere, chaine))

def analyse(chaine,i):
    rec_ligne(chaine,i)


def rec_ligne(chaine,i):
    "pour pas que les fichiers ayant derniere ligne comme \n renvoient erreur"
    if(chaine!="\n"):
            parties = chaine.split(":", 1)
            if len(parties) < 2:
                print(f"Erreur : la ligne numero'{i}' ne contient pas ':'")
                exit(1)

            valeur = parties[1].strip()
            if not rec_liste(valeur):
                print(f"Erreur : {valeur}' n'est pas au bon format dans la ligne {i}")
                exit(1)







def analyse_syntaxique(nom_fichier):
    with open(nom_fichier,"r",encoding='utf-8') as file:
        i=1
        for chaine in file:
            analyse(chaine,i)
            i=i+1
    print("aucune erreur syntaxique")


analyse_syntaxique("test.txt")