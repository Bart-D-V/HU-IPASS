import numpy as np

from vier_op_een_rij import rij_aantal, kolom_aantal, mens, bot


# functie om de score te berekenen van een positie.
def raam_analyse(raam, speler):
    score = 0

    if speler == mens:
        tegenstander = bot
    else:
        tegenstander = mens

    if raam.count(speler) == 4:
        score += 100

    elif raam.count(speler) == 3 and raam.count(0) == 1:
        score += 5

    elif raam.count(speler) == 2 and raam.count(0) == 2:
        score += 2

    if raam.count(tegenstander) == 3 and raam.count(0) == 1:
        score -= 4

    return score


# Deze functie berekend de score van een positie door, alle mogelijke win manieren te scannen op het speelbord.
def positie_score(bord, speler):
    score = 0

    # Horizontale score.
    for r in range(rij_aantal):
        rij = [int(i) for i in list(bord[r, :])]
        for k in range(kolom_aantal - 3):
            # Maak een horizontale raam.
            raam = rij[k:k + 4]
            score += raam_analyse(raam, speler)

    # Verticale score.
    for k in range(kolom_aantal):
        kolom = [int(i) for i in list(bord[:, k])]
        for r in range(rij_aantal - 3):
            # Maak een varticale raam.
            raam = kolom[r:r + 4]
            score += raam_analyse(raam, speler)

    # Negatief diagonale score.
    for r in range(rij_aantal - 3):
        for k in range(kolom_aantal - 3):
            # Maak een negatief diagonale raam
            raam = [bord[r + i][k + i] for i in range(4)]
            score += raam_analyse(raam, speler)

    # Positief diagonale score.
    for r in range(rij_aantal - 3):
        for k in range(kolom_aantal - 3):
            # Maak een positief diagonale raam.
            raam = [bord[r + 3 - i][k + i] for i in range(4)]
            score += raam_analyse(raam, speler)

    return score


# Checkt of er vier op een rij is in het speelbord.
def winst(bord, speler):
    # check voor hotizantale win mogelijkheden.
    for k in range(kolom_aantal - 3):
        for r in range(rij_aantal):
            if bord[r][k] == speler and bord[r][k + 1] == speler and bord[r][k + 2] == speler and bord[r][k + 3] == speler:
                return True

    # check voor verticale win mogelijkheden.
    for k in range(kolom_aantal):
        for r in range(rij_aantal - 3):
            if bord[r][k] == speler and bord[r + 1][k] == speler and bord[r + 2][k] == speler and bord[r + 3][k] == speler:
                return True

    # check voor negatief diagonale win mogelijkheden.
    for k in range(kolom_aantal - 3):
        for r in range(rij_aantal - 3):
            if bord[r][k] == speler and bord[r + 1][k + 1] == speler and bord[r + 2][k + 2] == speler and bord[r + 3][k + 3] == speler:
                return True

    # check voor positief diagonale win mogelijkheden.
    for k in range(kolom_aantal - 3):
        for r in range(3, rij_aantal):
            if bord[r][k] == speler and bord[r - 1][k + 1] == speler and bord[r - 2][k + 2] == speler and bord[r - 3][k + 3] == speler:
                return True


# Functie voor het zoeken naar speelbare kolommen.
def speelbare_kolommen(bord):
    kolommen = []
    for kol in range(kolom_aantal):
        if is_kolom_vol(bord, kol):
            kolommen.append(kol)
    return kolommen


# Checkt of een kolom speelbaar is.
def is_kolom_vol(bord, kolom):
    return bord[rij_aantal - 1][kolom] == 0
