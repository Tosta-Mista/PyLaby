#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Lab

if __name__ == "__main__":
	## Initialisation du personnage
	perso 			= "X"
	pos_perso 		= [1,1]
	tresor 			= "#"
	n_levels_total 	= 20
	data = {
		"or" : 0,
		"pv" : 25,
		"level" : None
	}

	# Lancement de la partie
	for n_level in range(1, n_levels_total, + 1):
		level = Lab.charge_labyrinthe("level" + str(n_level))
		data["level"] = n_level
		Lab.jeu(level, data, perso, pos_perso, tresor)
	print("Vous avez gagné !")