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


def main():
    print("Simplex :")

    print("Insira o numero de variaveis")

    nVariaveis = int(input())

    print("Insira os coeficientes das variaveis")

    entrada = input().split()
    coeficientes = []

    for x in entrada:
        coeficientes.append(int(x))

    print("insira o numero de restrições: ")

    nRestricoes = int(input())

    print("insira os coeficientes de cada restrição e o valor do termo independente")

    matriz = []
    linha = []
    for x in range(nVariaveis):

        linha.append("x" + str(x))
    linha.append("Z")

    matriz.append(linha)

    for x in range(nRestricoes):
        linha = []
        entrada = input().split()
        for e in entrada:
            linha.append(int(e))
        matriz.append(linha)

    printMatriz(matriz)

    matrizBasica = []
    matrizNBasica = []
    coeficientesBasicos = []
    coeficientesNBasicos = []

    for i in range(nRestricoes + 1):
        linhaBasica = []
        linhaNBasica = []
        for x in range(nVariaveis):
            if x < nRestricoes:
                linhaBasica.append(matriz[i][x])
            else:
                linhaNBasica.append(matriz[i][x])
        matrizBasica.append(linhaBasica)
        matrizNBasica.append(linhaNBasica)

    for i in range(nVariaveis):
        if i < nRestricoes:
            coeficientesBasicos.append(coeficientes[i])
        else:
            coeficientesNBasicos.append(coeficientes[i])

    coeficientesBasicos = [coeficientesBasicos]
    coeficientesNBasicos = [coeficientesNBasicos]

    print()

    print("Matriz basica")

    printMatriz(matrizBasica)

    print()

    print("Matriz não basica")

    printMatriz(matrizNBasica)

    print()

    print("Coeficientes Basicos")

    printMatriz(coeficientesBasicos)

    print()

    print("Coeficientes Não Basicos")

    printMatriz(coeficientesNBasicos)

    print()

    MultSimplex = multiplicarMatrizes(
        coeficientesBasicos, calcularInversa(matrizBasica[1:])
    )

    print("Multiplicador simplex:")

    printMatriz(MultSimplex)

    print()

    print("Custos :")

    custos = []

    for x in range(len(matrizNBasica[0])):
        colunaT = getColuna(matrizNBasica, x)[1:]
        coluna = []
        for e in colunaT:
            coluna.append([e])

        produto = multiplicarMatrizes(MultSimplex, coluna)
        custos.append(coeficientesNBasicos[0][x] - produto[0][0])

    print(custos)

    if x < 0 in custos:
        print("Valor de custo negativo")
