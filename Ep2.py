# Importação de pacotes
import random
import time

#---------------------------------------------------------------
# Constantes

# Quantidade de blocos por navio
CONFIGURACAO = {
    'destroyer': 3,
    'porta-avioes': 5,
    'submarino': 2,
    'torpedeiro': 3,
    'cruzador': 2,
    'couracado': 4
}

# Frotas de cada pais
PAISES =  {
    'Brasil': {
        'cruzador': 1,
        'torpedeiro': 2,
        'destroyer': 1,
        'couracado': 1,
        'porta-avioes': 1
    }, 
    'França': {
        'cruzador': 3, 
        'porta-avioes': 1, 
        'destroyer': 1, 
        'submarino': 1, 
        'couracado': 1
    },
    'Austrália': {
        'couracado': 1,
        'cruzador': 3, 
        'submarino': 1,
        'porta-avioes': 1, 
        'torpedeiro': 1
    },
    'Rússia': {
        'cruzador': 1,
        'porta-avioes': 1,
        'couracado': 2,
        'destroyer': 1,
        'submarino': 1
    },
    'Japão': {
        'torpedeiro': 2,
        'cruzador': 1,
        'destroyer': 2,
        'couracado': 1,
        'submarino': 1
    }
}

# cores para o terminal
CORES = {
    'reset': '\u001b[0m',
    'red': '\u001b[31m',
    'black': '\u001b[30m',
    'green': '\u001b[32m',
    'yellow': '\u001b[33m',
    'blue': '\u001b[34m',
    'magenta': '\u001b[35m',
    'cyan': '\u001b[36m',
    'white': '\u001b[37m'
}

LINHAS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
COLUNAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
#----------------------------------------------------------------


# Primeiramente, declara-se as funções que serão utilizadas no código
# Implementa-se a função que cria o mapa vazio, n x n
def cria_mapa(n):
    mapa = [[' ' for a in range(n)] for a in range(n)]
    return mapa
#----------------------------------------------

#função que verifica se, a posição escolhida para a peça, é suportada, com base no mapa e em peças posicionadas anteriormente
def posicao_suporta(mapa, blocos, l, c, ori):
    if blocos == 1:
        if mapa[l][c] == "N":
            return False
        else:
            return True
    
    elif blocos > 1:
        if ori in ["V", "v"]:
            for i in range(blocos):
                if (l + i ) >= len(mapa) or mapa[(l + i)][c] == "N":
                    return False 
            return True
                
        elif ori in ["h", "H"]:
            for j in range(blocos):
                if (c + j ) >= len(mapa[l]) or mapa[l][(c + j)] == "N":
                    return False
            
            return True
#---------------------------------------------------

# Retorna uma lista com as tropas a serem alocadas
def define_jogadas(escolha):
    jogadas = []
    for navio, qtd in PAISES[escolha].items():
        for _ in range(qtd):
            jogadas.append(navio)
    return jogadas
#---------------------------------------------------

# Função que aloca navios
def aloca_navio(mapa, posicao, blocos, orientacao, jogador='J'):
    pos_coluna = COLUNAS.index(posicao[0])
    pos_linha = int(posicao[1]) - 1

    # Testa se a posição já está ocupada!    
    if mapa[pos_linha][pos_coluna] == 'N':
        if jogador == 'J':
            print("Posição já ocupada! Tente novamente")
        raise Exception

    # Testa se a posição é suportada
    if not posicao_suporta(mapa, blocos, pos_linha, pos_coluna, orientacao):
        if jogador == 'J':
            print("Posição não suportada! Tente novamente")
        raise Exception

    if orientacao == 'V':
        for i in range(blocos):
            mapa[pos_linha + i][pos_coluna] = 'N'
    else:
        for i in range(blocos):
            mapa[pos_linha][pos_coluna + i] = 'N'
    
    if jogador == 'J':
        print("Navio alocado!")

    return mapa
#---------------------------------------------------

# Função que verifica se algum dos jogadores perdeu todos os navios
# A função "foi derrotado" foi modificada para que o código funcione melhor, agora recebendo o mapa do computador e do jogador como argumentos para verificar qual perdeu
def foi_derrotado(mapa_jogador, mapa_computador):
    cont_jogador = 0
    for l_j in mapa_jogador:
        if 'N' not in l_j:
            cont_jogador += 1
    if cont_jogador == len(mapa_jogador):
        return "Acabou para jogador"
    
    cont_computador = 0
    for l_c in mapa_computador:
        if 'N' not in l_c:
            cont_computador += 1
    if cont_computador == len(mapa_computador):
        return "Acabou para computador"
#--------------------------------------------------------------

#Função que printa o mapa. Esta leva em consideração se algum navio foi posicionado, se algum navio foi atingido, ou se o tiro caiu na água
#Para que o jogador não veja onde estão os navios inimigos, foram feitos três mapas no total
def print_mapa(mapa_computador, mapa_jogador):
    print(f"          \tCOMPUTADOR - {computador}                                        \tJOGADOR - {escolhido}            ")
    print("    A    B    C    D    E    F    G    H    I    J              A    B    C    D    E    F    G    H    I    J   ")

    for i in range(10):

        linha_c = '  '.join('\033[41m X \033[0m' if celula == 'X' else '\033[44m   \033[0m' if celula == 'A' else '   ' for celula in mapa_computador[i])

        linha_j = '  '.join('\033[41m X \033[0m' if celula == 'X' else ('\033[42m N \033[0m' if celula == 'N' else '\033[44m   \033[0m' if celula == 'A' else '   ') for celula in mapa_jogador[i])

        n_linha = f"{i + 1:2}"  

        print(f"{n_linha} {linha_c} {n_linha}      {n_linha} {linha_j} {n_linha}")

    print("    A    B    C    D    E    F    G    H    I    J              A    B    C    D    E    F    G    H    I    J   ")
    return ''
#--------------------------------------------------------------

#Essa função modifica o mapa para mostrar se o local atingido era um navio ou água e da diferentes respostas para o tipo de local atingido
def tiro(mapa, linha, coluna):
    if mapa[linha][coluna] == 'N':
        mapa[linha][coluna] = 'X'
        return "BOOOOOOOMMMMMM!!!!!"
    
    if mapa[linha][coluna] == ' ':
        mapa[linha][coluna] = 'A'
        return "Água"
#--------------------------------------------------------------

#Essa função modifica o mapa do computador visivel ao jogador caso o local atingido tenha sido um navio ou a água
def substitui_mapa(mapa_computador, linha, coluna, tiro):
    if tiro == "BOOOOOOOMMMMMM!!!!!":
        mapa_computador[linha][coluna] = 'X'
    if tiro == "Água":
        mapa_computador[linha][coluna] = 'A'
