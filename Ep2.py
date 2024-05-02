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
#--------------------------------------------------------------

#Inicia-se o jogo
if __name__ == '__main__':

    print(
    """
 ===================================== 
|                                     |
| Bem-vindo ao INSPER - Batalha Naval |
|                                     |
 =======   xxxxxxxxxxxxxxxxx   ======= 

Iniciando o Jogo!
    """
    )
    # Imprime os paises e suas frotas frotas
    for i, pais in enumerate(PAISES.items()):
        print(f"{i+1}: {pais[0]}")
        for navio, qtd in pais[1].items():
            print(f"   {qtd} {navio}")
    
    # Armazenando escolha do jogador com tratamento de erro
    opcoes = ('1','2','3','4','5')
    while True:
        jogador = str(input("\nQual o número da nação da sua frota? "))
        if jogador in opcoes:
            jogador = int(jogador)
            break
        else:
            print(f"'{jogador}' é uma opção inválida! Tente novamente")

    # Cria uma variável para armazenar a nação escolhida pelo jogador
    escolhido = list(PAISES.keys())[jogador-1]
    # Cria-se uma variável para o país que o computador irá representar
    computador = random.choice(list(PAISES.keys()))

    #printa qual nação foi escolhida pelo jogador e continua-se o jogo
    print(f"\nVocê escolheu a nação: {escolhido}")
    print(f"O computador escolheu a nação: {computador}")

    # Cria os mapas utilizados no jogo, o do computador, o do computador visível para o jogador, e o do jogador
    mapa_c = cria_mapa(10)
    mapa_c_real = cria_mapa(10)
    mapa_j = cria_mapa(10)

    # Define as jogadas
    jogadas_jogador = define_jogadas(escolhido)
    jogadas_computador = define_jogadas(computador)

    print(f"O computador está alocando os navios de guerra...")
    # Estrutura para alocação da fropa do computador
    for jogada in jogadas_computador:    
        # Criando lista das possíveis jogadas do computador
        posicoes_possiveis = []
        for i in range(len(COLUNAS)):
            for j in range(len(LINHAS)):
                posicoes_possiveis.append(f"{COLUNAS[i]}{LINHAS[j]}")

        while True:
            pos = random.choice(posicoes_possiveis)
            posicoes_possiveis.remove(pos)
            blocos = CONFIGURACAO[jogada]
            ori    = random.choice(('V', 'H'))
            try:
                mapa_c_real = aloca_navio(mapa_c_real, pos, blocos, ori, 'C')
                break
            except:
                pass
    print("O computador já está em posição de batalha!\n")
        
    # Exibe o tabuleiro
    print_mapa(mapa_c, mapa_j)

    # Estrutura para alocação da tropa do jogador
    for jogada in range(len(jogadas_jogador)):
        navio = jogadas_jogador[jogada]
        blocos = CONFIGURACAO[navio]

        # Imprime a jogada atual
        if blocos > 1:
            print(f"Alocar: {navio} ({blocos} blocos)")
        else:
            print(f"Alocar: {navio} (1 bloco)")
        # Imprime as próximas jogadas
        print(f"Próximos: { ', '.join(jogadas_jogador[jogada+1:]) }")

        while True:
            # Guarda a letra
            while True:
                opcoes = COLUNAS
                letra = str(input("Informe a letra: ")).upper()
                if letra in opcoes:
                    break
                else:
                    print(f"'{letra}' é uma opção inválida! Tente novamente")
            # Guarda a linha
            while True:
                opcoes = LINHAS
                linha = input("Informe a linha: ")
                if linha in opcoes:
                    break
                else:
                    print(f"'{linha}' é uma opção inválida! Tente novamente")

            # Guarda a orientação
            while True:
                opcoes = ['H', 'V']
                orientacao = str(input("Informe a orientação [ v | h ]: ")).upper()
                if orientacao in opcoes:
                    break
                else:
                    print(f"'{orientacao}' é uma opção inválida! Tente novamente")

            try:
                mapa_j = aloca_navio(mapa_j, letra+linha, blocos, orientacao)
                print_mapa(mapa_c, mapa_j)
                break
            except Exception:
                pass

    # Da início ao jogo, loop com contador
    print("\nIniciando a batalha naval!")
    for i in reversed(range(6)):
        time.sleep(1)
        print(f"{i}")

    # Escolhe, aleatoriamente, as coordenadas do tiro do computador
    tiros_possiveis = []
    for i in range(len(COLUNAS)):
        for j in range(len(LINHAS)):
            tiros_possiveis.append(f"{COLUNAS[i]}{LINHAS[j]}")

    while True:
        #Printa os mapas, do computador visível para o jogador, e do jogador
        print_mapa(mapa_c, mapa_j)
        
        #pergunta-se quais as coordenadas do tiro do jogador
        print("\nDefine as coordenadas do seu próximo disparo")
