# -*- coding: utf-8 -*-
__author__ = 'jgo'

import random
from tkinter import *


def charge_labyrinthe(nom):
    """
    Charge le labyrinthe depuis le fichier nom.txt

    :param nom: nom du fichier contenant le labyrinthe (sans l'extension .txt)
    :return:
        - une liste avec les données du labyrinthe
    """
    try:
        fic = open(nom + ".txt", "r")
        data = fic.readlines()
        fic.close()
    except IOError:
        print("Impossible de lire le fichier {}.txt".format(nom))
        exit(1)

    for i in range(len(data)):
        data[i] = data[i].strip()

    return data


def affiche_labyrinthe(lab, fenetre, size_sprite, pos_perso):
    """
    Affichage d'un labyrinthe.

    :param lab: Variable contenant le labyrinthe
    :param fenetre: Fenêtre graphique
    :param size_sprite: Taille des sprites en pixels
    :param pos_perso: Liste contenant la position du personnage
    :return:
        Tuple contenant le canevas, le sprite du personnage et un dictionnaire des images
        utilisées pour les sprites.
    """
    can = Canvas(fenetre, width=600, height=600)

    photo_wall = PhotoImage(file="sprite/wall.png")
    photo_treasure_cl = PhotoImage(file="sprite/treasure_closed.png")
    photo_treasure_op = PhotoImage(file="sprite/treasure_open.png")
    photo_exit = PhotoImage(file="sprite/exit.png")
    photo_enemy = PhotoImage(file="sprite/enemy.png")
    photo_hero = PhotoImage(file="sprite/hero.png")

    n_ligne = 0
    for ligne in lab:
        n_col = 0
        for car in ligne:
            # Walls
            if car == "+" or car == "-" or car == "|":
                can.create_image(n_col + n_col * size_sprite, n_ligne + n_ligne * size_sprite, anchor=NW,
                                 image=photo_wall)
            # Treasures
            if car == "1" or car == "2" or car == "3":
                can.create_image(n_col + n_col * size_sprite, n_ligne + n_ligne * size_sprite, anchor=NW,
                                 image=photo_treasure_cl)
            # Enemies
            if car == "$":
                can.create_image(n_col + n_col * size_sprite, n_ligne + n_ligne * size_sprite, anchor=NW,
                                 image=photo_enemy)
            # Exit
            if car == "0":
                can.create_image(n_col + n_col * size_sprite, n_ligne + n_ligne * size_sprite, anchor=NW,
                                 image=photo_exit)
            n_col += 1
        n_ligne += 1

    # Display the hero
    sprite_hero = can.create_image(pos_perso[0] + pos_perso[0] * size_sprite, pos_perso[1] + pos_perso[1] * size_sprite,
                                   anchor=NW, image=photo_hero)

    can.pack()

    return (can, sprite_hero, {
        "hero": photo_hero,
        "wall": photo_wall,
        "treasure": photo_treasure_cl,
        "enemy": photo_enemy,
        "exit": photo_exit
    })


def deplacement(event, can, dep, lab, pos_perso, perso):
    """
    Deplacement du personnage.

    :param event: objet décrivant l'evenement ayant déclenché l'appel à cette fonction
    :param can: canevas ou afficher les sprites
    :param dep: type de deplacement("up", "down", "left", ou "right")
    :param lab: liste contenant le labyrinthe
    :param pos_perso: position courante du personnage
    :param perso: sprite représentant le personnage
    :return:
        Pas de valeur de retour
    """
    # Calcul de la taille du labyrinthe
    n_cols = len(lab[0])
    n_lignes = len(lab)
    pos_col, pos_ligne = [pos_perso[0], pos_perso[1]]

    # Deplacement vers la droite
    if dep == "right":
        pos_col += 1

    # Teste si le deplacement conduit le personnage en dehors de l'aire de jeu
    if pos_ligne < 0 or pos_col < 0 or pos_ligne > (n_lignes - 1) or pos_col > (n_cols - 1):
        return None

    # Si le déplacement est possible sur une case vide :
    if lab[pos_ligne][pos_col] == " ":
        can.coords(perso, pos_col + pos_col * 30, pos_ligne + pos_ligne * 30)
        del pos_perso[0]
        del pos_perso[0]
        pos_perso.append(pos_col)
        pos_perso.append(pos_ligne)


def destroy(event, fenetre):
    """
    Fermeture de la fenêtre graphique.

    :param event: objet décrivant l'évènement ayant déclenché l'appel à cette fonction
    :param fenetre: fenêtre graphique
    :return:
        Pas de valeur de retour
    """
    fenetre.destroy()


def init_touches(fenetre, canvas, lab, pos_perso, perso):
    """
    Initialisation du comportement des touches du clavier

    :param canvas: canevas où afficher les sprites
    :param lab: liste contenant le labyrinthe
    :param pos_perso: position courante du personnage
    :param perso: sprite représentant le personnage
    :return:
        Pas de valeur de retour
    """
    fenetre.bind("<Right>", lambda event, can=canvas, l=lab, pos=pos_perso, p=perso: deplacement(event, can, "right", l,
                                                                                                 pos, p))
    fenetre.bind("<Left>", lambda event, can=canvas, l=lab, pos=pos_perso, p=perso: deplacement(event, can, "left", l,
                                                                                                pos, p))
    fenetre.bind("<Up>", lambda event, can=canvas, l=lab, pos=pos_perso, p=perso: deplacement(event, can, "up", l, pos,
                                                                                              p))
    fenetre.bind("<Down>", lambda event, can=canvas, l=lab, pos=pos_perso, p=perso: deplacement(event, can, "down", l,
                                                                                                pos, p))
    fenetre.bind("<Escape>", lambda event, fen=fenetre : destroy(event, fen))