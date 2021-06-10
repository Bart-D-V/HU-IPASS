import numpy as np
import analyse_functies as af
import random

kolom_aantal = 7
rij_aantal = 6
mens = 1
bot = 2


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


# zorgt ervoor dat stenen naar beneden in het bord zakken.
def vallende_steen(bord, kolom):
    for rij in range(rij_aantal):
        if bord[rij][kolom] == 0:
            return rij


# zet een steen in het speelbord.
def plaats_steen(bord, kolom, rij, speler):
    bord[rij][kolom] = speler


# functie om vier op een rij te spelen met inputs.
def speel():
    bord = maak_speelbord()
    speler = 1
    zet = ""
    while True:
        print_speelbord(bord)
        zet = input("Speler " + str(speler) + " kies een kolom: ")

        if zet == "stop":
            break
        elif int(zet) not in af.speelbare_kolommen(bord):
            print("Dat is geen speelbare kolom.")
            continue
        else:
            plaats_steen(bord, int(zet), vallende_steen(bord, int(zet)), speler)

        if af.winst(bord, speler):
            print("Speler " + str(speler) + " heeft gewonnen.")
            break

        if speler == 1:
            speler = 2
        else:
            speler = 1


# Checkt of het spel is afgelopen door te kijken of een speler vier op een rij heeft of het bord vol is.
def einde_spel(bord):
    return af.winst(bord, 1) or af.winst(bord, 2) or len(af.speelbare_kolommen(bord) == 0)


# minmax algoritme.
def minmax(bord, diepte, alpha, beta, maximaliseren):
    speelbaren_kolommen = af.speelbare_kolommen(bord)

    # Diepte bereikt en de score van de positie terug geven.
    if diepte == 0:
        return None, af.positie_score(bord, bot)
    # Check of er vier op een rij is of een vol speelbord.
    elif einde_spel(bord):
        if af.winst(bord, mens):
            return None, -999999
        elif af.winst(bord, bot):
            return None, 999999
        else:
            return None, 0

    # Maximaliseren van de score.
    if maximaliseren:
        score = -999999
        zet = random.choice(speelbaren_kolommen)

        # Alle speelbaren kolommen proberen.
        for kol in speelbaren_kolommen:
            # Maak een kopie van het speelbord.
            b_kopie = bord.copy()
            rij = vallende_steen(bord, kol)
            # Nieuwe zet plaatsen in het bord en de score berekenen.
            plaats_steen(b_kopie, rij, kol, bot)
            nieuwe_score = minmax(b_kopie, diepte - 1, alpha, beta, False)[1]

            if nieuwe_score > score:
                score = nieuwe_score
                zet = kol
            alpha = max(alpha, score)

            if alpha >= beta:
                break

        return zet, score

    # Minimaliseren van de score.
    else:
        score = 999999
        zet = random.choice(speelbaren_kolommen)

        # Alle speelbaren kolommen proberen.
        for kol in speelbaren_kolommen:
            # Maak een kopie van het speelbord.
            b_kopie = bord.copy()
            rij = vallende_steen(bord, kol)
            # Nieuwe zet plaatsen in het bord en de score berekenen.
            plaats_steen(b_kopie, rij, kol, mens)
            nieuwe_score = minmax(b_kopie, diepte - 1, alpha, beta, True)[1]

            if nieuwe_score < score:
                score = nieuwe_score
                zet = kol
            beta = min(beta, score)

            if alpha >= beta:
                break

        return zet, score
