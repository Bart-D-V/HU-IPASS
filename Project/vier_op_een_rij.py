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
        "\033[0;30;47m 0 \033[0;30;47m 1 \033[0;30;47m 2 \033[0;30;47m 3 \033[0;30;47m 4 \033[0;30;47m 5 \033["
        "0;30;47m 6 \033[0m")
    for i in gedraait_bord:
        # Een string met alle stenen van een rij.
        rij = ""

        for j in i:
            if j == 1:
                # Gele steen
                rij += "\033[1;37;43m   "
            elif j == 2:
                # Rode steen
                rij += "\033[1;37;41m   "
            else:
                # Geen steen
                rij += "\033[1;37;40m   "

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


# zet een steen in het speelbord.
def plaats_steen(bord, kolom, rij, speler):
    bord[rij][kolom] = speler
    return bord


# functie om vier op een rij te spelen met inputs.
def speel():
    bord = maak_speelbord()
    speler = 1
    zet = ""
    while True:
        print_speelbord(bord)
        zet = input("Kies kolom: ")

        if zet == "stop":
            break
        elif int(zet) not in speelbare_kolommen(bord):
            print("Dat is geen speelbare kolom.")
            continue
        else:
            bord = plaats_steen(bord, int(zet), vallende_steen(bord, int(zet)), speler)

        if speler == 1:
            speler = 2
        else:
            speler = 1