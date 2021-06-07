import numpy as np

kolom_aantal = 7
rij_aantal = 6

# Maakt een leeg speelbord.
def maak_speelbord():
    bord = np.zeros((rij_aantal, kolom_aantal))
    return bord


# Visualiseert het speelbord in de terminal.
def print_speelbord(bord):
    gedraait_bord = np.flipud(bord)

    # print de kolom nummers
    print(
        "\033[0;37;41m 0 \033[0;37;41m 1 \033[0;37;41m 2 \033[0;37;41m 3 \033[0;37;41m 4 \033[0;37;41m 5 \033["
        "0;37;41m 6 \033[0m")
    for i in gedraait_bord:
        # Een string met alle stenen van een rij.
        rij = ""

        for j in i:
            if j == 1:
                # Gele steen
                rij += "\033[0;37;43m   "
            elif j == 2:
                # Rode steen
                rij += "\033[0;37;41m   "
            else:
                # Geen steen
                rij += "\033[0;37;47m   "

        print(rij + "\033[0m")


# Functie voor het zoeken naar speelbare kolommen.
def speelbare_kolommen(bord):
    kolommen = []
    for kol in range(kolom_aantal):
        if is_kolom_vol(bord, kol):
            kolommen.append(kol)
    return kolommen


# kijkt of een kolom speelbaar is.
def is_kolom_vol(bord, kolom):
    return bord[rij_aantal - 1][kolom] == 0


# zorgt ervoor dat stenen naar beneden in het bord zakken.
def vallende_steen(bord, kolom):
    for rij in range(rij_aantal):
        if bord[rij][kolom] == 0:
            return rij
