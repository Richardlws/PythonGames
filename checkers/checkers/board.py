import pygame
from .constants import BLACK, ROWS, COLS, RED, WHITE, SQUARE_SIZE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            #print("ROWS=", ROWS)
            #print("COLS=", COLS)
            for col in range(COLS):
                #print("cols=",col)
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                        #print("<3 row:",row)
                        #print("<3 cod:",col)
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                        #print(">4 row:", row)
                        #print(">4 cod:", col)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            #print("rows=", row)
            for col in range(COLS):
                #print("cols=", col)
                piece = self.board[row][col]
                #print("piece:", piece)
                if piece != 0:
                    piece.draw(win)
