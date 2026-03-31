import socket
import pygame
import json
import select

SQUARE_SIZE = 64 # each square is 64 by 64
PIECE_SIZE = 48 # each piece on the board is 48 by 48

ALPHABETS = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

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

class Logic:
    def __init__(self):
        self.previous_opponent_move = []
        self.pieces = [self.rook, self.knight, self.bishop, self.queen, self.king, self.pawn,
                    self.rook, self.knight, self.bishop, self.queen, self.king, self.pawn
        ]

    def rook(self, current_notation, clientcolor): # -> todo: return legal moves in each function
        print("Rook")
        return ["d4", "d5"]

    def knight(self, current_notation, clientcolor):
        print("Knight")
        return ["d4", "d5"]

    def bishop(self, current_notation, clientcolor):
        print("Bishop")
        return ["d4", "d5"]

    def queen(self, current_notation, clientcolor):
        print("Queen")
        return ["d4", "d5"]
    
    def king(self, current_notation, clientcolor):
        print("King")
        return ["d4", "d5"]

    def pawn(self, current_notation, clientcolor):
        possible_capture_alphabets = []
        legal_moves = []

        # todo for enpassant:

        # check if previous move is a pawn move
        # check if it was a double push
        # if it was, check if this pawn is DIRECTLY beside it (same rank, beside it)
        # if it is, enpassant = true


        # to execute en passant,
        # send "y" or "n" as last thing to server
        # n means no en passant
        # y means yes en passant

        # add parameter to update_board() en_passant. (arguments is "y"/"n")
        # if en_passant == "y":
            # after pawn captures in front, remove the opponent pawn behind it
            # (in other words, make the pawn originally beside it disappear. effectively capturing the pawn. hence, enpassant)
            # (otherwise, the pawn wld go in front of the pawn. but the enemy pawn wldnt get captured)

        if clientcolor == "white":
            next_square = +1
            starting_square = 2
            second_square = 4
            enemy_color = "black"
        else:
            next_square = -1
            starting_square = 7
            second_square = 5
            enemy_color = "white"


        # forward moves

        one_square = current_notation[0] + f"{int(current_notation[1]) + next_square}" # 1 square above
        for square, notation in zip(board, notations):
            if one_square == notation:
                blockage = square != 0 # a piece is already blocking the square

        if not blockage:
            legal_moves.append(one_square)
            if int(current_notation[1]) == starting_square:
                    two_squares = current_notation[0] + str(second_square) # 2 squares above for starting position
                    legal_moves.append(two_squares)



        # captures 

        alps = list(ALPHABETS)
        alps.reverse()
        for i, each in enumerate(alps):
            if each == current_notation[0]:
                try: 
                    if each != 'h': possible_capture_alphabets.append(alps[i+1])
                except: pass

                try: 
                    if each != 'a': possible_capture_alphabets.append(alps[i-1])
                except: pass


        possible_captures = [f"{alp}{int(current_notation[1])+next_square}" for alp in possible_capture_alphabets]

        legal_captures = []
        for possible_capture in possible_captures:
            for square, notation in zip(board, notations):
                if possible_capture == notation:
                    if square != 0:
                        if get_color(square) == enemy_color: legal_captures.append(possible_capture) # capturing enemy pawn
                        break

        legal_moves += legal_captures


        # en passant (opponent's previous move is a 2 square push && my pawn is beside it)

        return legal_moves

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
    
    def update_board(self, old_notation, new_notation, piece, promotion_icon = "Q"):
        for i in range(len(notations)):
            if notations[i] == old_notation:
                board[i] = 0
            elif notations[i] == new_notation:
                board[i] = piece
                new_idx = i

        # pawn promotion
        # (later on make it so you can choose knight, bishop or rook)
        if piece == WHITE_PAWN:

            if promotion_icon == "Q":
                promotion_piece = WHITE_QUEEN
            elif promotion_icon == "N":
                promotion_piece = WHITE_KNIGHT
            elif promotion_icon == "B":
                promotion_piece = WHITE_BISHOP
            elif promotion_icon == "R":
                promotion_piece = WHITE_ROOK

            if int(new_notation[1]) == 8:
                board[new_idx] = promotion_piece

        elif piece == BLACK_PAWN:
            if promotion_icon == "Q":
                promotion_piece = BLACK_QUEEN
            elif promotion_icon == "N":
                promotion_piece = BLACK_KNIGHT
            elif promotion_icon == "B":
                promotion_piece = BLACK_BISHOP
            elif promotion_icon == "R":
                promotion_piece = BLACK_ROOK

            if int(new_notation[1]) == 1:
                board[new_idx] = promotion_piece

        print("Updated")
        print(old_notation, new_notation, piece)

    def render_board(self, screen, clientcolor):
        for notation, square in zip(notations, board):
            if square != 0: self.render_square(square, notation, screen, clientcolor)
    
    def render_square(self, square, notation, screen, clientcolor):
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

        screen.blit(piece, place_piece(notation, clientcolor))

def render_legals(screen, rects, legal_moves):
    for notation, rec in zip(notations, rects):
        if notation in legal_moves:
            pygame.draw.rect(screen, "black", rec)

def get_color(square):
    if square >= 1 and square <= 6:
        return "white"
    elif square >= 7 and square <= 12:
        return "black"
        

def get_coord(notation, clientcolor):
    alps = list(ALPHABETS)

    if clientcolor == "black":
        for i, alp in enumerate(alps):
            if notation[0] == alp:
                x = i * SQUARE_SIZE
        y = (int(notation[1]) - 1) * SQUARE_SIZE    

    elif clientcolor == "white":
        alps.reverse()
        for i, alp in enumerate(alps):
            if notation[0] == alp:
                x = i * SQUARE_SIZE
        y = abs(8-int(notation[1])) * SQUARE_SIZE

    return (x, y)

def place_piece(notation, clientcolor):
    coord = get_coord(notation, clientcolor)

    first = coord[0]
    second = coord[1]

    middle_x = (SQUARE_SIZE - PIECE_SIZE) / 2
    middle_y = (SQUARE_SIZE - PIECE_SIZE) / 2

    first += middle_x
    second += middle_y

    return (first, second)

def select_piece(notation, square, logic, clientcolor): # -> todo: also return legal moves 
    old = notation
    piece = square
    legal_moves = logic.pieces[square-1](old, clientcolor)
    print(f"Legal moves are {legal_moves}")
    return legal_moves, old, piece
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 15)
    
    labels = []
    coords = []
    rects = []

    sprites = Sprites()
    logic = Logic()

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

    legal_moves = []

    promotion_icon = "Q"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        
        clientcolor = (sock.recv(1024)).decode()
        print(clientcolor)

        if clientcolor == "white":
            turn = True
        else:
            turn = False

        for notation in notations:
            n = notation
            label = font.render(f"{n}", 1, "blue")
            labels.append(label)
            coords.append(get_coord(n, clientcolor))   

        for coord in coords:
            rect = pygame.Rect(*coord, 64, 64)   
            rects.append(rect)

        while running:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        promotion_icon = "Q"
                    elif event.key == pygame.K_b:
                        promotion_icon = "B"
                    elif event.key == pygame.K_n:
                        promotion_icon = "N"
                    elif event.key == pygame.K_r:
                        promotion_icon = "R"
                    print(promotion_icon)

            mousepos = pygame.mouse.get_pos()
            for rect, notation in zip(rects, notations):
                if rect.collidepoint(mousepos) and clicked:
                    print(f"Clicked on {notation}")

            if clicked and turn:
                state = (state + 1) % 2
                
                if state == 0: # select a piece
                    for square, notation, rect in zip(board, notations, rects):
                        if rect.collidepoint(mousepos):
                            if get_color(square) != clientcolor: # can only select my own color
                                state = 1
                                break
                            legal_moves, old, piece = select_piece(notation, square, logic, clientcolor)

                else: # move the piece
                    for square, notation, rect in zip(board, notations, rects):
                        if rect.collidepoint(mousepos):
                            if get_color(square) == clientcolor: # cannot capture my own color. instead, select it as new piece
                                legal_moves, old, piece = select_piece(notation, square, logic, clientcolor)
                                state = 0
                                break
                            
                            if notation in legal_moves:
                                new = notation
                                sprites.update_board(old, new, piece, promotion_icon)
                                data = f"{old},{new},{piece}" # unsafe af, but who gives a shit?
                                sock.sendall(bytes(data, 'utf-8'))
                                old = ""
                                new = ""
                                piece = ""
                                legal_moves = []
                                turn = False

                            else:
                                state = 0
                                break

            screen.blit(sprites.board, (0,0))

            sock.setblocking(0)

            ready = select.select([sock], [], [], 0)
            if ready[0]:
                data = sock.recv(4096)
                old, new, piece = data.decode().split(",")
                sprites.update_board(old, new, int(piece))
                logic.previous_opponent_move = [old, new, int(piece)]
                turn = True

            for coord, label in zip(coords,labels):
                screen.blit(label, coord)

            sprites.render_board(screen, clientcolor)
            render_legals(screen, rects, legal_moves)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()