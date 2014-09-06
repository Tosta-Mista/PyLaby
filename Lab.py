# -*- coding: utf-8 -*-
import sys
import os
import random


def charge_labyrinthe(nom):
	"""
		Charge le labyrinthe selon le fichier nom.txt

		nom: nom du fichier contenant le labyrinthe (sans .txt)

		Valeur de retour:
		Tuple contenant les données du labyrinthe
	"""
	try:
		fic = open(nom + ".txt", "r")
		data = fic.readlines()
		fic.close()
	except IOError:
		print("Impossible de lire les fichier {}.txt".format(nom))
		exit(1)

	for i in range(len(data)):
		data[i] = data[i].strip()

	return tuple(data)


def barre_score(data):
	"""
		Barre de score affichant les données du jeu.

		n_level : niveau courant.
		data : dictionnaire de données de la barre de score.

		Pas de valeur de retour
	"""
	print("PV: {:2d}	PO: {:4d}	Level: {3d}".format(data["pv"], data["po"], data["level"]))


def affiche_labyrinthe(lab, perso, pos_perso, tresor):
	"""
		Affichage d'un labyrinthe.

		lab: variable contenant le labyrinthe
		perso: caractère reprèsentant le personnage
		pos_perso: liste contenant la position du personnage[ligne, colonne]

		Pas de valeur en retour
	"""
	n_ligne = 0

	for ligne in lab:
		for i in range(1, 4):
			ligne = ligne.replace(str(i), tresor)
		if n_ligne == pos_perso[1]:
			print(ligne[0:pos_perso[0]] + perso + ligne[pos_perso[0] + 1:])
		else:
			print(ligne)
		n_ligne += 1


def efface_ecran():
	"""
		Efface l'ecran de console
	"""
	if sys.platform.startswith("win"):
		# Si systeme windows
		os.system("cls")
	else:
		# Si system unix ou OS x
		os.system("clear")


def decouverte_tresor(categorie, data):
	"""
		Incrémente le nombre de pièces d'or d'un joueur en fonction du trésor.

		catégories: type de tresor
			- 1 : entre 1 et 5 po 
			- 2 : entre 5 et 10 po 
			- 3 : entre 0 et 25 po 
		data : données de jeu (niveaux, nombre de pièces d'or et points de vie)
	"""
	if categorie == "1":
		data["po"] = data["po"] + random.randint(1, 5)
	elif categorie == "2":
		data["po"] = data["po"] + random.randint(5, 10)
	else:
		data["po"] = data["po"] + random.randint(0, 25)


def combat(data):
	"""
		Determine le nombre de points de vie perdus lors d'un combat

		data : données de jeu (niveaux, nombre de pièces d'or et points de vie)
	"""
	de = random.randint(1, 10)
	if de == 1:
		data["pv"] = data["pv"] - random.randint(5, 10)
	elif de >= 2 and de <= 4:
		data["pv"] = data["pv"] - random.randint(1, 5)


def verification_deplacement(lab, pos_col, pos_ligne, data):
	"""
		Indique si le déplacement du personnage est autorisé ou pas.

		lab: labyrinthe
		pos_ligne: position du personnage dans le lignes
		pos_col: position du personnage sur les colonnes

		Valeurs de retour:
			None: deplacement interdit
			[col,ligne]: deplacement autorisé sur la case indiquée par la liste
	"""
	# Calcul de la taille du labyrithe 
	n_cols = len(lab[0])
	n_lignes = len(lab)

	# Teste si le deplacement conduit le personnage en dehors de l'aire de jeu
	if pos_ligne < 0 or pos_col < 0 or pos_ligne > (n_lignes -1) or pos_col > (n_cols -1):
		return None
	elif lab[pos_ligne][pos_col] != " ":
		return None
	elif lab[pos_ligne][pos_col] == "0":
		# Position hors du labyrinthe = victoire
		return [-1, -1]
	elif lab[pos_ligne][pos_col] == "1" or lab[pos_ligne][:pos_col] == "2" or lab[pos_col][pos_ligne] == "3":
		# Decouverte d'un tresor
		decouverte_tresor(lab[pos_ligne][pos_col], data)
		lab[pos_ligne] = lab[pos_ligne][:pos_col] + " " + lab[pos_ligne][pos_col + 1:]
		return [pos_col, pos_ligne]
	elif lab[pos_ligne][pos_col] == "$":
		# Rencontre un enemie
		combat(data)
		lab[pos_ligne] = lab[pos_ligne][:pos_col] + " " + lab[pos_ligne][pos_col + 1:]
		return [pos_col, pos_ligne]
	else:
		return [pos_col, pos_ligne]


def choix_joueur(lab, pos_perso, data):
	"""
		Demande au joueur de saisir son déplacement et vérifie s'il est possible.
		Si ce n'est pas le cas affiche un messagel sinon modifie la position du 
		perso dans la liste pos_perso.

		lab: Labyrinthe 
		pos_perso: liste contenant la position du personnage [colonne, ligne]

		Pas de valeur de retour
	"""
	dep = None
	choix = input("Votre deplacement (Haut/Bas/Droite/Gauche/Quitter ? ")
	
	if choix == "H" or choix == "Haut":
		dep = verification_deplacement(lab, pos_perso[0], pos_perso[1] -1)
	elif choix == "B" or choix == "Bas":
		dep = verification_deplacement(lab, pos_perso[0], pos_perso[1] +1)
	elif choix == "G" or choix == "Gauche":
		dep = verification_deplacement(lab, pos_perso[0] -1, pos_perso[1])
	elif choix == "D" or choix == "Droite":
		dep = verification_deplacement(lab, pos_perso[0] +1, pos_perso[1])
	elif choix == "Q" or choix == "Quiter":
		exit(0)

	if dep == None:
		print("Deplacement impossible")
		input("Appuyez sur <Return> pour continuer")
	else:
		pos_perso[0] = dep[0]
		pos_perso[1] = dep[1]


def jeu(level, data, perso, pos_perso, tresor):
	"""
		Boucle principale du jeu. Affiche le labyrinthe dans ses differents
		états après les déplacements du joueur.

		level : Labyrinthe
		n_level: Numéro du niveau courant 
		perso : caractère représentant le personnage
		pos_perso: liste contenant la position du personnage [colonne, ligne]
		tresor: caractère représentant le trésor
	"""
	while True:
		efface_ecran()
		affiche_labyrinthe(level, perso, pos_perso, tresor)
		barre_score(data)
		if data["pv"] <= 0:
			print("Vous avez perdu...")
			exit(0)
		choix_joueur(level, pos_perso, data)
		if pos_perso == [-1, -1]:
			print("Vous avez passé le niveau !")
			input("Appuyez sur <Return> pour continuer")
			break
