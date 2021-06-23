import numpy as np
from game2dboard import Board
from vier_op_een_rij import speelbare_kolommen, plaats_steen, vallende_steen, winst, minmax, maak_speelbord, rij_aantal, \
    kolom_aantal, mens, bot, print_speelbord


# functie om vier op een rij te spelen met inputs in de terminal.
def speel_terminal():
    bord = Board(rij_aantal, kolom_aantal)
    beurt = mens
    zet = ""
    bord.show()

    while True:
        if beurt == bot:
            zet = minmax(bord, 6, alpha=-999999, beta=999999, maximaliseren=True)[0]
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
    global bord
    global voorbeeld
    global diepte

    if knop == "Return":
        bord = voorbeeld.copy()
        if winst(bord, mens):
            gui_bord.print("Je hebt gewonnen!")
            stop()
            return
        elif len(speelbare_kolommen(bord)) == 0:
            gui_bord.print("Gelijkspel")
            stop()
            return

        zet = minmax(bord, diepte, alpha=-999999, beta=999999, maximaliseren=True)[0]
        plaats_steen(bord, zet, vallende_steen(bord, zet), 2)
        gui_bord.load(np.flipud(bord))

        if winst(bord, bot):
            gui_bord.print("Helaas je hebt verloren")
            stop()
            return

    # moeilijkheid aanpassen
    elif knop == "plus":
        diepte += 1
        gui_bord.print(gui_info, "moeilijkheid:", diepte)
    elif knop == "minus":
        diepte -= 1
        gui_bord.print(gui_info, "moeilijkheid:", diepte)

    # zet kiezen via toestenbord
    elif int(knop) in kol_knop:
        zet = int(knop)-1
        if zet not in speelbare_kolommen(bord):
            return

        voorbeeld = bord.copy()
        plaats_steen(voorbeeld, zet, vallende_steen(voorbeeld, zet), 1)
        gui_bord.load(np.flipud(voorbeeld))

    # eindig spel
    elif knop == "Escape":
        gui_bord.close()
    # restart spel
    elif knop == "F2":
        bord = maak_speelbord()
        gui_bord.load(bord)


def stop():
    gui_bord.pause(5000)
    global bord
    bord = maak_speelbord()
    gui_bord.load(bord)
    gui_bord.print(gui_info)


diepte = 5
kol_knop = [1, 2, 3, 4, 5, 6, 7]
gui_info = "Controles: klik op een kolom, en druk op enter. F2: restart  Esc: stop"
bord = maak_speelbord()
gui_bord = Board(rij_aantal, kolom_aantal)
gui_bord.load(np.flipud(bord))
gui_bord.title = "Vier op een rij"
gui_bord.cell_size = 100
gui_bord.cell_color = "DodgerBlue"
gui_bord.on_mouse_click = muisklik
gui_bord.on_key_press = knoppen

gui_bord.create_output(background_color="wheat4", color="white", font_size=14)
gui_bord.print(gui_info, "moeilijkheid:", diepte)

gui_bord.show()
