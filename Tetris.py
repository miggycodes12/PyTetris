import pygame
import random
import math
pygame.init()

# screen
WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))


# configurations
title = "PyTetris"
running = True
max_fps_setting = pygame.time.Clock()
max_fps = 60
pygame.display.set_caption(title)
arial_font = pygame.font.SysFont("Arial", 25)

# data storage
board = []
for i in range(20):
    board.append([0]*10)
col_board = []
for i in range(20):
    col_board.append(["non"]*10)

global_x = 3
global_y = 0
global_rot = 0
value_line = 100
score = 0
lvl_buffer = 0 # max is 57, reduces fall_cooldown and adds ups 3 per lvl (10 lines)
lines_global = 0
global_col = [0, 0, 0]
nxt_col = [0, 0, 0]
col_keep = []

# tetrominoes
rSPiece = [
    [
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 0],
        [1, 1],
        [0, 1]
    ],
]

iPiece = [
    [
        [1, 1, 1, 1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ]
]

lSPiece = [
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1],
        [1, 1],
        [1, 0]
    ],
]

blockPiece = [
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1],
        [1, 1]
    ]
]

tPiece = [
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1],
        [1, 1],
        [0, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 1],
        [1, 0]
    ]
]

rLPiece = [
    [
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [1, 1],
        [1, 0],
        [1, 0]
    ],
    [
        [1, 1, 1],
        [0, 0, 1],
    ],
    [
        [0, 1],
        [0, 1],
        [1, 1]
    ]
]

lLPiece = [
    [
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    [
        [1, 1, 1],
        [1, 0, 0],
    ],
    [
        [1, 1],
        [0, 1],
        [0, 1]
    ]
]

# functions

# render display
def render(data):
    tile_size = 50
    width_inc = 0
    height_inc = 0
    cols = {
    "r": [255, 0, 0],
    "g": [0, 255, 0],
    "b": [0, 0, 255],
    "y": [255, 255, 0],
    "c": [0, 255, 255],
    "m": [255, 0, 255],
    "t": [0, 255, 125]
    }
    #width
    for row in range(len(board)):
        for tile in range(len(board[row])):
            if board[row][tile] == 0:
                pygame.draw.rect(SCREEN, (0, 0, 0), (0+width_inc, 0+height_inc, tile_size, tile_size))
                pygame.draw.rect(SCREEN, (255, 255, 255), (0+width_inc, 0+height_inc, tile_size, tile_size), width=1)
            elif board[row][tile] == 1:
                if col_board[row][tile] != "non":
                    pygame.draw.rect(SCREEN, cols[col_board[row][tile]], (0+width_inc, 0+height_inc, tile_size, tile_size))
                    pygame.draw.rect(SCREEN, (255, 255, 255), (0+width_inc, 0+height_inc, tile_size, tile_size), width=1)
            elif board[row][tile] == 2:
                pygame.draw.rect(SCREEN, global_col, (0+width_inc, 0+height_inc, tile_size, tile_size))
                pygame.draw.rect(SCREEN, (255, 255, 255), (0+width_inc, 0+height_inc, tile_size, tile_size), width=1)
            width_inc += tile_size
        width_inc = 0
        height_inc += tile_size

def next_display(next):
    tile_size = 50
    width_inc = 650
    height_inc = 200
    # clearer
    for y in range(4):
        for x in range(4):
            pygame.draw.rect(SCREEN, (0, 0, 0), (0+width_inc, 0+height_inc, tile_size, tile_size))
            width_inc += tile_size
        width_inc = 650
        height_inc += tile_size
    width_inc = 650
    height_inc = 200
    for row in next[0]:
        for tile in row:
            if tile == 1:
                pygame.draw.rect(SCREEN, nxt_col, (0+width_inc, 0+height_inc, tile_size, tile_size))
                pygame.draw.rect(SCREEN, (255, 255, 255), (0+width_inc, 0+height_inc, tile_size, tile_size), width=1)
            width_inc += tile_size
        width_inc = 650
        height_inc += tile_size


def spawn_piece(piece):
    alive = True
    rotation = 0
    max_x = len(piece[rotation][0]) 
    X = [3, 2 + (max_x)]
    gen_offset = [0, 3]
    for i in piece[rotation]:
        for x in i:
            if board[gen_offset[0]][gen_offset[1]] == 1:
                return False
            if x:
                board[gen_offset[0]][gen_offset[1]] = 2
            gen_offset[1] += 1
        gen_offset[1] = 3
        gen_offset[0] += 1
    return True
    
def kill_piece(piece):
    col = ""
    if piece == rSPiece:
        col = "r"
    elif piece == iPiece:
        col = "g"
    elif piece == lSPiece:
        col = "b"
    elif piece == blockPiece:
        col = "y"
    elif piece == tPiece:
        col = "c"
    elif piece == rLPiece:
        col = "m"
    elif piece == lLPiece:
        col = "t"
    for row in range(len(board)):
        if not 2 in board[row]:
            continue
        else:
            for tile in range(len(board[row])):
                if board[row][tile] == 2:
                    board[row][tile] = 1
                    col_board[row][tile] = col
                    
def fall_piece(piece):
    fall_row = 0
    total_fall = 0
    loading = []
    succ = []
    failed = []
    for row in range(len(board)-1, 0-1, -1):
        if not 2 in board[row]:
            continue
        else:
            for tile in range(len(board[row])):
                if board[row][tile] == 2:
                    if row + 1 > 19 or board[row+1][tile] == 1:
                            #kill_piece()
                            failed.append(tile)
                    else:
                        #board[row][tile] = 0
                        #board[row+1][tile] = 2
                        succ.append(tile)
                        total_fall += 1
            loading.append(succ)
            succ = []
    if not failed and total_fall == 4:
        for row in range(len(board)-1, 0-1, -1):
            if not 2 in board[row]:
                continue
            else:
                for tile in loading[fall_row]:
                    board[row][tile] = 0
                    board[row+1][tile] = 2
            fall_row += 1
    else:
        kill_piece(piece)

def bring_down(amount, ignore):
    before = None
    for row in range(len(board)-1, 0-1, -1):
        if not 1 in board[row] or row > ignore:
            continue
        else:
            for tile in range(len(board[row])):
                if board[row][tile] == 1:
                    board[row][tile] = 0
                    board[row+amount][tile] = 1
                if col_board[row][tile] != "non":
                    before = col_board[row][tile]
                    col_board[row][tile] = "non"
                    col_board[row+amount][tile] = before

def clear_row():
    lines = 0
    cleared = []
    for row in range(len(board)):
        if not 1 in board[row]:
            continue
        elif board[row] == [1]*10:
            board[row] = [0]*10
            lines += 1
            cleared.append(row)
    if lines:
        bring_down(lines, cleared[0])
        return [lines]
    else:
        return 0

def checking_piece():
    for i in board:
        if 2 in i:
            return False
    return True      

def quick_clear():
    for row in range(len(board)):
        if not 2 in board[row]:
            continue
        else:
            for tile in range(len(board[row])):
                if board[row][tile] == 2:
                    board[row][tile] = 0

def check_rot(piece, Y, X, rotation):
    offset = 0
    for i in piece[rotation]:
        for x in i:
            if x:
                try:
                    if board[Y][X] == 1:
                        return False
                except:
                    return False
            X += 1
            offset += 1
        X -= offset
        Y += 1
        offset = 0
    return True


def move_piece(move, piece, X, Y, rotation):
    offset = 0
    if not checking_piece():
        if move == "up":
            quick_clear()
            for i in piece[rotation]:
                for x in i:
                    if x:
                        board[Y][X] = 2
                    X += 1
                    offset += 1
                X = X - offset
                Y += 1
                offset = 0
        if move == "right":
            R_SUC = []
            R_sub = []
            total = 0
            for row in range(len(board)):
                if not 2 in board[row]:
                    continue
                else:
                    for tile in range(len(board[row]), 0-1, -1):
                        if tile < 9:
                            if board[row][tile] == 2 and board[row][tile+1] != 1:
                                #board[row][tile] = 0
                                #board[row][tile+1] = 2
                                R_sub.append(tile)
                                total += 1
                    R_SUC.append(R_sub)
                    R_sub = []
            if total == 4:
                row1 = 0
                for row in range(len(board)):
                    if not 2 in board[row]:
                        continue
                    else:
                        for tile in R_SUC[row1]:
                            board[row][tile] = 0
                            board[row][tile+1] = 2
                    row1 += 1
                return True
            else:
                return False
        if move == "left":
            L_SUC = []
            L_sub = []
            total1 = 0
            for row in range(len(board)):
                if not 2 in board[row]:
                    continue
                else:
                    for tile in range(len(board[row])):
                        if tile > 0:
                            if board[row][tile] == 2 and board[row][tile-1] != 1:
                                #board[row][tile] = 0
                                #board[row][tile+1] = 2
                                L_sub.append(tile)
                                total1 += 1
                    L_SUC.append(L_sub)
                    L_sub = []
            if total1 == 4:
                row2 = 0
                for row in range(len(board)):
                    if not 2 in board[row]:
                        continue
                    else:
                        for tile in L_SUC[row2]:
                            board[row][tile] = 0
                            board[row][tile-1] = 2
                    row2 += 1
                return True
            else:
                return False
                                    
            
def create_text(text, font, tex_col, x, y, ):
    txt = font.render(text, True, tex_col, (0, 0, 0))
    SCREEN.blit(txt, (x, y))

            
fall_cooldown = 60 - lvl_buffer # same as max fps, amount of frames to fall
fall_counter = 0
drop_speed = 3
all_pieces = [rSPiece, iPiece, lSPiece, blockPiece, tPiece, rLPiece, lLPiece]
next_piece = random.choice(all_pieces)
piece = None
prev = next_piece
next_lvl = 1
# system
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        create_text("Next Piece:", arial_font, (255, 255, 255), 500, 200)
        create_text("PyTetris", arial_font, (255, 255, 255), 700, 0)
        create_text("Programmed in Python", arial_font, (255, 255, 255), 620, 970)
        create_text(f"Score: {score}", arial_font, (255, 255, 255), 500, 600)
        create_text(f"Lines: {lines_global}", arial_font, (255, 255, 255), 500, 650)
        create_text(f"Level: {math.floor(lines_global / 10)}", arial_font, (255, 255, 255), 500, 700)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if global_rot >= len(piece)-1:
                    global_rot = 0
                else:
                    global_rot += 1
                if check_rot(piece, global_y, global_x, global_rot):
                    move_piece("up", piece, global_x, global_y, global_rot)
                else:
                    global_rot -= 1
            elif event.key == pygame.K_d:
                if move_piece("right", piece, global_x, global_y, global_rot):
                    global_x += 1
            elif event.key == pygame.K_a:
                if move_piece("left", piece, global_x, global_y, global_rot):
                    global_x -= 1
            elif event.key == pygame.K_s:
                fall_counter = 0
                fall_cooldown = drop_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                fall_cooldown = 60 - lvl_buffer
        

    if fall_counter == 0 and checking_piece():
        global_y = 0
        global_x = 3
        global_rot = 0
        piece = next_piece
        next_piece = random.choice(all_pieces)
        while next_piece == prev:
            next_piece = random.choice(all_pieces)
        prev = next_piece
        running = spawn_piece(piece)
        if piece == rSPiece:
            global_col = [255, 0, 0]
        elif piece == iPiece:
            global_col = [0, 255, 0]
        elif piece == lSPiece:
            global_col = [0, 0, 255]
        elif piece == blockPiece:
            global_col = [255, 255, 0]
        elif piece == tPiece:
            global_col = [0, 255, 255]
        elif piece == rLPiece:
            global_col = [255, 0, 255]
        elif piece == lLPiece:
            global_col = [0, 255, 125]

        if next_piece == rSPiece:
            nxt_col = [255, 0, 0]
        elif next_piece == iPiece:
            nxt_col = [0, 255, 0]
        elif next_piece == lSPiece:
            nxt_col = [0, 0, 255]
        elif next_piece == blockPiece:
            nxt_col = [255, 255, 0]
        elif next_piece == tPiece:
            nxt_col = [0, 255, 255]
        elif next_piece == rLPiece:
            nxt_col = [255, 0, 255]
        elif next_piece == lLPiece:
            nxt_col = [0, 255, 125]
        next_display(next_piece)
    fall_counter += 1
    if fall_counter == fall_cooldown:
        fall_counter = 0
        fall_piece(piece)
        global_y += 1
    
    cleared = clear_row()
    if type(cleared) is list:
        lines_global += cleared[0]
        if cleared[0]:
            score += value_line * cleared[0]
    if math.floor(lines_global / 10) == next_lvl:
        value_line += 100
        if lvl_buffer < 57:
            lvl_buffer += 3
            fall_counter = 0
            fall_cooldown -= lvl_buffer
        next_lvl += 1
    render(board)
    pygame.display.update()
    max_fps_setting.tick(max_fps)
pygame.quit()