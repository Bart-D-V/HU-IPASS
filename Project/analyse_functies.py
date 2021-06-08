import numpy as np

from vier_op_een_rij import rij_aantal, kolom_aantal


def raam_analyse(raam, speler):
    pass


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
