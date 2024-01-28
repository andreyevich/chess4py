import pygame
import os

# For the ICT lab.
window_pos = (50, 50)
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{window_pos[0]},{window_pos[1]}'

pygame.init()

window = pygame.display.set_mode((784, 784))
pygame.display.set_caption("chess4py")

board_img = pygame.image.load('rect-8x8.png')
selected_sqr_img = pygame.image.load('selected-square.png')
available_sqr_img = pygame.image.load('available-square.png')
available_capture_img = pygame.image.load('available-capture.png')

sqr_size = 96
border_width = 8
border_height = border_width


class Piece:
    def __init__(self, y, x, piece_type, color):
        self.y = y
        self.x = x
        self.type = piece_type
        self.color = color
        self.selected = False
        self.sqr = pygame.Rect(self.x * sqr_size + border_width,
                               self.y * sqr_size + border_height, sqr_size, sqr_size)

        self.img = pygame.image.load(f'{color}-{piece_type}.png')
        self.img = pygame.transform.scale(self.img, (sqr_size, sqr_size))

    def draw(self, board):
        if self.selected:
            window.blit(selected_sqr_img, (self.x * sqr_size +
                        border_width, self.y * sqr_size + border_height))

            self.draw_available_moves(board)

        window.blit(self.img, (self.x * sqr_size + border_width,
                    self.y * sqr_size + border_height))

    def update(self, event, board):
        global turn

        if turn != self.color:
            return

        self.sqr = pygame.Rect(self.x * sqr_size + border_width,
                               self.y * sqr_size + border_height, sqr_size, sqr_size)

        if event == None:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sqr.collidepoint(pygame.mouse.get_pos()):
                self.selected = not self.selected
            elif self.selected:
                moves = self.available_moves(board)

                for move in moves:
                    sqr = pygame.Rect(move[1] * sqr_size + border_width,
                                      move[0] * sqr_size + border_height, sqr_size, sqr_size)

                    if sqr.collidepoint(pygame.mouse.get_pos()):
                        board[self.y][self.x] = None
                        self.y = move[0]
                        self.x = move[1]

                        if move[2] == 'capture':
                            pieces.remove(board[self.y][self.x])

                        board[self.y][self.x] = self

                        if turn == 'white':
                            turn = 'black'
                        elif turn == 'black':
                            turn = 'white'

                self.selected = False
            else:
                self.selected = False

    # Returns the available moves a piece can do in the form [(y, x, type)].
    # type - move or capture.

    def available_moves(self, board):
        return []

    def draw_available_moves(self, board):
        for move in self.available_moves(board):
            if move[2] == 'move':
                window.blit(
                    available_sqr_img, (move[1] * sqr_size + border_width, move[0] * sqr_size + border_height))
            elif move[2] == 'capture':
                window.blit(
                    available_capture_img, (move[1] * sqr_size + border_width, move[0] * sqr_size + border_height))


class Rook(Piece):
    def available_moves(self, board):
        moves = []

        for y in range(self.y + 1, 8):
            if board[y][self.x] == None:
                moves.append((y, self.x, 'move'))
            elif board[y][self.x].color != self.color:
                moves.append((y, self.x, 'capture'))
                break
            else:
                break

        for y in range(self.y - 1, -1, -1):
            if board[y][self.x] == None:
                moves.append((y, self.x, 'move'))
            elif board[y][self.x].color != self.color:
                moves.append((y, self.x, 'capture'))
                break
            else:
                break

        for x in range(self.x + 1, 8):
            if board[self.y][x] == None:
                moves.append((self.y, x, 'move'))
            elif board[self.y][x].color != self.color:
                moves.append((self.y, x, 'capture'))
                break
            else:
                break

        for x in range(self.x - 1, -1, -1):
            if board[self.y][x] == None:
                moves.append((self.y, x, 'move'))
            elif board[self.y][x].color != self.color:
                moves.append((self.y, x, 'capture'))
                break
            else:
                break

        return moves


class Knight(Piece):
    def available_moves(self, board):
        moves = []
        # I'm too lazy to develop an algorithm for this...
        hardcoded_moves = [
            (self.y + 2, self.x - 1),
            (self.y + 2, self.x + 1),

            (self.y - 1, self.x + 2),
            (self.y + 1, self.x + 2),

            (self.y - 2, self.x + 1),
            (self.y - 2, self.x - 1),

            (self.y + 1, self.x - 2),
            (self.y - 1, self.x - 2)
        ]

        for move in hardcoded_moves:
            if (move[0] <= 7 and move[0] >= 0) and (move[1] <= 7 and move[1] >= 0):
                if board[move[0]][move[1]] == None:
                    moves.append((move[0], move[1], 'move'))
                elif board[move[0]][move[1]].color != self.color:
                    moves.append((move[0], move[1], 'capture'))

        return moves


class Bishop(Piece):
    def available_moves(self, board):
        moves = []

        y = self.y - 1
        x = self.x - 1
        while y >= 0 and x >= 0:
            if board[y][x] == None:
                moves.append((y, x, 'move'))
            elif board[y][x].color != self.color:
                moves.append((y, x, 'capture'))
                break
            else:
                break

            y -= 1
            x -= 1

        y = self.y + 1
        x = self.x + 1
        while y <= 7 and x <= 7:
            if board[y][x] == None:
                moves.append((y, x, 'move'))
            elif board[y][x].color != self.color:
                moves.append((y, x, 'capture'))
                break
            else:
                break

            y += 1
            x += 1

        y = self.y + 1
        x = self.x - 1
        while y <= 7 and x >= 0:
            if board[y][x] == None:
                moves.append((y, x, 'move'))
            elif board[y][x].color != self.color:
                moves.append((y, x, 'capture'))
                break
            else:
                break

            y += 1
            x -= 1

        y = self.y - 1
        x = self.x + 1
        while y >= 0 and x <= 7:
            if board[y][x] == None:
                moves.append((y, x, 'move'))
            elif board[y][x].color != self.color:
                moves.append((y, x, 'capture'))
                break
            else:
                break

            y -= 1
            x += 1

        return moves


class Queen(Piece):
    def available_moves(self, board):
        moves = []

        rook = Rook(self.y, self.x, 'rook', self.color)
        bishop = Bishop(self.y, self.x, 'bishop', self.color)

        moves.extend(rook.available_moves(board))
        moves.extend(bishop.available_moves(board))

        return moves


class King(Piece):
    def available_moves(self, board):
        moves = []

        # I'm too lazy to code an algorithm here...
        hardcoded_moves = [
            (self.y - 1, self.x),
            (self.y + 1, self.x),
            (self.y, self.x - 1),
            (self.y, self.x + 1),

            (self.y + 1, self.x - 1),
            (self.y + 1, self.x + 1),
            (self.y - 1, self.x + 1),
            (self.y - 1, self.x - 1)
        ]

        for move in hardcoded_moves:
            if (move[0] <= 7 and move[0] >= 0) and (move[1] <= 7 and move[1] >= 0):
                if board[move[0]][move[1]] == None:
                    moves.append((move[0], move[1], 'move'))
                elif board[move[0]][move[1]].color != self.color:
                    moves.append((move[0], move[1], 'capture'))

        return moves


class Pawn(Piece):
    def available_moves(self, board):
        moves = []
        direction = 1

        if self.color == 'white':
            direction = -direction

        if self.y + direction >= 0 and self.y + direction <= 7:
            if board[self.y + direction][self.x] == None:
                moves.append((self.y + direction, self.x, 'move'))

        if self.color == 'white':
            if self.y == 6 and board[self.y - 2][self.x] == None:
                moves.append((self.y - 2, self.x, 'move'))
        elif self.color == 'black':
            if self.y == 1 and board[self.y + 2][self.x] == None:
                moves.append((self.y + 2, self.x, 'move'))

        if self.color == 'white':
            if self.y - 1 >= 0 and self.x - 1 >= 0:
                if board[self.y - 1][self.x - 1] != None:
                    moves.append((self.y - 1, self.x - 1, 'capture'))
            if self.y - 1 >= 0 and self.x + 1 >= 0:
                if board[self.y - 1][self.x + 1] != None:
                    moves.append((self.y - 1, self.x + 1, 'capture'))
        elif self.color == 'black':
            if self.y + 1 >= 0 and self.x - 1 >= 0:
                if board[self.y + 1][self.x - 1] != None:
                    moves.append((self.y + 1, self.x - 1, 'capture'))
            if self.y + 1 >= 0 and self.x + 1 >= 0:
                if board[self.y + 1][self.x + 1] != None:
                    moves.append((self.y + 1, self.x + 1, 'capture'))

        return moves


pieces = [
    Rook(0, 0, 'rook', 'black'),
    Rook(0, 7, 'rook', 'black'),
    Rook(7, 0, 'rook', 'white'),
    Rook(7, 7, 'rook', 'white'),

    Knight(0, 1, 'knight', 'black'),
    Knight(0, 6, 'knight', 'black'),
    Knight(7, 1, 'knight', 'white'),
    Knight(7, 6, 'knight', 'white'),

    Bishop(0, 2, 'bishop', 'black'),
    Bishop(0, 5, 'bishop', 'black'),
    Bishop(7, 2, 'bishop', 'white'),
    Bishop(7, 5, 'bishop', 'white'),

    Queen(0, 3, 'queen', 'black'),
    Queen(7, 3, 'queen', 'white'),

    King(0, 4, 'king', 'black'),
    King(7, 4, 'king', 'white')
]

for p in range(0, 8):
    pieces.append(Pawn(1, p, 'pawn', 'black'))
    pieces.append(Pawn(6, p, 'pawn', 'white'))

board = []
turn = 'white'

for y in range(0, 8):
    board.append([])
    for x in range(0, 8):
        board[y].append(None)

for piece in pieces:
    board[piece.y][piece.x] = piece

running = True
while running:
    event = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(board_img, (0, 0))

    for piece in pieces:
        piece.draw(board)

    for piece in pieces:
        piece.update(event, board)

    pygame.display.update()

pygame.quit()
