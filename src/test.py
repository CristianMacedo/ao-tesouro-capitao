import pygame
from pygame.locals import *
from sys import exit

from Menu import Menu
from Animation import Animation
from Hint import Hint
from Map import Map
from Character import Character
from Treasure import Treasure

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
w, h = pygame.display.get_surface().get_size()

clock = pygame.time.Clock()


def print_click(label):
    print('the button "{}" has been clicked'.format(label))

# def start_screen():

print('game iniciado')

def start_screen():

    menu = Menu(SCREEN)
    menu.add_button('iniciar 1', ['img/button_frame_1.png', 'img/button_frame_2.png'], play)
    #menu.add_button('iniciar 2', ['img/button_frame_1.png', 'img/button_frame_2.png'], print_click)

    bg = Animation(["img/start_background_frame_1.jpg", "img/start_background_frame_2.jpg"], (0, 0), SCREEN)
    bg.set_fps(15)

    tree1 = Animation(["img/tree_frame_1.png", "img/tree_frame_2.png"], (150, h/2), SCREEN)
    tree1.reduce_scale(4)
    tree1.centralize()
    tree1.flip()

    tree2 = Animation(["img/tree_frame_1.png", "img/tree_frame_2.png"], (w-150, h/2), SCREEN)
    tree2.reduce_scale(4)
    tree2.centralize()

    title = Animation(["img/title_frame_1.png"], (w/2,200), SCREEN)
    title.reduce_scale(3)
    title.centralize()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONUP:
                menu.check_click(pygame.mouse.get_pos())

        bg.draw()
        tree1.draw()
        tree2.draw()
        title.draw()
        menu.draw()
        pygame.display.update()

        clock.tick(27)

def play(label):

    # print('button {}'.format(label))

    bg = Animation(["img/start_background_frame_1.jpg", "img/start_background_frame_2.jpg"], (0, 0), SCREEN)
    bg.set_fps(15)

    # title = Animation(["img/title_frame_1.png"], (w/2,200), SCREEN)
    # title.reduce_scale(3)
    # title.centralize()

    mapa = Map(4, SCREEN, w, h)
    block_index = 0
    last_dig = False
    char = Character(SCREEN, 1, mapa.blocks[block_index])
    char.reduce_scale(4)
    char.centralize()
    print(char.image)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if last_dig != False:
                    print('changing dig to false')
                    last_dig = False
                if event.key == K_RIGHT:
                    if (not block_index + 1 >= len(mapa.blocks)):
                        if(char.dir == 0):
                            char.dir = 1
                            char.flip()
                        block_index += 1
                        char.update_block(mapa.blocks[block_index])
                        char.centralize()
                if event.key == K_LEFT:
                    if (not block_index - 1 < 0):
                        if(char.dir == 1):
                            char.dir = 0
                            char.flip()
                        block_index -= 1
                        char.update_block(mapa.blocks[block_index])
                        char.centralize()
                if event.key == K_DOWN:
                    if (not block_index + mapa.col >= len(mapa.blocks)):
                        block_index += mapa.col
                        char.update_block(mapa.blocks[block_index])
                        char.centralize()
                if event.key == K_UP:
                    if (not block_index - mapa.col < 0):
                        block_index -= mapa.col
                        char.update_block(mapa.blocks[block_index])
                        char.centralize()
                if event.key == K_SPACE:
                    print('digging')
                    last_dig = char.dig()



        bg.draw()
        mapa.draw()
        char.draw()

        if(last_dig != False):

            if(isinstance(last_dig, Treasure)):

                print('treasure found')
                last_dig.draw()

            if(isinstance(last_dig, Hint)):

                print('hint found')
                last_dig.draw()

            if(last_dig == None):

                print('Empty block')
        
        # title.draw()
        # hint.draw()
        pygame.display.update()


    clock.tick(27)

start_screen()
