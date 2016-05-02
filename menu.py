import pygame
from pygame import*
import subprocess
import Project

class Buttom():
    def __init__(self):
        self.color = (70, 250, 50)
        self.size = 15
        self.x, self.y = 360, 120

    def update(self, menu):
        #show choice
        #1 buttom (385,85), (700,150)
        if menu.m_pos[0] > 385 and menu.m_pos[1] > 85\
           and menu.m_pos[0] < 700 and menu.m_pos[1] < 150:
            self.x, self.y = 360, 120
        #2 buttom (385,170),(700,230)
        if menu.m_pos[0] > 385 and menu.m_pos[1] > 170\
           and menu.m_pos[0] < 700 and menu.m_pos[1] < 230:
            self.x, self.y = 360, 205
        #3 buttom (385,260),(700,320)
        if menu.m_pos[0] > 385 and menu.m_pos[1] > 260\
           and menu.m_pos[0] < 700 and menu.m_pos[1] < 320:
            self.x, self.y = 360, 290
        #4 buttom (385,345),(700,400)
        if menu.m_pos[0] > 385 and menu.m_pos[1] > 345\
           and menu.m_pos[0] < 700 and menu.m_pos[1] < 400:
            self.x, self.y = 360, 380
        #back buttom
            

        self.pos = self.x, self.y

        #when press buttom
        if menu.m_pressed == (1, 0, 0):
            if self.y == 120: menu.image = menu.develop
            if self.y == 205:
                game = Project.Game()
                game.execute()
            if self.y == 290: menu.image = menu.develop
            if self.y == 380: menu.exit()
            #back buttom
            if menu.m_pos[0] > 20 and menu.m_pos[1] > 20\
               and menu.m_pos[0] < 160 and menu.m_pos[1] < 80:
                menu.image = menu.main_menu
        
    def render(self, menu):
        draw.circle(menu.screen, self.color, self.pos, self.size)
        
    
class Menu:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 60 fps"""
        self.delta = self.clock.tick(60) / 1000.0

    def __init__(self):
        """Constructor of the Game"""
        self._running = True
        self.size = self.width, self.height = 1040, 500
        # create main display - 1040x500 window
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('Menu')
        # get object to help track time
        self.clock = pygame.time.Clock()
        # set default tool
        self.tool = 'run'
        self.buttom = Buttom()

        self.main_menu = pygame.image.load("./images/menu/main_menu.gif").convert()
        self.pause = pygame.image.load("./images/menu/pause.gif").convert()
        self.develop = pygame.image.load("./images/menu/develop.gif").convert()
        self.image = self.main_menu
        
    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        self.pressed = pygame.key.get_pressed()
        self.m_pressed = pygame.mouse.get_pressed()
        self.m_pos = mouse.get_pos()
        self.buttom.update(self)            

    def render(self):
        """Render the scene"""
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.image, (1,1))
        self.buttom.render(self)
        pygame.display.flip()

    def exit(self):
        """Exit the game"""
        self._running = False        

    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                self.event_handler(event)
            self.move()
            self.render()
        pygame.quit()

if __name__ == "__main__":
    menu = Menu()
    menu.execute()
