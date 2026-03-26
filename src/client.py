import socket
import pygame

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

all_notations = [
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
    
    def update_board(self,parameter):
        pass

    def render_board(self, screen):
        for notation, square in zip(all_notations, board):
            self.render_square(square, notation, screen)
    
    def render_square(self, square, notation, screen):
        if square == WHITE_ROOK:
            screen.blit(self.white_rook, place_piece(notation))
        elif square == WHITE_KNIGHT:
            screen.blit(self.white_knight, place_piece(notation))
        elif square == WHITE_BISHOP:
            screen.blit(self.white_bishop, place_piece(notation))
        elif square == WHITE_QUEEN:
            screen.blit(self.white_queen, place_piece(notation)) 
        elif square == WHITE_KING:
            screen.blit(self.white_king, place_piece(notation)) 
        elif square == WHITE_PAWN:
            screen.blit(self.white_pawn, place_piece(notation))

        elif square == BLACK_ROOK:
            screen.blit(self.black_rook, place_piece(notation))
        elif square == BLACK_KNIGHT:
            screen.blit(self.black_knight, place_piece(notation))
        elif square == BLACK_BISHOP:
            screen.blit(self.black_bishop, place_piece(notation))
        elif square == BLACK_QUEEN:
            screen.blit(self.black_queen, place_piece(notation)) 
        elif square == BLACK_KING:
            screen.blit(self.black_king, place_piece(notation)) 
        elif square == BLACK_PAWN:
            screen.blit(self.black_pawn, place_piece(notation))

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
    notations = []
    coords = []
    rects = []

    for y in range(8):
        for x in range(8):
            notation = get_notation(y, x)
            label = font.render(f"{notation}", 1, (255,0,0))
            labels.append(label)
            notations.append(notation)
            coords.append((x*64,y*64))   

    for s in notations:
        print(s)

    for coord in coords:
        rect = pygame.Rect(*coord, 64, 64)   
        rects.append(rect)

    sprites = Sprites()

    running = True
    
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

        screen.blit(sprites.board, (0,0))

        for coord, label in zip(coords,labels):
            screen.blit(label, coord)

        sprites.render_board(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()