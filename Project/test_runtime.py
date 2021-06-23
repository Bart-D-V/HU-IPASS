import numpy as np
import pandas as pd
import cProfile as cp
from vier_op_een_rij import rij_aantal, kolom_aantal, vallende_steen, plaats_steen, minmax

file = pd.read_csv("test_data/Test_L1_R3.csv")


def lees_bord(posities):
    bord = np.zeros((rij_aantal, kolom_aantal))
    speler = 1
    for zet in posities:
        if zet == " ":
            break
        zet = int(zet) - 1
        plaats_steen(bord, zet, vallende_steen(bord, zet), speler)
        if speler == 1:
            speler = 2
        else:
            speler = 1
    return bord


def lees_bestand(file):
    i = 0
    scores = []
    for line in file["positie"]:
        score = minmax(lees_bord(line), 7, alpha=-999999, beta=999999, maximaliseren=True)[1]
        scores.append(score)
        i += 1
        if i % 100 == 0:
            print("+10% gedaan")
    print(scores)


cp.run('lees_bestand(file)')
