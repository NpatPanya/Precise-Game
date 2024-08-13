# IMPORTS
import pygame, os, math, random, time, sys


# DISPLAY_SETUP
pygame.init()
WIDTH = 800
HEIGHT = 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Precise")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
bgpic = pygame.image.load("iconBg.png")


# IMAGES & CURSOR
icon_ingame = pygame.transform.scale(bgpic,(400, 400))
cursor = pygame.transform.scale(pygame.image.load("Crosshair.png"), (100, 100)).convert_alpha()


# FONTS
font_point = pygame.font.SysFont("Gill sans", 30)
font_menu = pygame.font.SysFont("Gill sans", 50)
font_final = pygame.font.SysFont("Gill sans", 50)
font_time = pygame.font.SysFont("Gill sans", 100)
font_title = pygame.font.SysFont("Gill sans", 70)


# COLOURS
Grey = (169,169,169)
Black = (0,0,0)
red = (255,0,0)


# VARIABLES
Outer_circle = 25
Mid_Circle = 15
Center_Circle = 3
crosshair = cursor


# AXIS_FOR_RANDOM_TARGET
def Random():
    global x, y

    x = random.randint(0 + Outer_circle, WIDTH - Outer_circle)
    y = random.randint(0 + Outer_circle, HEIGHT - Outer_circle)


# MENU SYSTEM
def menu():
    menu = True
    display.fill(Grey)
    clock.tick()

    # INGAME_ICON_PIC
    display.blit(icon_ingame, (WIDTH - 400,  HEIGHT - 400))

    # TITLE
    titleText = font_title.render("Precise", 1, Black)
    display.blit(titleText, (int(WIDTH / 2 - titleText.get_width() /2), 10))

    # MENU_OPTION
    playText = font_menu.render("Play", 1, Black)
    playText_x = WIDTH / 5.25 - playText.get_width() / 1
    playText_y = 200
    display.blit(playText, (int(playText_x), int(playText_y)))

    # FPS_OPTION
    RefreshText = font_menu.render("Refreshrate", 1, Black)
    RefreshText_x = WIDTH / 2.6 - RefreshText.get_width() / 1
    RefreshText_y = 300
    display.blit(RefreshText, (int(RefreshText_x), int(RefreshText_y)))

    # QUIT_OPTION
    quitText = font_menu.render("Quit", 1, Black)
    quitText_x = WIDTH / 4.9 - quitText.get_width() / 1
    quitText_y = 450
    display.blit(quitText, (int(quitText_x), int(quitText_y)))
    pygame.display.update()

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                print(m_x, m_y)

                if m_x >= playText_x and m_x <= playText_x + playText.get_width() and m_y >= playText_y and m_y <= playText_y + playText.get_height():
                    Random()
                    start()
                    #menu = False

                elif m_x >= RefreshText_x and m_x <= RefreshText_x + RefreshText.get_width() and m_y >= RefreshText_y and m_y <= RefreshText_y + RefreshText.get_height():
                    settings()

                elif m_x >= quitText_x and m_x <= quitText_x + quitText.get_width() and m_y >= quitText_y and m_y <= quitText_y + quitText.get_height():
                    pygame.quit()
                    quit()


def start():
    global p
    p = 1
    start = True
    startTime = time.time()
    while start:
        TimecountBefore_Start = 3
        endTime = time.time()
        seconds = (endTime - startTime)
        secondsLeft = round(TimecountBefore_Start - seconds)
        display.fill(Grey)
        timetext = font_time.render(str(secondsLeft), 1, Black)
        display.blit(timetext, (int(WIDTH / 2 - timetext.get_width() / 2), int(HEIGHT / 2 - timetext.get_height() / 2)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if secondsLeft == 0:
            if p == 1:
                game()

        clock.tick(RefreshRate)


#GAME
def game():
    global Points
    run = True
    Points = 0
    pygame.mouse.set_visible(False)
    startTime = time.time()

    while run:
        clock.tick(RefreshRate)
        display.fill(Grey)


        # TARGET
        pygame.draw.circle(display, red, (x, y), Outer_circle, 3)
        pygame.draw.circle(display, red, (x, y), Mid_Circle, 3)
        pygame.draw.circle(display, red, (x, y), Center_Circle, 3)


        # CROSSHAIR
        mousePos_x, mousePos_y = pygame.mouse.get_pos()
        display.blit(crosshair, (mousePos_x - crosshair.get_width() / 2, mousePos_y - crosshair.get_height() / 2))


        # POINT_COUNTER
        pointtext = font_point.render("Point: " + str(Points), 1, Black)
        display.blit(pointtext, (10, 10))
        

        # TIME_COUNTER_IN_GAME
        global TimeC
        TimeC = 30
        endTime = time.time()
        seconds = (endTime - startTime)
        secondsLeft = TimeC - seconds

        
        if secondsLeft >= 10:
            secondsLeft = round(secondsLeft)

        else:
            secondsLeft = round(secondsLeft, 2)

        timeText = font_point.render("Time: " + str(secondsLeft), 1, Black)
        display.blit(timeText, (WIDTH - 10 - timeText.get_width(), 10))

        if round(secondsLeft) == 0:
            endMenu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                pygame.quit()

            # RETURN_TO_MENU
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        endMenu()

            # POINT_COUNTER_WHEN_HIT_TARGET
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                print(dis)

                if  Outer_circle > dis > Mid_Circle:
                    Points = Points + 1
                    print(Points)
                    Random()

                elif Mid_Circle > dis > Center_Circle:
                    Points = Points + 5
                    print(Points)
                    Random()

                elif dis < Center_Circle:
                    Points = Points + 10
                    print(Points)
                    Random()

                elif dis > Outer_circle:
                    Points = Points - 1


#ตัวเลือกหลังเกมจบ และ โชว์คะแนน
def endMenu():
    end = True
    display.fill(Grey)
    pygame.mouse.set_visible(True)
    
    # TIME_SYNCRONISE_FOR_SHOWPOINTS
    startTime = time.time()
    endTime = time.time()
    seconds = (endTime - startTime)
    secondsLeft = TimeC - seconds


    # SHOW_SCORE_AND_MENU_AFTER_PLAYED
    if p == 1:
        puntText2 = font_final.render("Point: " + str(Points), 1, Black)
        display.blit(puntText2, (int(WIDTH / 2 - puntText2.get_width() / 2), 100))

    playagainText = font_menu.render("Play again", 1, Black)
    playagainText_x = WIDTH / 2 - playagainText.get_width() / 2
    playagainText_y = 250
    display.blit(playagainText, (int(playagainText_x), int(playagainText_y)))

    mainmenuText = font_menu.render("Menu", 1, Black)
    mainmenuText_x = WIDTH / 2 - mainmenuText.get_width() / 2
    mainmenuText_y = 350
    display.blit(mainmenuText, (int(mainmenuText_x), int(mainmenuText_y)))

    quitText = font_menu.render("Quit", 1, Black)
    quitText_x = WIDTH / 2 - quitText.get_width() / 2
    quitText_y = 450
    display.blit(quitText, (int(quitText_x), int(quitText_y)))

    pygame.display.update()
    m_x,m_y = pygame.mouse.get_pos()

    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()

                if m_x >= playagainText_x and m_x <= playagainText_x + playagainText.get_width() and m_y >= playagainText_y and m_y <= playagainText_y + playagainText.get_height():
                    game()

                elif m_x >= mainmenuText_x and m_x <= mainmenuText_x + mainmenuText.get_width() and m_y >= mainmenuText_y and m_y <= mainmenuText_y + mainmenuText.get_height():
                    menu()

                elif m_x >= quitText_x and m_x <= quitText_x + quitText.get_width() and m_y >= quitText_y and m_y <= quitText_y + quitText.get_height():
                    pygame.quit()
                    quit()



# FPS_SETTINGS
def settings():
    display.fill(Grey)
    m_x,m_y = pygame.mouse.get_pos()

    FPS_60 = font_menu.render("60 FPS", 1, Black)
    FPS_60_x = WIDTH / 2 - FPS_60.get_width() / 2
    FPS_60_y = 250
    display.blit(FPS_60, (int(FPS_60_x), int(FPS_60_y)))

    FPS_144 = font_menu.render("144 FPS", 1,  Black)
    FPS_144_x = WIDTH / 2 - FPS_144.get_width() / 2
    FPS_144_y = 350
    display.blit(FPS_144, (int(FPS_144_x), int(FPS_144_y)))

    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()

                if m_x >= FPS_60_x and m_x <= FPS_60_x + FPS_60.get_width() and m_y >= FPS_60_y and m_y <= FPS_60_y + FPS_60.get_height():
                    fps(60)
                    menu()
                elif m_x >= FPS_144_x and m_x <= FPS_144_x + FPS_144.get_width() and m_y >= FPS_144_y and m_y <= FPS_144_y + FPS_144.get_height():
                    fps(144)
                    menu()
        
        pygame.display.update()


# SET_GAME_FPS
clock = pygame.time.Clock()

# T0_CHANGE_FRAMERATE
def fps(framerate):
    global RefreshRate
    RefreshRate = framerate
    return RefreshRate

RefreshRate = 60



menu()

pygame.quit()