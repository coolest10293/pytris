import sys
from os import path
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
    imageDir = path.abspath(path.join(path.dirname(__file__), 'pytris\\images\\icon.bmp')).split('icon.bmp')[0]
    debugPrints = False
else:
    print('running in a normal Python process')
    imageDir = ''
    debugPrints = True





import pygame
try:
    import pytris_pieces
    import pytris_rng_logic
except:
    print('Supplimentary files not present!')
    
import random

# Some parts of initial setup and main loop kept from Pygame Template

# initial program setup

pygame.init()
icon = pygame.Surface((81, 81))
icon_image = pygame.image.load(f'{imageDir}icon.bmp')
icon.blit(icon_image, (0, 0))
pygame.display.set_icon(icon)
x = 720
y = 720
screen = pygame.display.set_mode((x, y))
sqwidth = x // 36
clock = pygame.time.Clock()
running = True
dt = 0
rot = 0
font = pygame.font.Font('freesansbold.ttf', 32)


# make the touch arrows
arrow = pygame.Surface((39, 39))
arrow.fill('darkgreen')
pygame.draw.line(arrow, 'red', (0, 19), (19, 0))
pygame.draw.line(arrow, 'red', (0, 19), (20, 39))
pygame.draw.line(arrow, 'red', (0, 19), (19, 19))
arrow_up = pygame.transform.rotate(arrow, 270)
arrow_right = pygame.transform.rotate(arrow, 180)
arrow_down = pygame.transform.rotate(arrow, 90)
arrow.convert()
arrow_up.convert()
arrow_down.convert()
arrow_right.convert()

newpiecestart = pygame.Vector2(16,4)
pytris_rng_logic.pieceroll()
pytris_rng_logic.pieceroll()
pytris_rng_logic.pieceroll()
pytrisboard = {}
piecenum = pytris_rng_logic.piecenum # the number for the current piece
npiecenum1 = pytris_rng_logic.nextpiece1 # the number for the very next piece 
npiecenum2 = pytris_rng_logic.nextpiece2 # the number for the 2nd piece waiting
npiecenum3 = pytris_rng_logic.nextpiece3 # the number for the third piece waiting
piecenumbers = {0: 't', 1: 'l', 2: 'j', 3: 'z', 4: 's', 5: 'o', 6: 'i'} # the lookup table for determining all the pieces
piececolors = {0: 'purple', 1: 'green', 2: 'blue', 3: 'orange', 4: 'yellow', 5: 'red', 6: 'cyan'} # the lookup table for determining the piece colors
isgrav = 1
current_piece = {}
nextpiece1 = {}
nextpiece2 = {}
nextpiece3 = {}
pytrisboard = {}
heldpiece = {}
lines = 0
griddraw = False
hasheldpiece = False
has_started_game = False
speed = 120
initSpeed = speed
levels = 20
gravTime = 0

if pygame.joystick.get_count() != 0:
    gpadn = 0
    while gpadn < pygame.joystick.get_count():
        exec(f'gamepad{gpadn} = pygame.joystick.Joystick({gpadn})')
        gpadn += 1
        

pieces_to_draw = {'self.shadow_piece': 'lightgrey', 'current_piece': 'piececol', 'nextpiece1': 'npiececol1', 'nextpiece2': 'npiececol2', 'nextpiece3': 'npiececol3', 'heldpiece': 'heldpiececol'}
lightgrey = 'lightgrey'
on = 'green'
off = 'red'
TextColor = 'White'
gridCol = 'white'
dark_mode = False

def rotset(piece):
    if rot == 0:
        piece += 'up'
    if rot == 1:
        piece += 'right'
    if rot == 2:
        piece += 'down'
    if rot == 3:
        piece += 'left'
    return piece

def drawgrid(w, rows, surface): # Code taken from a user on Stack Overflow
    """
    Draws a grid
    """
    sizebtwn = w // rows 
    for i in range(0, w, sizebtwn):
        x, y = i, i
        pygame.draw.line(surface, gridCol, (x, 0), (x, w))
        pygame.draw.line(surface, gridCol, (0, y), (w, y))




def keyinput():
    """
    Registers Key presses
    """
    global player_pos
    global rot
    global hasheldpiece
    global griddraw
    if (keys[pygame.K_p] and has_started_game) ^ (in_menu and keys[pygame.K_ESCAPE]):
        menu.pause()
        return
    if keys[pygame.K_w] ^ keys[pygame.K_UP] ^ pygame.Rect.colliderect(w_button, mouse_spot):
        pytris.hard_drop()
    if keys[pygame.K_a] ^ keys[pygame.K_LEFT] ^ pygame.Rect.colliderect(a_button, mouse_spot):
        if not(pytris.collide_detect_horiz('left')) and not(pytris.borders('l')):
            player_pos.x -= 1
    if keys[pygame.K_d] ^ keys[pygame.K_RIGHT] ^ pygame.Rect.colliderect(d_button, mouse_spot):
        horicol = not(pytris.collide_detect_horiz('right'))
        borcol = not(pytris.borders('r'))
        if horicol and borcol:
            player_pos.x += 1
    if keys[pygame.K_s] ^ keys[pygame.K_DOWN] ^ pygame.Rect.colliderect(s_button, mouse_spot):
        player_pos.y += 1
        pytris.collide_detect()
    if keys[pygame.K_q] ^ pygame.Rect.colliderect(q_button, mouse_spot):
        pytris.rotation('l')
                
    if keys[pygame.K_e] ^ pygame.Rect.colliderect(e_button, mouse_spot):
        pytris.rotation('r')

    if (keys[pygame.K_f] ^ pygame.Rect.colliderect(f_button, mouse_spot)) and hasheldpiece == 0:
        pytris.hold_piece()
        hasheldpiece += 1
    if (keys[pygame.K_p] and has_started_game) ^ (keys[pygame.K_ESCAPE] and has_started_game):
        menu.pause()
    if keys[pygame.K_m]:
        griddraw = not(griddraw)
    if keys[pygame.K_SLASH]:
        print(player_pos)
    if keys[pygame.K_BACKSLASH]:
        pygame.image.save(screen, 'screenshot.bmp')
        print('Screenshot!')
    rot = rot % 4
    return

    

class pytris:
    def __init__(self):
        global pytrisboard, lines, held_piece, heldpiece, heldpiececol, heldpiecenum
        lines = 0
        pytrisboard = {}
        num = 29
        while num > 2:
            pytrisboard[num] = {}
            num -= 1
        held_piece = {}
        self.hold = {}
        heldpiece = {}
        heldpiececol = {}
        
        self.basicRotations = {'01': [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)], '10': [(0,0), (1,0), (1,-1), (0,2), (1,2)], '12': [(0,0), (1,0), (1,-2), (0,2), (1,2)], '21': [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)], '23': [(0,0), (1,1), (1,1), (0,-2), (1,-2)], '32': [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)], '30': [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)], '03': [(0,0), (1,0), (1,1), (0,-2), (1,-2)]}
        self.iRotations = {'01': [(0,0), (-2,0), (1,0), (-2,-1), (1,2)], '10': [(0,0), (2,0), (-1,0), (2,1), (-1,-2)], '12': [(0,0), (-1,0), (2,0), (-1,2), (2,-1)], '21': [(0,0), (1,0), (-2,0), (1,-2), (-2,1)], '23': [(0,0), (2,0), (-1,0), (2,1), (-1,-2)], '32': [(0,0), (-2,0), (1,0), (-2,-1), (1,2)], '30': [(0,0), (1,0), (-2,0), (1,-2), (-2,1)], '03': [(0,0), (-1,0), (2,0), (-1,2), (2,-1)]}
        
    def collide_detect(self):
        """
        Detect a collision about to happen and add the current piece to the Board, then set a new piece
        """
        global pytrisboard
        test_piece = 0
        added_piece = 0
        while test_piece < 4:
            for key in pytrisboard:
                for key1 in pytrisboard[key]:
                    if key == self.piece[test_piece].y + 1 and key1 == self.piece[test_piece].x:
                        while added_piece < 4:
                            pytrisboard[int(self.piece[added_piece].y)][int(self.piece[added_piece].x)] = piececol
                            added_piece += 1
                        self.setnewpiece()
                        return False
                if len(pytrisboard[key].keys()) == 0:
                    if self.piece[test_piece].y == 29:
                        while added_piece < 4:
                            pytrisboard[int(self.piece[added_piece].y)][int(self.piece[added_piece].x)] = piececol
                            added_piece += 1
                        self.setnewpiece()
                        return False 

            test_piece += 1
        return True

    def makePiece(self, sqlist=list, place=pygame.Vector2, player=False):
        if player:
            curpiecenum = 0
            while curpiecenum < 4:
                if self.curpiece[curpiecenum] <= 3:
                    self.piece[curpiecenum] = pygame.Vector2(place.x - 2 + self.curpiece[curpiecenum] % 4, place.y - 2)
                elif self.curpiece[curpiecenum] <= 7:
                    self.piece[curpiecenum] = pygame.Vector2(place.x - 2 + self.curpiece[curpiecenum] % 4, place.y - 1)
                elif self.curpiece[curpiecenum] <= 11:
                    self.piece[curpiecenum] = pygame.Vector2(place.x - 2 + self.curpiece[curpiecenum] % 4, place.y)
                elif self.curpiece[curpiecenum] <= 15:
                    self.piece[curpiecenum] = pygame.Vector2(place.x - 2 + self.curpiece[curpiecenum] % 4, place.y + 1)
                curpiecenum += 1

        piece = [0,0,0,0]
        curpiecenum = 0
        while curpiecenum < 4:
            if sqlist[curpiecenum] <= 3:
                piece[curpiecenum] = squares(place.x - 2 + sqlist[curpiecenum] % 4, place.y - 2, 1, 1)
            elif sqlist[curpiecenum] <= 7:
                piece[curpiecenum] = squares(place.x - 2 + sqlist[curpiecenum] % 4, place.y - 1, 1, 1)
            elif sqlist[curpiecenum] <= 11:
                piece[curpiecenum] = squares(place.x - 2 + sqlist[curpiecenum] % 4, place.y, 1, 1)
            elif sqlist[curpiecenum] <= 15:
                piece[curpiecenum] = squares(place.x - 2 + sqlist[curpiecenum] % 4, place.y + 1, 1, 1)
            curpiecenum += 1
            
        return piece
        
        

    def rotation(self, RotDir='r' or 'l'):
        global rot, player_pos, gravTime
        if RotDir == 'r':
            RotSym = '+'
        elif RotDir == 'l':
            RotSym = '-'
        
        newRot = eval(f'{rot} {RotSym} 1') % 4
        oldRot = rot
                
        # Official Tetris Super Rotation System
        if piecenum < 6:
            rotationSet = 'basic'
        else:
            rotationSet = 'i'
        rotTest = f'{rot}{newRot}'
        rot = newRot
        for test in eval(f'self.{rotationSet}Rotations[rotTest]'):
            player_pos.x += test[0]
            player_pos.y -= test[1]
            self.update()
            
            if self.collide_detect_Dummy() and self.wall_detect_Dummy() and self.floor_detect_Dummy():
                gravTime = 0
                return
            else:
                player_pos.x -= test[0]
                player_pos.y += test[1]
        
        rot = oldRot
        self.update()
        return

                
            
        
    def collide_detect_Dummy(self):
        test_piece = 0
        while test_piece < 4:
            for key in pytrisboard:
                for key1 in pytrisboard[key]:
                    if key == self.piece[test_piece].y and key1 == self.piece[test_piece].x:
                        return False
            test_piece += 1
        return True
    
    def wall_detect_Dummy(self):
        test_piece = 1
        for pnum in self.piece:
            piece = self.piece[pnum]
            if piece.x == play_area_sides[0] or piece.x == play_area_sides[1]:
                return False
            
        return True
    
    def floor_detect_Dummy(self):
        test_piece = 1
        for pnum in self.piece:
            piece = self.piece[pnum]
            if piece.y == 30:
                return False
        return True
    
    def shadow_detect(self):
        """
        second part of the shadow piece code
        """
        test_piece = 0
        while test_piece < 4:
            for key in pytrisboard:
                for key1 in pytrisboard[key]:
                    if key == self.piece[test_piece].y + 1 and key1 == self.piece[test_piece].x:
                        return False
                if len(pytrisboard[key].keys()) == 0:
                    if self.piece[test_piece].y == 29:
                        return False
            test_piece += 1
        return True
                

    def collide_detect_horiz(self, direction):
        """
        Detect a collision about to happen horizontally and stop the piece from moving
        
        Paramaters:
        Direction: Values are left or right
        Determines which way it checks for a piece
        """
        if direction.lower() == 'left':
            symbol = -1
        elif direction.lower() == 'right':
            symbol = +1
        test_piece = 0
        while test_piece < 4:
            for key in pytrisboard:
                for key1 in pytrisboard[key]:
                    if key == self.piece[test_piece].y and key1 == self.piece[test_piece].x + symbol:
                        return True
            test_piece += 1
        return False        
        
    
    def gravity(self):
        """
        Gravity for the pytris Pieces
        """
        global player_pos
        player_pos.y += 1

    def update(self):
        """
        Update the piece with the new Player Position
        """
        global current_piece
        self.curpiece = eval(f'pytris_pieces.{rotset(piecenumbers[piecenum])}')
        current_piece = self.makePiece(self.curpiece, player_pos, player=True)
        
        
    def draw(self):
        """
        Draw the pieces to the board
        """
        
        screen.fill(BackgroundCol)
        pygame.draw.rect(screen, Area1Col, held_piece_area1)
        pygame.draw.rect(screen, Area1Col, play_area1)
        pygame.draw.rect(screen, Area2Col, play_area2)
        pygame.draw.rect(screen, Area1Col, upcoming_piece_area1)
        pygame.draw.rect(screen, Area2Col, upcoming_piece_area2)
        pygame.draw.rect(screen, Area2Col, held_piece_area2)

        piece_num = 0
        while piece_num < len(pieces_to_draw):
            curpiecedrawn = 0
            while curpiecedrawn < 4:
                try:
                    pygame.draw.rect(screen, eval(pieces_to_draw[list(pieces_to_draw.keys())[piece_num]]), eval(list(pieces_to_draw.keys())[piece_num])[curpiecedrawn])
                except:
                    pass
                curpiecedrawn += 1
            piece_num += 1
        
        if not(draw_held_piece):
            pygame.draw.rect(screen, 'lightgray', held_piece_area1)
        
        if not(draw_upcoming_pieces):
            pygame.draw.rect(screen, 'lightgray', upcoming_piece_area1)

        for key1 in pytrisboard:
            for key2 in pytrisboard[key1]:
                if not(key1 == '30'):
                    pygame.draw.rect(screen, pytrisboard[key1][key2], squares(key2,key1,1,1))
        
        
        pygame.draw.rect(screen, 'red', q_button)
        pygame.draw.rect(screen, 'yellow', e_button)
        screen.blit(arrow, (0 * sqwidth + 1, 21 * sqwidth + 1))
        screen.blit(arrow_up, (2 * sqwidth + 1, 19 * sqwidth + 1))
        screen.blit(arrow_right, (4 * sqwidth + 1, 21 * sqwidth + 1))
        screen.blit(arrow_down, (2 * sqwidth + 1, 21 * sqwidth + 1))
        pygame.draw.rect(screen, 'red', f_button)
        drawgrid(x, x // sqwidth, screen)
        pygame.display.flip()
        
        return
    
    def borders(self, side):
        """
        Keep the pytris piece in the borders of the play area
        """
        testpiece = 0
        while testpiece < 4:
            if side == 'l':
                if self.piece[testpiece].x <= play_area_sides[0] + 1:
                    return True
            if side == 'r':
                if self.piece[testpiece].x >= play_area_sides[1] - 1:
                    return True
            testpiece += 1
            
            
        return False
    
    def rotborders(self):
        """
        Stop pieces from rotating outside of the play area
        """
        testpiece = 1
        while testpiece < 5:
            if self.piece[testpiece].x == play_area_sides[0]:
                return False
            if self.piece[testpiece].x == play_area_sides[1]:
                return False
            testpiece += 1
        return True
        
        
    
    def make_shadow_piece(self):
        """
        have a shadow of the piece to show you where its going to drop
        """
        global player_pos
        global current_piece
        self.shadow_piece = {}
        hold_player_pos = player_pos.y + 1
        hold_player_pos -= 1
        self.update()
        while self.shadow_detect():
            player_pos.y += 1
            self.update()
        self.shadow_piece = current_piece
        player_pos.y = hold_player_pos
        self.update()
        
    def setnewpiece(self):
        """
        Sets up the next piece
        
        Used when piece hits the next piece
        """
        global hasheldpiece, current_piece, piecenum, player_pos, piececol, npiececol1, npiececol2, npiececol3, npiecenum1, npiecenum2, npiecenum3, rot, heldpiececol, nextpiece1, nextpiece2, nextpiece3
        rot = 0
        pytris_rng_logic.pieceroll()
        piecenum = pytris_rng_logic.piecenum # the number for the current piece
        npiecenum1 = pytris_rng_logic.nextpiece1 # the number for the very next piece 
        npiecenum2 = pytris_rng_logic.nextpiece2 # the number for the 2nd piece waiting
        npiecenum3 = pytris_rng_logic.nextpiece3 # the number for the third piece waiting
        self.piece = {}
        curpiecenum = 0
        currentspot = 1
        try:
            heldpiececol = self.tempheldpiececol
        except:
            pass
        
        player_pos.xy = newpiecestart.xy
        self.curpiece = eval('pytris_pieces.' + (piecenumbers[piecenum] + 'up'))
        npiece1 = eval('pytris_pieces.' + (piecenumbers[npiecenum1] + 'up'))
        npiece2 = eval('pytris_pieces.' + (piecenumbers[npiecenum2] + 'up'))
        npiece3 = eval('pytris_pieces.' + (piecenumbers[npiecenum3] + 'up'))
        
        piececol = piececolors[piecenum]
        npiececol1 = piececolors[npiecenum1]
        npiececol2 = piececolors[npiecenum2]
        npiececol3 = piececolors[npiecenum3]

        self.update()
        
        
        
        nextpiece1 = self.makePiece(npiece1, npiecespot1)
        nextpiece2 = self.makePiece(npiece2, npiecespot2)
        nextpiece3 = self.makePiece(npiece3, npiecespot3)
        hasheldpiece = 0
        self.line_detect()
        return
    
    def hold_piece(self):
        """
        Hold a Piece
        """
        global current_piece
        global piececol
        global heldpiece
        global heldpiececol
        global player_pos
        global piecenum
        global heldpiecenum
        global rot
        rot = 0
        self.update()
        try:
            self.hold[1]
            
        except:
            self.hold = {}
            self.tempheldpiececol = piececol
            self.hold = self.curpiece
            heldpiecenum = piecenum
            # set the held piece
            heldpiece = self.makePiece(self.hold, heldpiecespot)
            self.setnewpiece()
            heldpiececol = lockedHeldPieceCol
            return
        else:
            tempcol = heldpiececol
            self.tempheldpiececol = piececol
            piececol = tempcol
            heldpiececol = lockedHeldPieceCol
            temppiece = self.hold
            self.hold = self.curpiece
            self.curpiece = temppiece
            temppiecenum = piecenum
            piecenum = heldpiecenum
            heldpiecenum = temppiecenum
    
        player_pos = pygame.Vector2(16, 3)
        current_piece = self.makePiece(self.curpiece, player_pos, player=True)
        
        # set the held piece
        heldpiece = self.makePiece(self.hold, heldpiecespot)

    
    def line_detect(self):
        """
        Detects lines that need to be cleared and updates score
        """
        global lines, rowstodelete, pytrisboard, safeBoard
        rowtocheck = 3
        rowstodelete = []
        while rowtocheck < 30:
            if len(pytrisboard[rowtocheck]) == 10:
                if mode == 'number_of_lines':
                    lines -= 1
                    if lines == 0:
                        print("You win! Congrats!")
                        menu.reset()
                else:
                    lines += 1


                rowstodelete.append(rowtocheck)
            rowtocheck += 1
                
        for row in rowstodelete:
            pytrisboard.pop(row)
            self.move_rows_down(row)

        self.game_over_detect()
        return

    def move_rows_down(self, linenumber):
        """
        Clears lines when called.
        
        Paramaters:
        linenumber = The line to be cleared
        """
        global pytrisboard
        line = linenumber
        while line > 3:
            pytrisboard[line] = pytrisboard.pop(line - 1)
            line -= 1
        pytrisboard[3] = {}
        return
    def hard_drop(self):
        """
        Do a hard drop
        """
        global player_pos
        player_pos.y += 1
        self.update()
        while self.collide_detect():
            player_pos.y += 1
            self.update()
        
        
        
    def game_over_detect(self):
        """
        Detect if you lost
        """
        global in_menu
        global in_game
        if len(pytrisboard[3].keys()) == 0:
            return
        else:
            menu.reset()
    def garbage_set(self):
        """
        Add garbage to the board
        """
        global pytrisboard
        line = 29
        numofgarbage = 0
        prevgarb = {0: 0}
        while (line + level) > 29:
            while numofgarbage < 7:
                checking = True
                garbage = random.randint(play_area_sides[0] + 1, play_area_sides[1] - 1)
                while checking:
                    try:
                        for key in prevgarb:
                            if garbage == prevgarb[key]:
                                garbage = random.randint(play_area_sides[0] + 2, play_area_sides[1] - 1)
                            else:
                                checking = False
                    except:
                        checking = False
                pytrisboard[line][garbage] = [0,0]
                pytrisboard[line][garbage][0] = 'black'
                pytrisboard[line][garbage][1] = squares(garbage, line, 1, 1)
                prevgarb[numofgarbage] = garbage
                numofgarbage += 1
            line -= 1
            prevgarb = {0: 0}
            numofgarbage = 0
        

def squares(x, y, h, w): # Code modified from code provided by a user on stack overflow
    cx, cy = x * sqwidth, y * sqwidth
    square = pygame.Rect(cx, cy, sqwidth * w, sqwidth * h)
    return square


def mouse_pos(x, y): # Code likely taken from a user on stack overflow
    ix, iy = x // sqwidth, y // sqwidth
    pos = pygame.Vector2(ix, iy)
    return pos



class menu:
    def __init__(self):
        self.main = ['play', 'settings']
        self.mode = ['endless','lines','garbage']
    def display_main(self):
        """
        Display the main menu
        """
        logo = pygame.image.load(f'{imageDir}pytris.bmp')
        screen.blit(logo, (0, 35))

        # play button
        pygame.draw.rect(screen, 'blue', play_button)
        play_text = font.render('Play', True, 'green')
        play_textRect = play_text.get_rect()
        play_textRect.center = play_button.center
        screen.blit(play_text, play_textRect)

        # settings button
        pygame.draw.rect(screen, 'red', settings_button)
        settings_text = font.render('Settings', True, 'green')
        settings_textRect = settings_text.get_rect()
        settings_textRect.center = settings_button.center
        screen.blit(settings_text, settings_textRect)
        
    def display_settings(self):
        """
        Display the Settings Menu
        """
        logo = pygame.image.load(f'{imageDir}settings.bmp')
        screen.blit(logo, (0, 0))
        
        # Speed settings Button
        pygame.draw.rect(screen, 'blue', speed_button)
        speed_text1 = font.render('Adjust', True, 'green')
        speed_text1Rect = speed_text1.get_rect()
        speed_text1Rect.center = (10 * sqwidth, 16 * sqwidth)
        screen.blit(speed_text1, speed_text1Rect)
        speed_text2 = font.render('Speed', True, 'green')
        speed_text2Rect = speed_text2.get_rect()
        speed_text2Rect.center = (10 * sqwidth, 18 * sqwidth)
        screen.blit(speed_text2, speed_text2Rect)
        
        # Display settings button
        pygame.draw.rect(screen, 'blue', display_settings_button)
        display_text1 = font.render('Display', True, 'red')
        display_text1Rect = display_text1.get_rect()
        display_text1Rect.center = (24 * sqwidth, 16 * sqwidth)
        screen.blit(display_text1, display_text1Rect)
        display_text2 = font.render('Settings', True, 'red')
        display_text2Rect = display_text2.get_rect()
        display_text2Rect.center = (24 * sqwidth, 18 * sqwidth)
        screen.blit(display_text2, display_text2Rect)
        
        # Back button
        pygame.draw.rect(screen, 'blue', back_button)
        back_text = font.render('Back', True, TextColor)
        back_textRect = back_text.get_rect()
        back_textRect.center = back_button.center
        screen.blit(back_text, back_textRect)

    def display_display_settings(self):
        global on, off
        logo = pygame.image.load(f'{imageDir}display.bmp')
        screen.blit(logo, (0, 0))
        settings = pygame.image.load(f'{imageDir}settings.bmp')
        screen.blit(settings, (0, logo.get_height() - sqwidth))
        
        # Set up colors for the buttons
        if draw_upcoming_pieces:
            toggle_upcoming_color = on
        else:
            toggle_upcoming_color = off
        if draw_held_piece:
            toggle_held_color = on
        else:
            toggle_held_color = off
        if dark_mode:
            toggle_dark_mode_color = on
        else:
            toggle_dark_mode_color = off

        # Toggle upcoming pieces button
        pygame.draw.rect(screen, toggle_upcoming_color, toggle_upcoming_pieces_button)
        toggle_upcoming_text1 = font.render('Toggle', True, TextColor)
        toggle_upcoming_text1Rect = toggle_upcoming_text1.get_rect()
        toggle_upcoming_text1Rect = (8.75 * sqwidth, 15 * sqwidth)
        screen.blit(toggle_upcoming_text1, toggle_upcoming_text1Rect)
        toggle_upcoming_text2 = font.render('Upcoming', True, TextColor)
        toggle_upcoming_text2Rect = toggle_upcoming_text2.get_rect()
        toggle_upcoming_text2Rect = (7.5 * sqwidth, 17 * sqwidth)
        screen.blit(toggle_upcoming_text2, toggle_upcoming_text2Rect)
        toggle_upcoming_text3 = font.render('Pieces', True, TextColor)
        toggle_upcoming_text3Rect = toggle_upcoming_text3.get_rect()
        toggle_upcoming_text3Rect = (8.75 * sqwidth, 19 * sqwidth)
        screen.blit(toggle_upcoming_text3, toggle_upcoming_text3Rect)

        
        # Toggle held piece button
        pygame.draw.rect(screen, toggle_held_color, toggle_held_piece_button)
        toggle_held_text1 = font.render('Toggle', True, TextColor)
        toggle_held_text1Rect = toggle_held_text1.get_rect()
        toggle_held_text1Rect = (21.25 * sqwidth, 15 * sqwidth)
        screen.blit(toggle_held_text1, toggle_held_text1Rect)
        toggle_held_text2 = font.render('Held', True, TextColor)
        toggle_held_text2Rect = toggle_held_text2.get_rect()
        toggle_held_text2Rect = (22 * sqwidth, 17 * sqwidth)
        screen.blit(toggle_held_text2, toggle_held_text2Rect)
        toggle_held_text3 = font.render('Pieces', True, TextColor)
        toggle_held_text3Rect = toggle_held_text3.get_rect()
        toggle_held_text3Rect = (21.25 * sqwidth, 19 * sqwidth)
        screen.blit(toggle_held_text3, toggle_held_text3Rect)
        
        
        # Dark Mode Toggle
        pygame.draw.rect(screen, toggle_dark_mode_color, toggle_dark_mode_button)
        toggle_DM_text1 = font.render('Toggle', True, TextColor)
        toggle_DM_text1Rect = toggle_DM_text1.get_rect()
        toggle_DM_text1Rect = (16.5 * sqwidth, 23 * sqwidth)
        screen.blit(toggle_DM_text1, toggle_DM_text1Rect)
        toggle_DM_text2 = font.render('Dark', True, TextColor)
        toggle_DM_text2Rect = toggle_DM_text2.get_rect()
        toggle_DM_text2Rect = (17 * sqwidth, 25 * sqwidth)
        screen.blit(toggle_DM_text2, toggle_DM_text2Rect)
        toggle_DM_text3 = font.render('Mode', True, TextColor)
        toggle_DM_text3Rect = toggle_DM_text3.get_rect()
        toggle_DM_text3Rect = (16.5 * sqwidth, 27 * sqwidth)
        screen.blit(toggle_DM_text3, toggle_DM_text3Rect)
        
        
        # Back button
        pygame.draw.rect(screen, 'blue', back_button)
        back_text = font.render('Back', True, TextColor)
        back_textRect = back_text.get_rect()
        back_textRect.center = back_button.center
        screen.blit(back_text, back_textRect)


        
    def display_number_select(self, Logo, Size):
        logo = pygame.image.load(Logo)
        screen.blit(logo, (0, 0))
        select = pygame.image.load(f'{imageDir}select.bmp')
        screen.blit(select, (0, logo.get_height() - sqwidth))
        
        button_number = 1
        while button_number < 10:
            button_text = button_number * Size
            button_number = str(button_number)
            exec('pygame.draw.rect(screen, "blue", num' + button_number + '_button)')
            exec('buttonnumber' + button_number + ' = font.render("' + str(button_text) + '", True, "green")')
            exec('buttonnumber' + button_number + 'Rect = buttonnumber' + button_number + '.get_rect()')
            exec('buttonnumber' + button_number + 'Rect.center = num' + button_number + '_button.center')
            exec('screen.blit(buttonnumber' + button_number + ', buttonnumber' + button_number + 'Rect)')
            button_number = int(button_number)
            button_number += 1
            
        # Back button
        pygame.draw.rect(screen, 'blue', back_button)
        back_text = font.render('Back', True, TextColor)
        back_textRect = back_text.get_rect()
        back_textRect.center = back_button.center
        screen.blit(back_text, back_textRect)

                
    def display_mode_select(self):
        logo = pygame.image.load(f'{imageDir}mode.bmp')
        screen.blit(logo, (0, 0))
        select = pygame.image.load(f'{imageDir}select.bmp')
        screen.blit(select, (0, logo.get_height() - sqwidth))
        
        pygame.draw.rect(screen, 'blue', mode_endless_button)
        pygame.draw.rect(screen, 'red', mode_garbage_button)
        pygame.draw.rect(screen, 'green', mode_number_lines_button)
        endless_text = font.render('Endless', True, 'red')
        garbage_text = font.render('Garbage', True, 'green')
        lines_text = font.render('Lines', True, 'blue')
        endless_textRect = endless_text.get_rect()
        garbage_textRect = garbage_text.get_rect()
        lines_textRect = lines_text.get_rect()
        endless_textRect.center = mode_endless_button.center
        garbage_textRect.center = mode_garbage_button.center
        lines_textRect.center = mode_number_lines_button.center
        screen.blits(((lines_text, lines_textRect), (endless_text, endless_textRect), (garbage_text, garbage_textRect)))
        
        # Back button
        pygame.draw.rect(screen, 'blue', back_button)
        back_text = font.render('Back', True, TextColor)
        back_textRect = back_text.get_rect()
        back_textRect.center = back_button.center
        screen.blit(back_text, back_textRect)

        
        
    def reset(self):
        """
        Reset the game
        """
        global pytrisboard, in_menu, main_menu, settings_menu, in_game, lines, mode_selection, level_select, number_lines_select, speed_settings, heldpiece, speed, display_settings, draw_held_piece, draw_upcoming_pieces
        pytrisboard = {}
        num = 29
        while num > 2:
            pytrisboard[num] = {}
            num -= 1
        heldpiece = {}
        pytris.setnewpiece()
        in_game = False
        settings_menu = False
        main_menu = True
        in_menu = True
        level_select = False
        mode_selection = False
        number_lines_select = False
        speed_settings = False
        display_settings = False
        draw_held_piece = True
        draw_upcoming_pieces = True
        isgrav = 1
        lines = 0
        speed = 120
    
    def pause(self):
        global in_menu
        global in_game
        global main_menu
        in_menu = not(in_menu)
        in_game = not(in_game)
        main_menu = not(main_menu)
    
    def darkModeSet(self):
        global TextColor, Area1Col, Area2Col, BackgroundCol, gridCol, lockedHeldPieceCol
        if dark_mode:
            TextColor = 'black'
            Area1Col = 'dark gray'
            Area2Col = 'black'
            BackgroundCol = 'dark green'
            gridCol = 'light gray'
            lockedHeldPieceCol = 'dark gray'
        else:
            TextColor = 'white'
            Area1Col = 'light gray'
            Area2Col = 'dark gray'
            BackgroundCol = 'green'
            gridCol = 'white'
            lockedHeldPieceCol = 'black'



play_area_sides = [10, 21]

# play area spots
held_piece_area1 = squares(1, 5, 6, 6)
held_piece_area2 = squares(2, 6, 4, 4)
play_area1 = squares(play_area_sides[0], 1, 30, play_area_sides[1] - play_area_sides[0] + 1)
play_area2 = squares(play_area_sides[0] + 1, 2, 28, play_area_sides[1] - play_area_sides[0] - 1)
upcoming_piece_area1 = squares(25, 2, 16, 6)
upcoming_piece_area2 = squares(26, 3, 14, 4)

# default values for pieces
player_pos = pygame.Vector2(14, 4)
npiecespot1 = pygame.Vector2(28, 5)
npiecespot2 = pygame.Vector2(28, 10)
npiecespot3 = pygame.Vector2(28, 15)
heldpiecespot = pygame.Vector2(4, 8)

# setting up the pytris class
pytris = pytris()

# main menu
play_button = squares(10, 15, 3, 4)
settings_button = squares(20, 15, 3, 8)

# setings
display_settings_button = squares(20, 15, 4, 8)
speed_button = squares(7, 15, 4, 6)
back_button = squares(3, 30, 3, 5)

# display settings buttons
toggle_upcoming_pieces_button = squares(7, 15, 6, 9)
toggle_held_piece_button = squares(20, 15, 6, 8)
toggle_dark_mode_button = squares(15, 23, 6, 8)

# number buttons
num1_button = squares(7, 15, 2, 2)
num2_button = squares(10, 15, 2, 2)
num3_button = squares(13, 15, 2, 2)
num4_button = squares(7, 18, 2, 2)
num5_button = squares(10, 18, 2, 2)
num6_button = squares(13, 18, 2, 2)
num7_button = squares(7, 21, 2, 2)
num8_button = squares(10, 21, 2, 2)
num9_button = squares(13, 21, 2, 2)

# mode buttons
mode_endless_button = squares(15, 15, 2, 7)
mode_number_lines_button = squares(19, 20, 2, 6)
mode_garbage_button = squares(9, 20, 2, 8)

# control buttons
w_button = squares(2, 19, 2, 2)
a_button = squares(0, 21, 2, 2)
s_button = squares(2, 21, 2, 2)
d_button = squares(4, 21, 2, 2)
q_button = squares(0, 19, 2, 2)
e_button = squares(4, 19, 2, 2)
f_button = squares(6, 21, 2, 2)

# setting up the menu
menu = menu()
menu.reset()
menu.darkModeSet()

def manual_restart():
    global screen
    global pygame
    pygame.init()
    screen = pygame.display.set_mode((x, y))
    pytris.draw()
    

while running:
    dt = clock.tick(60) / 1000
    event_list = pygame.event.get()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    mouse_spot = squares(mouse[0] // sqwidth, mouse[1] // sqwidth, 1, 1)

    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            keyinput()
    screen.fill('black')

    # The menu that comes up when you start the game
    if in_menu:
        if main_menu:
            pygame.display.set_caption('Pytris, Main Menu')
            menu.display_main()
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect.colliderect(play_button, mouse_spot):
                        main_menu = False
                        mode_selection = True
                    if pygame.Rect.colliderect(settings_button, mouse_spot):
                        main_menu = False
                        settings_menu = True

        elif mode_selection:
            pygame.display.set_caption('Pytris, Mode selection')
            menu.display_mode_select()
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect.colliderect(mode_endless_button, mouse_spot):
                        mode = 'endless'
                        mode_selection = False
                        in_game = True
                        in_menu = False
                        pytris.__init__()
                    if pygame.Rect.colliderect(mode_number_lines_button, mouse_spot):
                        mode = 'number_of_lines'
                        mode_selection = False
                        number_lines_select = True
                        pytris.__init__()
                    if pygame.Rect.colliderect(mode_garbage_button, mouse_spot):
                        mode = 'garbage'
                        mode_selection = False
                        level_select = True
                        pytris.__init__()
                    if pygame.Rect.colliderect(back_button, mouse_spot):
                        mode_selection = False
                        main_menu = True

        # Select the level for garbage mode
        elif level_select:
            pygame.display.set_caption('Pytris, Level selection')
            menu.display_number_select('level.bmp', 1)
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    a = 1
                    while a < 10:
                        a = str(a)
                        if eval('pygame.Rect.colliderect(num' + a + '_button, mouse_spot)'):
                            level = int(a)
                            pytris.garbage_set()
                            level_select = False
                            in_game = True
                            in_menu = False
                        a = int(a)
                        a += 1
                    if pygame.Rect.colliderect(back_button, mouse_spot):
                        level_select = False
                        mode_selection = True

        # Select the number of lines to clear
        # Only used when lines mode is selected
        elif number_lines_select:
            pygame.display.set_caption('Pytris, Number of Lines selection')
            menu.display_number_select('lines.bmp', 10)
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    a = 1
                    while a < 10:
                        a = str(a)
                        if eval('pygame.Rect.colliderect(num' + a + '_button, mouse_spot)'):
                            lines = int(str(a + '0'))
                            number_lines_select = False
                            in_game = True
                            in_menu = False
                        a = int(a)
                        a += 1
                    if pygame.Rect.colliderect(back_button, mouse_spot):
                        number_lines_select = False
                        mode_selection = True


        elif settings_menu:
            if speed_settings:
                pygame.display.set_caption('Pytris, Speed settings')
                menu.display_number_select('speed.bmp', 1)
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        a = 1
                        while a < 10:
                            a = str(a)
                            if eval(f'pygame.Rect.colliderect(num{a}_button, mouse_spot)'):
                                a = int(a)
                                speed = 60 - (60 * ((a - 1) / 10))
                                print(speed)
                            a = int(a)
                            a += 1
                        if pygame.Rect.colliderect(back_button, mouse_spot):
                            speed_settings = False
                            init_speed = speed

            
            elif display_settings:
                menu.display_display_settings()
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.Rect.colliderect(back_button, mouse_spot):
                            display_settings = False
                        if pygame.Rect.colliderect(toggle_upcoming_pieces_button, mouse_spot):
                            draw_upcoming_pieces = not(draw_upcoming_pieces)
                        if pygame.Rect.colliderect(toggle_held_piece_button, mouse_spot):
                            draw_held_piece = not(draw_held_piece)
                        if pygame.Rect.colliderect(toggle_dark_mode_button, mouse_spot):
                            dark_mode = not(dark_mode)
                            menu.darkModeSet()


            else:
                pygame.display.set_caption('Pytris, Settings')
                menu.display_settings()
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.Rect.colliderect(speed_button, mouse_spot):
                            speed_settings = True
                        if pygame.Rect.colliderect(display_settings_button, mouse_spot):
                            display_settings = True
                        if pygame.Rect.colliderect(back_button, mouse_spot):
                            settings_menu = False
                            main_menu = True
        if griddraw:
            drawgrid(x, 35, screen)
            

    # the main game code
    if in_game:
        has_started_game = True 
        screen.fill(BackgroundCol)
        if mode == 'endless' or mode == 'garbage':
            pygame.display.set_caption(f'Pytris  Lines cleared: {lines}  Speed: {speed}')
        elif mode == 'number_of_lines':
            pygame.display.set_caption(f'Pytris  Lines remaining: {lines}  Speed: {speed}')
        pytris.update()
        pytris.make_shadow_piece()
        pytris.draw()
        level = lines // 10
        speed = initSpeed - (level * 6)
        isgrav += initSpeed * dt
        if isgrav % speed < isgrav:
            print(pygame.time.get_ticks() - gravTime)
            gravTime = pygame.time.get_ticks()
            
            isgrav %= speed
            pytris.gravity()
            pytris.collide_detect()
    pygame.display.flip()

print('THANK YOU SO MUCH FOR PLAYING MY GAME :)')
pygame.quit()