#New project_python
#game: Fighting multiplayer
#мультиплеер. Будет возможность перехода по уровням
#Возможность взаимодействия с выпадающими предметами (оружие)
#Различные умения/характеристики персонажа
#В идеале наличие искусственного интеллекта

import pygame
from pygame import*

""" We will use these colours """
red = (200,10,10)
gray = (120,126,135)
green = (10,200,10)

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        """ Constructor of Platform class """
        sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.color, self.height, self.width = gray, 10, 40
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)

    def render(self, game):
        """ Draw Platfotm on Game window """
        draw.rect(game.screen,self.color,(int(self.x),int(self.y),int(self.width),int(self.height)))



class Player(sprite.Sprite):
    def __init__(self, game, x = 100, y = 100, vy = 0, vx = 0):
        """ Constructor of Player class """
        sprite.Sprite.__init__(self)
        self.x, self.y, self.vy, self.vx = \
                x, y, vy, vx
        self.HP, self.power = 400, 20
        self.On_ground = False
        self.hurt = False
        self.hit = False

        """ Control keys """
        self.UP = K_UP
        self.DOWN = K_DOWN
        self.RIGHT = K_RIGHT
        self.LEFT = K_LEFT
        self.HIT = K_RSHIFT

        """ Load images """
        self.image_hands_down = pygame.image.load("./images/player/hands_down.gif").convert()
        self.image_hands_up = pygame.image.load("./images/player/hands_up.gif").convert()
        self.image_hands_hit = pygame.image.load("./images/player/hands_hit.gif").convert()
        self.image0 = pygame.image.load("./images/player/man_r.gif").convert()
        self.image1 = pygame.image.load("./images/player/man_r_stand.gif").convert()
        self.anim = 0
        self.width, self.height = 60, 100
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)
        # self.head = Rect(int self.x)

    def collide_platform(self, game, vx, vy):
        """ Обработка столкновений с платформой """
        for p in game.platforms:
            if sprite.collide_rect(self, p):
                # Спуск с платформы
                if game.pressed[self.DOWN]:
                    self.On_ground = False
                # Прыжок на платформу
                elif vy > 0 and (self.y < p.y - self.height + 30):
                    self.y = p.y - self.height + 1
                    self.On_ground = True
                    vy = 0
            else:
                self.On_ground = False

    def collide_enemy(self, enemy):
        """" Обработка столкновений с другим игроком """
        if self.rect.colliderect(enemy.image_hands.get_rect(center=enemy.rect.center)):
            """ When enemy is hitting you """
            if enemy.hit and not self.hurt:
                self.hurt = True
                if self.HP >= self.power:
                    self.HP -= self.power
                else:
                    self.HP = 0
            elif not enemy.hit:
                self.hurt = False
            #""" When enemy is jumping on you """
            if self.rect.top <= enemy.rect.bottom \
             and self.rect.top >= enemy.rect.bottom - 10 \
             and enemy.vy > 0:
                self.HP -= enemy.power
                enemy.vy = - enemy.vy
                enemy.y -= 12
                self.hurt = True
            #else:
                #self.hurt = False
        else:
            self.hurt = False

    def be_in(self, game):
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

    def control(self):
        """ player's moving when key press """
        if game.pressed[self.LEFT]:
            self.vx -= 10
        if game.pressed[self.RIGHT]:
            self.vx += 10
        if game.pressed[self.UP]:
            if self.On_ground:
                self.vy -= 800
                self.On_ground = False
        if game.pressed[self.HIT]:
            self.hit = True

    def update(self, game):
        """ Update Player state """
        #self.rect = Rect(int(self.x), int(self.y), self.width, self.height)
        self.hit = False
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.vx = 0
        self.collide_enemy(game.player2)
        self.control()

        """ Player's move """
        self.x +=self.vx
        self.collide_platform(game, self.vx, 0)
        if not self.On_ground:
            self.vy += game.delta * 1500 
            self.y += self.vy * game.delta
            self.collide_platform(game, 0, self.vy)

        self.be_in(game)
            
        if self.On_ground:
            self.vy = 0

    def show_HP(self, game):
        """ define and draw HP on the Game screen """
        self.color_HP = red
        self.rect_HP = Rect(10, 10, self.HP + 10, 20)
        draw.rect(game.screen, self.color_HP, self.rect_HP)

    def animation(self):
        if self.anim > 0.5:
            self.image = self.image0
        elif self.anim <= 0.5:
            self.image = self.image1
        if self.anim >= 1:
            self.anim = 0
        return self.anim + 0.1

    def face2face(self, player):
        if self.x > player.x:
            self.image = transform.flip(self.image, True, False)
            if self.image_hands == self.image_hands_hit:
                self.h_x, self.h_y = self.x - 35, self.y
            self.image_hands = transform.flip(self.image_hands, True, False)

    def render(self, game):
        """ Draw Player on the Game window """
        if self.HP > 0:
            self.image = self.image0
            self.image_hands = self.image_hands_up
            self.h_x, self.h_y = self.x-20, self.y
            if self.On_ground:
                self.image = self.image1
                self.image_hands = self.image_hands_down
                self.h_x, self.h_y = self.x, self.y
                if self.vx != 0:
                    self.anim = self.animation()
            if self.hit:
                self.image_hands = self.image_hands_hit
                self.h_x, self.h_y = self.x - 20, self.y
            if self.hurt:
                self.image = transform.rotate(self.image, 10)
            self.show_HP(game)
            self.face2face(game.player2)
            game.screen.blit(self.image_hands, (int(self.h_x), int(self.h_y)))
        else:
            self.font = pygame.font.Font(None, 25)
            self.image = self.font.render("second player wins", True, red)
            self.x, self.y = 470, 50

        game.screen.blit(self.image, (int(self.x),int(self.y)))



class Player2(Player):

    def __init__(self, game, x=800, y=100, vy=0, vx=0,):
        """ Constructor of Player class """
        sprite.Sprite.__init__(self)
        self.x, self.y, self.vy, self.vx = \
             x, y, vy, vx
        self.HP, self.power = 400, 20
        self.On_ground = False
        self.hurt = False
        self.hit = False

        """ Control keys """
        self.UP = K_w
        self.DOWN = K_s
        self.RIGHT = K_d
        self.LEFT = K_a
        self.HIT = K_SPACE

        """ Load images """
        self.image_hands_down = pygame.image.load("./images/player/hands_down.gif").convert()
        self.image_hands_up = pygame.image.load("./images/player/hands_up.gif").convert()
        self.image_hands_hit = pygame.image.load("./images/player/hands_hit.gif").convert()
        self.image0 = pygame.image.load("./images/player/man_r2.gif").convert()
        self.image1 = pygame.image.load("./images/player/man_r2_stand.gif").convert()
        self.anim = 0
        self.width, self.height = 60, 100
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, game):
        """ Update Player state """
        #self.rect = Rect(int(self.x), int(self.y), self.width, self.height)
        self.hit = False
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.vx = 0
        self.collide_enemy(game.player)
        self.control()

        """ Player's move """
        self.x +=self.vx
        self.collide_platform(game, self.vx, 0)
        if not self.On_ground:
            self.vy += game.delta * 1500
            self.y += self.vy * game.delta
            self.collide_platform(game, 0, self.vy)

        self.be_in(game)

        if self.On_ground:
            self.vy = 0

    def show_HP(self, game):
        """ define and draw HP on the Game screen """
        self.color_HP = red
        self.rect_HP = Rect((game.width - self.HP - 10), 10, game.width - 10, 20)
        draw.rect(game.screen, self.color_HP, self.rect_HP)

    def render(self, game):
        """ Draw Player on the Game window """
        if self.HP > 0:
            self.image = self.image0
            self.image_hands = self.image_hands_up
            self.h_x, self.h_y = self.x - 20, self.y
            if self.On_ground:
                self.image = self.image1
                self.image_hands = self.image_hands_down
                self.h_x, self.h_y = self.x, self.y
                if self.vx != 0:
                    self.anim = self.animation()
            if self.hit:
                self.image_hands = self.image_hands_hit
                self.h_x, self.h_y = self.x - 20, self.y
            if self.hurt:
                self.image = transform.rotate(self.image, 10)
            self.show_HP(game)
            self.face2face(game.player)
            game.screen.blit(self.image_hands, (int(self.h_x), int(self.h_y)))
        else:
            self.font = pygame.font.Font(None, 25)
            self.image = self.font.render("first player wins", True, red)
            self.x, self.y = 470, 50

        game.screen.blit(self.image, (int(self.x), int(self.y)))



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
        """ when press buttom """
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
                if self.y == 205:
                    game.default_state()
                    game.tool = 'main'
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

    def timer(self, time):
        """ writes time to the fight end on the Game window """
        self.timer
        self.font = pygame.font.Font(None, 40)
        self.image = self.font.render(str(int(time)), True, (120, 0, 0))
        self.T -= self.delta
        game.screen.blit(self.image, (500, 10))
        if self.player.HP <= 0 or self.player2.HP <= 0:
            self.T = -1

    def __init__(self):
        """ Constructor of the Game """
        self._running = True
        pygame.font.init()
        # create main display - 1040x400 window
        self.size = self.width, self.height = 1040, 500
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size)#, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('Fight game')
        # get object to help track time
        self.clock = pygame.time.Clock()
        self.tool = 'start'
        self.T0 = 31
        self.T = self.T0

        self.menu = Menu(self)
        self.platform = Platform(x = 300, y = 350)
        self.entities = pygame.sprite.Group() # Все объекты
        self.platforms = [] # то, во что мы будем врезаться или опираться
        self.players = pygame.sprite.Group() # игроки
        self.player2 = Player2(self)
        self.player = Player(self)
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

    def define_winner(self):
        """ define winner when time is over """
        if self.T <= 0:
            if self.player.HP > self.player2.HP:
                self.player2.HP = 0
            elif self.player.HP < self.player2.HP:
                self.player.HP = 0

    def default_state(self):
        """ set the first position and HP of players"""
        self.player2.x, self.player2.y, self.player2.vy = \
            800, 100, 0
        self.player.x, self.player.y, self.player.vy = \
            100, 100, 0
        self.player2.HP, self.player.HP = 400, 400
        self.player2.hurt, self.player.hurt = False, False
        self.T = self.T0

    def move(self):
        """ Here game objects update their positions """
        self.pressed = pygame.key.get_pressed()
        self.m_pressed = pygame.mouse.get_pressed()
        self.m_pos = mouse.get_pos()
        self.tick()
        if self.tool == 'main':
            self.player.update(self)
            self.player2.update(self)
        else:
            self.menu.update(self)
            self.menu.button_press(self)
            

    def render(self):
        """ Render the scene """
        self.screen.fill((255, 255, 255))
        if self.tool == 'main':
            if self.T >= 0:
                self.timer(self.T)
            self.platform.render(self)
            self.player.render(self)
            self.player2.render(self)
            self.define_winner()
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

if __name__ == "__main__":
    game = Game()
    game.execute()
    pygame.quit()