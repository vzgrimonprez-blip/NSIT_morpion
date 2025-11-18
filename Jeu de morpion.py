import random
import pygame
import pygame, sys
from pygame import* 


pygame.font.init()
screen_width = 800 
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption ('Hello, bienvenue au jeu de Morpion contre un bot!')

sysFont = pygame.font.SysFont("Arial", 30)
text_content ='Hello, bienvenue au jeu de Morpion contre un bot!'
rendered_text = sysFont.render(text_content, True, (240, 255, 255))

running = True
while running:
    # GESTION DES ÉVÉNEMENTS
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False 
screen.fill((0, 0, 0)) 
screen.blit(rendered_text,(text_x, text_y))
pygame.display.update()
pygame.quit()
sys.exit()

def afficher_plateau(plateau):
    """Affiche le plateau de jeu."""
    for i in range(3):
        print(f" {plateau[i*3]} | {plateau[i*3+1]} | {plateau[i*3+2]} ")
        if i < 2:
            print("-----------")

def verifier_victoire(plateau):
    """Vérifie si un joueur a gagné."""
    # Lignes
    for i in range(0, 9, 3):
        if plateau[i] == plateau[i+1] == plateau[i+2] != " ":
            return plateau[i]
    # Colonnes
    for i in range(3):
        if plateau[i] == plateau[i+3] == plateau[i+6] != " ":
            return plateau[i]
    # Diagonales
    if plateau[0] == plateau[4] == plateau[8] != " ":
        return plateau[0]
    if plateau[2] == plateau[4] == plateau[6] != " ":
        return plateau[2]
    return None

def coup_bot(plateau):
    """Le bot choisit une position aléatoire parmi les positions disponibles."""
    positions_disponibles = [i for i, val in enumerate(plateau) if val == " "]
    return random.choice(positions_disponibles)

def morpion():
    """Lance le jeu de morpion contre un bot."""
    plateau = [" "] * 9
    joueur_actuel = "X"

    print("Bienvenue au jeu de Morpion contre un bot !")
    print("Les positions sont numérotées de 1 à 9, de gauche à droite et de haut en bas.")

    for tour in range(9):
        afficher_plateau(plateau)

        if joueur_actuel == "X":
            position = int(input("Joueur X, choisissez une position (1-9) : ")) - 1
        else:
            print("Le bot réfléchit...")
            position = coup_bot(plateau)

        if plateau[position] != " ":
            print("Cette position est déjà prise. Essayez une autre position.")
            continue

        plateau[position] = joueur_actuel

        gagnant = verifier_victoire(plateau)
        if gagnant:
            afficher_plateau(plateau)
            if gagnant == "X":
                print("Félicitations, tu as gagné !")
            else:
                print("Le bot a gagné !")
            return

        joueur_actuel = "O" if joueur_actuel == "X" else "X"

    afficher_plateau(plateau)
    print("Match nul !")

# Lancer le jeu
morpion()

