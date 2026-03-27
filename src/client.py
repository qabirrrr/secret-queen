import socket
import pygame
import json

SQUARE_SIZE = 64 # each square is 64 by 64
PIECE_SIZE = 48 # each piece on the board is 48 by 48

# enums
# 0 = empty
WHITE_ROOK = 1
WHITE_KNIGHT = 2
WHITE_BISHOP = 3
WHITE_QUEEN = 4
WHITE_KING = 5
WHITE_PAWN = 6
BLACK_ROOK = 7
BLACK_KNIGHT = 8
BLACK_BISHOP = 9
BLACK_QUEEN = 10
BLACK_KING = 11
BLACK_PAWN = 12

notations = [
    'h1', 'g1', 'f1', 'e1', 'd1', 'c1', 'b1', 'a1',
    'h2', 'g2', 'f2', 'e2', 'd2', 'c2', 'b2', 'a2',
    'h3', 'g3', 'f3', 'e3', 'd3', 'c3', 'b3', 'a3',
    'h4', 'g4', 'f4', 'e4', 'd4', 'c4', 'b4', 'a4',
    'h5', 'g5', 'f5', 'e5', 'd5', 'c5', 'b5', 'a5',
    'h6', 'g6', 'f6', 'e6', 'd6', 'c6', 'b6', 'a6',
    'h7', 'g7', 'f7', 'e7', 'd7', 'c7', 'b7', 'a7',
    'h8', 'g8', 'f8', 'e8', 'd8', 'c8', 'b8', 'a8'
]

board = [
    WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK,
    WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN,
    BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK
]

'''
def main():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            string = input("What would you like to send to the server?: ")
            s.sendall(bytes(string, 'utf-8'))
            data = s.recv(1024)
            print(f"Data sent to server : '{data}'")
'''

class Sprites:
    def __init__(self):
        self.board = self.load_texture("res/board.png", (512, 512))
        self.black_pawn = self.load_texture("res/bP.png")
        self.black_rook = self.load_texture("res/bR.png")
        self.black_knight = self.load_texture("res/bN.png")
        self.black_bishop = self.load_texture("res/bB.png")
        self.black_king = self.load_texture("res/bK.png")
        self.black_queen = self.load_texture("res/bQ.png")
        self.white_pawn = self.load_texture("res/wP.png")
        self.white_rook = self.load_texture("res/wR.png")
        self.white_knight = self.load_texture("res/wN.png")
        self.white_bishop = self.load_texture("res/wB.png")
        self.white_king = self.load_texture("res/wK.png")
        self.white_queen = self.load_texture("res/wQ.png")

    def load_texture(self, fp, scale = (PIECE_SIZE, PIECE_SIZE)):
        texture = pygame.image.load(fp)
        texture = pygame.transform.scale(texture, scale)
        return texture
    
    def update_board(self, old_notation, new_notation, piece):
        for i in range(len(notations)):
            if notations[i] == old_notation:
                board[i] = 0
            elif notations[i] == new_notation:
                board[i] = piece
        print("Updated")
        print(old_notation, new_notation, piece)

    def render_board(self, screen):
        for notation, square in zip(notations, board):
            if square != 0: self.render_square(square, notation, screen)
    
    def render_square(self, square, notation, screen):
        piece = ""
        if square == WHITE_ROOK:
            piece = self.white_rook
        elif square == WHITE_KNIGHT:
            piece = self.white_knight
        elif square == WHITE_BISHOP:
            piece = self.white_bishop
        elif square == WHITE_QUEEN:
            piece = self.white_queen
        elif square == WHITE_KING:
            piece = self.white_king
        elif square == WHITE_PAWN:
            piece = self.white_pawn

        elif square == BLACK_ROOK:
           piece = self.black_rook
        elif square == BLACK_KNIGHT:
            piece = self.black_knight
        elif square == BLACK_BISHOP:
            piece = self.black_bishop
        elif square == BLACK_QUEEN:
            piece = self.black_queen
        elif square == BLACK_KING:
            piece = self.black_king
        elif square == BLACK_PAWN:
            piece = self.black_pawn

        screen.blit(piece, place_piece(notation))

def is_black(square):
    if square >= 1 and square <= 6:
        return True
    elif square >= 7 and square <= 12:
        return False


def get_notation(y, x):
    notation = ""
    alps = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
    for i, alp in enumerate(alps):
        if x == i:
            notation += alp
            break
    notation += f'{y+1}'
    return notation

def get_coord(notation):
    alps = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
    for i, alp in enumerate(alps):
        if notation[0] == alp:
            x = i * SQUARE_SIZE
    y = (int(notation[1]) - 1) * SQUARE_SIZE
    return (x,y)

def place_piece(notation):
    notation = get_coord(notation)

    first = notation[0]
    second = notation[1]

    middle_x = (SQUARE_SIZE - PIECE_SIZE) / 2
    middle_y = (SQUARE_SIZE - PIECE_SIZE) / 2

    first += middle_x
    second += middle_y

    return (first, second)
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 15)
    
    labels = []
    coords = []
    rects = []

    for y in range(8):
        for x in range(8):
            n = get_notation(y, x)
            label = font.render(f"{n}", 1, "blue")
            labels.append(label)
            coords.append((x*64,y*64))   

    for coord in coords:
        rect = pygame.Rect(*coord, 64, 64)   
        rects.append(rect)

    sprites = Sprites()

    running = True

    state = 1
    selected = False
    # 0 -> finding a piece to select (source)
    # 1 -> finding where to place piece (destination)

    old = ""
    new = ""
    piece = ""

    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        
        #while True:
            #string = input("What would you like to send to the server?: ")
            #s.sendall(bytes(string, 'utf-8'))
            #data = s.recv(1024)
            #print(f"Data sent to server : '{data}'")
    
        while running:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True

            mousepos = pygame.mouse.get_pos()
            for rect, notation in zip(rects, notations):
                if rect.collidepoint(mousepos) and clicked:
                    print(notation)

            if clicked:
                state = (state + 1) % 2
                
                if state == 0:
                    for square, notation, rect in zip(board, notations, rects):
                        if rect.collidepoint(mousepos):
                            old = notation
                            piece = square

                else:
                    for square, notation, rect in zip(board, notations, rects):
                        if rect.collidepoint(mousepos):
                            new = notation
                            sprites.update_board(old, new, piece)
                            data = f"{old},{new},{piece}" # unsafe approach, but who gives a shit?
                            sock.sendall(bytes(data, 'utf-8'))
                            old = ""
                            new = ""
                            piece = ""

            screen.blit(sprites.board, (0,0))

            for coord, label in zip(coords,labels):
                screen.blit(label, coord)

            sprites.render_board(screen)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()