# -*- coding: utf-8 -*-
__author__ = 'jgo'
import Lab
from tkinter import *


if __name__=="__main__":
    # Initialisation du personnage
    perso="X"
    pos_perso=[1, 1]
    tresor="#"
    n_levels_total=20
    data = {
        "po": 0,
        "pv": 25,
        "level": 1
    }
    size_sprite = 29

    # Initialisation de l'affichage graphique
    fenetre = Tk()
    fenetre.title("PyLaby Game v0.1")

    # Lancement de la partie
    level = Lab.charge_labyrinthe("level1")

    (canvas, sprite_perso, photos) = Lab.affiche_labyrinthe(level, fenetre, size_sprite, pos_perso)
    Lab.init_touches(fenetre, canvas, level, pos_perso, sprite_perso)

    # Boucle evenementielle
    fenetre.mainloop()