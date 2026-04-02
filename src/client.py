import socket
import pygame
import json
import select
import sys
import os

SQUARE_SIZE = 64 # each square is 64 by 64
PIECE_SIZE = 48 # each piece on the board is 48 by 48

ALPHABETS = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

letters = list(reversed((ALPHABETS))) # ['a', 'b', ..]

g_kingside_castle_possible = True
g_queenside_castle_possible = True
g_castled = False

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
        self.possible_enpassant = [] # [initial notation, capture notation]
        self.possible_kingside_castle = []
        self.possible_queenside_castle = []
        self.pieces = [self.rook, self.knight, self.bishop, self.queen, self.king, self.pawn,
                    self.rook, self.knight, self.bishop, self.queen, self.king, self.pawn
        ]

    def rook(self, current_notation, clientcolor): 

        def get_moves(ranges, current_notation, clientcolor, direction):
            legal_moves = []
            iterate = True 
            for i in ranges:
                if not iterate: break

                if direction == "vertical": move_notation = f"{current_notation[0]}{i}"
                if direction == "horizontal": move_notation = f"{letters[i]}{current_notation[1]}"

                for square, notation in zip(board, notations):
                    if move_notation == notation:
                        if square != 0:
                            if get_color(square) != clientcolor: legal_moves.append(notation)
                            iterate = False
                            break
                        else:
                            legal_moves.append(notation)
                            break
            return legal_moves

        possibles = []
        legals = []

        current_rank = int(current_notation[1])

        current_file = current_notation[0]
        for i, letter in enumerate(letters):
            if current_file == letter:
                current_file_index = i

        up = get_moves(range(current_rank+1, 8+1), current_notation, clientcolor, "vertical")
        down = get_moves(range(current_rank-1, 0, -1), current_notation, clientcolor, "vertical")
        left = get_moves(range(current_file_index+1, 8), current_notation, clientcolor, "horizontal")
        right = get_moves(range(current_file_index-1, -1, -1), current_notation, clientcolor, "horizontal")
       
        legals += up
        legals += down
        legals += left
        legals += right
        
        return legals

    def knight(self, current_notation, clientcolor):
        legals = []
        possibles = []

        one_letter_beside = get_beside(current_notation[0])
        two_letter_beside = get_beside(current_notation[0], 2)

        for e in one_letter_beside:
            try: possibles.append (f"{e}{int(current_notation[1]) + 2}")
            except: pass

        for e in two_letter_beside:
            try: possibles.append (f"{e}{int(current_notation[1]) + 1}")
            except: pass

        for e in one_letter_beside:
            try:
                if int(current_notation[1]) > 2: possibles.append (f"{e}{int(current_notation[1]) - 2}")
            except: pass

        for e in two_letter_beside:
            try: 
                if int(current_notation[1]) > 1: possibles.append (f"{e}{int(current_notation[1]) - 1}")
            except: pass

        for possible in possibles:
            if possible in notations:
                for square, notation in zip(board, notations):
                    if notation == possible:
                        if get_color(square) != clientcolor:
                            legals.append(possible)
        
        return legals

    def bishop(self, current_notation, clientcolor):
        def get_moves(possibles, clientcolor):
            legal_moves = []
            iterate = True
            for possible in possibles:
                if not iterate: break
                for square, notation in zip(board, notations):
                    if possible == notation:
                        if square != 0:
                            if get_color(square) != clientcolor: legal_moves.append(notation)
                            iterate = False
                            break
                        else:
                            legal_moves.append(notation)
                            break
            return legal_moves

        letters_right = [] # letters beside
        letters_left = []

        possibles_left_up = []
        possibles_right_up = []
        possibles_left_down = []
        possibles_right_down = []

        possibles = []
        legals = []

        current_letter = current_notation[0]

        left = True
        for i, letter in enumerate(letters):
            if letter == current_letter:
                left = False
                continue
            if left: letters_left.append(letter)
            else: letters_right.append(letter)

        letters_left.reverse()

        for i, letter_left in enumerate(letters_left):
            try: possibles_left_up.append (f"{letter_left}{int(current_notation[1])+(i+1)}")
            except: break

        for i, letter_right in enumerate(letters_right):
            try: possibles_right_up.append (f"{letter_right}{int(current_notation[1])+(i+1)}")
            except: break

        for i, letter_left in enumerate(letters_left):
            try: 
                possibles_left_down.append (f"{letter_left}{int(current_notation[1])-(i+1)}")
            except: break

        for i, letter_right in enumerate(letters_right):
            try: possibles_right_down.append (f"{letter_right}{int(current_notation[1])-(i+1)}")
            except: break

        left_down = get_moves(possibles_left_down, clientcolor)
        right_down = get_moves(possibles_right_down, clientcolor)
        left_up = get_moves(possibles_left_up, clientcolor)
        right_up = get_moves(possibles_right_up, clientcolor)
    
        legals += left_down
        legals += right_down
        legals += left_up
        legals += right_up

        return legals

    def queen(self, current_notation, clientcolor):
        diagonals = self.bishop(current_notation, clientcolor)
        sides = self.rook(current_notation, clientcolor)
        return diagonals + sides
    
    def king(self, current_notation, clientcolor):
        # king moves
        self.possible_kingside_castle = []
        self.possible_queenside_castle = []

        possibles = []
        legals = []

        besides = get_beside(current_notation[0])

        try: possibles.append (f"{current_notation[0]}{int(current_notation[1])+1}")
        except: pass

        try: 
            if int(current_notation[1]) != 1:
                possibles.append (f"{current_notation[0]}{int(current_notation[1])-1}")
        except: pass

        for beside in besides:
            try: 
                possibles.append (f"{beside}{int(current_notation[1])}")
            except: pass

            try: 
                possibles.append (f"{beside}{int(current_notation[1])+1}")
            except: pass

            try: 
                if int(current_notation[1]) != 1:
                    possibles.append (f"{beside}{int(current_notation[1])-1}")
            except: pass
           

        for possible in possibles:
            for square, notation in zip(board, notations):
                if possible == notation:
                    if get_color(square) != clientcolor:
                        legals.append(possible)

        global g_kingside_castle_possible, g_queenside_castle_possible, g_castled

        if not g_castled:   
            if g_kingside_castle_possible:
                if get_square(f"f{current_notation[1]}") == 0 and get_square(f"g{current_notation[1]}") == 0:
                    legals += [f"g{current_notation[1]}"]
                    self.possible_kingside_castle.append(current_notation)
                    self.possible_kingside_castle.append(f"g{current_notation[1]}")
            if g_queenside_castle_possible:
                if get_square(f"b{current_notation[1]}") == 0 and get_square(f"c{current_notation[1]}") == 0 and get_square(f"d{current_notation[1]}") == 0:
                    legals += [f"c{current_notation[1]}"]
                    self.possible_queenside_castle.append(current_notation)
                    self.possible_queenside_castle.append(f"c{current_notation[1]}")
        return legals

    def pawn(self, current_notation, clientcolor):
        self.possible_enpassant = []

        possible_capture_alphabets = []
        legal_moves = []

        if clientcolor == "white":
            next_square = +1
            enemy_double_push = -2
            starting_square = 2
            second_square = 4
            enemy_color = "black"

        else:
            next_square = -1
            enemy_double_push = 2
            starting_square = 7
            second_square = 5
            enemy_color = "white"

        # todo for enpassant:

        # check if previous move is a pawn move
        # check if it was a double push
        # if it was, check if this pawn is DIRECTLY beside it (same rank, beside it)
        # if it is, enpassant = true

        enpassant = False

        try:
            if int(self.previous_opponent_move[1][1]) == int(self.previous_opponent_move[0][1]) + enemy_double_push:
                beside_letters = get_beside(self.previous_opponent_move[1][0])
                if current_notation[0] in beside_letters and int(current_notation[1]) == int(self.previous_opponent_move[1][1]):
                    enpassant = True
        except: pass

        if enpassant:
            enpassant_notation = f"{self.previous_opponent_move[1][0]}{int(self.previous_opponent_move[1][1])+next_square}"
            self.possible_enpassant = [current_notation, enpassant_notation]
            legal_moves += [enpassant_notation]

        # forward moves

        one_square = current_notation[0] + f"{int(current_notation[1]) + next_square}" # 1 square above
        double_square = current_notation[0] + f"{int(current_notation[1]) + (next_square * 2)}" # 1 square above
        
        for square, notation in zip(board, notations):
            if one_square == notation:
                blockage = square != 0 # a piece is already blocking the square
            if double_square == notation:
                blockage2 = square != 0

        try:

            if not blockage:
                legal_moves.append(one_square)
            
            if not blockage and not blockage2:
                if int(current_notation[1]) == starting_square:
                    two_squares = current_notation[0] + str(second_square) # 2 squares above for starting position
                    legal_moves.append(two_squares)

        except: pass

        # captures 

        possible_capture_alphabets = get_beside(current_notation[0])
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
        self.board = self.load_texture(resource_path("res/board.png"), (512, 512))
        self.black_pawn = self.load_texture(resource_path("res/bP.png"))
        self.black_rook = self.load_texture(resource_path("res/bR.png"))
        self.black_knight = self.load_texture(resource_path("res/bN.png"))
        self.black_bishop = self.load_texture(resource_path("res/bB.png"))
        self.black_king = self.load_texture(resource_path("res/bK.png"))
        self.black_queen = self.load_texture(resource_path("res/bQ.png"))
        self.white_pawn = self.load_texture(resource_path("res/wP.png"))
        self.white_rook = self.load_texture(resource_path("res/wR.png"))
        self.white_knight = self.load_texture(resource_path("res/wN.png"))
        self.white_bishop = self.load_texture(resource_path("res/wB.png"))
        self.white_king = self.load_texture(resource_path("res/wK.png"))
        self.white_queen = self.load_texture(resource_path("res/wQ.png"))

    def load_texture(self, fp, scale = (PIECE_SIZE, PIECE_SIZE)):
        texture = pygame.image.load(fp)
        texture = pygame.transform.scale(texture, scale)
        return texture
    
    def update_board(self, old_notation, new_notation, piece, me, enpassant, o_o, o_o_o, secret_pawn, promotion_icon):
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

            if int(new_notation[1]) == 8 and new_notation != secret_pawn:
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

            if int(new_notation[1]) == 1 and new_notation != secret_pawn:
                board[new_idx] = promotion_piece

        # en passant
        # remove pawn behind it
        if enpassant:
            notation_remove = f"{new_notation[0]}{old_notation[1]}"

            for i in range(len(notations)):
                if notations[i] == notation_remove:
                    board[i] = 0
                    break

        if me: 
            global g_kingside_castle_possible, g_queenside_castle_possible
            if piece == WHITE_ROOK or piece == BLACK_ROOK:
                if old_notation[0] == 'a': g_queenside_castle_possible = False
                elif old_notation[0] == 'h': g_kingside_castle_possible = False        

            elif piece == WHITE_KING or piece == BLACK_KING: 
                g_queenside_castle_possible = False
                g_kingside_castle_possible = False    

        global g_castled
        if o_o:
            rank = int(new_notation[1])
            for i in range(len(board)):
                if notations[i] == f"h{rank}":
                    board[i] = 0
                if notations[i] == f"f{rank}":
                    if rank == 1: board[i] = WHITE_ROOK
                    else: board[i] = BLACK_ROOK
            if me: 
                g_castled = True

        if o_o_o:
            rank = int(new_notation[1])
            for i in range(len(board)):
                if notations[i] == f"a{rank}":
                    board[i] = 0
                if notations[i] == f"d{rank}":
                    if rank == 1: board[i] = WHITE_ROOK
                    else: board[i] = BLACK_ROOK
            if me:
                g_castled = True

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

def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

def get_square(note):
    for square, notation in zip(board, notations):
        if note == notation:
            return square

def check_val(idx):
    if idx < 0:
        raise ValueError
    else:
        return idx

def get_beside(letter, n = 1): # -> returns letters beside pawn
    ml = []
    
    for i, each in enumerate(letters):
        if each == letter:
            try: 
                if i < len(letters) - n: ml.append(letters[i+n])
            except: pass

            try: 
                if i >= n: ml.append(letters[i-n])
            except: pass
    return ml

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
    return legal_moves, old, piece
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Secret Queen")
    icon = pygame.image.load('res/wQ.png')
    pygame.display.set_icon(icon)

    font = pygame.font.SysFont("monospace", 45)

    text_width, text_height = font.size("xxxxx wins!")
    win_msg = font.render("-", 1, "red")
    
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

    HOST = input("Host: ")
    PORT = 65432

    start = False

    legal_moves = []
    secret_pawn = ""

    promotion_icon = "Q"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        
        clientcolor = (sock.recv(1024)).decode()

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

            white_king_present = False
            black_king_present = False

            for square in board:
                if square == WHITE_KING:
                    white_king_present = True
                if square == BLACK_KING:
                    black_king_present = True

            if not black_king_present: win_msg = font.render("White wins!", 1, "red")
            if not white_king_present: win_msg = font.render("Black wins!", 1, "red")

            if not white_king_present or not black_king_present:
                screen.blit(sprites.board, (0,0))
                sprites.render_board(screen, clientcolor)
                screen.blit(win_msg, ((512-text_width)/2, (512-text_height)/2))
                pygame.display.flip()
                clock.tick(60)
                continue

            mousepos = pygame.mouse.get_pos()
            
            if start:
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
                                    enpassant = 0
                                    o_o = 0
                                    o_o_o = 0
                                    new = notation

                                    if logic.possible_enpassant == [old, new]:
                                        enpassant = 1

                                    if logic.possible_kingside_castle == [old, new]:
                                        o_o = 1

                                    if logic.possible_queenside_castle == [old, new]:
                                        o_o_o = 1

                                    sprites.update_board(old, new, piece, True, enpassant, o_o, o_o_o, secret_pawn, promotion_icon)

                                    if clientcolor == "white":
                                        if piece == WHITE_QUEEN:
                                            if old == secret_pawn:
                                                piece = WHITE_PAWN
                                                secret_pawn = new

                                    elif clientcolor == "black":
                                        if piece == BLACK_QUEEN:
                                            if old == secret_pawn:
                                                piece = BLACK_PAWN
                                                secret_pawn = new

                                    data = f"{old},{new},{piece},{enpassant},{o_o},{o_o_o},{secret_pawn},{promotion_icon}" # unsafe af, but who gives a shit?
                                    sock.sendall(bytes(data, 'utf-8'))
                                    old = ""
                                    new = ""
                                    piece = ""
                                    legal_moves = []
                                    turn = False

                                else:
                                    state = 0
                                    break
            else:
                if clicked:
                    for i in range(len(board)):
                                if rects[i].collidepoint(mousepos):
                                    if get_color(board[i]) == clientcolor:
                                        if clientcolor == "white":
                                            board[i] = WHITE_QUEEN
                                        else:
                                            board[i] = BLACK_QUEEN
                                        secret_pawn = notations[i]
                                        start = True
                                        break


            sock.setblocking(0)

            ready = select.select([sock], [], [], 0)
            if ready[0]:
                data = sock.recv(4096)
                old, new, piece, enpassant, o_o, o_o_o, sp, promotion_icon = data.decode().split(",")
                sprites.update_board(old, new, int(piece), False, int(enpassant), int(o_o), int(o_o_o), sp, promotion_icon)
                if new == secret_pawn or get_square(secret_pawn) == 0:# secret queen has been captured or en passanted
                    secret_pawn = ""
                logic.previous_opponent_move = [old, new, int(piece)]
                turn = True

            screen.blit(sprites.board, (0,0))
            sprites.render_board(screen, clientcolor)

            if start: render_legals(screen, rects, legal_moves)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()