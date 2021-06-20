import numpy as np
import tkinter as tk
from game2dboard import Board

kolom_aantal = 7
rij_aantal = 6
mens = 1
bot = 2

""" setup functies """


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


# Checkt of een kolom speelbaar is.
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


""" analyse functies """


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
            if bord[r][k] == speler and bord[r][k + 1] == speler and bord[r][k + 2] == speler and bord[r][
                k + 3] == speler:
                return True

    # check voor verticale win mogelijkheden.
    for k in range(kolom_aantal):
        for r in range(rij_aantal - 3):
            if bord[r][k] == speler and bord[r + 1][k] == speler and bord[r + 2][k] == speler and bord[r + 3][
                k] == speler:
                return True

    # check voor negatief diagonale win mogelijkheden.
    for k in range(kolom_aantal - 3):
        for r in range(rij_aantal - 3):
            if bord[r][k] == speler and bord[r + 1][k + 1] == speler and bord[r + 2][k + 2] == speler and bord[r + 3][
                k + 3] == speler:
                return True

    # check voor positief diagonale win mogelijkheden.
    for k in range(kolom_aantal - 3):
        for r in range(3, rij_aantal):
            if bord[r][k] == speler and bord[r - 1][k + 1] == speler and bord[r - 2][k + 2] == speler and bord[r - 3][
                k + 3] == speler:
                return True


""" algoritme functies """


# Checkt of het spel is afgelopen door te kijken of een speler vier op een rij heeft of het bord vol is.
def einde_spel(bord):
    return winst(bord, 1) or winst(bord, 2) or len(speelbare_kolommen(bord)) == 0


# minmax algoritme.
def minmax(bord, diepte, alpha, beta, maximaliseren):
    speelbaren_kolommen = speelbare_kolommen(bord)

    # Check of er vier op een rij is of een vol speelbord.
    if einde_spel(bord):
        if winst(bord, mens):
            return None, -999999
        elif winst(bord, bot):
            return None, 999999
        else:
            return None, 0
    # Diepte bereikt en de score van de positie terug geven.
    elif diepte == 0:
        return None, positie_score(bord, bot)

    # Maximaliseren van de score.
    if maximaliseren:
        score = -999999
        zet = 3

        # Alle speelbaren kolommen proberen.
        for kol in speelbaren_kolommen:
            # Maak een kopie van het speelbord.
            b_kopie = bord.copy()
            rij = vallende_steen(bord, kol)
            # Nieuwe zet plaatsen in het bord en de score berekenen.
            plaats_steen(b_kopie, kol, rij, bot)
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
        zet = 3

        # Alle speelbaren kolommen proberen.
        for kol in speelbaren_kolommen:
            # Maak een kopie van het speelbord.
            b_kopie = bord.copy()
            rij = vallende_steen(bord, kol)
            # Nieuwe zet plaatsen in het bord en de score berekenen.
            plaats_steen(b_kopie, kol, rij, mens)
            nieuwe_score = minmax(b_kopie, diepte - 1, alpha, beta, True)[1]

            if nieuwe_score < score:
                score = nieuwe_score
                zet = kol

            beta = min(beta, score)
            if alpha >= beta:
                break

        return zet, score


# functie om vier op een rij te spelen met inputs.
def speel():
    bord = Board(rij_aantal, kolom_aantal)
    beurt = mens
    zet = ""
    bord.show()

    while True:
        if beurt == bot:
            zet = minmax(bord, 5, alpha=-999999, beta=999999, maximaliseren=True)[0]
            plaats_steen(bord, zet, vallende_steen(bord, zet), beurt)

        else:
            zet = input("Kies een kolom: ")
            if zet == "stop":
                break
            elif int(zet) not in speelbare_kolommen(bord):
                print("Dat is geen speelbare kolom.")
                continue
            else:
                plaats_steen(bord, int(zet), vallende_steen(bord, int(zet)), beurt)

        print_speelbord(bord)
        if winst(bord, beurt):
            print("Speler " + str(beurt) + " heeft gewonnen.")
            break

        if beurt == mens:
            beurt = bot
        else:
            beurt = mens


""" Gui functies """


# Als er een kolom gekozen is word er een voorbeeld van de positie gegeven.
def muisklik(btn, rij, kolom):
    if kolom not in speelbare_kolommen(bord):
        return

    global voorbeeld
    voorbeeld = bord.copy()
    plaats_steen(voorbeeld, kolom, vallende_steen(voorbeeld, kolom), 1)
    gui_bord.load(np.flipud(voorbeeld))


# Stelt de zet van de speler vast, en maakt de zet van de bot. plus een check of een van de twee heeft gewonnen.
def knoppen(knop):
    if knop == "Return":
        global bord
        bord = voorbeeld.copy()
        if winst(bord, mens):
            gui_bord.print("Je hebt gewonnen!")
            stop()

        zet = minmax(bord, 5, alpha=-999999, beta=999999, maximaliseren=True)[0]
        plaats_steen(bord, zet, vallende_steen(bord, zet), 2)
        gui_bord.load(np.flipud(bord))

        if winst(bord, bot):
            gui_bord.print("Helaas je hebt verloren")
            stop()

    elif knop == "Escape":
        gui_bord.close()

    elif knop == "F2":
        bord = maak_speelbord()
        gui_bord.load(bord)


def stop():
    gui_bord.pause(5000)
    bord = maak_speelbord()
    gui_bord.load(bord)
    gui_bord.print(gui_info)


gui_info = "Controles: klik op een kolom, en druk op enter.   F2: restart   Esc: stop"
bord = maak_speelbord()
gui_bord = Board(rij_aantal, kolom_aantal)
gui_bord.load(np.flipud(bord))
gui_bord.title = "Vier op een rij"
gui_bord.cell_size = 100
gui_bord.cell_color = "DodgerBlue"
gui_bord.on_mouse_click = muisklik
gui_bord.on_key_press = knoppen

gui_bord.create_output(background_color="wheat4", color="white", font_size=20)

gui_bord.print(gui_info)

gui_bord.show()
