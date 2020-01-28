import pygame
import random
import os
import time 

wx = 450
wy = 502
pw = 25
random_a = random.uniform(50,297)
random_b = random.uniform(140,187)
a = {1: {'x': wx,'y': 0,'w': pw,'h': random_a}}
b = {1: {'x': wx,'y': (a[1]['h'] + random_b),'w': pw,'h': (wy - (a[1]['h'] + random_b))}}
_bird = {'x': 50, 'y': 255, 'w': 0, 'h': 0}
ss = 0
pygame.init()
screen = pygame.display.set_mode((wx, wy))
done = False
home = False
jump_wait = True
is_blue = True
game_over = False
_image_library = {}
jump_t = 0
jump_d = 0
jump = False
t = 0
runtime = 0
background_x = 0
xx = 0
clock = pygame.time.Clock()

# Classes section!

# class pipe:
#     def __init__(self, wx, wy):
#         self.wx = wx
#         self.wy = wy

#     def create():
#         rA = random.uniform(10, 150)
#         rB = random.uniform(60, 150)
#         a = {'x': 390,'y': 0,'w': 10,'h': rA}
#         b = {'x': 390,'y': (a['h'] + rB),'w': 10,'h': (wy - (a['h'] + rB))}
#         pygame.draw.rect(screen, color, pygame.Rect(a['x'], a['y'], a['w'], a['h']))
#         pygame.draw.rect(screen, color, pygame.Rect(b['x'], b['y'], b['w'], b['h']))

#     def move():
#         if a['x'] >= 0:
#             a['x'] -= 1
#             b['x'] -= 1

def get_image(path):
        global _image_library
        image = _image_library.get(path)
        
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
                
        return image

def new_pipe(id):
    ra = random.uniform(70,350)
    rb = random.uniform(100,190)
    a[id] = {'x': wx,'y': 0,'w': pw,'h': ra}
    b[id] = {'x': wx,'y': (a[id]['h'] + rb),'w': pw,'h': (wy - (a[id]['h'] + rb))}

def create_pipe(id):
    pygame.draw.rect(screen, color, pygame.Rect(a[id]['x'], a[id]['y'], a[id]['w'], a[id]['h']))
    pygame.draw.rect(screen, color, pygame.Rect(b[id]['x'], b[id]['y'], b[id]['w'], b[id]['h']))

def move(id):
    if a[id]['x'] < -26:

        a[id]['x'] == 390
        b[id]['x'] == 390

    elif a[id]['x'] > -25:

        a[id]['x'] -= 1
        b[id]['x'] -= 1

def bird():
    bird = screen.blit(get_image('img/bird5.png'), (_bird['x'], _bird['y']))

def score(s_type=0):
    font = pygame.font.SysFont("comicsansms", 32)
    text = font.render("Score: ", True, (0, 0, 0))
    
    screen.blit(text,(10,0))
    
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
        
# Time (Per second), path => sound path
# time = -1, infinity 
def sound(time1=0, path=0):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(time1)
    
        
for np in range(300):
    if np > 0:
        new_pipe(np)

# Music
sound(-1, 'sound/back_faster.mp3')
# pygame.mixer.music.load('sound/back_faster.mp3')
# pygame.mixer.music.play(-1)
# pygame.mixer.music.load('sound/full_track_fly_backgorund.mp3')
# pygame.mixer.music.play(-1)
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        is_blue = not is_blue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # left click grows radius
                        jump = True
                        jump_wait = True

        if (jump is True) & ( jump_t <= 32 ) & (_bird['y'] >= 0):
            jump_wait = True
            if (jump_wait == True):
                jump = True
                _bird['y'] -= 1.2
                jump_t += 1
                if jump_t >= 32:
                    jump = False
                    jump_wait = True
                    jump_t = 0

        if game_over is False:
            if (jump is False) & (_bird['y'] <= 450):
                _bird['y'] += 1.2

            for id in range(300):
                if id != 0:
                    
                    if( (a[id]['h'] - 4) < _bird['y'] < b[id]['y'] ) & ( (_bird['x'] + 20) == a[id]['x'] ):
                        ss += 1
                        
                    elif (a[id]['y'] < _bird['y'] < (a[id]['h'] -8 )) & ( (_bird['x'] + 20) == a[id]['x'] ):
                        game_over = True
                        
                    elif ( (b[id]['y'] - 220) < _bird['y']) & ( (_bird['x'] + 20) == b[id]['x'] ):
                        game_over = True
                        
            # TO-DO:
            # Make background like one infinite image
            if (background_x == 0) | (450 != (923 - xx)):
                
                background_x -= 1
                xx += 1
                
            else:
                
                background_x = 0
                xx = 0

            background = screen.blit(get_image('img/background1.png'), (background_x, 0))
            if is_blue: color = (0, 102, 51)
            else: color = (255, 100, 0)

            for np in range(300):
                if np > 0:
                    if t > (200 * np):
                        
                        create_pipe(np)
                        move(np)

            score()
            score_font = pygame.font.SysFont("comicsansms", 32)
            score_text = score_font.render("{0}".format(ss), True, (0, 0, 0))
            screen.blit(score_text,(120,0))
            bird()
            t += 1

        if (game_over is True) & (home == False):
            
            image = pygame.image.load('img/black.jpg').convert()
            image.set_alpha(128)
            screen.blit(image, (0, 0))
            game_over_title_font = pygame.font.SysFont("comicsansms", 32)
            game_over_title_text = game_over_title_font.render("GAME OVER!", True, (224, 224, 224))
            screen.blit(game_over_title_text,(162,225))
            game_over_score_font = pygame.font.SysFont("comicsansms", 32)
            game_over_score_text = game_over_score_font.render("Score: {}".format(ss), True, (224, 224, 224))
            screen.blit(game_over_score_text,(162,285))
            home = True
            
        runtime -= 1
        pygame.display.flip()
        clock.tick(110)