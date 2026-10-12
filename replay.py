"""Open and run the saved-game replay screen.

Usage:
    python replay.py [game name]

Passing the name on the command line skips the name prompt, which is handy for
scripts and for replaying a game that was just saved.
"""

import pygame
import sys
import os
from database import load_game


def game_name(screen=None):
    
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
                    return text        
                elif ev.key == pygame.K_ESCAPE:
                    return None
                elif ev.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 40:
                        text += ev.unicode

        if background is not None:
            screen.blit(background, (0,0))
        else:
            screen.fill((30,30,30))

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0,0))

        prompt = font.render("Enter game name :", True, (255,255,255))
        screen.blit(prompt, (100, 70))

        pygame.draw.rect(screen, color, box, 2)
        txt_surf = font.render(text, True, (255,255,255))
        screen.blit(txt_surf, (box.x + 6, box.y + 6))

        pygame.display.update()
        clock.tick(30)


def _requested_game_name():
    """Return the game name from the command line, or ask for it in a window."""
    from_command_line = " ".join(sys.argv[1:]).strip()
    if from_command_line:
        return from_command_line

    entered = game_name()
    if entered is None:
        return None            # user closed or cancelled the prompt
    return entered.strip()


def _load_requested_game():
    """Resolve which game to replay.

    Returns ``(moves, notice)``. ``moves`` is None when there is nothing to
    replay, in which case ``notice`` explains why and is shown on screen.
    """
    name = _requested_game_name()
    if not name:
        return None, "No game name entered - nothing to replay."

    moves, notice = load_game(name)
    print(notice)
    if moves is None:
        return None, notice
    return moves, notice


moves_replay, notice = _load_requested_game()


pygame.init()
WIDTH=870
HEIGHT=800
BOARD_PIXEL = 800 * 5/6           
SQUARE = BOARD_PIXEL / 8.0       
BOARD_ORIGIN = (0, 0)            
screen=pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Replay')
font= pygame.font.Font('freesansbold.ttf',50)
big_font = pygame.font.Font('freesansbold.ttf', 40)
# replay pointer 
replay_index = 0
def reset_replay():
    global replay_index
    replay_index = 0

def seek_replay(idx):
    global replay_index
    replay_index = max(0, min(idx, len(moves_replay)))



timer=pygame.time.Clock()
fps=60


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


def show_notice(message):
    """Display a message until the user clicks or presses a key, then exit."""
    body_font = pygame.font.Font('freesansbold.ttf', 26)
    hint_font = pygame.font.Font('freesansbold.ttf', 20)
    waiting = True
    while waiting:
        timer.tick(fps)
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False
        screen.fill((30, 30, 30))
        y = HEIGHT // 2 - 40
        for line in wrap_lines(message, body_font, WIDTH - 80):
            surf = body_font.render(line, True, (255, 214, 112))
            screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
            y += 34
        hint_surf = hint_font.render("Press any key or click to close", True, (200, 200, 200))
        screen.blit(hint_surf, (WIDTH // 2 - hint_surf.get_width() // 2, y + 30))
        pygame.display.flip()
    pygame.quit()
    sys.exit(0)


# Nothing to replay: explain why on screen instead of opening an empty board.
if moves_replay is None:
    show_notice(notice)






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

    LIGHT_WOOD = (240, 217, 181)  # #F0D9B5
    DARK_WOOD  = (181, 136, 99)   # #B58863

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

    status_text = ["Press-> for next move(white's turn)",
                   "Press-> for next move(white's turn)",
                   "Press-> for next move(black's turn)",
                   "Press-> for next move(black's turn)"]
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (13, 700))

    
    for i in range(9):
        x = bx + i * SQUARE
        pygame.draw.line(screen, 'black', (x, by), (x, by + 8 * SQUARE), 4)
        y = by + i * SQUARE
        pygame.draw.line(screen, 'black', (bx, y), (bx + 8 * SQUARE, y), 4)

#drawing pices
# drawing pieces
def draw_pieces():
    # draw white pieces
    for i in range(len(white_pieces)):
        x, y = white_locations[i]
        # pick the image
        try:
            idx = piece_list.index(white_pieces[i])
        except ValueError:
            idx = 0
        img = white_images[idx]  # white_images[0] is pawn already
        img_w, img_h = img.get_size()
        px = int(BOARD_ORIGIN[0] + x * SQUARE + (SQUARE - img_w) / 2)
        py = int(BOARD_ORIGIN[1] + y * SQUARE + (SQUARE - img_h) / 2)
        screen.blit(img, (px, py))

        

    # draw black pieces
    for i in range(len(black_pieces)):
        x, y = black_locations[i]
        try:
            idx = piece_list.index(black_pieces[i])
        except ValueError:
            idx = 0
        img = black_images[idx]
        img_w, img_h = img.get_size()
        px = int(BOARD_ORIGIN[0] + x * SQUARE + (SQUARE - img_w) / 2)
        py = int(BOARD_ORIGIN[1] + y * SQUARE + (SQUARE - img_h) / 2)
        screen.blit(img, (px, py))

            
        
    
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

       




        


                         
                     
#loop and functions



try:
    replay_index
except NameError:
    replay_index = 0

def reset_board_to_start():
    """Reset the board pieces and captures to the standard initial position."""
    global white_pieces, white_locations, black_pieces, black_locations, captured_pieces_white, captured_pieces_black
    white_pieces = ['rook','knight','bishop','king','queen','bishop','knight','rook'] + ['pawn']*8
    white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                       (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]
    black_pieces = ['rook','knight','bishop','king','queen','bishop','knight','rook'] + ['pawn']*8
    black_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                       (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
    captured_pieces_white.clear()
    captured_pieces_black.clear()

def apply_move_force(move):
    """
    Apply a single move dict/array to the current board with the same logic you used in
    play_next_replay_move's forced branch. move may be [[sx,sy],[ex,ey]] or {"from":[..],"to":[..]}.
    """
    # normalize formats
    if isinstance(move, dict):
        start = tuple(move.get("from") or move.get("from_sq") or move.get("from_pos"))
        end = tuple(move.get("to") or move.get("to_sq") or move.get("to_pos"))
    else:
        # treat as a 2-element list/tuple like [[sx,sy],[ex,ey]]
        try:
            start = tuple(move[0])
            end = tuple(move[1])
        except Exception:
            return False

    sx, sy = start
    ex, ey = end
    dest = (ex, ey)

    # find piece in white or black lists and move it (with capture handling)
    if start in white_locations:
        idx = white_locations.index(start)
        # capture if black piece at dest
        if dest in black_locations:
            bi = black_locations.index(dest)
            captured_pieces_white.append(black_pieces[bi])
            black_pieces.pop(bi); black_locations.pop(bi)
        white_locations[idx] = dest
        return True
    elif start in black_locations:
        idx = black_locations.index(start)
        if dest in white_locations:
            wi = white_locations.index(dest)
            captured_pieces_black.append(white_pieces[wi])
            white_pieces.pop(wi); white_locations.pop(wi)
        black_locations[idx] = dest
        return True
    else:
        # piece not found — maybe move stored using different indexing; skip it
        return False

def set_board_to_replay_index(idx):
    """
    Reset board to initial position and apply the first idx moves from moves_replay.
    Also updates replay_index, turn_step, selection, valid_moves, and recomputes options.
    """
    global replay_index, turn_step, selection, valid_moves, white_options, black_options
    if idx < 0:
        idx = 0
    if idx > len(moves_replay):
        idx = len(moves_replay)

    # if same index, nothing to do
    if idx == replay_index:
        return False

    # reset board and clears captures
    reset_board_to_start()

    # replay first idx moves
    replay_index = 0
    for i in range(idx):
        mv = moves_replay[i]
        applied = False
        # try manual_move (if available)
        try:
            if 'manual_move' in globals() and callable(manual_move):
                s = tuple(mv[0]); e = tuple(mv[1])
                applied = manual_move(s, e)
        except Exception:
            applied = False

        if not applied:
            applied = apply_move_force(mv)

        if applied:
            replay_index += 1
        else:
            # still advance logical pointer so idx matches requested history length
            # (this depends on whether you want to skip or stop; we choose to continue)
            replay_index += 0

    # Now set turn: after N moves, if N is even -> white to play (turn_step 0),
    # if N is odd -> black to play (turn_step 2).
    if replay_index % 2 == 0:
        turn_step = 0   # white: select a piece
    else:
        turn_step = 2   # black: select a piece

    # clear any selection and valid moves
    selection = 100
    valid_moves = []

    # recompute options lists for the current board state
    try:
        white_options = check_options(white_pieces, white_locations, 'white')
    except Exception:
        white_options = check_options(white_pieces, white_locations, 'white') if 'check_options' in globals() else []
    try:
        black_options = check_options(black_pieces, black_locations, 'black')
    except Exception:
        black_options = check_options(black_pieces, black_locations, 'black') if 'check_options' in globals() else []

    return True


def play_next_replay_move():
    """Advance by one move (->). Rebuilds board to replay_index+1 and updates turn state."""
    global replay_index
    if replay_index >= len(moves_replay):
        return False
    target = replay_index + 1
    changed = set_board_to_replay_index(target)
    return changed


def play_prev_replay_move():
    """Go back one move (Left Arrow). Rebuilds board to replay_index-1 and updates turn state."""
    global replay_index
    if replay_index <= 0:
        return False
    target = replay_index - 1
    changed = set_board_to_replay_index(target)
    return changed





run=True
while run:
    timer.tick(fps) 
    screen.fill('black')
    draw_board()
    draw_pieces()
    draw_captured()
 
#events
    
            # events
    # events
        # --- process manual_moves_queue (automatically play moves while running) ---
    now = pygame.time.get_ticks()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moved = play_next_replay_move()
                if moved:
                    screen.fill('black')
                    draw_board()
                    draw_pieces()
                    draw_captured()
                    pygame.display.flip()
                else:
                    print("No more moves to play (replay_index =", replay_index, "len =", len(moves_replay), ")")
            if event.key == pygame.K_LEFT:
                moved = play_prev_replay_move()
                if moved:
                    screen.fill('black')
                    draw_board()
                    draw_pieces()
                    draw_captured()
                    pygame.display.flip()
                else:
                    print("Already at start (replay_index =", replay_index, ")")



                
                




    pygame.display.flip()
pygame.quit()
