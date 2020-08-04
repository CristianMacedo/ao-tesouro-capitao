import pygame
import os
import sys

from Animation import Animation
from Block import Block
from Button import Button
from Character import Character
from Hint import Hint
from Map import Map
from Menu import Menu
from Treasure import Treasure
from Text import Text

''' A classe game e a controladora da maquina de estados do jogo, e a controladora de mais alto nivel.
    1 - Recebe um dicionario de estados, que usa como base para saber qual instancia de 'State' chamar
    2 - A exclusao do jogo pode acontecer em qualquer estado, entao ela também checa se usuario escolheu sair
a partir do atributo 'quit' do estado atual, se ele for verdade (if self.state.quit (== True)) , o estado da instancia de Game é marcado como
terminado (self.done = True) e o jogo termina, abandonando todas sequencias de estados que poderiam estar por vir
    3 - Sempre que um estado e marcado como 'done' (state.done = True), a instancia de game troca o estado
atual pelo proximo estado (que estava referenciado no atributo next_state do evento que acabou de terminar)
    4 - E a unica a conter loop gerenciador de eventos (event_loop), sendo assim, cada evento que acontece,
e enviado como parametro para a funcao checadora de evento (check_event) do estado atual, que dai pode fazer
o handling baseado no valor/tipo do evento
    5 - E a unica a conter um loop game (run), dentro dele, são chamados os metodos de gerenciamento de eventos (event_loop), e 
os metodos genericos do estado atual responsaveis por, desenhar os elementos deste estado (self.state.draw), e atualizar dados do estado que não
seja encatilhado por uma ação do usuario ou dentro do loop de 'draw' (self.state.update)
    
'''
class Game:

    def __init__(self, screen, states):

        self.screen = screen
        self.done = False
        self.fade_offset = 2000
        self.fps = 27
        self.clock = pygame.time.Clock()
        self.bg_channel = pygame.mixer.Channel(1)
        self.effects_channel = pygame.mixer.Channel(2)
        self.sounds_queue = []

        ''' 1. '''
        self.states = states
        self.state = list(self.states.values())[0]()

    def update(self):
        
        ''' 2. '''
        if self.state.quit:
            self.done = True
            ''' 3. '''
        elif self.state.done:
            self.state = self.states[self.state.next_state]()
            if(State.volume == 1):
                self.bg_channel.fadeout(self.fade_offset)
                self.effects_channel.fadeout(self.fade_offset)
                # pygame.time.wait(self.fade_offset)
 
        self.state.update()
    
    ''' 4. '''
    def events_loop(self):
        for event in pygame.event.get():
            self.state.check_event(event)
    
    def sound(self):

        while len(self.state.sound_queue) > 0:
            sound = self.state.sound_queue.pop()
            if sound['type'] == 0:
                self.bg_channel.play(sound['sound'], -1, 0, self.fade_offset)
            elif sound['type'] == 1:
                self.effects_channel.play(sound['sound'])
                # pygame.time.wait(int(sound['sound'].get_length()*1000))

        self.bg_channel.set_volume(State.volume)
        self.effects_channel.set_volume(State.volume)

    def draw(self):
        self.state.draw()
    
    def run(self):

        ''' 5. '''
        while not self.done:
            self.sound()
            self.clock.tick(self.fps)
            self.update()
            self.draw()
            self.events_loop()
            pygame.display.update()


''' 

    Esta e a classe abstrata responsavel por criar o 'template' de qualquer um dos estados que
sejam criados
    * Armazena o status do estado atual em 'done' (True ou False)
    * Armazena o verificador de exclusao do jogo em 'quit' (True ou False)
    * Armazena uma referencia ao proximo estado, pois assim que este for terminado, o proximo
estado a ser executado pela maquina de estados controladora, vai ser o estado que esta armazenado
nesta variavle
    * Todas as instancias ja vao ter a screen usada como padrao no jogo em execucao, pegando sempre de
'pygame.display.get_surface()' para que entao os elementos contidos no mesmo possam ser 'blitados' na
surface em questão
    pass: O python permite que essa funcao seja vazia (abstrata), pois, vai ser implementada (ou nao) de forma
diferente para cada estado
'''
class State:

    volume = 1

    def __init__(self):

        self.done = False
        self.quit = False
        self.next_state = None
        self.sound_queue = []
        self.screen = pygame.display.get_surface()
    
    def check_event(self, event):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def sound(self):
        pass

    def switch_sound(self):
        State.volume = (State.volume + 1)%2

''' 
    Estado da tela inicial, herda de 'State'
    * Contem todos os elementos presentes na tela inicial, seu construtor instancia todos eles,
armazena-os no atributo de elementos (elements), e a funcao draw, chama a funcao draw para cada
respectivo elemento

'''

class StartScreen(State):
    
    def __init__(self):

        super().__init__()

        self.w, self.h = self.screen.get_size()
        self.sound_queue.append(sounds['menu'])

        bg = Animation(frames_path['play-background'], (0, 0), self.screen)

        tree1 = Animation(frames_path['tree'], (150, self.h/2), self.screen)
        tree1.reduce_scale(4)
        tree1.centralize()
        tree1.flip()

        tree2 = Animation(frames_path['tree'], (self.w-150, self.h/2), self.screen)
        tree2.reduce_scale(4)
        tree2.centralize()

        title = Animation(frames_path['title'], (self.w/2,200), self.screen)
        title.reduce_scale(3)
        title.centralize()

        self.ship = Animation(frames_path['ship'], ((self.w/16)*2, 200), self.screen)
        self.ship.reduce_scale(4)
        self.ship.centralize()
        self.ship_speed = -1
        
        self.next_state 
        self.menu = Menu(self.screen)

        ''' 
            O botao criado no menu inicial recebe como parametro o nome do proximo estado que sera executado
            assim que este aqui acabar
        '''
        
        self.menu.add_button('start', frames_path['start-button'], (self.w/2, self.h/2), 'SELECTCHAR')
        self.menu.buttons['start'].reduce_scale(1.5)
        self.menu.buttons['start'].centralize()

        self.menu.add_button('htp', frames_path['htp-button'], (self.w/2, self.h/2 + 100), 'HOWTOPLAY')
        self.menu.buttons['htp'].reduce_scale(1.5)
        self.menu.buttons['htp'].centralize()


        self.menu.add_button('sound', frames_path['sound'],(int((self.w/16)*15), int((self.h/10)*1)),self.switch_sound)
        self.menu.buttons['sound'].reduce_scale(5)
        self.menu.buttons['sound'].centralize()

        self.elements = [bg, self.ship, self.menu, tree1, tree2, title]

    def check_event(self, event):

        if event.type == pygame.QUIT:
            self.quit = True
            ''' 
                Assim que o mouse for clicado o handler de evento deste estado chama a funcao do menu que verifica
                se este click ocorreu em algum dos botoes presentes no menu
            '''
        elif event.type == pygame.MOUSEBUTTONUP:
            if(self.menu.check_click(pygame.mouse.get_pos())):

                ''' Colocar o som de selecao de botão aqui '''
                self.sound_queue.append(sounds['button-switch'])

                if(callable(self.menu.last_clicked_state)):
                    self.menu.last_clicked_state()
                    self.menu.last_clicked_state = None
                    return

                ''' 
                    Se algum botao foi clicado e conter um estado como callback, o status desse evento e marcado como 'done' (self.done = True) e o
                    ponteiro para o proximo estado vira o valor que havia sido armazenado como next_state, do botão
                    em questão
                '''

                self.next_state = self.menu.last_clicked_state
                self.done = True

    def switch_sound(self):
        super().switch_sound()
        if (State.volume == 0):
            self.menu.buttons['sound'].switch_state('off')
        elif(State.volume == 1):
            self.menu.buttons['sound'].switch_state('on')

    def draw(self):
        for element in self.elements:
            element.draw()

    def update(self):
        
        self.ship.update_pos((self.ship.rect.x + self.ship_speed, self.ship.rect.y))
        if(self.ship.rect.x == 0 or self.ship.rect.x == self.w):
            self.ship_speed *= -1
            print('ship speed is now ' + str(self.ship_speed))
            self.ship.rect.x + self.ship_speed * 1000
            self.ship.flip()

class HowToPlay(State):

    def __init__(self):

        super().__init__()
        self.w, self.h = self.screen.get_size()
        self.next_state = "STARTMENU"

        self.sound_queue.append(sounds['menu'])

        bg = Animation(frames_path['play-background'], (0, 0), self.screen)
        image = Animation(frames_path['how-to-play'], (0, 0), self.screen)

        self.elements = [bg, image]

    def draw(self):
        for element in self.elements:
            element.draw()

    def check_event(self, event):

        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
            self.sound_queue.append(sounds['button-switch'])
            self.done = True

class SelectChar(State):

    def __init__(self):

        super().__init__()
        self.w, self.h = self.screen.get_size()

        bg = Animation(frames_path['play-background'], (0, 0), self.screen)
        text = Text(self.screen, (int(self.w/2), 100), 'Escolha seu Pirata, marujo!', True, (255,255,255), 50)

        self.menu = Menu(self.screen)
        self.menu.add_button('boy-pirate', frames_path['boy-pirate'],((self.w/4), (self.h/2)),self.selectBoy)
        self.menu.buttons['boy-pirate'].reduce_scale(3)
        self.menu.buttons['boy-pirate'].centralize()

        self.menu.add_button('girl-pirate', frames_path['girl-pirate'],((self.w/4)*3, (self.h/2)),self.selectBoy)
        self.menu.buttons['girl-pirate'].reduce_scale(3)
        self.menu.buttons['girl-pirate'].centralize()

        self.elements = [bg, self.menu, text]

    def selectBoy(self):

        Gameplay.char_sex = 1
        self.next_state = 'GAMEPLAY'
        self.done = True

    def selectGirl(self):

        Gameplay.char_sex = 0
        self.next_state = 'GAMEPLAY'
        self.done = True

    def check_event(self, event):

        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.MOUSEBUTTONUP:
            if(self.menu.check_click(pygame.mouse.get_pos())):
                self.sound_queue.append(sounds['button-switch'])
                if(callable(self.menu.last_clicked_state)):
                    self.menu.last_clicked_state()
                    self.menu.last_clicked_state = None
                    return

    def draw(self):
        for element in self.elements:
            element.draw()


class Gameplay(State):

    char_sex = 1

    def __init__(self):

        super().__init__()
        self.w, self.h = self.screen.get_size()
        
        self.sound_queue.append(sounds['stage'])

        self.menu = Menu(self.screen)
        self.menu.add_button('sound', frames_path['sound'],(int((self.w/16)*15), int((self.h/10)*1)),self.switch_sound)
        self.menu.buttons['sound'].reduce_scale(5)
        self.menu.buttons['sound'].centralize()

        self.msgs = {
            'lose': Text(self.screen, (int(self.w/2), 200), 'Oh não, os piratas chegaram na ilha, melhor zarparmos e tentarmos denovo outro dia!', True, (255,255,255))
        }

        ''' Sessões de Jogo '''
        self.played_sections = 0
        self.wins = 0
        self.stage_done = False
        self.stage_begin = True

        ''' Mapa '''
        self.block_index = 0
        self.stage_map = Map(3, self.screen, self.w, self.h)
        
        ''' Escavações '''
        self.last_dig = None
        self.curr_dig = None
        self.show_item = False

        ''' Personagem '''
        self.char = Character(self.screen, Gameplay.char_sex, self.stage_map.blocks[self.block_index])
        self.char.reduce_scale(4)
        self.char.centralize()

        ''' Cena '''
        self.ship = Animation(frames_path['ship'], ((self.w/16)*14, 200), self.screen)
        self.ship.reduce_scale(4)
        self.ship.centralize()
        self.bg = Animation(frames_path['play-background'], (0, 0), self.screen)
        self.elements = [self.bg, self.stage_map, self.ship, self.char]

    def update(self):

        if(self.curr_dig != None):
            if(isinstance(self.curr_dig, Treasure)):
                self.sound_queue.append(sounds['win'])
                self.stage_done = True
                self.wins += 1
            
            if(isinstance(self.curr_dig, Hint)):
                self.sound_queue.append(sounds['hint'])

            self.last_dig = self.curr_dig
            self.curr_dig = None
            self.show_item = True
        
        elif(self.char.chances <= 0):
            self.stage_done = True
            self.last_dig = self.msgs['lose']         

        if(self.played_sections == 3):
            self.done = True
            '''fim de jogo, ir para tela de resultados(?)'''

    def check_event(self, event):

        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if(self.menu.check_click(pygame.mouse.get_pos())):

                self.sound_queue.append(sounds['button-switch'])

                if(callable(self.menu.last_clicked_state)):
                    self.menu.last_clicked_state()
                    self.menu.last_clicked_state = None

        if event.type == pygame.KEYDOWN:

            if(self.stage_begin):
                self.stage_begin = False
                return

            if(self.stage_done):
                self.next_stage()
                return

            if self.show_item:
                self.show_item = False
                return

            if event.key == pygame.K_RIGHT:
                self.sound_queue.append(sounds['stepping-sand'])
                if (not self.block_index + 1 >= len(self.stage_map.blocks)):
                    if(self.char.dir == 0):
                        self.char.flip()
                    self.block_index += 1
                    self.char.update_block(self.stage_map.blocks[self.block_index])
                    self.char.centralize()

            elif event.key == pygame.K_LEFT:
                self.sound_queue.append(sounds['stepping-sand'])
                if (not self.block_index - 1 < 0):
                    if(self.char.dir == 1):
                        self.char.flip()
                    self.block_index -= 1
                    self.char.update_block(self.stage_map.blocks[self.block_index])
                    self.char.centralize()

            elif event.key == pygame.K_DOWN:
                self.sound_queue.append(sounds['stepping-sand'])
                if (not self.block_index + self.stage_map.col >= len(self.stage_map.blocks)):
                    self.block_index += self.stage_map.col
                    self.char.update_block(self.stage_map.blocks[self.block_index])
                    self.char.centralize()

            elif event.key == pygame.K_UP:
                self.sound_queue.append(sounds['stepping-sand'])
                if (not self.block_index - self.stage_map.col < 0):
                    self.block_index -= self.stage_map.col
                    self.char.update_block(self.stage_map.blocks[self.block_index])
                    self.char.centralize()

            elif event.key == pygame.K_SPACE:
                self.sound_queue.append(sounds['digging'])
                self.move_ship()
                self.char.chances -= 1
                self.curr_dig = self.char.dig()

    def draw(self):

        for element in self.elements:
            element.draw()

        if(self.stage_begin):
            self.stage_map.first_hint.draw()

        elif(self.show_item): 
            self.last_dig.draw()
        
        self.menu.draw()

    def move_ship(self):

        self.ship.update_pos((self.ship.rect.x - 200, 200))
        self.ship.reduce_scale(0.9)
        self.ship.centralize()
        
    def next_stage(self):

        self.ship = Animation(frames_path['ship'], ((self.w/16)*14, 200), self.screen)
        self.ship.reduce_scale(4)
        self.ship.centralize()

        self.sound_queue.append(sounds['stage'])

        self.played_sections += 1

        self.last_dig = None
        self.curr_dig = None
        self.show_item = False

        self.stage_done = False
        self.treasure_found = False
        
        self.stage_begin = True

        self.block_index = 0

        self.stage_map = Map(3 + self.played_sections, self.screen, self.w, self.h)

        self.char = Character(self.screen, Gameplay.char_sex, self.stage_map.blocks[self.block_index])
        self.char.reduce_scale(4)
        self.char.centralize()

        self.elements = [self.bg, self.stage_map, self.ship, self.char]

    def switch_sound(self):
        super().switch_sound()
        if (State.volume == 0):
            self.menu.buttons['sound'].switch_state('off')
        elif(State.volume == 1):
            self.menu.buttons['sound'].switch_state('on')  
    
pygame.init()
screen = pygame.display.set_mode((1280, 720))

''' Dicionario de caminhos das imagens usadas no jogo '''
frames_path = {
    'boy-pirate': ["img/pirate_frame1.png", "img/pirate_frame2.png"],
    'girl-pirate': ["img/girlpirate_frame1.png", "img/girlpirate_frame2.png"],
    'ship': ["img/ship_frame1.png", "img/ship_frame2.png"],
    'how-to-play': ["img/how_to_play.png"],
    'htp-button': ["img/button_htp_frame_1.png", "img/button_htp_frame_2.png"],
    'start-button': ["img/button_frame_1.png", "img/button_frame_2.png"],
    'background': ["img/start_background_frame_1.jpg", "img/start_background_frame_2.jpg"],
    'play-background' : ["img/play_bg_frame1.jpg","img/play_bg_frame2.jpg","img/play_bg_frame3.jpg","img/play_bg_frame4.jpg","img/play_bg_frame5.jpg","img/play_bg_frame6.jpg"],
    'tree': ["img/tree_frame_1.png", "img/tree_frame_2.png"],
    'title': ["img/title_frame_1.png"],
    'sound': {'on': ["img/sound_on.png"],
             'off': ["img/sound_off.png"]
    }
}


sounds = {
    'ambiance': {
        'type': 0,
        'sound': pygame.mixer.Sound("audio/ambiance.ogg")
        },
    'win': {
        'type': 0,
        'sound': pygame.mixer.Sound("audio/win.ogg")
        },
    'stage': {
        'type': 0,
        'sound': pygame.mixer.Sound("audio/stage.ogg")
        },
    'menu': {
        'type': 0,
        'sound': pygame.mixer.Sound("audio/menu.ogg")
        },
    'button-switch': {
        'type': 1,
        'sound': pygame.mixer.Sound("audio/button-switch.ogg")
        },
    'digging': {
        'type': 1,
        'sound': pygame.mixer.Sound("audio/digging-cut.ogg")
        },
    'hint': {
        'type': 1,
        'sound': pygame.mixer.Sound("audio/hint.ogg")
        },
    'stepping-sand': {
        'type': 1,
        'sound': pygame.mixer.Sound("audio/stepping-sand-cut.ogg")
        }
}

states = {"STARTMENU": StartScreen,
            # "SWITCHSOUND": SwitchSound(),
            "SELECTCHAR": SelectChar,
            "HOWTOPLAY": HowToPlay,
            "GAMEPLAY": Gameplay}

game = Game(screen, states)
game.run()
pygame.quit()
sys.quit()
