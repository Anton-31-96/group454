#New project_python
#game: Fighting multiplayer
#мультиплеер. Будет возможность перехода по уровням
#Возможность взаимодействия с выпадающими предметами (оружие)
#Различные умения/характеристики персонажа
#В идеале наличие искусственного интеллекта

import pygame
from pygame import*

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        """ Constructor of Platform class """
        sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.color, self.height, self.width = (120,126,135), 10, 40
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)

    def render(self, game):
        """ Draw Platfotm on Game window """
        draw.rect(game.screen,self.color,(int(self.x),int(self.y),int(self.width),int(self.height)))



class Player(sprite.Sprite):
    def __init__(self, number,x = 100, y = 100, vy = 0, vx = 0):
        """ Constructor of Player class """
        sprite.Sprite.__init__(self)
        self.number, self.x, self.y, self.vy, self.vx = \
                number, x, y, vy, vx
        self.image1 = pygame.image.load("./images/player/man_r.gif").convert()
        self.image2 = pygame.image.load("./images/player/hit_r.gif").convert()
        self.image3 = pygame.image.load("./images/player/man_r_j.gif").convert()
        self.On_ground = False
        self.width, self.height = 100, 100
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)

    """ Обработка столкновений с платформой """
    def collide(self, game, vx, vy):
        for p in game.platforms:            
            if sprite.collide_rect(self, p):
                # Спуск с платформы
                if self.number == 1 and game.pressed[K_DOWN]\
                   or self.number == 2 and game.pressed[K_s]:
                    #and (self.y < game.height - self.height):
                    self.On_ground = False
                    # Прыжок на платформу"""
                elif vy > 0 and (self.y < p.y - self.height + 30):
                    self.y = p.y - self.height + 1
                    self.On_ground = True
                    vy = 0
                    
            else: self.On_ground = False

    def update(self, game):
        """ Update Player state """
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)
        self.vx = 0

        """ Deferent keys for first and secont player """
        if self.number == 1:
            if game.pressed[K_LEFT]:
                self.vx -= 10
            if game.pressed[K_RIGHT]:
                self.vx += 10
            if game.pressed[K_UP]:
                if self.On_ground == True:
                    self.vy -= 800
                    self.On_ground = False
                    
        elif self.number == 2:
            if game.pressed[K_a]:
                self.vx -= 10
            if game.pressed[K_d]:
                self.vx += 10
            if game.pressed[K_w]:
                if self.On_ground == True:
                    self.vy -= 800
                    self.On_ground = False

        """ Player's move """

        self.x +=self.vx
        self.collide(game, self.vx, 0)

        if self.On_ground == False:
            self.vy += game.delta * 1500 
            self.y += self.vy * game.delta
            self.collide(game, 0, self.vy)

        """ Do not let Player get out of the Game window """
        
        if self.x < 0:
            self.x = 0
        if self.y <= 0:
            self.y = 0
        if self.x > game.width - self.width:
            self.x = game.width - self.width
        if self.y >= game.height - self.height:
            self.y = game.height - self.height
            self.On_ground = True
            
        if self.On_ground == True:
            self.vy = 0

    def render(self, game):
        """ Draw Player on the Game window """
        self.image = self.image3
        if self.On_ground == True:
            self.image = self.image1
        if self.number == 1 and\
           game.pressed[K_RSHIFT]:
            self.image = self.image2
        if self.number == 2 and \
             game.pressed[K_SPACE]:
                self.image = self.image2
        game.screen.blit(self.image, (int(self.x),int(self.y)))
        #game.entities.draw(game.screen)

    def save_motion(self):
        """ Сохранение параметров положения игрока """
        self.sy, self.svy = self.y, self.vy

    def load_motion(self):
        """ Загрузка параметров положения игрока """
        self.y, self.vy = self.sy, self.svy



class Menu:
    def __init__(self, game):
        """ Constructor of Menu class """
        self.main_image = pygame.image.load("./images/menu/main_menu.gif").convert()
        self.develop = pygame.image.load("./images/menu/develop.gif").convert()
        self.pause = pygame.image.load("./images/menu/pause.gif").convert()
        
        self.color = (70, 250, 50)
        self.size = 15
        self.x, self.y = 360, 120

        if game.tool == 'start':
            self.image = self.main_image
        else:
            self.image = self.pause

    def update(self, game):
        if self.image != self.develop:
            if game.tool == 'start':
                self.image = self.main_image
            elif game.tool == 'pause':
                self.image = self.pause
            
        # show choice
        # 1 buttom (385,85), (700,150)
        if game.m_pos[0] > 385 and game.m_pos[1] > 85\
           and game.m_pos[0] < 700 and game.m_pos[1] < 150:
            self.x, self.y = 360, 120
        # 2 buttom (385,170),(700,230)
        if game.m_pos[0] > 385 and game.m_pos[1] > 170\
           and game.m_pos[0] < 700 and game.m_pos[1] < 230:
            self.x, self.y = 360, 205
        # 3 buttom (385,260),(700,320)
        if game.m_pos[0] > 385 and game.m_pos[1] > 260\
           and game.m_pos[0] < 700 and game.m_pos[1] < 320:
            self.x, self.y = 360, 290
        # 4 buttom (385,345),(700,400)
        if game.m_pos[0] > 385 and game.m_pos[1] > 345\
           and game.m_pos[0] < 700 and game.m_pos[1] < 400:
            self.x, self.y = 360, 380
        self.pos = self.x, self.y
    
    def button_press(self, game):
        """when press buttom"""
        if game.m_pressed == (1, 0, 0):
            if game.tool == 'start':
                if self.y == 120: self.image = self.develop
                if self.y == 205: game.tool = 'main'
                if self.y == 290: self.image = self.develop
                if self.y == 380: game.exit()
                # back buttom
                if game.m_pos[0] > 20 and game.m_pos[1] > 20\
                   and game.m_pos[0] < 160 and game.m_pos[1] < 80:
                    self.image = self.main_image
            if game.tool == 'pause':
                if self.y == 120: game.tool = 'main'
                if self.y == 205: game.tool = 'main'
                if self.y == 290: self.image = self.develop
                if self.y == 380: game.exit()
                # back buttom
                if game.m_pos[0] > 20 and game.m_pos[1] > 20\
                   and game.m_pos[0] < 160 and game.m_pos[1] < 80:
                    self.image = self.pause

    def button_render(self, game):
        draw.circle(game.screen, self.color, self.pos, self.size)


 
class Game:
    def tick(self):
        """ Return time in seconds since previous call
        and limit speed of the game to 60 fps """
        self.delta = self.clock.tick(60) / 1000.0

    def __init__(self):
        """ Constructor of the Game """
        self._running = True
        # create main display - 1040x400 window
        self.size = self.width, self.height = 1040, 500
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('Fight game')
        # get object to help track time
        self.clock = pygame.time.Clock()
        self.tool = 'start'

        self.menu = Menu(self)
        self.platform = Platform(x = 300, y = 300)
        self.entities = pygame.sprite.Group() # Все объекты
        self.platforms = [] # то, во что мы будем врезаться или опираться
        self.players = pygame.sprite.Group() # игроки
        self.player2 = Player(2, x = 600)
        self.player = Player(1)
        self.players.add(self.player, self.player2)
        self.entities.add(self.player, self.platform)
        self.platforms.append(self.platform)

        
    def event_handler(self, event):
        """ Handling one pygame event """
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        elif event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                if self.tool == 'main':
                    self.tool = 'pause'
                elif self.tool == 'pause':
                    self.tool = 'main'

    def move(self):
        """ Here game objects update their positions """
        self.pressed = pygame.key.get_pressed()
        self.m_pressed = pygame.mouse.get_pressed()
        self.m_pos = mouse.get_pos()
        
        if self.tool == 'main':
            self.tick()
            self.player.update(self)
            self.player2.update(self)
        else:
            self.menu.update(self)
            self.menu.button_press(self)
            

    def render(self):
        """ Render the scene """
        self.screen.fill((255, 255, 255))
        if self.tool == 'main':
            self.player.render(self)
            self.player2.render(self)
            self.platform.render(self)
        else:
            self.screen.blit(self.menu.image, (1,1))
            if self.menu.image != self.menu.develop:
                self.menu.button_render(self)
        pygame.display.flip()

    def exit(self):
        """ Exit the game """
        self._running = False

    def execute(self):
        """ Execution loop of the game """
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                self.event_handler(event)
            self.move()
            self.render()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.execute()
