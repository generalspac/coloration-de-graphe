import ast
import subprocess
import sys
import tkinter as tk
import math
from analyse_lexicale import *
from analyse_fichier import *


# Vérifie que les arguments passés sont corrects (fichier graphe + nombre de couleurs)
def verifier_arguments():
    if len(sys.argv) != 3:
        print(
            f"Erreur : Vous devez fournir exactement 2 arguments.\nUtilisation : python {sys.argv[0]} FichierGraphe NombreCouleurs")
        sys.exit(1)
    if int(sys.argv[2]) < 0:
        print(f"Erreur: nombre de couleurs:", sys.argv[2], "< 0")
        exit(1)


# Convertit un couple (sommet, couleur) en un identifiant unique pour MiniSat
def convertir_variable(sommet, couleur, nombre_couleurs):
    return (sommet - 1) * nombre_couleurs + couleur


# Convertit une variable MiniSat en (sommet, couleur)
def convertir_inverse(variable, nombre_couleurs):
    sommet = (variable - 1) // nombre_couleurs + 1
    couleur = (variable - 1) % nombre_couleurs + 1
    return sommet, couleur


# Lit le graphe depuis un fichier
def lire_graphe(fichier_graphe):
    graphe = {}
    with open(fichier_graphe, "r") as fichier:
        analyser_lexeme(fichier)
        analyse_syntaxique(fichier)
        for ligne in fichier:
            if ligne.strip():
                numero, voisins = ligne.split(":")
                numero = int(numero.strip())
                graphe[numero] = ast.literal_eval(voisins.strip())
    return graphe


# Vérifie que le graphe est valide (pas de boucle, connexions réciproques)
def verifier_graphe(graphe):
    for key in graphe:
        for voisin in graphe[key]:
            if voisin == key:
                print("Erreur,", voisin, "est voisin de lui-même")
                exit(1)
            if key not in graphe[voisin]:
                print("Erreur,", key, "a pour voisin", voisin, "mais ce n'est pas réciproque.")
                exit(1)


# Génère la liste des arêtes à partir du graphe
def generer_arretes(graphe):
    arretes = set()
    for sommet in graphe:
        for voisin in graphe[sommet]:
            if (voisin, sommet) not in arretes:
                arretes.add((sommet, voisin))
    return list(arretes)


# Génère les clauses CNF pour MiniSat
def generer_clauses(arretes, nombre_sommets, nombre_couleurs):
    clauses = []

    # Règle 1 : Deux sommets adjacents ne peuvent pas avoir la même couleur
    for (sommet1, sommet2) in arretes:
        for couleur in range(1, nombre_couleurs + 1):
            clauses.append([-convertir_variable(sommet1, couleur, nombre_couleurs),
                            -convertir_variable(sommet2, couleur, nombre_couleurs)])

    # Règle 2 : Chaque sommet doit avoir au moins une couleur
    for sommet in range(1, nombre_sommets + 1):
        clauses.append([convertir_variable(sommet, couleur, nombre_couleurs)
                        for couleur in range(1, nombre_couleurs + 1)])

    # Règle 3 : Chaque sommet ne peut pas avoir plus d'une couleur
    for sommet in range(1, nombre_sommets + 1):
        for couleur1 in range(1, nombre_couleurs + 1):
            for couleur2 in range(couleur1 + 1, nombre_couleurs + 1):
                clauses.append([-convertir_variable(sommet, couleur1, nombre_couleurs),
                                -convertir_variable(sommet, couleur2, nombre_couleurs)])

    return clauses


# Écrit le fichier DIMACS pour MiniSat
def ecrire_dimacs(fichier_dimacs, nombre_variables, clauses):
    with open(fichier_dimacs, "w") as fichier:
        fichier.write(f"p cnf {nombre_variables} {len(clauses)}\n")
        for clause in clauses:
            fichier.write(" ".join(map(str, clause)) + " 0\n")


# Exécute MiniSat et récupère la solution
def executer_minisat(fichier_dimacs, fichier_sortie):
    subprocess.run(["minisat", fichier_dimacs, fichier_sortie], capture_output=True, text=True)


# Lit la solution MiniSat
def lire_solution(fichier_sortie):
    with open(fichier_sortie, "r") as fichier:
        return fichier.read()


# Vérifie si la solution est correcte
def verifier_solution(lignes, nombre_couleurs, nombre_sommets):
    couleurs_attribuees = {}

    if "UNSAT" in lignes:
        print("Impossible à réaliser (INSATISFIABLE)")
        return None

    elif "SAT" in lignes:
        lignes.pop(0)
        valeurs_sat = list(map(int, lignes[0].split()))

        for valeur in valeurs_sat:
            if valeur > 0:
                sommet, couleur = convertir_inverse(valeur, nombre_couleurs)
                couleurs_attribuees[sommet] = couleur
    return couleurs_attribuees


# Vérifie que la solution respecte les contraintes
def afficher_verification_couleurs(arretes, couleurs_attribuees):
    for (sommet1, sommet2) in arretes:
        if sommet1 in couleurs_attribuees and sommet2 in couleurs_attribuees:
            if couleurs_attribuees[sommet1] == couleurs_attribuees[sommet2]:
                print(
                    f"⚠️ ERREUR : Les sommets {sommet1} et {sommet2} ont la même couleur {couleurs_attribuees[sommet1]}")
                print("Le Sat-Solveur s'est trompé.")


# Affiche les couleurs attribuées aux sommets
def afficher_couleurs_attribuées(arretes, couleurs_attribuees):
    if couleurs_attribuees:
        print("\nSATISFIABLE\n")
        print("\n========================================")
        print("\n 🎨  Coloration du Graphe")
        print("\n========================================")
        for sommet, couleur in couleurs_attribuees.items():
            print(f"🎨 Le sommet {sommet} doit avoir la couleur {couleur}")

        print("\n")
        afficher_verification_couleurs(arretes, couleurs_attribuees)


# Dessine le graphe avec Tkinter
def dessiner_graphe(arretes, couleurs_attribuees):
    if len(couleurs_attribuees)>34:
        print("Le graphe ne peut pas etre affiche car il contient plus de couleurs que la palette n'en contient")
        exit(1)

    fenetre = tk.Tk()
    fenetre.title("Coloration du Graphe")

    largeur, hauteur = 500, 500
    canvas = tk.Canvas(fenetre, width=largeur, height=hauteur, bg="white")
    canvas.pack()

    palette_couleurs = [
        "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown",
        "cyan", "magenta", "lime", "teal", "indigo", "violet", "gold", "silver",
        "maroon", "navy", "turquoise", "olive", "salmon", "coral", "darkred",
        "darkblue", "darkgreen", "darkcyan", "darkmagenta", "darkorange", "gray",
        "lightblue", "lightgreen", "lightcoral", "lightgray", "plum", "chocolate"
    ]

    sommets = sorted(set(u for u, v in arretes) | set(v for u, v in arretes))
    n = len(sommets)

    positions = {}
    rayon = 200
    centre_x, centre_y = largeur // 2, hauteur // 2

    for i, sommet in enumerate(sommets):
        angle = 2 * math.pi * i / n
        x = centre_x + rayon * math.cos(angle)
        y = centre_y + rayon * math.sin(angle)
        positions[sommet] = (x, y)

    for u, v in arretes:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    rayon_sommet = 20
    for sommet, (x, y) in positions.items():
        couleur_index = couleurs_attribuees.get(sommet, 0) - 1
        couleur_graphique = palette_couleurs[couleur_index] if couleur_index >= 0 else "gray"

        canvas.create_oval(x - rayon_sommet, y - rayon_sommet, x + rayon_sommet, y + rayon_sommet,
                           fill=couleur_graphique, outline="black")
        canvas.create_text(x, y, text=str(sommet), font=("Arial", 14, "bold"))

    fenetre.mainloop()
