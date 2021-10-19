from matrizInversa import *
from print import *


def getLinha(m: list, n: int):
    return m[0]


def getColuna(m: list, n: int):
    r = []
    for x in m:
        r.append([x[n]])

    return r


def getColunaT(m: list, n: int):
    r = []
    for x in m:
        r.append(x[n])

    return r


def multiplicarMatrizes(m1: list, m2: list):
    r = []

    for linha in range(len(m1)):
        aux = []
        for coluna in range(len(m2[0])):
            s = 0

            for elemento in range(len(m1[linha])):
                s += m1[linha][elemento] * getColunaT(m2, coluna)[elemento]
            aux.append(s)
        r.append(aux)

    return r