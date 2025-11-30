import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Définition des couleurs globales
BLANC = (255, 255, 255)
GRIS_CLAIR = (220, 220, 220)
VIOLET = (148, 0, 211)
NOIR = (0, 0, 0)
VERT = (0, 150, 0)
ROUGE = (200, 0, 0)
JAUNE = (255, 255, 0)

# Paramètres de l'écran principal
largeur_ecran = 1000
hauteur_ecran = 600
screen = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Morpion - Accueil")

# Chargement des polices globales
font_accueil = pygame.font.SysFont('Gorgia', 30)
font_titre_regles = pygame.font.SysFont('Gorgia', 45, bold=True)
font_regles = pygame.font.SysFont('Arial', 25)
font_jeu = pygame.font.SysFont('Arial', 80)
font_message = pygame.font.SysFont('Arial', 40)

# Chargement de l'image de fond
try:
    background = pygame.image.load("fond_morpion.jpg")
    background = pygame.transform.scale(background, (600, 600))
except pygame.error:
    print("Erreur: Image 'fond_morpion.jpg' non trouvée. Utilisation d'un fond noir.")
    background = None

# État initial du jeu
etat = 1  # 1: Accueil, 2: Règles, 3: Jeu

# --- Fonctions pour l'état "Accueil" ---
def dessiner_accueil():
    screen.fill(BLANC)
    if background:
        screen.blit(background, (0, 0))
    else:
        pygame.draw.rect(screen, NOIR, (0, 0, 600, 600))
    pygame.draw.rect(screen, GRIS_CLAIR, (600, 0, 400, 600))

    # Texte de bienvenue
    message = "Bienvenus, voici un jeu de morpion contre un bot !"
    max_width = 380
    lines = []
    words = message.split()
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        text_surface_test = font_accueil.render(test_line, True, VIOLET)
        if text_surface_test.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_offset = 200
    for line in lines:
        text_surface = font_accueil.render(line, True, VIOLET)
        screen.blit(text_surface, (620, y_offset))
        y_offset += 30

    # Bouton "Commencer le jeu"
    bouton_rect = pygame.Rect(650, 450, 300, 70)
    pygame.draw.rect(screen, VIOLET, bouton_rect)
    texte_bouton = font_accueil.render("Commencer le jeu", True, BLANC)
    texte_bouton_rect = texte_bouton.get_rect(center=bouton_rect.center)
    screen.blit(texte_bouton, texte_bouton_rect)

    # Instruction pour les règles
    instruction_regle = font_regles.render("Appuyez sur ESPACE pour les règles", True, NOIR)
    screen.blit(instruction_regle, (620, 550))

# --- Fonctions pour l'état "Règles" ---
def dessiner_regles():
    screen.fill(JAUNE)
    pygame.draw.rect(screen, NOIR, (50, 50, 900, 500), 5)

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

    titre_surface = font_titre_regles.render(texte_instructions[0], True, NOIR)
    screen.blit(titre_surface, (100, 80))

    y_offset = 150
    for line in texte_instructions[1:]:
        couleur_texte = VIOLET if "ESPACE" in line else NOIR
        text_surface = font_regles.render(line, True, couleur_texte)
        screen.blit(text_surface, (100, y_offset))
        y_offset += 35

# --- Fonctions pour l'état "Jeu" ---
def dessiner_plateau_jeu():
    screen.fill(GRIS_CLAIR)
    for x1, y1, x2, y2 in lignes_grille:
        pygame.draw.line(screen, NOIR, (x1, y1), (x2, y2), 5)
    for i in range(9):
        symbole = plateau[i]
        if symbole != " ":
            col = i % 3
            ligne = i // 3
            centre_x = col * taille_case + taille_case // 2
            centre_y = ligne * taille_case + taille_case // 2
            couleur = ROUGE if symbole == "X" else VERT
            texte_surface = font_jeu.render(symbole, True, couleur)
            texte_rect = texte_surface.get_rect(center=(centre_x, centre_y))
            screen.blit(texte_surface, texte_rect)

def verifier_victoire(plateau):
    victoires = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in victoires:
        if plateau[a] == plateau[b] == plateau[c] != " ":
            return plateau[a]
    if " " not in plateau:
        return "NUL"
    return None

def coup_bot(plateau):
    positions_disponibles = [i for i, val in enumerate(plateau) if val == " "]
    if positions_disponibles:
        return random.choice(positions_disponibles)
    return -1

def gerer_clic(pos):
    x, y = pos
    col = x // taille_case
    ligne = y // taille_case
    position = ligne * 3 + col
    if 0 <= position < 9 and plateau[position] == " ":
        plateau[position] = joueur_actuel
        return True
    return False

# --- Boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if etat == 1:
                    etat = 2  # Accueil → Règles
                elif etat == 2:
                    etat = 1  # Règles → Accueil

        if event.type == pygame.MOUSEBUTTONDOWN:
            if etat == 1:
                # Vérifier si le clic est sur le bouton "Commencer le jeu"
                bouton_rect = pygame.Rect(650, 450, 300, 70)
                if bouton_rect.collidepoint(event.pos):
                    etat = 3  # Accueil → Jeu
            elif etat == 3 and jeu_en_cours and joueur_actuel == "X":
                if gerer_clic(event.pos):
                    gagnant = verifier_victoire(plateau)
                    if gagnant:
                        jeu_en_cours = False
                    else:
                        joueur_actuel = "O"

    # Affichage selon l'état
    if etat == 1:
        dessiner_accueil()
    elif etat == 2:
        dessiner_regles()
    else:  # etat == 3: Jeu
        if not 'plateau' in locals():
            # Initialisation des variables du jeu
            plateau = [" "] * 9
            joueur_actuel = "X"
            jeu_en_cours = True
            taille_case = 200
            lignes_grille = [
                (taille_case, 0, taille_case, 600),
                (2 * taille_case, 0, 2 * taille_case, 600),
                (0, taille_case, 600, taille_case),
                (0, 2 * taille_case, 600, 2 * taille_case)
            ]

        if jeu_en_cours and joueur_actuel == "O":
            pygame.time.wait(500)
            position_bot = coup_bot(plateau)
            if position_bot != -1:
                plateau[position_bot] = "O"
                gagnant = verifier_victoire(plateau)
                if gagnant:
                    jeu_en_cours = False
                else:
                    joueur_actuel = "X"

        dessiner_plateau_jeu()

        if not jeu_en_cours:
            gagnant = verifier_victoire(plateau)
            if gagnant == "X":
                message_final = "Félicitations, tu as gagné !"
                couleur_message = ROUGE
            elif gagnant == "O":
                message_final = "Le bot a gagné !"
                couleur_message = VERT
            else:
                message_final = "Match nul !"
                couleur_message = VIOLET

            message_surface = font_message.render(message_final, True, couleur_message, BLANC)
            message_rect = message_surface.get_rect(center=(300, 300))
            screen.blit(message_surface, message_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
