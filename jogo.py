#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-
"""
Created on Sun Sep 23 15:33:59 2018
@author: talles medeiros, decsi-ufop
"""

"""
Este código servirá de exemplo para o aprendizado do algoritmo MINIMAX 
na disciplina de Inteligência Artificial - CSI457
Semestre: 2018/2
"""

"""
[NOVO]
Autores das modificações (tabuleiro 3x3 para 4x4, consideração da profundidade no cálculo da função de utilidade e
implementação da poda alfa-beta):
Mateus Martins Pereira - 17.1.8109
Gabriel Batista Araujo Almeida - 17.1.8083
Semestre: 2019/1
Disciplina: Inteligência Artificial (Turma 21 - Sistemas de Informação)
"""

# !/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system
from copy import copy, deepcopy

"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)
# indicando o jogador que movimentou nessa posição.
# Começa vazio, com zero em todas posições.
HUMANO = -1
COMP = +1
tabuleiro = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:retorna quantidade de células vazias se o computador vence; -quantidade de células vazias se o HUMANO vence; 0 empate
 """


def avaliacao(estado):
    total_vazio = len(celulas_vazias(estado))
    if vitoria(estado, COMP):
        #Retorna o total de células vazias como placar
        placar = total_vazio
    elif vitoria(estado, HUMANO):
        #Retorna o valor negativo do total de células vazias como placar
        placar = -total_vazio
    else:
        placar = 0

    return placar


""" fim avaliacao (estado)------------------------------------- """


def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence. Possibilidades:
    * Quatro linhas     [X X X X] or [O O O O]
    * Quatro colunas    [X X X X] or [O O O O]
    * Duas diagonais  [X X X X] or [O O O O]
    :param. (estado): o estado atual do tabuleiro
    :param. (jogador): um HUMANO ou um Computador
    :return: True se jogador vence
    """
    win_estado = [
        [estado[0][0], estado[0][1], estado[0][2], estado[0][3]],  # toda linha 1
        [estado[1][0], estado[1][1], estado[1][2], estado[1][3]],  # toda linha 2
        [estado[2][0], estado[2][1], estado[2][2], estado[2][3]],  # toda linha 3
        [estado[3][0], estado[3][1], estado[3][2], estado[3][3]],  # toda linha 4
        [estado[0][0], estado[1][0], estado[2][0], estado[3][0]],  # toda coluna 1
        [estado[0][1], estado[1][1], estado[2][1], estado[3][1]],  # toda coluna 2
        [estado[0][2], estado[1][2], estado[2][2], estado[3][2]],  # toda coluna 3
        [estado[0][3], estado[1][3], estado[2][3], estado[3][3]],  # toda coluna 4
        [estado[0][0], estado[1][1], estado[2][2], estado[3][3]],  # diagonal principal
        [estado[3][0], estado[2][1], estado[1][2], estado[0][3]],  # diagonal secundária
    ]
    # Se um, dentre todos os alinhamentos pertence um mesmo jogador,
    # então o jogador vence!
    if [jogador, jogador, jogador, jogador] in win_estado:
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""


def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)


""" ---------------------------------------------------------- """

"""
Verifica celular vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""


def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0: celulas.append([x, y])
    return celulas


""" ---------------------------------------------------------- """

"""
Um movimento é valido se a célula escolhida está vazia.
:param (x): coordenada X
:param (y): coordenada Y
:return: True se o tabuleiro[x][y] está vazio
"""


def movimento_valido(x, y):
    if [x, y] in celulas_vazias(tabuleiro):
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (x): coordenadas X
:param (y): coordenadas Y
:param (jogador): o jogador da vez
"""


def exec_movimento(x, y, jogador):
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 16),
mas nunca será dezesseis neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:param (alpha): valor de alpha (maior valor até então para MAX)
:param (beta): valor de beta (menor valor até então para MIN)
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""


def minimax(estado, profundidade, jogador, alpha, beta):
    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        #placar é quantidade de células vazias se COMP ganhar e -quantidade de células vazias se HUMANO ganhar
        placar = avaliacao(estado)
        return [-1, -1, placar]

    if jogador == COMP:
        #Percorre todas as células vazias
        for cell in celulas_vazias(estado):
            #x e y recebem a linha e a coluna que representam a célula
            x, y = cell[0], cell[1]
            #célula do tabuleiro recebe o identificador do jogador (+1 se é COMP e -1 se é HUMANO)
            estado[x][y] = jogador
            #é feita uma chamada recursiva com uma célula vazia a menos e trocando-se o jogador
            placar = minimax(estado, profundidade - 1, -jogador, alpha, beta)
            #célula do tabuleiro é definida novamente como vazia
            estado[x][y] = 0
            #linha e coluna dessa célula são definidas como possíveis melhores linha e coluna
            placar[0], placar[1] = x, y
            #se o placar obtido no minimax é melhor (maior) que alpha (maior valor até então para MAX), então alpha recebe esse placar
            if placar[2] > alpha:
                alpha = placar[2]
            #se alpha é maior ou igual a beta (menor valor para MIN), então retorna-se alpha como melhor placar
            if alpha >= beta:
                return [placar[0], placar[1], alpha]
        #é retornado o melhor placar para o estado em questão
        return [placar[0], placar[1], alpha]

    else:
        # Percorre todas as células vazias
        for cell in celulas_vazias(estado):
            # x e y recebem a linha e a coluna que representam a célula
            x, y = cell[0], cell[1]
            # célula do tabuleiro recebe o identificador do jogador (+1 se é COMP e -1 se é HUMANO)
            estado[x][y] = jogador
            # é feita uma chamada recursiva com uma célula vazia a menos e trocando-se o jogador
            placar = minimax(estado, profundidade - 1, -jogador, alpha, beta)
            # célula do tabuleiro é definida novamente como vazia
            estado[x][y] = 0
            # linha e coluna dessa célula são definidas como possíveis melhores linha e coluna
            placar[0], placar[1] = x, y
            # se o placar obtido no minimax é melhor (menor) que beta (menor valor até então para MIN), então beta recebe esse placar
            if placar[2] < beta:
                beta = placar[2]
            # se alpha é maior ou igual a beta (menor valor para MIN), então retorna-se beta como melhor placar
            if alpha >= beta:
                return [placar[0], placar[1], beta]
        # é retornado o melhor placar para o estado em questão
        return [placar[0], placar[1], beta]

""" ---------------------------------------------------------- """

"""
Limpa o console para SO Windows
"""


def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


""" ---------------------------------------------------------- """

"""
Imprime o tabuleiro no console
:param. (estado): estado atual do tabuleiro
"""


def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    print('--------------------')
    for row in estado:
        print('\n--------------------')
        for cell in row:
            if cell == +1:
                print('|', comp_escolha, '|', end='')
            elif cell == -1:
                print('|', humano_escolha, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n--------------------')


""" ---------------------------------------------------------- """

"""
Chama a função minimax se a profundidade < 16,
ou escolhe uma coordenada aleatória.
:param (comp_escolha): Computador escolhe X ou O
:param (humano_escolha): HUMANO escolhe X ou O
:return:
"""


def IA_vez(comp_escolha, humano_escolha):
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    if profundidade == 16:
        x = choice([0, 1, 2, 3])
        y = choice([0, 1, 2, 3])
    else:
        #Verifica se é possível vencer no próximo movimento. Se for possível, é feito esse movimento
        copia_tabuleiro = deepcopy(tabuleiro)
        for cell in celulas_vazias(copia_tabuleiro):
            x, y = cell[0], cell[1]
            copia_tabuleiro[x][y] = COMP
            if vitoria(copia_tabuleiro, COMP):
                exec_movimento(x, y, COMP)
                return
            copia_tabuleiro[x][y] = 0

        #Verifica se o oponente pode vencer no próximo movimento. Se for possível, bloqueamos esse movimento
        copia_tabuleiro = deepcopy(tabuleiro)
        for cell in celulas_vazias(copia_tabuleiro):
            x, y = cell[0], cell[1]
            copia_tabuleiro[x][y] = HUMANO
            if vitoria(copia_tabuleiro, HUMANO):
                exec_movimento(x, y, COMP)
                return
            copia_tabuleiro[x][y] = 0

        #Chama a função minimax com poda alfa-beta, passando o valor de alpha como -infinito e o de beta como +infinito
        move = minimax(tabuleiro, profundidade, COMP, -infinity, +infinity)
        x, y = move[0], move[1]

    exec_movimento(x, y, COMP)


""" ---------------------------------------------------------- """


def HUMANO_vez(comp_escolha, humano_escolha):
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    # Dicionário de movimentos válidos
    movimento = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3],
        5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3],
        9: [2, 0], 10: [2, 1], 11: [2, 2], 12: [2, 3],
        13: [3, 0], 14: [3, 1], 15: [3, 2], 16: [3, 3],
    }

    limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    while (movimento < 1 or movimento > 16):
        try:
            movimento = int(input('Use numero (1..16): '))
            coord = movimentos[movimento]
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO)

            if tenta_movimento == False:
                print('Movimento Inválido')
                movimento = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')


""" ---------------------------------------------------------- """

"""
Funcao Principal que chama todas funcoes
"""


def main():
    limpa_console()
    humano_escolha = ''  # Pode ser X ou O
    comp_escolha = ''  # Pode ser X ou O
    primeiro = ''  # se HUMANO e o primeiro

    # HUMANO escolhe X ou O para jogar
    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    # Setting Computador's choice
    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    # HUMANO pode começar primeiro
    limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    # Laço principal do jogo
    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(comp_escolha, humano_escolha)
        IA_vez(comp_escolha, humano_escolha)

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()