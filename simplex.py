from functions import *
from matrizInversa import *
import copy


def inputCoeficiente():
    print("Insira os coeficientes da função objetiva incluindo as variaveis de folga")

    rawInput = input().split()
    coeficientes = []

    for x in rawInput:
        coeficientes.append(float(x))

    return [coeficientes]


def inputMatrizBasica():
    print("Insira a ordem da matriz basica")
    ordem = int(input())

    matriz = []

    for x in range(ordem):
        print("Insira os coeficientes da matriz basica")
        rawInput = input().split()
        coeficientes = []
        for value in rawInput:
            coeficientes.append(float(value))
        matriz.append(coeficientes)

    return matriz


def inputMatrizNaoBasica(matrizBasica: list):

    altura = len(matrizBasica[0])
    matriz = []

    for x in range(altura):
        print("Insira os coeficientes da matriz nao basica")
        rawInput = input().split()
        coeficientes = []
        for value in rawInput:
            coeficientes.append(float(value))
        matriz.append(coeficientes)

    return matriz


def inputTermosIndependentes(ordem):

    coeficientes = []

    for x in range(ordem):
        print("insira os termos independentes:")
        rawInput = input()
        coeficientes.append([float(rawInput)])

    return coeficientes


def inputIndiceVariaveisBasicas():
    print("insira o indice das variaveis da matriz basica")
    rawInput = input().split()
    indices = []

    for x in rawInput:
        indices.append(int(x))

    return [indices]


def inputIndiceVariaveisNaoBasicas():
    print("insira o indice das variaveis da matriz nao basica")
    rawInput = input().split()
    indices = []

    for x in rawInput:
        indices.append(int(x))

    return [indices]


def calcSolucaoBasica(matrizBasica: list, termosIndependentes: list):
    print(matrizBasica)
    inversaBasica = calcularInversa(copy.deepcopy(matrizBasica))
    solucao = multiplicarMatrizes(inversaBasica, termosIndependentes)
    print(matrizBasica)

    return solucao


def calcCustosRelativos(
    coeficientesBasicos: list,
    coeficientesNaoBasicos: list,
    matrizBasica: list,
    matrizNaoBasica: list,
):

    # Passo 2.1 - calcular vetor multiplicador simplex

    print("Passo 2.1 - calcular vetor multiplicador simplex \n")
    basicaTransposta = calcularInversa(copy.deepcopy(matrizBasica))

    multiplicadorSimplex = multiplicarMatrizes(coeficientesBasicos, basicaTransposta)

    print("Multiplicador simplex:")

    printMatriz(multiplicadorSimplex)

    # Passo 2.2 Custos Relativos

    print("Passo 2.2 Custos Relativos")

    custos = []

    for x in range(len(coeficientesNaoBasicos[0])):
        coluna = getColuna(matrizNaoBasica, x)
        produto = multiplicarMatrizes(multiplicadorSimplex, coluna)
        custo = coeficientesNaoBasicos[0][x] - produto[0][0]
        custos.append(custo)

    return [custos]


def calcCoeficientesBasicosENaobasicos(coeficientes: list, indicesBasicos: list):
    coeficientesBasicos = []
    coeficientesNaoBasicos = []
    linhaBasica = []
    linhaNaobasica = []

    for i in range(len(coeficientes[0])):
        c = coeficientes[0][i]
        if i + 1 in indicesBasicos[0]:
            linhaBasica.append(c)
        else:
            linhaNaobasica.append(c)

    coeficientesBasicos.append(linhaBasica)
    coeficientesNaoBasicos.append(linhaNaobasica)

    return (coeficientesBasicos, coeficientesNaoBasicos)


def calcEntraNaBase(custosRelativos: list):
    # Passo 2.3

    entraNabase = 1
    menor = custosRelativos[0][0]

    for i in range(len(custosRelativos[0])):
        if custosRelativos[0][i] < menor:
            menor = custosRelativos[0][i]
            entraNabase = i + 1

    print("Variavel x" + str(entraNabase) + " com valor: " + str(menor))

    return entraNabase


def calcDirecaoSimplex(
    entraNaBase: int, indicesNaoBasicos: list, matrizBasica: list, matrizNaoBasica: list
):
    matrizInversa = calcularInversa(copy.deepcopy(matrizBasica))

    indiceEntra = indicesNaoBasicos[0].index(entraNaBase)

    coluna = getColuna(matrizNaoBasica, indiceEntra)

    direcaoSimplex = multiplicarMatrizes(matrizInversa, coluna)

    return direcaoSimplex


def calcTamanhoDoPassoEVariavelASairDabase(
    solucaoBasica: list, direcaoSimplex: list, indicesBasicos: list
):
    Icandidatos = []
    values = []

    for i in range(len(direcaoSimplex)):
        if direcaoSimplex[i][0] > 0:

            Icandidatos.append(i)
            values.append(solucaoBasica[i][0] / direcaoSimplex[i][0])

    menor = values[0]
    menorIndice = Icandidatos[0]

    for i in range(len(values)):
        if menor > values[i]:
            menor = values[i]
            menorIndice = Icandidatos[i]

    return (indicesBasicos[0][menorIndice], menor)


def trocaIndiceVariaveis(
    indicesBasicos: list,
    indicesNaoBasicos: list,
    matrizBasica: list,
    matrizNaoBasica: list,
    coeficientesBasicos: list,
    coeficientesNaoBasicos: list,
    indiceSai: int,
    indiceEntra,
):

    iSai = indicesBasicos[0].index(indiceSai)
    iEntra = indicesNaoBasicos[0].index(indiceEntra)

    aux = indicesNaoBasicos[0][iEntra]

    indicesNaoBasicos[0][iEntra] = indicesBasicos[0][iSai]
    indicesBasicos[0][iSai] = aux

    colunaSai = getColunaT(matrizBasica, iSai)
    colunaEntra = getColunaT(matrizNaoBasica, iEntra)

    for i in range(len(colunaEntra)):
        matrizBasica[i][iSai] = colunaEntra[i]

    for i in range(len(colunaSai)):
        matrizNaoBasica[i][iEntra] = colunaSai[i]

    aux = coeficientesBasicos[0][iSai]
    coeficientesBasicos[0][iSai] = coeficientesNaoBasicos[0][iEntra]
    coeficientesNaoBasicos[0][iEntra] = aux

    return (
        indicesBasicos,
        indicesNaoBasicos,
        matrizBasica,
        matrizNaoBasica,
        coeficientesBasicos,
        coeficientesNaoBasicos,
    )


def compilaSolucao(
    solucaoBasica,
    indicesBasicos,
    coeficientesOriginais,
):

    indices = []
    valores = []

    solucaoT = getColunaT(solucaoBasica, 0)

    for x in indicesBasicos[0]:
        indices.append(x)
    for x in solucaoT:
        valores.append(x)

    for i in range(len(coeficientesOriginais[0])):
        if not i + 1 in indices:
            indices.append(i + 1)
            valores.append(0)

    for j in range(len(indices) - 1):
        for i in range(len(indices) - 1 - j):
            if indices[i] > indices[i + 1]:
                aux = indices[i]
                indices[i] = indices[i + 1]
                indices[i + 1] = aux

                aux = valores[i]
                valores[i] = valores[i + 1]
                valores[i + 1] = aux

    soma = 0
    for i in range(len(coeficientesOriginais[0])):
        soma += coeficientesOriginais[0][i] * valores[i]

    return ([indices, valores], soma)


def simplex():
    coeficientes = inputCoeficiente()
    printMatriz(coeficientes)

    # Talvez esse tenha que ser removido
    indicesBasicos = inputIndiceVariaveisBasicas()
    printMatriz(indicesBasicos)

    matrizBasica = inputMatrizBasica()
    printMatriz(matrizBasica)

    ordem = len(matrizBasica)

    # Talvez tenha que ser removido
    indicesNaoBasicos = inputIndiceVariaveisNaoBasicas()
    printMatriz(indicesNaoBasicos)

    matrizNaoBasica = inputMatrizNaoBasica(matrizBasica)
    printMatriz(matrizNaoBasica)

    termosIndependentes = inputTermosIndependentes(ordem)
    printMatriz(termosIndependentes)

    coeficientesBasicos, coeficientesNaoBasicos = calcCoeficientesBasicosENaobasicos(
        coeficientes, indicesBasicos
    )

    iteracao = 0

    while True:

        iteracao += 1

        print("Iteracao " + str(iteracao))

        # Passo 1 : Calculo da solução basica

        print("Passo 1 : Calculo da solução basica\n")

        solucaoBasica = calcSolucaoBasica(matrizBasica, termosIndependentes)
        print("Solucao basica:")
        printMatriz(solucaoBasica)

        # Passo 2: Calculo dos custos relativos
        print("Passo 2: Calculo dos custos relativos\n")
        custosRelativos = calcCustosRelativos(
            coeficientesBasicos,
            coeficientesNaoBasicos,
            matrizBasica,
            matrizNaoBasica,
        )

        printMatriz(custosRelativos)

        entraNaBase = calcEntraNaBase(custosRelativos)

        # Passo 3 : Teste de otimidade

        otimalidade = True

        for x in custosRelativos[0]:
            if x < 0:
                otimalidade = False

        print("O resultado nao é otimo\n") if not otimalidade else print(
            "O resultado é otimo!"
        )

        if otimalidade:
            return compilaSolucao(solucaoBasica, indicesBasicos, coeficientes)

        # Passo 4 : calculo da direção simplex

        print("Passo 4 : calculo da direção simplex\n")

        direcaoSimplex = calcDirecaoSimplex(
            entraNaBase, indicesNaoBasicos, matrizBasica, matrizNaoBasica
        )

        printMatriz(direcaoSimplex)
        stop = True
        for v in direcaoSimplex:
            if v[0] > 0:
                stop = False

        if stop:
            print("O problema nao possui solução otima finita\n")
            return None

        # Passo 5 : determinação do passo e variavel a sair da base

        print("Passo 5 : determinação do passo e variavel a sair da base\n")

        variavelASair, passo = calcTamanhoDoPassoEVariavelASairDabase(
            solucaoBasica, direcaoSimplex, indicesBasicos
        )

        print("variavel a sair é X" + str(variavelASair) + "\n")
        print("Tamanho do passo : " + str(passo) + "\n")

        # Passo 6: Nova partição basica

        print("Passo 6: Nova partição basica\n")

        (
            indicesBasicos,
            indicesNaoBasicos,
            matrizBasica,
            matrizNaoBasica,
            coeficientesBasicos,
            coeficientesNaoBasicos,
        ) = trocaIndiceVariaveis(
            indicesBasicos,
            indicesNaoBasicos,
            matrizBasica,
            matrizNaoBasica,
            coeficientesBasicos,
            coeficientesNaoBasicos,
            variavelASair,
            entraNaBase,
        )

        print("variaveis basicas :\n")
        printMatriz(indicesBasicos)

        print("variaveis não basicas :\n")
        printMatriz(indicesNaoBasicos)

        print("matriz basica :\n")

        printMatriz(matrizBasica)

        print("matriz não basica :\n")

        printMatriz(matrizNaoBasica)

        print("coeficientes basicos da função objetiva\n")

        printMatriz(coeficientesBasicos)

        print("coeficientes nao basicos da função objetiva\n")

        printMatriz(coeficientesNaoBasicos)


resultado = simplex()

if resultado != None:
    print("Valores otimos")
    printMatriz(resultado[0])
    print("Solução otima:")
    print(resultado[1])
