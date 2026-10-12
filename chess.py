"""Launch and run the Chess desktop game."""

import pygame
import sys
import time
import os
import subprocess
from database import save_game as store_game


pygame.init()
WIDTH=870
HEIGHT=800
BOARD_PIXEL = 800 * 5/6          
SQUARE = BOARD_PIXEL / 8.0       
BOARD_ORIGIN = (0, 0)            
screen=pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess!')
font= pygame.font.Font('freesansbold.ttf',50)
big_font = pygame.font.Font('freesansbold.ttf', 40)

timer=pygame.time.Clock()
fps=60


def save_game(moves_list, player_name):
    """Save a named game and report the outcome.

    Delegates to :func:`database.save_game`, which tries MySQL first and falls
    back to a local file, so saving works even without a database. Returns a
    ``(saved, message)`` pair; the message is shown on the win screen.
    """
    saved, message = store_game(player_name, moves_list)
    print(message)
    return saved, message


def wrap_lines(text, text_font, max_width):
    """Split text into lines no wider than max_width pixels."""
    lines = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if text_font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


#NAME


def save_name(screen=None):
    """Modal input overlay on the existing screen. Returns trimmed string, "" if empty,
       or None if cancelled. Does NOT call pygame.quit()."""
    created_screen = False
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((600, 300))
        created_screen = True

    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    box = pygame.Rect(100, 120, 400, 40)
    active = True
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active
    text = ""

  
    try:
        background = screen.copy()
    except Exception:
        background = None

    caret_visible = True
    last_caret_toggle = time.time()
    caret_interval = 0.5  # seconds

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(ev.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive
            if ev.type == pygame.KEYDOWN and active:
                if ev.key == pygame.K_RETURN:
                    return text.strip()
                elif ev.key == pygame.K_ESCAPE:
                    return None
                elif ev.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 40:
                        # only add printable characters
                        if ev.unicode and ord(ev.unicode) >= 32:
                            text += ev.unicode

        # toggle caret
        if time.time() - last_caret_toggle > caret_interval:
            caret_visible = not caret_visible
            last_caret_toggle = time.time()

        # draw overlay
        if background is not None:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        prompt = font.render("Enter name (Enter=save, Esc=cancel):", True, (255, 255, 255))
        screen.blit(prompt, (100, 70))

        pygame.draw.rect(screen, color, box, 2)
        txt_surf = font.render(text, True, (255, 255, 255))
        screen.blit(txt_surf, (box.x + 6, box.y + 6))

        # draw blinking caret
        if caret_visible and active:
            caret_x = box.x + 6 + txt_surf.get_width()
            caret_y1 = box.y + 8
            caret_y2 = box.y + box.height - 8
            pygame.draw.line(screen, (255, 255, 255), (caret_x, caret_y1), (caret_x, caret_y2), 2)

        pygame.display.update()
        clock.tick(30)


    








# Pieces
white_pieces=['rook','knight','bishop','king','queen','bishop','knight','rook',
              'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
white_locations=[(0, 0),(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0),(7, 0),
                 (0, 1),(1, 1),(2, 1),(3, 1),(4, 1),(5, 1),(6, 1),(7, 1)]

black_pieces=['rook','knight','bishop','king','queen','bishop','knight','rook',
              'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
black_locations=[(0, 7),(1, 7),(2, 7),(3, 7),(4, 7),(5, 7),(6, 7),(7, 7),
                 (0, 6),(1, 6),(2, 6),(3, 6),(4, 6),(5, 6),(6, 6),(7, 6)]
captured_pieces_white=[]
captured_pieces_black=[]
moves_replay = []





#status 0:wn 1:w 2:bn 3:b
turn_step=0
selection=100
valid_moves=[]
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
#IMAGES
# WHITE PIECES
white_pawn  = pygame.image.load(os.path.join(IMAGE_DIR, "white-pawn.png"))
white_pawn  = pygame.transform.scale(white_pawn, (75, 75))
white_pawn_small = pygame.transform.scale(white_pawn, (60, 60))

white_rook  = pygame.image.load(os.path.join(IMAGE_DIR, "white-rook.png"))
white_rook  = pygame.transform.scale(white_rook, (78, 78))
white_rook_small = pygame.transform.scale(white_rook, (60, 60))

white_knight = pygame.image.load(os.path.join(IMAGE_DIR, "white-knight.png"))
white_knight = pygame.transform.scale(white_knight, (78, 78))
white_knight_small = pygame.transform.scale(white_knight, (60, 60))

white_bishop = pygame.image.load(os.path.join(IMAGE_DIR, "white-bishop.png"))
white_bishop = pygame.transform.scale(white_bishop, (78, 78))
white_bishop_small = pygame.transform.scale(white_bishop, (60, 60))

white_queen = pygame.image.load(os.path.join(IMAGE_DIR, "white-queen.png"))
white_queen = pygame.transform.scale(white_queen, (78, 78))
white_queen_small = pygame.transform.scale(white_queen, (60, 60))

white_king = pygame.image.load(os.path.join(IMAGE_DIR, "white-king.png"))
white_king = pygame.transform.scale(white_king, (78, 78))
white_king_small = pygame.transform.scale(white_king, (60, 60))


# BLACK PIECES
black_pawn  = pygame.image.load(os.path.join(IMAGE_DIR, "black-pawn.png"))
black_pawn  = pygame.transform.scale(black_pawn, (75, 75))
black_pawn_small = pygame.transform.scale(black_pawn, (60, 60))

black_rook  = pygame.image.load(os.path.join(IMAGE_DIR, "black-rook.png"))
black_rook  = pygame.transform.scale(black_rook, (78, 78))
black_rook_small = pygame.transform.scale(black_rook, (60, 60))

black_knight = pygame.image.load(os.path.join(IMAGE_DIR, "black-knight.png"))
black_knight = pygame.transform.scale(black_knight, (78, 78))
black_knight_small = pygame.transform.scale(black_knight, (60, 60))

black_bishop = pygame.image.load(os.path.join(IMAGE_DIR, "black-bishop.png"))
black_bishop = pygame.transform.scale(black_bishop, (78, 78))
black_bishop_small = pygame.transform.scale(black_bishop, (60, 60))

black_queen = pygame.image.load(os.path.join(IMAGE_DIR, "black-queen.png"))
black_queen = pygame.transform.scale(black_queen, (78, 78))
black_queen_small = pygame.transform.scale(black_queen, (60, 60))

black_king = pygame.image.load(os.path.join(IMAGE_DIR, "black-king.png"))
black_king = pygame.transform.scale(black_king, (78, 78))
black_king_small = pygame.transform.scale(black_king, (60, 60))

white_images = [
    white_pawn,
    white_rook,
    white_knight,
    white_bishop,
    white_queen,
    white_king
]

black_images = [
    black_pawn,
    black_rook,
    black_knight,
    black_bishop,
    black_queen,
    black_king
]
small_white_images = [
    white_pawn_small,
    white_rook_small,
    white_knight_small,
    white_bishop_small,
    white_queen_small,
    white_king_small
]

small_black_images = [
    black_pawn_small,
    black_rook_small,
    black_knight_small,
    black_bishop_small,
    black_queen_small,
    black_king_small
]

piece_list = [
    "pawn",
    "rook",
    "knight",
    "bishop",
    "queen",
    "king"]

#check variables



#MAIN BOARD
def draw_board():
    bx, by = BOARD_ORIGIN

    LIGHT_WOOD = '#eeeed2' 
    DARK_WOOD  = '#93b86f'   

    # draw 8x8 board
    for row in range(8):
        for col in range(8):
            color = LIGHT_WOOD if (row + col) % 2 == 0 else DARK_WOOD
            rect = (bx + col * SQUARE, by + row * SQUARE, SQUARE, SQUARE)
            pygame.draw.rect(screen, color, rect)

   
    pygame.draw.rect(screen, 'gray', [0, 810*5/6, WIDTH, 110])
    pygame.draw.rect(screen, 'brown', [0, 810*5/6, WIDTH, 110], 5)
    pygame.draw.rect(screen, 'gray', [810*5/6, 0, 200, HEIGHT])
    pygame.draw.rect(screen, 'brown', [810*5/6, 0, 200, HEIGHT], 5)

    status_text = ['White: select a piece to move.',
                   'White: select a destination',
                   'Black: select a piece to move.',
                   'Black: select a destination']
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (10, 700))

    
    for i in range(9):
        x = bx + i * SQUARE
        pygame.draw.line(screen, 'black', (x, by), (x, by + 8 * SQUARE), 4)
        y = by + i * SQUARE
        pygame.draw.line(screen, 'black', (bx, y), (bx + 8 * SQUARE, y), 4)

#drawing pices
def draw_pieces():
    # draw white pieces
    for i in range(len(white_pieces)):
        x, y = white_locations[i]
        # pick the image
        try:
            idx = piece_list.index(white_pieces[i])
        except ValueError:
            idx = 0
        img = white_pawn if white_pieces[i] == 'pawn' else white_images[idx]
        img_w, img_h = img.get_size()
        px = BOARD_ORIGIN[0] + x * SQUARE + (SQUARE - img_w) / 2
        py = BOARD_ORIGIN[1] + y * SQUARE + (SQUARE - img_h) / 2
        screen.blit(img, (px, py))

        # highlight selection for white
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'green',
                             [BOARD_ORIGIN[0] + x * SQUARE + 1,
                              BOARD_ORIGIN[1] + y * SQUARE + 1,
                              SQUARE - 2, SQUARE - 2], 4)

    # draw black pieces
    for i in range(len(black_pieces)):
        x, y = black_locations[i]
        try:
            idx = piece_list.index(black_pieces[i])
        except ValueError:
            idx = 0
        img = black_pawn if black_pieces[i] == 'pawn' else black_images[idx]
        img_w, img_h = img.get_size()
        px = BOARD_ORIGIN[0] + x * SQUARE + (SQUARE - img_w) / 2
        py = BOARD_ORIGIN[1] + y * SQUARE + (SQUARE - img_h) / 2
        screen.blit(img, (px, py))

        # highlight selection for black
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'green',
                             [BOARD_ORIGIN[0] + x * SQUARE + 1,
                              BOARD_ORIGIN[1] + y * SQUARE + 1,
                              SQUARE - 2, SQUARE - 2], 4)

                
        
#VALID OPTIONS
def check_options(pieces, locations, turn):
    moves_list=[]
    all_moves_list=[]
    for i in range(len(pieces)):
        location=locations[i]
        piece=pieces[i]
        if piece=='pawn':
            moves_list=check_pawn(location, turn)
        elif piece=='rook':
            moves_list=check_rook(location, turn)
        elif piece=='knight':
            moves_list=check_knight(location, turn)
        elif piece=='bishop':
            moves_list=check_bishop(location, turn)
        elif piece=='queen':
            moves_list=check_queen(location, turn)
        elif piece=='king':
            moves_list=check_king(location, turn)

        all_moves_list.append(moves_list)







    return all_moves_list
#check KING
def check_king(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        enemies_list=white_locations
        friends_list=black_locations
 
    
    targets=[(1,0),(1,-1),(1,1),(-1,-1),(-1,0),(-1,1),(0,1),(0,-1)]
    for i in range(8):
        target=(position[0]+targets[i][0],position[1]+targets[i][1])
        if target not in friends_list and 0<=target[0]<=7 and 0<=target[1]<=7:
            moves_list.append(target)
        
    return moves_list

#check QUEEN
def check_queen(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        enemies_list=white_locations
        friends_list=black_locations
    for i in range(8): #Ur Ul Dr Dl
        path=True
        chain=1
        if i==0:
            x=1
            y=-1
        elif i==1:
            x=-1
            y=-1
        elif i==2:
            x=1
            y=1
        elif i==3:
            x=-1
            y=1
        elif i==4:
            x=0
            y=1
        elif i==5:
            x=0
            y=-1
        elif i==6:
            x=1
            y=0
        else:
            x=-1
            y=0
        
        while path:
            if (position[0]+(chain*x),position[1]+(chain*y)) not in friends_list and 0<=position[0]+(chain*x)<=7 and 0<=position[1]+(chain*y)<=7:
                moves_list.append((position[0]+(chain*x),position[1]+(chain*y))) in enemies_list
                if (position[0]+(chain*x),position[1]+(chain*y))in enemies_list:
                    path=False
                chain+=1
            else:
                path=False
        
            

    return moves_list

#check bishops
def check_bishop(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        enemies_list=white_locations
        friends_list=black_locations
    for i in range(4): #Ur Ul Dr Dl
        path=True
        chain=1
        if i==0:
            x=1
            y=-1
        elif i==1:
            x=-1
            y=-1
        elif i==2:
            x=1
            y=1
        else:
            x=-1
            y=1
        while path:
            if (position[0]+(chain*x),position[1]+(chain*y)) not in friends_list and 0<=position[0]+(chain*x)<=7 and 0<=position[1]+(chain*y)<=7:
                moves_list.append((position[0]+(chain*x),position[1]+(chain*y))) in enemies_list
                if (position[0]+(chain*x),position[1]+(chain*y))in enemies_list:
                    path=False
                chain+=1
            else:
                path=False
            

    return moves_list

#CHECK KNIHGT OMVES
def check_knight(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        enemies_list=white_locations
        friends_list=black_locations
    targets=[(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]
    for i in range(8):
        target=(position[0]+targets[i][0],position[1]+targets[i][1])
        if target not in friends_list and 0<=target[0]<=7 and 0<=target[1]<=7:
            moves_list.append(target)

    return moves_list


#check rook movees
def check_rook(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        enemies_list=white_locations
        friends_list=black_locations
    for i in range(4): #U D R L
        path=True
        chain=1
        if i==0:
            x=0
            y=1
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x=1
            y=0
        else:
            x=-1
            y=0
        while path:
            if (position[0]+(chain*x),position[1]+(chain*y)) not in friends_list and 0<=position[0]+(chain*x)<=7 and 0<=position[1]+(chain*y)<=7:
                moves_list.append((position[0]+(chain*x),position[1]+(chain*y))) in enemies_list
                if (position[0]+(chain*x),position[1]+(chain*y))in enemies_list:
                    path=False
                chain+=1
            else:
                path=False
            
            
    return moves_list
   
#check valid pawn moves
# white -> forward is y+1; black -> forward is y-1

def check_pawn(position, color):
    moves_list=[]
    x,y = position
    if color=='white':
        if y+1<=7 and (x,y+1) not in white_locations and (x,y+1) not in black_locations:
            moves_list.append((x,y+1))
            if y==1 and (x,y+2) not in white_locations and (x,y+2) not in black_locations:
                moves_list.append((x,y+2))
        for dx in (-1,1):
            nx, ny = x+dx, y+1
            if 0<=nx<=7 and ny<=7 and (nx,ny) in black_locations:
                moves_list.append((nx,ny))
    else:
        if y-1>=0 and (x,y-1) not in white_locations and (x,y-1) not in black_locations:
            moves_list.append((x,y-1))
            if y==6 and (x,y-2) not in white_locations and (x,y-2) not in black_locations:
                moves_list.append((x,y-2))
        for dx in (-1,1):
            nx, ny = x+dx, y-1
            if 0<=nx<=7 and ny>=0 and (nx,ny) in white_locations:
                moves_list.append((nx,ny))
    return moves_list


#check valid fro sleected
def check_valid_moves():
    if turn_step<2:
        options_list=white_options
    else:
        options_list=black_options
    valid_options=options_list[selection]
    return valid_options


#drraw valid moves
def draw_valid(moves):
    # draw small circle centered in each valid square
    radius = max(10, int(SQUARE * 0.08))
    for (mx, my) in moves:
        cx = BOARD_ORIGIN[0] + mx * SQUARE + SQUARE / 2
        cy = BOARD_ORIGIN[1] + my * SQUARE + SQUARE / 2
        pygame.draw.circle(screen, '#d64224', (int(cx), int(cy)), radius)
    
        
    
#DRaw captured pieces
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece=captured_pieces_white[i]
        index=piece_list.index(captured_piece)
        screen.blit(small_black_images[index],(790,5+58*i))
    for i in range(len(captured_pieces_black)):
        captured_piece=captured_pieces_black[i]
        index=piece_list.index(captured_piece)
        screen.blit(small_white_images[index],(700,5+58*i))

       



def _win_screen(title, subtitle_line, replay_path):
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))

    # Set after a save attempt so the outcome is visible on screen instead of
    # only in a terminal window the player may not have open.
    status = ""
    status_font = pygame.font.Font('freesansbold.ttf', 22)

    waiting = True
    while waiting:
        timer.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

           
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.quit()
                sys.exit()

            # KEYUP for R or S
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_r :
                    try:
                        subprocess.Popen([sys.executable, replay_path])
                        
                    except Exception as e:
                        print("Failed to launch replay:", e)

               
                elif event.key == pygame.K_s:
                   
                    player_name = None
                    try:
                      
                        player_name = save_name(screen)
                    except Exception as e:
                        print("Name input error:", e)

                    
                    if player_name:
                        try:
                            _, status = save_game(moves_replay, player_name)
                        except Exception as e:
                            status = "Error saving game: %s" % e
                            print(status)
                    elif player_name is None:
                        status = "Save cancelled."
                    else:
                        status = "No game name entered, nothing was saved."


        # draw screen
        screen.fill((0, 0, 0))
        draw_board()         
        screen.blit(overlay, (0, 0))

        # big centered title
        title_surf = big_font.render(title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(title_surf, title_rect)

        # subtitle: click to quit
        sub_surf = font.render(subtitle_line, True, (200, 200, 200))
        sub_rect = sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(sub_surf, sub_rect)

        # subtitle 2: press R / S info
        press_surf = font.render("Press R to replay old games", True, (200, 200, 200))
        press_rect = press_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(press_surf, press_rect)
        
        press_surf = font.render("Press S to save game", True, (200, 200, 200))
        press_rect = press_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
        screen.blit(press_surf, press_rect)        

        # Save outcome (success or error) without needing a terminal open.
        if status:
            status_y = HEIGHT // 2 + 185
            for line in wrap_lines(status, status_font, WIDTH - 60):
                line_surf = status_font.render(line, True, (255, 214, 112))
                screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, status_y))
                status_y += 26

        pygame.display.flip()



def display_white_wins():
    

    
    white_pieces.clear()
    black_pieces.clear()
    white_locations.clear()
    black_locations.clear()
    captured_pieces_white.clear()
    captured_pieces_black.clear()

    
    replay_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replay.py")
    _win_screen("WHITE WINS", "Click anywhere to quit", replay_path)


def display_black_wins():
    # optional: clear board state 
    
    white_pieces.clear()
    black_pieces.clear()
    white_locations.clear()
    black_locations.clear()
    captured_pieces_white.clear()
    captured_pieces_black.clear()
    

    replay_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replay.py")
    _win_screen("BLACK WINS", "Click anywhere to quit", replay_path)



        


                         
                     
#loop and functions
black_options=check_options(black_pieces,black_locations,'black')
white_options=check_options(white_pieces,white_locations,'white')

run=True
while run:
    timer.tick(fps) 
    screen.fill('black')
    draw_board()
    draw_pieces()
    draw_captured()
    if selection!=100:
        valid_moves=check_valid_moves()
        draw_valid(valid_moves)
#events
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                if turn_step <= 1:
                    display_black_wins()
                else:
                    display_white_wins()

             


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = int((event.pos[0] - BOARD_ORIGIN[0]) // SQUARE)
            y_coord = int((event.pos[1] - BOARD_ORIGIN[1]) // SQUARE)
            click_coords = (x_coord, y_coord)
     
                




            if turn_step <= 1:
                # select a white piece
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                    
                    try:
                        valid_moves = white_options[selection]
                    except Exception:
                        valid_moves = []

                # move the selected white piece (two-click model)
                elif selection != 100 and turn_step == 1 and click_coords in valid_moves:
                    # record old pos and move
                    old_x, old_y = white_locations[selection]
                    white_locations[selection] = click_coords
                    moves_replay.append([[old_x, old_y], [x_coord, y_coord]])

                    # capture if black piece at destination
                    if click_coords in black_locations:
                        idx = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[idx])
                        black_pieces.pop(idx)
                        black_locations.pop(idx)

                    
                    try:
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                    except NameError:
                        pass

                    # hand turn to black
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            # ----- BLACK TURN (turn_step 2 = select, 3 = destination) -----
            else:
                # select a black piece
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                    
                    try:
                        valid_moves = black_options[selection]
                    except Exception:
                        valid_moves = []

                # move the selected black piece
                elif selection != 100 and turn_step == 3 and click_coords in valid_moves:
                    
                    old_x, old_y = black_locations[selection]
                    black_locations[selection] = click_coords
                    moves_replay.append([[old_x, old_y], [x_coord, y_coord]])

                    # capture if white piece at destination
                    if click_coords in white_locations:
                        idx = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[idx])
                        white_pieces.pop(idx)
                        white_locations.pop(idx)

                    
                    try:
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                    except NameError:
                        pass

                    # hand turn to white
                    turn_step = 0
                    selection = 100
                    valid_moves = []

            # check for king capture 
            if "king" in captured_pieces_black:
                print(moves_replay)
                
                
                display_black_wins()
                
                
                

            if "king" in captured_pieces_white:
                print(moves_replay)
                
                display_white_wins()



                
                




    pygame.display.flip()


    
pygame.quit()
