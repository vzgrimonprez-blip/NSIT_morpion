import random
import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Morpion - Accueil")
# Charger et redimensionner l'image de fond
background = pygame.image.load("fond_morpion.jpg")
background = pygame.transform.scale(background, (600, 600))  # 60% de la largeur
# Préparation du texte avec gestion du débordement
font = pygame.font.SysFont('Gorgia', 30)  # Taille réduite pour éviter le débordement
message = "Bienvenus, voici un jeu de morpion contre un bot !"
# Découpement du texte en plusieurs lignes
max_width = 380  # Largeur maximale pour le texte (400px - marge)
lines = []
words = message.split()
current_line = ""
for word in words:
    test_line = current_line + word + " "
    text_surface = font.render(test_line, True, (148,0,211))
    if text_surface.get_width() <= max_width:
        current_line = test_line
    else:
        lines.append(current_line)
        current_line = word + " "
lines.append(current_line)  # Ajouter la dernière ligne
# Création d'un fond coloré pour la zone de texte 
pygame.draw.rect(screen, (220, 220, 220), (600, 0, 400, 600))  # Fond gris clair
etat = 1  # Présentation. 2 : Règles du jeu. 3 : Le jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if etat == 1:  # Présentation
       # Charger et redimensionner l'image de fond
        background = pygame.image.load("fond_morpion.jpg")
        background = pygame.transform.scale(background, (600, 600))
        # Préparation du texte avec gestion du débordement
        font = pygame.font.SysFont('Gorgia', 30)
        message = "Bienvenus, voici un jeu de morpion contre un bot !"
        # Découpement du texte en plusieurs lignes
        max_width = 380
        lines = []
        words = message.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            text_surface = font.render(test_line, True, (148,0,211))
            if text_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        # Création d'un fond coloré pour la zone de texte
        pygame.draw.rect(screen, (220, 220, 220), (600, 0, 400, 600))
        # Afficher l'image à gauche
        screen.blit(background, (0, 0))
        # Afficher le texte à droite, ligne par ligne
        y_offset = 200
        for line in lines:
            text_surface = font.render(line, True, (148,0,211))
            screen.blit(text_surface, (620, y_offset))
            y_offset += 30
        # Définition du bouton "Commencer le jeu"
        font_bouton = pygame.font.SysFont('Gorgia', 30)
        bouton_rect = pygame.Rect(650, 450, 300, 70)
        pygame.draw.rect(screen, (148,0,211), bouton_rect)  # Fond du bouton
        texte_bouton = font_bouton.render("Commencer le jeu", True, (255, 255, 255))
        texte_bouton_rect = texte_bouton.get_rect(center=bouton_rect.center)
        screen.blit(texte_bouton, texte_bouton_rect)

    
    elif etat == 2:  # Règle du jeu
        # Définition des couleurs supplémentaires pour les règles
        BLANC = (255, 255, 255)
        GRIS_CLAIR = (220, 220, 220)
        VIOLET = (148, 0, 211)
        NOIR = (0, 0, 0)
        JAUNE = (255, 255, 0)  # Couleur pour le fond des règles

        # Préparation des polices
        font_titre_regles = pygame.font.SysFont('Gorgia', 45, bold=True)
        font_regles = pygame.font.SysFont('Arial', 25)

        # Texte des règles
        texte_instructions = [
            "--- Les Règles du Morpion ---",
            "",
            "1. Le jeu se déroule sur une grille de 3x3.",
            "2. Le **Joueur X** commence, l'ordinateur (Bot) est le **Joueur O**.",
            "3. Les joueurs placent à tour de rôle leur symbole dans une case vide.",
            "4. Le premier joueur à aligner trois de ses symboles",
            "   (horizontalement, verticalement ou en diagonale) gagne la partie.",
            "5. Si toutes les cases sont remplies et qu'aucun joueur n'a gagné,",
            "   la partie est déclarée **Match Nul**.",
            "",
            "Appuyez sur ESPACE pour revenir à l'accueil."
        ]

        def dessiner_regles():
            """Affiche l'écran des règles sur toute la zone de l'écran."""
            screen.fill(JAUNE)  # Fond jaune pour se démarquer
            # Dessiner le cadre principal
            pygame.draw.rect(screen, NOIR, (50, 50, 900, 500), 5)
            # Titre
            titre_surface = font_titre_regles.render(texte_instructions[0], True, NOIR)
            screen.blit(titre_surface, (100, 80))

            # Texte des règles
            y_offset = 150
            for line in texte_instructions[1:]:
                couleur_texte = VIOLET if "ESPACE" in line else NOIR
                text_surface = font_regles.render(line, True, couleur_texte)
                screen.blit(text_surface, (100, y_offset))
                y_offset += 35

        # Afficher les règles
        dessiner_regles()

    
    else:  # 3 : Le jeu
        screen.fill((255, 255, 255))  # Fond blanc
        # Afficher l'image à gauche
        screen.blit(background, (0, 0))
        # Afficher le texte à droite, ligne par ligne
        y_offset = 200  # Position verticale de départ
        for line in lines:
            text_surface = font.render(line, True, (148,0,211))
            screen.blit(text_surface, (620, y_offset))  # 620 = 600 + marge de 20px
            y_offset += 30  # Espacement entre les lignes
    pygame.display.flip()
pygame.quit()
# Fonctions du jeu de morpion
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
# Lancer le jeu après la fermeture de la fenêtre
morpion()                                                                                                                                                    


