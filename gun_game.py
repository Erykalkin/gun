import math
from random import *

import pygame
from pygame.draw import *

from numpy import sign


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1000
HEIGHT = 700


class Ball:
    def __init__(self, screen: pygame.Surface, x, y=(HEIGHT-80)):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        #self.limit = []
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 50
        self.y_acceleration = 2

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy

        if HEIGHT - self.r > self.y > 0:
            self.vy += self.y_acceleration

        '''разделение условия столкновения со стенками 
        во избежание проблем при небольшом прохождении через стенку'''
        if self.x <= self.r:
            self.vx = abs(self.vx) * 0.9
            self.live -= 1
        if self.x >= WIDTH - self.r:
            self.vx = -abs(self.vx) * 0.9
            self.live -= 1

        if self.y >= HEIGHT - self.r:    # and -(abs(self.vy) - 1) <= 0:
            self.vy = -(abs(abs(self.vy) - min(5, abs(self.vy))))
            self.vx = (abs(self.vx) - min(1, abs(self.vx))) * sign(self.vx)    # трение
            self.live -= 1
        if self.y <= self.r:
            self.vy = abs(abs(self.vy) - min(5, abs(self.vy)))
            self.live -= 1

    def draw(self):
        circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        # line(self.screen, (255, 0, 0), (0, min(self.limit)), (WIDTH, min(self.limit)), 1)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            try:
                balls.remove(self)
            except ValueError:
                pass
            return True
        else:
            return False


class Bullet:
    def __init__(self, screen: pygame.Surface, x, y=(HEIGHT-80)):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        #self.limit = []
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1
        self.y_acceleration = 2

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > WIDTH:
            bullets.remove(self)
        if self.y > HEIGHT or self.y < 0:
            try:
                bullets.remove(self)
            except ValueError:
                pass

    def draw(self):
        circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            try:
                bullets.remove(self)
            except ValueError:
                pass
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.live = 30
        self.f2_power = 30
        self.f2_on = 0
        self.an = 1
        self.color = (100, 100, 100)
        self.x0 = 80
        self.y0 = HEIGHT - 80
        self.go_to_left = 0
        self.go_to_right = 0
        self.direction = ''

    def fire2_start(self, event):
        if event.button != 3:
            self.f2_on = 1
        if event.button == 3:
            new_bullet = Bullet(self.screen, x=self.x0)
            self.an = math.atan2((self.y0 - event.pos[1]), (event.pos[0] - self.x0))
            new_bullet.vx = 70 * math.cos(self.an)
            new_bullet.vy = -70 * math.sin(self.an)
            bullets.append(new_bullet)

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if event.button != 3:
            global balls
            new_ball = Ball(self.screen, x=self.x0)
            self.an = math.atan2((self.y0 - event.pos[1]), (event.pos[0] - self.x0))
            new_ball.vx = self.f2_power * math.cos(self.an) * 0.8
            new_ball.vy = -self.f2_power * math.sin(self.an) * 0.8
            balls.append(new_ball)
            self.f2_on = 0
            self.f2_power = 30

    def targetting(self, pos):
        """Прицеливание. Зависит от положения мыши."""
        self.an = math.atan2((self.y0 - pos[1]), (pos[0] - self.x0))

    def start_move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.go_to_left = 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.go_to_right = 1

    def end_move(self):
        if not pygame.key.get_pressed()[pygame.K_LEFT]:
            self.go_to_left = 0
        if not pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.go_to_right = 0

    def move(self):
        if self.go_to_left and not self.go_to_right:
            if 50 <= self.x0 - 5 <= WIDTH - 50:
                self.x0 -= 5
                self.direction = 'left'
        if not self.go_to_left and self.go_to_right:
            if 50 <= self.x0 + 5 <= WIDTH - 50:
                self.x0 += 5
                self.direction = 'right'
        elif self.go_to_left and self.go_to_right:
            if 50 <= self.x0 - 5 <= WIDTH - 50:
                if self.direction == 'right':
                    self.x0 -= 5
            if 50 <= self.x0 + 5 <= WIDTH - 50:
                if self.direction == 'left':
                    self.x0 += 5
        if self.go_to_left or self.go_to_right:
            self.targetting(pygame.mouse.get_pos())


    def draw(self):
        #line(screen, self.color, (self.x0, self.y0), (self.x0 + self.f2_power * math.cos(self.an), self.y0 - self.f2_power * math.sin(self.an)), 5)
        polygon(screen, self.color, [[self.x0 - 5 * math.sin(self.an), self.y0 - 5 * math.cos(self.an)],
                                     [self.x0 + (20 + self.f2_power * 0.8) * math.cos(self.an) - 5 * math.sin(self.an),
                                      self.y0 - (20 + self.f2_power * 0.8) * math.sin(self.an) - 5 * math.cos(self.an)],
                                     [self.x0 + (20 + self.f2_power * 0.8) * math.cos(self.an) + 5 * math.sin(self.an),
                                      self.y0 - (20 + self.f2_power * 0.8) * math.sin(self.an) + 5 * math.cos(self.an)],
                                     [self.x0 + 5 * math.sin(self.an), self.y0 + 5 * math.cos(self.an)],
                                     ])
        circle(screen, (80, 80, 80), (self.x0 - 50, HEIGHT-20), 20)
        circle(screen, (80, 80, 80), (self.x0 + 50, HEIGHT-20), 20)
        circle(screen, (100, 100, 100), (self.x0, HEIGHT-70), 20)
        rect(screen, (131, 77, 24), (self.x0 - 50, HEIGHT-70, 100, 50))
        rect(screen, (100, 100, 100), (self. x0 - 50, HEIGHT-70, 100, 50), 5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1


class Target:
    def __init__(self, screen):
        self.live = 1
        self.color = RED
        self.r = randint(5, 50)
        self.x = randint(self.r + 10, WIDTH - self.r - 10)
        self.y = randint(self.r + 10, HEIGHT - self.r - 10)
        self.vx = randint(20, 20)
        self.vy = randint(5, 20)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.vy = -self.vy
        if self.x <= self.r or self.x >= WIDTH - self.r:
            self.vx = -self.vx

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = randint(self.r + 1, WIDTH - self.r -1)
        self.y = randint(self.r + 1, HEIGHT - self.r - 1)
        self.r = randint(5, 50)
        self.vx = randint(-20, 20)
        self.vy = randint(-20, -5)

    def hit(self):
        """Попадание шарика в цель."""
        global points
        points += 1

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        if obj.x0 - 50 - self.r < self.x < obj.x0 + 50 + self.r and self.y > HEIGHT - 70:
            return True
        else:
            return False


class Boss:
    def __init__(self):
        self.health = 20
        self.y = 30
        self.x = 30
        self.vx = 5
        self.cloud_surf = pygame.transform.scale(pygame.image.load('облако.png'), (176, 148))
        self.cloud_surf = pygame.transform.flip(self.cloud_surf, True, False)

    def move(self):
        self.x += self.vx
        if self.vx < 0 and self.x + self.vx <= 0:
            self.vx = -self.vx
            self.cloud_surf = pygame.transform.flip(self.cloud_surf, True, False)
        if self.vx > 0 and self.x + self.vx >= WIDTH - 176:
            self.vx = -self.vx
            self.cloud_surf = pygame.transform.flip(self.cloud_surf, True, False)

    def draw(self):
        cloud_rect = self.cloud_surf.get_rect(topleft=(self.x, self.y))
        screen.blit(self.cloud_surf, cloud_rect)


class Bomb:
    def __init__(self, cloud):
        self.x = cloud.x + 90
        self.y = cloud.y + 75
        self.r = 20
        self.vy = 0
        self.alive = 1

    def move(self):
        self.y += self.vy
        self.vy += 1
        if self.y >= WIDTH:
            try:
                bombs.remove(self)
            except ValueError:
                pass

    def draw(self):
        a = randint(0, 200)
        circle(screen, (a, a, a), (self.x, self.y), self.r)

    def hittest(self, obj):
        if obj.x0 - 50 - self.r < self.x < obj.x0 + 50 + self.r and self.y > HEIGHT - 70:
            return True
        else:
            return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
points = 0
transparency = 0
balls = []
bullets = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
angry_cloud = Boss()
target = Target(screen)
target2 = Target(screen)
finished = False
i = 0

while not finished:
    i += 1
    screen.fill(WHITE)
    gun.draw()
    angry_cloud.draw()
    target.draw()
    target2.draw()

    while transparency != 0:
        transparency -= 1

    if i % 100 == 0:
        bombs.append(Bomb(angry_cloud))

    for b in balls:
        b.draw()

    for bullet in bullets:
        bullet.draw()

    for bomb in bombs:
        if bomb.alive:
            bomb.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            gun.start_move()
        elif event.type == pygame.KEYUP:
            gun.end_move()

    target.move()
    target2.move()
    angry_cloud.move()

    for bullet in bullets:
        bullet.move()
        if bullet.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if bullet.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()

    if target.hittest(gun) or target2.hittest(gun):
        if transparency == 0:
            gun.live -= 1
            print(gun.live)
            transparency = 200

    for bomb in bombs:
        if bomb.alive:
            bomb.move()
        else:
            bombs.remove(bomb)
        if bomb.hittest(gun) or target2.hittest(gun):
            if transparency == 0:
                gun.live -= 1
                print(gun.live)
                transparency = 200

    for b in balls:
        if b.live:
            b.move()
        else:
            balls.remove(b)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
    gun.power_up()
    gun.move()

    if gun.live == 0:
        finished = True

pygame.quit()