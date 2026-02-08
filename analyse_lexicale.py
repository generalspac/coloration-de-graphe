def reconnaitre_lexeme(chaine,i):
    ensemble={ ":", "[" , "]" ,"\n" ," ",","}
    for mot in chaine:
        if not mot.isdigit() and mot not in ensemble:
            print(f"Erreur lexicale, dans la ligne {i}, {mot} ne peut  etre reconnu ")
            exit(1)




def analyser_lexeme(nom_fichier):
    with open(nom_fichier,"r",encoding="utf-8") as file:
        i=1
        for chaine in file:
            for mot in chaine:
               reconnaitre_lexeme(mot,i)
            i+=1
    print("Aucune erreur lexicale")


analyser_lexeme('test.txt')