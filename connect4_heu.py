import numpy as np
import time
from os import system, name

ROWS = 15
COLUMNS = 16

# ----------------------------------------------------------------------------------
def clear():
    # para windows
    if name == 'nt':
        _ = system('cls')

    # para mac e linux(aqui, os.name eh 'posix')
    else:
        _ = system('clear')

# ----------------------------------------------------------------------------------
def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

# ----------------------------------------------------------------------------------
def valid_location(board, column):
    return board[ROWS - 1][column] == 0

# ----------------------------------------------------------------------------------
def drop_piece(board, column, piece):
    for r in range(ROWS):
        if board[r][column] == 0:
            board[r][column] = piece
            return

# ----------------------------------------------------------------------------------

def is_winning_move(board, piece, ultima_jogada):
    linha, coluna = ultima_jogada
    # verifica se existem quatro peças em linha na horizontal, vertical e diagonais

    #horizontal
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
            else:
                break
    
    #vertical
    for r in range(ROWS - 3):
        if board[r][coluna] == piece and board[r + 1][coluna] == piece and board[r + 2][coluna] == piece and board[r + 3][coluna] == piece:
            return True
        else:
            break

    #diagonal [/]
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
            else:
                break

    #diagonal invertida [\]
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
            else:
                break

# ----------------------------------------------------------------------------------
def minimax(board, depth, maximizing_player):
    if is_winning_move(board, 2, ultima_jogada):  # IA ganhou
        return (None, 100)
    elif is_winning_move(board, 1, ultima_jogada):  # jogador humano ganhou
        return (None, -100)
    elif len(get_valid_locations(board)) == 0:  # jogo empatado
        return (None, 0)
    elif depth == 0:  # profundidade máxima atingida
        return (None, 0)

    valid_locations = get_valid_locations(board)
    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 2)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # minimizing player
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 1)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


# ----------------------------------------------------------------------------------
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# ----------------------------------------------------------------------------------
# CSI457 e CSI701
# Programa Principal
# Data: 06/05/2023
# ----------------------------------------------------------------------------------
board = create_board()
game_over = False
turn = 0

clear()
while not game_over:
    # Movimento do Jogador 1
    if turn == 0:
        col = int(input("Jogador 1, selecione a coluna (0-6):"))
        if valid_location(board, col):
            drop_piece(board, col, 1)
            ultima_jogada = (np.where(board[:, col] != 0)[0][0], col) # salva a ultima jogada do jogador 1 por meio da biblioteca numpy
            if is_winning_move(board, 1, ultima_jogada):
                print("Jogador 1 Vence!! Parabéns!!")
                game_over = True
    # Movimento da IA
    else:
        inicio = time.time()
        col, minimax_score = minimax(board, 4, True)
        if valid_location(board, col):
            drop_piece(board, col, 2)
            ultima_jogada = (np.where(board[:, col] != 0)[0][0], col) # salva a ultima jogada da IA por meio da biblioteca numpy
            if is_winning_move(board, 2, ultima_jogada):
                print("Jogador 2 Vence!!!")
                game_over = True
        fim = time.time()
        tempo = fim - inicio
        tempo = round(tempo,3)
        print("Tempo de execução (IA): ", tempo, "segundos")
    print(board)
    print(" ")
    turn += 1
    turn = turn % 2