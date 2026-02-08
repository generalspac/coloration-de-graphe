import sys
from fonctions import (
    verifier_arguments, lire_graphe, verifier_graphe, generer_arretes, generer_clauses, ecrire_dimacs, executer_minisat,
    lire_solution, verifier_solution, afficher_couleurs_attribuées, dessiner_graphe
)

# Vérifie que l'utilisateur a bien fourni 2 arguments (fichier graphe + nombre de couleurs)
verifier_arguments()


# Récupération des arguments depuis la ligne de commande
fichier_graphe = sys.argv[1]
nombre_couleurs = int(sys.argv[2])


# Lecture du graphe depuis le fichier et vérification de son format
graphe = lire_graphe(fichier_graphe)
verifier_graphe(graphe)
nombre_sommets = len(graphe)
nombre_variables = nombre_sommets * nombre_couleurs


# Génération de la liste des arêtes à partir du graphe
arretes = generer_arretes(graphe)


# Génération des clauses SAT selon les règles de la coloration de graphe
clauses = generer_clauses(arretes, nombre_sommets, nombre_couleurs)


# Écriture du problème de coloration sous format DIMACS pour MiniSat
ecrire_dimacs("FichierDimacs.cnf", nombre_variables, clauses)


# Exécution de MiniSat pour résoudre le problème SAT
executer_minisat("FichierDimacs.cnf", "solution.txt")


# Lecture de la solution retournée par MiniSat
solution = lire_solution("solution.txt")


# Vérification et interprétation de la solution obtenue
lignes = solution.strip().splitlines()
couleurs_attribuees = verifier_solution(lignes, nombre_couleurs, nombre_sommets)


# Affichage des couleurs attribuées à chaque sommet
afficher_couleurs_attribuées(arretes, couleurs_attribuees)


# Dessin du graphe si il y a une solution
if couleurs_attribuees:
    dessiner_graphe(arretes,couleurs_attribuees)

