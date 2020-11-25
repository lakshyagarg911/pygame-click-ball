'''
YaY i made it finally
Instructions:
1) Run the file
2) Click to place line
3) 'F' to change end of line
4) use 'UP' and "DOWN" arrow keys to increase and decrease tht thickness of the selected line
5) 'N' to add a new line and 'D' to delete the current line 
6) 'Enter' to change line 
7) 'S' to print the coordinates (for now atleast)
8) 'M' to change mode (line, flag, player)
9) If u wanna change these shortcuts, u can tell me or change urself!!
10) Have fun
11) Keep Coding :)

** last and last second are compulsary :p **
'''

from imports.settings import WW, WH
import pygame, math, json, os

pygame.init()

screen_flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WW, WH), screen_flags)
font = pygame.font.Font('Roboto-Thin.ttf', 32)

GRID_SIZE = 20
GRID_COLOR = (200, 200, 200)

SELECTED_LINE_COLOR = (255, 255, 50)
LINE_COLOR = (100, 255, 255)

SELECTED_BALL_COLOR = (255, 255, 50)
BALL_COLOR = (100, 255, 255)

class Line:
    def __init__(self, x1, y1, x2, y2, width):
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)
        self.width = width
        self.color = LINE_COLOR
    
    def draw(self):
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)

class Flag:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/imgs/victory_flag.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/imgs/skins_png/ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class BouncingBall:
    def __init__(self, x, y, r, color):
        self.center = (x, y)
        self.radius = r
        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

flag = Flag(WW//2, WH//2)
player = Player(WW//2, WH//2)

## balls
num_of_balls = 1
balls = []
for i in range(num_of_balls):
    b = BouncingBall(WW//2, WH//2, 10, BALL_COLOR)
    balls.append(b)

selected_ball_index = 0
selected_ball = balls[selected_ball_index]

## lines
num_of_lines = 1
lines = []
for i in range(num_of_lines):
    l = Line(WW//2, WH//2, WW//2, WH//2, 10)
    lines.append(l)

selected_line_index = 0
selected_line = lines[selected_line_index]
selected_line_end = 'start'

running = True
clicked = False

def save():
    ## saving data in a variable for now
    start_positions = []
    end_positions = []
    widths = []
    ball_positions = []
    ball_radius = []
    ## Lines
    for line in lines:
        start_positions.append(line.start_pos)
        end_positions.append(line.end_pos)
        widths.append(line.width)
    ## Flag
    victory_position = [flag.rect.bottomleft]
    ## Player
    player_position = [player.rect.center]
    ## Balls
    for ball in balls:
        ball_positions.append(ball.center)
        ball_radius.append(ball.radius)

    # printing the final result ;)
    print('--------------------------------------------------')
    print("level = {")
    print("    \'start\' :", start_positions, ",")
    print("    \'end\' :", end_positions, ",")
    print("    \'thickness\' :", widths, ",")
    print("    \'moves\' :", 5, ",", "## ;)")
    print("    \'victory\' :", victory_position, ",")
    print("    \'player\' :", player_position, ",")
    print("    \'ball_center\' :", ball_positions, ",")
    print("    \'ball_radius\' :", ball_radius)
    print("}")
    print('--------------------------------------------------')

    to_dump_dict = {
    'start':start_positions,
    'end':end_positions,
    'thickness':widths,
    'moves':5,
    'victory':victory_position,
    'player':player_position,
    'ball_center':ball_positions,
    'ball_radius':ball_radius
    }

    f_name = str(len(os.listdir(os.path.join('assets', 'level_editor_saves'))))
    f_path = os.path.join('assets', 'level_editor_saves', f_name + '.json')

    with open(os.path.join('assets', 'level_editor_saves',f_name + '.json'), "w") as f:
        json.dump(to_dump_dict,f ,indent = 4)
    print('saved at', f_path)



## line / flag / player
modes = ['line', 'flag', 'player', 'bouncing ball']
mode_index = 0
mode = modes[mode_index]
while running:
    
    mx, my = pygame.mouse.get_pos()
    mx = round(mx/GRID_SIZE)*GRID_SIZE
    my = round(my/GRID_SIZE)*GRID_SIZE

    screen.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        ## Clicking
        if e.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif e.type == pygame.MOUSEBUTTONUP:
            clicked = False

        if e.type == pygame.KEYDOWN:
            ## Will Run ALWAYS
            if e.key == pygame.K_m:
                mode_index += 1

            ## To save press S
            if e.key == pygame.K_s:
                save()

            ## Will only run if mode is line
            if mode == 'line':
                ## iterating thru lines
                if e.key == pygame.K_RETURN:
                    selected_line_index += 1

                ## iterating thru line ends
                if e.key == pygame.K_f:
                    if selected_line_end == 'start':
                        selected_line_end = 'end'
                    elif selected_line_end == 'end':
                        selected_line_end = 'start'

                ## adding a new line
                if e.key == pygame.K_n:
                    l = Line(WW//2, WH//2, WW//2, WH//2, 10)
                    lines.append(l)
                    selected_line_index = lines.index(l) 
                
                ## deleting the current line
                if e.key == pygame.K_d:
                    lines.remove(selected_line)

                ## To increase width, press up arrow
                if e.key == pygame.K_UP:
                    selected_line.width += 5

                ## To decrease width, press down arrow
                if e.key == pygame.K_DOWN:
                    selected_line.width -= 5

            ## Will only run if mode is bouncing ball
            if mode == 'bouncing ball':
                ## iterating thru balls
                if e.key == pygame.K_RETURN:
                    selected_ball_index += 1

                ## adding a new ball
                if e.key == pygame.K_n:
                    b = BouncingBall(WW//2, WH//2, 10, BALL_COLOR)
                    balls.append(b)
                    selected_ball_index = balls.index(b) 
                
                ## deleting the current ball
                if e.key == pygame.K_d:
                    balls.remove(selected_ball)

                ## To increase radius, press up arrow
                if e.key == pygame.K_UP:
                    selected_ball.radius += 5

                ## To decrease radius, press down arrow
                if e.key == pygame.K_DOWN:
                    selected_ball.radius -= 5

    ## Drawing the grid
    for x in range(0, WW, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WH))
    for y in range(0, WH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WW, y))

    ## Defining the selected line
    try:
        selected_line = lines[selected_line_index]
    except IndexError:
        selected_line_index = 0

    ## Defining the selected ball
    try:
        selected_ball = balls[selected_ball_index]
    except IndexError:
        selected_ball_index = 0

    ## Defining mode
    mode_indicator = font.render("Mode: "+mode, True, (0, 0, 0))     ## Indicating current mode
    screen.blit(mode_indicator, (0, 0))
    try:
        mode = modes[mode_index]            ## Managing modes
    except IndexError:
        mode_index = 0

    ## Drawing lines
    for line in lines:
        line.draw()
        if line == selected_line and mode == 'line':
            line.color = SELECTED_LINE_COLOR
            if clicked and mode == 'line':
                if selected_line_end == 'start':
                    line.start_pos = (mx, my)
                if selected_line_end == 'end':
                    line.end_pos = (mx, my)
        else:
            line.color = LINE_COLOR
    
    ## Drawing balls
    for ball in balls:
        ball.draw()
        if ball == selected_ball and mode == 'bouncing ball':
            ball.color = SELECTED_BALL_COLOR
            if clicked and mode == 'bouncing ball':
                ball.center = (mx, my)
        else:
            ball.color = BALL_COLOR

    ## Drawing flag
    if clicked and mode == 'flag':
        flag.rect.center = (mx, my)
    flag.draw()

    ## Drawing player
    if clicked and mode == 'player':
        player.rect.center = (mx, my)
    player.draw()


    pygame.display.update()

save()

pygame.quit()