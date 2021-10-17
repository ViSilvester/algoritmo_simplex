import copy


def getIndentidade(mSize: int):
    matrizInversa = []

    for i in range(mSize):
        l = []
        for j in range(mSize):
            if i == j:
                l.append(1)
            else:
                l.append(0)
        matrizInversa.append(copy.deepcopy(l))

    return matrizInversa


def dividirLinha(linha: list, valor: float):

    l = copy.deepcopy(linha)
    for x in range(len(l)):
        l[x] = round(l[x] / valor, 4)
    return l


def multiplicarLinha(linha: list, valor: float):
    l = copy.deepcopy(linha)
    for x in range(len(l)):
        l[x] = round(l[x] * valor, 4)
    return l


def subtrairLinhas(linha1: list, linha2: list):
    l = copy.deepcopy(linha1)
    for x in range(len(l)):
        l[x] = round(l[x] - linha2[x], 4)
    return l


def calcularInversa(matriz: list):

    mSize = len(matriz)
    matrizInversa = getIndentidade(mSize)

    for i in range(mSize):

        # se o pivo for 0
        cont = i + 1
        while matriz[i][i] == 0 and cont < mSize:
            if matriz[cont][i] != 0:
                # fazer troca de linha
                aux = copy.deepcopy(matriz[cont])
                matriz[cont] = matriz[i]
                matriz[i] = aux
                # para inversa tambem
                aux = copy.deepcopy(matrizInversa[cont])
                matrizInversa[cont] = matrizInversa[i]
                matrizInversa[i] = aux

        if matriz[i][i] < 0:
            matriz[i] = multiplicarLinha(matriz[i], -1)
            matrizInversa[i] = multiplicarLinha(matrizInversa[i], -1)

        if matriz[i][i] != 1:
            divisor = matriz[i][i]
            matriz[i] = dividirLinha(matriz[i], divisor)
            matrizInversa[i] = dividirLinha(matrizInversa[i], divisor)

        for j in range(mSize):
            if j != i and matriz[j][i] != 0:
                multiplicador = matriz[j][i]
                temp1 = multiplicarLinha(matriz[i], multiplicador)
                temp2 = multiplicarLinha(matrizInversa[i], multiplicador)

                matriz[j] = subtrairLinhas(matriz[j], temp1)
                matrizInversa[j] = subtrairLinhas(matrizInversa[j], temp2)

    return matrizInversa


def determinante(matriz: list):

    if len(matriz) == 1:
        return matriz[0][0]
    else:
        det = 0

        for i in range(len(matriz)):

            subMatriz = copy.deepcopy(matriz)
            subMatriz.pop(0)
            for l in subMatriz:
                l.pop(i)

            det += matriz[0][i] * pow(-1, 1 + (i + 1)) * determinante(subMatriz)
        return det
