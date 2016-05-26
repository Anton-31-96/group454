#New project_python
#game: Fighting multiplayer
#мультиплеер. Будет возможность перехода по уровням
#Возможность взаимодействия с выпадающими предметами (оружие)
#Различные умения/характеристики персонажа
#В идеале наличие искусственного интеллекта

import pygame
from pygame import*
import random

""" We will use these colours """
red = (200,10,10)
gray = (120,126,135)
green = (10,200,10)
black = (0,0,0)
white = (250,250,250)
lemon_ch = (250,250,200)

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
        self.HP, self.power, self.shoot_n = 400, 20, 10
        self.On_ground = False
        self.hurt = False
        self.hit = False
        self.shoot = True

        """ Control keys """
        self.UP = K_w
        self.DOWN = K_s
        self.RIGHT = K_d
        self.LEFT = K_a
        self.HIT = K_g
        self.SHOOT = K_h

        """ Load images """
        self.image_hands_down = pygame.image.load("./images/player/hands_down.gif").convert()
        self.image_hands_up = pygame.image.load("./images/player/hands_up.gif").convert()
        self.image_hands_hit = pygame.image.load("./images/player/hands_hit.gif").convert()
        self.image0 = pygame.image.load("./images/player/man_r.gif").convert()
        self.image1 = pygame.image.load("./images/player/man_r_stand.gif").convert()
        self.image_atom = pygame.image.load("./images/player/atom2.gif").convert()
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

    def collide_atom(self, game):
        """ Collide with one of the atoms """
        for p in game.atoms:
            if self.rect.colliderect(p.rect):
                self.HP -= p.power
                game.atoms.remove(p)

    def collide_enemy(self, enemy):
        """" Обработка столкновений с другим игроком """
        if self.rect.colliderect(enemy.image_hands.get_rect(center=enemy.rect.center)):
            # When enemy is hitting you
            if enemy.hit and not self.hurt:
                self.hurt = True
                if self.HP >= self.power:
                    self.HP -= self.power
                else:
                    self.HP = 0
            elif not enemy.hit:
                self.hurt = False
            # When enemy is jumping on you
            if self.rect.top <= enemy.rect.bottom \
             and self.rect.top >= enemy.rect.bottom - 10 \
             and enemy.vy > 0:
                self.HP -= enemy.power
                enemy.vy = - enemy.vy
                enemy.y -= 12
                self.hurt = True
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

    def control(self, enemy):
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
        if game.pressed[self.SHOOT]:
            if self.shoot and self.shoot_n > 0:
                self.shoot_n -= 1
                if self.x > enemy.x:
                    if self.vx < 0:
                        game.atoms.append(Atom(self.x - 50, self.rect.centery, -650))
                    else:
                        game.atoms.append(Atom(self.x - 20, self.rect.centery, -650))
                else:
                    if self.vx > 0:
                        game.atoms.append(Atom(self.x + self.width + 50, self.rect.centery, 650))
                    else:
                        game.atoms.append(Atom(self.x + self.width + 20, self.rect.centery, 650))
            self.shoot = False
        if not game.pressed[self.SHOOT]:
            self.shoot = True

    def update(self, game):
        """ Update Player state """
        self.hit = False
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.vx = 0
        if game.mode == 'multi':
            self.collide_enemy(game.player2)
        self.collide_atom(game)
        self.control(game.player2)

        # Player's move
        self.x += self.vx
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

    def show_atoms_n(self):
        """ Show the number of available atoms """
        rect_atoms = Rect(10, 20, 20, 30).center
        self.font = pygame.font.Font(None, 35)
        self.at = self.font.render(str(self.shoot_n), True, black)
        game.screen.blit(self.image_atom, rect_atoms)
        game.screen.blit(self.at,(55, 40))

    def animation(self):
        """ Simulate the walking """
        if self.anim > 0.5:
            self.image = self.image0
        elif self.anim <= 0.5:
            self.image = self.image1
        if self.anim >= 1:
            self.anim = 0
        return self.anim + 0.1

    def face2face(self, player):
        """ players will watch on each other """
        if game.mode == 'multi':
            if self.x > player.x:
                self.image = transform.flip(self.image, True, False)
                if self.image_hands == self.image_hands_hit:
                    self.h_x, self.h_y = self.x - 35, self.y
                self.image_hands = transform.flip(self.image_hands, True, False)

        elif game.mode == 'single':
            if self.vx < 0:
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
            self.show_atoms_n()
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
        self.HP, self.power, self.shoot_n = 400, 20, 10
        self.On_ground = False
        self.hurt = False
        self.hit = False
        self.shoot = True

        """ Control keys """
        self.UP = K_UP
        self.DOWN = K_DOWN
        self.RIGHT = K_RIGHT
        self.LEFT = K_LEFT
        self.HIT = K_PERIOD
        self.SHOOT = K_COMMA

        """ Load images """
        self.image_hands_down = pygame.image.load("./images/player/hands_down.gif").convert()
        self.image_hands_up = pygame.image.load("./images/player/hands_up.gif").convert()
        self.image_hands_hit = pygame.image.load("./images/player/hands_hit.gif").convert()
        self.image0 = pygame.image.load("./images/player/man_r2.gif").convert()
        self.image1 = pygame.image.load("./images/player/man_r2_stand.gif").convert()
        self.image_atom = pygame.image.load("./images/player/atom2.gif").convert()
        self.anim = 0
        self.width, self.height = 60, 100
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, game):
        """ Update Player state """
        self.hit = False
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.vx = 0
        self.collide_enemy(game.player)
        self.collide_atom(game)
        self.control(game.player)

        """ Player's move """
        self.x += self.vx
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

    def show_atoms_n(self):
        """ Show the number of available atoms """
        self.font = pygame.font.Font(None, 35)
        self.at = self.font.render(str(self.shoot_n), True, black)
        game.screen.blit(self.image_atom, (game.width-50, 35))
        game.screen.blit(self.at,(game.width-80, 40))

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
            self.show_atoms_n()
            self.face2face(game.player)
            game.screen.blit(self.image_hands, (int(self.h_x), int(self.h_y)))
        else:
            self.font = pygame.font.Font(None, 25)
            self.image = self.font.render("first player wins", True, red)
            self.x, self.y = 470, 50

        game.screen.blit(self.image, (int(self.x), int(self.y)))



class Single_Play():

    def __init__(self, game):
        """ Constructor of Single Game """
        self.font = pygame.font.Font(None, 55)
        self.stage = 0
        self.time = 0
        self.t = 0
        self.x = game.width/2
        self.text = self.font.render(" ", True, black)
        self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        self.image1 = self.font.render(" ", True, black)
        self.rect1 = self.image1.get_rect(center=(game.width / 2, game.height / 5))
        self.image2 = self.font.render(" ", True, black)
        self.rect2 = self.image2.get_rect(center=(game.width / 2, game.height / 5))
        game.player.shoot_n = 0
        self.goal = 0

    def stage_0(self):
        """ Начальный текст """
        if self.time > 3:
            self.text = self.font.render("Тебе что, не с кем поиграть?", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 7:
            self.text = self.font.render("Иди в мультиплеер, там интереснее!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 11:
            self.text = self.font.render("Как тут выиграть?!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 13:
            self.text = self.font.render("Очень просто!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 14.5:
            self.text = self.font.render("Поздравляю! Ты победил!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 19:
            self.text = self.font.render("Слишком просто?", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 21.5:
            self.text = self.font.render("Слушай, мне некогда с тобой возиться", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 24:
            self.text = self.font.render("Уходи!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 26:
            self.text = self.font.render("Дверь там", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 27.5:
            self.image1 = pygame.image.load("./images/world/door.gif").convert()
            self.text = self.font.render("", True, black)
            if game.player.x >= game.width / 2:
                self.rect1 = self.image1.get_rect(bottomleft=(30, game.height))
            else:
                self.rect1 = self.image1.get_rect(bottomright=(game.width - 30, game.height))
            self.stage += 1
            self.time = 0

    def stage_1(self):
        """ Игра с дверью """
        if game.player.x >= game.width/2 + 200:
            self.rect1 = self.image1.get_rect(bottomleft=(30, game.height))
        if game.player.x <= game.width/2 - 200:
            self.rect1 = self.image1.get_rect(bottomright=(game.width - 30, game.height))
        if self.time > 3.5:
            self.text = self.font.render("Сложнааа!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 5.5:
            self.text = self.font.render("Ладно", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.image1 = self.font.render(" ", True, black)
            self.stage += 1
            self.time = 0

    def stage_2(self):
        """ Игра с кнопкой """
        if  1 <self.time < 2.5:
            self.text = self.font.render("Если хочешь выиграть", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if 2.5 < self.time < 2.6:
            self.t = 0
            self.text = self.font.render("Встань на красную кнопку", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.image1 = Surface((60, 15))
            self.image1.fill(green)
            self.image2 = Surface((60,15))
            self.image2.fill(red)
            if game.player.x < game.width/2:
                self.rect1 = self.image1.get_rect(bottomright=(game.width - 30, game.height))
                self.rect2 = self.image2.get_rect(bottomright=(game.width - 100, game.height))
            else:
                self.rect1 = self.image1.get_rect(bottomleft=(30, game.height))
                self.rect2 = self.image2.get_rect(bottomleft=(100, game.height))
        if self.time > 2.1:
            if (self.rect2.centerx - 30) < game.player.rect.centerx < (self.rect2.centerx + 30):
                self.t += game.delta
                if self.t > 0.1:
                    self.image1.fill(red)
                    self.image2.fill(green)
                    game.player.RIGHT, game.player.LEFT = 1, 1
                    self.text = self.font.render("Ну и что ты сделал?", True, black)
                    self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
                    self.time = 0
                    self.stage += 1
                    self.t = 0

    def stage_3(self):
        """ Игра с кнопкой. Вторая попытка """
        if self.time > 2:
            self.text = self.font.render("На какой кнопке ты стоишь?", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 4:
            self.text = self.font.render("Давай попробуем еще раз", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if 5 < self.time < 5.05:
            game.player.RIGHT, game.player.LEFT = K_d, K_a
            if game.player.x > game.width/2:
                game.player.x = 100
            else:
                game.player.x = game.width - 100
            self.image1.fill(green)
            self.image2.fill(red)

        if self.time > 6:
            self.text = self.font.render("Встань на КРАСНУЮ кнопку", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 6.1 and self.rect2.colliderect(game.player.rect):
            self.t += game.delta
            self.text = self.font.render("Вот теперь молодец!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.t > 3:
            self.t = 0
            self.time = 0
            self.stage += 1
            self.image1 = self.font.render(" ", True, black)
            self.image2 = self.font.render(" ", True, black)

    def stage_4(self):
        """ Взять припасы """
        if self.time > 1.5:
            self.text = self.font.render("Ты готов к настоящей схватке!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 4:
            self.text = self.font.render("Видишь те атомы на платформе?", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if 4.1 < self.time < 4.2:
            self.image1 = pygame.image.load("./images/player/atom2.gif").convert()
            self.rect1 = self.image1.get_rect(midbottom=game.platform.rect.midtop)
        if self.time > 6:
            self.text = self.font.render("Ты должен их взять", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 6 and game.player.rect.colliderect(game.platform.rect) \
         and game.player.On_ground:
            self.text = self.font.render("Так держать!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.image1 = self.font.render(" ", True, black)
            game.player.shoot_n = 5
            self.time = 0
            self.stage += 1

    def stage_5(self):
        """ Драка """
        if 1.9 < self.time < 2:
            self.image1 = Surface((62, 100))
            self.image1.fill((255, 255, 255))
            self.image1.blit(pygame.image.load("./images/player/man_r2_stand.gif").convert(), (0, 0))
            self.image1.blit(pygame.image.load("./images/player/hands_down.gif").convert(), (0, 0))
            self.image1 = transform.flip(self.image1, True, False)
            self.rect1 = self.image1.get_rect(bottomright=(game.width - 100, game.height))
            self.x = self.rect1.centerx
        if self.time > 2.5:
            self.text = self.font.render("Заметил того рыжего?", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 4:
            self.text = self.font.render("Запусти в него атомы, нажав 'H'", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        for b in game.atoms:
            if self.rect1.colliderect(b.rect):
                game.atoms.remove(b)
                self.goal += 1
        if self.goal == 1:
            self.text = self.font.render("Молодец!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.goal == 2:
            self.text = self.font.render("И еще один!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.goal == 3:
            self.text = self.font.render("Ты справился!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.image1 = self.font.render(" ", True, black)
            self.time = 0
            self.stage += 1
        if game.player.shoot_n == 0 and self.t < 1.5:
            self.text = self.font.render("Кажется, у тебя закончились снаряды!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.t += game.delta
        if game.player.shoot_n == 0 and self.t >= 1.5:
            self.text = self.font.render("Ладно, держи еще несколько!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.t += game.delta
        if game.player.shoot_n == 0 and self.t >= 3:
            self.text = self.font.render("Ладно, держи еще несколько!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
            self.t = 0
            game.player.shoot_n = 5

    def stage_6(self):
        """ Конец игры """
        if self.time > 1.5:
            self.text = self.font.render("Невероятно!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 3:
            self.text = self.font.render("Вот это победа!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 5.5:
            self.text = self.font.render("А теперь беги в мультиплеер!", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height / 5))
        if self.time > 7.5:
            self.font = pygame.font.Font(None, 30)
            self.text = self.font.render("Developed by Anton Bozhedarov", True, black)
            self.text_rect = self.text.get_rect(center=(game.width / 2, game.height - self.t))
            self.t += 1
        if self.t >= game.height + 50:
            game.tool = 'start'

    def update(self, game):
        """ Ececute different stages """
        self.time += game.delta
        if self.stage == 0:
            self.stage_0()
        elif self.stage == 1:
            self.stage_1()
        elif self.stage == 2:
            self.stage_2()
        elif self.stage == 3:
            self.stage_3()
        elif self.stage == 4:
            self.stage_4()
        elif self.stage == 5:
            self.stage_5()
        elif self.stage == 6:
            self.stage_6()

    def render(self, game):
        """ Draw 'single play' images """
        game.screen.blit(self.image1, self.rect1.topleft)
        game.screen.blit(self.image2, self.rect2.topleft)
        game.screen.blit(self.text, self.text_rect.topleft)



class Atom:
    def __init__(self, x, y, vx, vy=0):
        """ Constructor of Atom class """
        self.image = pygame.image.load("./images/player/atom2.gif").convert()
        self.x, self.y, self.vx, self.vy = \
         x, y, vx, vy
        self.power = 20
        self.rect = Rect(0,0, 10,10)
        self.COLLIDE = False

    def collide(self):
        """  When two atoms collide """
        for p in game.atoms:
            if self.rect.colliderect(p.rect):
                if self != p and not self.COLLIDE:
                    self.vx *= 1.5
                    self.power += 1
                    self.vy = random.gauss(0, 1) * 110
                    self.COLLIDE = True
            else:
                self.COLLIDE = False

    def update(self, game):
        """ Update the atom's options """
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.x += self.vx * game.delta
        self.y += self.vy * game.delta
        self.collide()
        # Delete atom if it out of the gamescreen
        if self.x < 0 \
         or self.y <= 0 \
         or self.x > game.width - self.rect.width \
         or self.y >= game.height:
            game.atoms.remove(self)

    def render(self, game):
        """ render the atom """
        game.screen.blit(self.image, self.rect)



class Menu:
    def buttons_rect(self, list1, list2, x = 210, y = 130, d_y = 60):
        """ Create list of rectangles for buttons """
        self.image = self.clear_image.convert()
        for b in list1:
            for b in list1:
                self.image.blit(self.font.render(b, True, white), (x, y))
                list2.append(self.font.render(b, True, white).get_rect(topleft=(x, y)))
                y += d_y

    def __init__(self, game):
        """ Constructor of Menu class """
        self.clear_image = pygame.image.load("./images/menu/main1.gif")
        self.font = pygame.font.Font(None, 55)
        self.m_pres = False
        # Buttons for start menu
        self.b_list1 = ["Одиночная игра", "Мультиплеер", "Настройки", "Выход"]
        self.b_list1_rects = []
        self.buttons_rect(self.b_list1,self.b_list1_rects)
        # Buttons for pause menu
        self.b_list2 = ["Продолжить", "Новая игра", "Настройки", "Выход"]
        self.b_list2_rects = []
        self.buttons_rect(self.b_list2, self.b_list2_rects)
        self.b_list3 = ["Время матча:", "30 секунд", "60 секунд", "2 минуты"]
        self.b_list3_rects = []
        self.buttons_rect(self.b_list3, self.b_list3_rects)

    def render_button_list(self, list1, list2):
        """ Renders the list of buttons on the menu page """
        x, y = 210, 130
        for b in list1:
            self.image.blit(self.font.render(b, True, white), (x, y))
            y += 60

    def update(self, game):
        """ Update the menu state """
        self.case = 0

        # Handling the events in the start menu
        if game.tool == 'start':
            self.image = self.clear_image.convert()
            self.render_button_list(self.b_list1,self.b_list1_rects)
            # If mouse cursor on the button 1
            if self.b_list1_rects[0].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list1[0], True, lemon_ch)), self.b_list1_rects[0].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 1
            # If mouse cursor on the button 2
            if self.b_list1_rects[1].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list1[1], True, lemon_ch)), self.b_list1_rects[1].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 2
            # If mouse cursor on the button 3
            if self.b_list1_rects[2].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list1[2], True, lemon_ch)), self.b_list1_rects[2].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 3
            # If mouse cursor on the button 4
            if self.b_list1_rects[3].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list1[3], True, lemon_ch)), self.b_list1_rects[3].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 4

        # Handling the events in the pause menu
        if game.tool == 'pause':
            self.image = self.clear_image.convert()
            self.render_button_list(self.b_list2, self.b_list2_rects)
            if self.b_list2_rects[0].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list2[0], True, lemon_ch)), self.b_list2_rects[0].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 1
            # If mouse cursor on the button 2
            if self.b_list2_rects[1].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list2[1], True, lemon_ch)), self.b_list2_rects[1].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 2
            # If mouse cursor on the button 3
            if self.b_list2_rects[2].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list2[2], True, lemon_ch)), self.b_list2_rects[2].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 3
            # If mouse cursor on the button 4
            if self.b_list2_rects[3].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list2[3], True, lemon_ch)), self.b_list2_rects[3].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 4

        # Handling the events in the pause menu
        if game.tool == 'option':
            self.image = self.clear_image.convert()
            # Create button BACK
            self.b_back = self.font.render("Назад", True, white)
            self.b_back_rect = self.b_back.get_rect(topleft = (20, 20))
            self.image.blit(self.b_back, (20, 20))
            self.render_button_list(self.b_list3, self.b_list3_rects)

            # If mouse cursor on the button BACK
            if self.b_back_rect.collidepoint(game.m_pos):
                self.image.blit((self.font.render("Назад", True, lemon_ch)),
                                self.b_back_rect.topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 1
            # If mouse cursor on the button 2
            if self.b_list3_rects[1].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list3[1], True, lemon_ch)),
                                self.b_list3_rects[1].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 2
            # If mouse cursor on the button 3
            if self.b_list3_rects[2].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list3[2], True, lemon_ch)),
                                self.b_list3_rects[2].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 3
            # If mouse cursor on the button 4
            if self.b_list3_rects[3].collidepoint(game.m_pos):
                self.image.blit((self.font.render(self.b_list3[3], True, lemon_ch)),
                                self.b_list3_rects[3].topleft)
                if game.m_pressed == (1, 0, 0):
                    self.case = 4

    def button_pres(self):
        """ Handle the user's choice when he press button """
        execute = True

        if game.tool == 'start' and execute:
            if self.case == 1:
                # This function doesn't work properly
                game.tool = 'main'
                game.player2 = Single_Play(game)
                game.mode = 'single'
            elif self.case == 2:
                # Start the Game
                game.player2 = Player2(game)
                game.default_state()
                game.tool = 'main'
                game.mode = 'multi'
                game.start = True
            elif self.case == 3:
                # Options page
                game.tool = 'option'
            elif self.case == 4:
                game.exit()
            execute = False

        if game.tool == 'pause' and execute:
            if self.case == 1:
                # return in the game
                game.tool = 'main'
            elif self.case == 2:
                # start the new game
                game.default_state()
                game.tool = 'start'
                game.start = False
            elif self.case == 3:
                # Options page
                game.tool = 'option'
            elif self.case == 4:
                game.exit()
            execute = False

        if game.tool == 'option' and execute:
            if self.case == 1:
                if game.start:
                    game.tool = 'pause'
                else:
                    game.tool = 'start'
            elif self.case == 2:
               # game.T = 31
                game.T0 = 31
            elif self.case == 3:
                #game.T = 61
                game.T0 = 61
            elif self.case == 4:
                #game.T = 121
                game.T0 = 121
            execute = False



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
        self.tool = 'start'
        self.start = False
        #self.m_pressed = (0,0,0)
        pygame.font.init()
        # create main display - 1040x400 window
        self.size = self.width, self.height = 1040, 500
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('Sciense WAR')
        # get object to help track time
        self.clock = pygame.time.Clock()
        self.T0 = 61
        self.T = self.T0
        # initialize all objects
        self.menu = Menu(self)
        self.platform = Platform(x = 300, y = 350)
        self.platforms = [] # то, во что мы будем врезаться или опираться
        self.atoms = [] # атомы в игрре
        #self.player2 = Player2(self)
        self.player = Player(self)
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
        if event.type == MOUSEBUTTONUP:
            self.m_pressed = (1,0,0)
        else:
            self.m_pressed = (0, 0, 0)

    def define_winner(self):
        """ define winner when time is over """
        if self.T <= 0:
            if self.player.HP > self.player2.HP:
                self.player2.HP = 0
            elif self.player.HP < self.player2.HP:
                self.player.HP = 0

    def default_state(self):
        """ set the default options of the entities """
        for p in self.atoms:
            for i in self.atoms:
                self.atoms.remove(i)
        # set the first position and HP of players
        self.player2.x, self.player2.y, self.player2.vy = \
            800, 100, 0
        self.player.x, self.player.y, self.player.vy = \
            100, 100, 0
        self.player2.HP, self.player.HP = 400, 400
        self.player.shoot_n, self.player2.shoot_n = 10, 10
        self.player2.hurt, self.player.hurt = False, False
        self.T = self.T0

    def move(self):
        """ Here game objects update their positions """
        self.pressed = pygame.key.get_pressed()
        self.m_pos = mouse.get_pos()
        self.tick()
        if self.tool == 'main':
            # update the world
            self.player.update(self)
            self.player2.update(self)
            if self.mode == 'multi':
                self.define_winner()
            #elif self.mode == 'single':
                #self.player2.update()
            for i in self.atoms:
                i.update(game)
        else:
            # update the menu
            self.menu.update(self)
            self.menu.button_pres()

    def render(self):
        """ Render the scene """
        self.screen.fill((255, 255, 255))
        if self.tool == 'main':
            if self.mode == 'multi' and self.T >= 0:
                self.timer(self.T)
            self.platform.render(self)
            self.player2.render(self)
            self.player.render(self)
            for i in self.atoms:
                i.render(game)
        else:
            self.screen.blit(self.menu.image, (0,0))
            #if self.menu.image != self.menu.develop:
            #    self.menu.button_render(self)
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
            self.m_pressed = (0,0,0)
            self.render()

if __name__ == "__main__":
    game = Game()
    game.execute()
    pygame.quit()