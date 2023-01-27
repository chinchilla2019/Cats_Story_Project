import pygame
import sys
import os
import random

money = 200
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.init()


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# окошко начала и конца
COINS_COUNT = 0
possible_choices = [-3, -2, -1, 1, 2]
particle_v = [random.choice(possible_choices), random.choice(possible_choices), random.choice(possible_choices)]
a = 0
v = 0
enemy_x = 0
costume = False
running = True
platform_list_ordinary = None
platform_list_disappearing = None
all_sprites_here = []
enemies, hp_sprites, coin_sprites, = None, None, None
n1, n2, n3, players, c1, c2 = None, None, None, None, None, None

# карта для перемещения игрока
MAP_ALL = [['.', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '-', '-', '-', '.'],
           ['.', '-', '-', '-', '*', '*', '.', '.', '.', '.', '.', '.', '-', '-', '.', '.'],
           ['.', '.', '-', '-', '-', '.', '.', '.', '.', '-', '-', '*', '-', '-', '.', '.'],
           ['.', '.', '.', '.', '.', '.', '.', '.', '-', '-', '&', '.', '.', '.', '0', '.'],
           ['.', '.', '.', '.', '.', '.', '.', '.', '.', '-', '-', '-', '*', '-', '-', '.'],
           ['.', '.', '.', '.', '.', '.', '.', '-', '.', '.', '.', '.', '.', '.', '.', '.'],
           ['.', '.', '.', '.', '.', '.', '-', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
           ['*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '*', '.'],
           ['.', '-', '-', '-', '.', '.', '.', '-', '*', '*', '.', '.', '.', '.', '-', '-'],
           ['.', '.', '-', '-', '-', '.', '*', '*', '-', '*', '*', '-', '.', '.', '.', '.'],
           ['.', '.', '.', '-', '-', '-', '.', '.', '-', '-', '-', '.', '.', '.', '.', '.'],
           ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '-', '.', '.', '.', '.']]

numbers_dict = {'1': '1.png', '2': '2.png',
                '3': '3.png', '4': '4.png',
                '5': '5.png', '6': '6.png',
                '7': '7.png', '8': '8.png',
                '9': '9.png', '0': '0.png'}


# экран в начале игры
def started_screen():
    intro_text = ["",
                  "Правила игры:",
                  "Стараться собрать как можно больше,",
                  "монет, не попадаясь врагу."]

    fon = pygame.transform.scale(load_image('begin.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 420
    run_ss = True
    pygame.display.set_caption('Cat Game')
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while run_ss:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_ss = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(30)


# экран в конце игры
def game_over_screen():
    global money
    fon = pygame.transform.scale(load_image('game_over.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
    run_ss = True
    pygame.display.set_caption('Game Over')
    clock = pygame.time.Clock()

    while run_ss:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_ss = False

            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(30)


# generate_coins
while COINS_COUNT != 10:
    y_c = random.randint(0, len(MAP_ALL) - 1)
    x_c = random.randint(0, len(MAP_ALL[0]) - 1)
    if MAP_ALL[y_c][x_c] == '.':
        MAP_ALL[y_c][x_c] = '$'
        COINS_COUNT += 1


# загрузка изображения
def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# иконка приложения
icon = load_image('p0.png')


# создание карты
def generate_map():
    global enemy_x
    for y in range(len(MAP_ALL)):
        for x in range(len(MAP_ALL[0])):
            if MAP_ALL[y][x] == '-':
                block = Platform('платформа1син')
                block.rect = block.image.get_rect().move(block.rect.width * x, block.rect.height * y)
                platform_list_ordinary.add(block)
                all_sprites_here.add(block)
            elif MAP_ALL[y][x] == '*':
                block = Platform('платформа1сер')
                block.rect = block.image.get_rect().move(block.rect.width * x, block.rect.height * y)
                platform_list_disappearing.add(block)
                all_sprites_here.add(block)
            elif MAP_ALL[y][x] == '&':
                enemy = Enemy()
                enemy_x = 60 * x + 5
                enemy.rect = enemy.image.get_rect().move(60 * x + 15, 64 * y + 5)
            elif MAP_ALL[y][x] == '0':
                hps = HP()
                hps.rect = hps.image.get_rect().move(60 * x + 15, 64 * y + 25)
            elif MAP_ALL[y][x] == '$':
                cn = COIN()
                cn.rect = cn.image.get_rect().move(60 * x + 15, 64 * y + 25)


# остановка игры
def stop():
    global running
    running = False


# классы спрайтов
class Player(pygame.sprite.Sprite):
    rotation = 0

    def __init__(self):
        super().__init__()
        self.image_normal = load_image('p0.png')
        self.image = self.image_normal
        self.image_left = load_image('left.png')
        self.image_right = load_image('right.png')
        self.images = ['p0.png', 'p1.png', 'p2.png',
                       'p3.png', 'p4.png', 'p5.png',
                       'p6.png', 'p5.png', 'p4.png',
                       'p3.png', 'p2.png', 'p1.png']
        self.rect = self.image.get_rect()
        self.enemy_list = []
        self.hp = 200
        self.money = 0
        self.change_x = 0
        self.change_y = 0

    def update(self):
        global money
        self.calc_grav()
        self.rect.x += self.change_x
        hp_hit_list = pygame.sprite.spritecollide(self, hp_sprites, False)
        coin_hit_list = pygame.sprite.spritecollide(self, coin_sprites, False)
        block_hit_list = pygame.sprite.spritecollide(self, platform_list_disappearing, False)
        bhl = pygame.sprite.spritecollide(self, platform_list_ordinary, False)
        block_hit_list += bhl
        self.enemy_list = pygame.sprite.spritecollide(self, enemies, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list_or = pygame.sprite.spritecollide(self, platform_list_disappearing, False)
        block_hit_list_dis = pygame.sprite.spritecollide(self, platform_list_ordinary, False)
        for block in block_hit_list_dis:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
        for block in block_hit_list_or:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                if block.count <= 20:
                    block.count += 1
                else:
                    block.kill()
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
        for enemy in self.enemy_list:
            if self.change_x > 0:
                self.rect.right = enemy.rect.left
            elif self.change_x < 0:
                self.rect.left = enemy.rect.right
            elif self.change_y > 0:
                self.rect.bottom = enemy.rect.top
            elif self.change_y < 0:
                self.rect.top = enemy.rect.bottom
            self.hp -= 1
            if self.hp < 10:
                n1t, n2t = '0', '0'
                n3t = str(self.hp)
            elif 9 < self.hp < 100:
                n1t = '0'
                n2t, n3t = str(self.hp)[0], str(self.hp)[1]
            else:
                n1t, n2t, n3t = str(self.hp)[0], str(self.hp)[1], str(self.hp)[2]
            if int(n3t) > -1:
                n1.image = load_image(f'{n1t}.png')
                n2.image = load_image(f'{n2t}.png')
                n3.image = load_image(f'{n3t}.png')
            if self.hp < 1:
                stop()
        for hp_s in hp_hit_list:
            self.hp += 50
            hp_s.kill()
            if self.hp < 10:
                n1t, n2t = '0', '0'
                n3t = str(self.hp)
            elif 9 < self.hp < 100:
                n1t = '0'
                n2t, n3t = str(self.hp)[0], str(self.hp)[1]
            else:
                n1t, n2t, n3t = str(self.hp)[0], str(self.hp)[1], str(self.hp)[2]
            n1.image = load_image(f'{n1t}.png')
            n2.image = load_image(f'{n2t}.png')
            n3.image = load_image(f'{n3t}.png')
        for coin in coin_hit_list:
            self.money += 1
            money += 1
            coin.kill()
            if self.money < 10:
                c1t, c2t = '0', str(self.money)
            else:
                c1t, c2t = str(self.money)[0], str(self.money)[1]
            c1.image = load_image(f'{c1t}.png')
            c2.image = load_image(f'{c2t}.png')

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 10
        self.enemy_list = pygame.sprite.spritecollide(self, enemies, False)
        platform_hit_list_or = pygame.sprite.spritecollide(self, platform_list_ordinary, False)
        platform_hit_list_dis = pygame.sprite.spritecollide(self, platform_list_disappearing, False)
        # добавить изчезновение
        self.rect.y -= 10

        if (len(platform_hit_list_dis) > 0 or
            self.rect.bottom >= SCREEN_HEIGHT
            or len(platform_hit_list_or) > 0) \
                and len(self.enemy_list) == 0:
            self.change_y = -20

    def go_left(self):
        self.change_x = -9
        self.image = self.image_left

    def go_right(self):
        self.change_x = 9
        self.image = self.image_right

    def stop(self):
        self.change_x = 0

    def change_to_normal(self):
        self.image = self.image_normal


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites_here, enemies)
        self.image = load_image('enemy.png')
        self.image_n = load_image('enemy.png')
        self.image_fl = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rect.x += self.change_x
        player_list = pygame.sprite.spritecollide(self, players, False)
        if len(player_list) == 0:
            if (v // 100) % 2 == 0:
                if self.rect.x < enemy_x + 200:
                    self.rect.x += 2
                    self.image = self.image_fl
            else:
                if self.rect.x > enemy_x:
                    self.rect.x -= 2
                    self.image = self.image_n
        for pl in player_list:
            if self.change_x > 0:
                self.rect.right = pl.rect.left
            elif self.change_x < 0:
                self.rect.left = pl.rect.right
            elif self.change_y > 0:
                self.rect.bottom = pl.rect.top
            elif self.change_y < 0:
                self.rect.top = pl.rect.bottom


class Number(pygame.sprite.Sprite):
    def __init__(self, type_of_image):
        if int(type_of_image) > -1:
            super().__init__(all_sprites_here)
            self.image = load_image(f'{type_of_image}.png')
            self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):
    def __init__(self, type_of_image):
        super().__init__(all_sprites_here)
        self.image = load_image(f'{type_of_image}.png')
        self.rect = self.image.get_rect()
        self.count = 0


class HP(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__(all_sprites_here, hp_sprites)
        self.image = load_image('hp.png')
        self.rect = self.image.get_rect()


class COIN(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites_here, coin_sprites)
        self.image = load_image('coin.png')
        self.rect = self.image.get_rect()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__(all_sprites_here)
        self.speed = speed
        self.image = load_image("cloud.png")
        self.rect = self.image.get_rect()
        self.change_x = speed

    def update(self):
        width = self.image.get_width()
        if self.rect.x >= SCREEN_WIDTH:
            self.change_x = -self.speed
        elif self.rect.x <= -self.rect.width:
            self.change_x = self.speed
        self.rect.x += self.change_x


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites_here)
        self.image = load_image("star.png")
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


# украшения
def generate_clouds():
    hp_im = Cloud(0)
    hp_im.image = load_image('hp.png')
    hp_im.rect.x, hp_im.rect.y = 15, 10
    cn_im = Cloud(0)
    cn_im.image = load_image('coin.png')
    cn_im.rect.x, cn_im.rect.y = 165, 12
    cl1 = Cloud(5)
    cl2 = Cloud(4)
    cl3 = Cloud(2)
    cl4 = Cloud(7)
    cl1.image = pygame.transform.scale(cl1.image, (250, 150))
    cl2.rect.x = 7 * SCREEN_WIDTH // 8
    cl2.rect.y = cl1.rect.height
    cl3.rect.x = SCREEN_WIDTH // 2
    cl3.rect.y = cl2.rect.height + cl1.rect.height
    cl3.image = pygame.transform.scale(cl3.image, (200, 100))
    cl4.rect.x = SCREEN_WIDTH // 2
    cl4.rect.y = cl2.rect.height + cl1.rect.height + cl3.rect.height
    cl4.image = pygame.transform.scale(cl4.image, (500, 300))


# игра
def start_game1():
    global platform_list_ordinary, \
        platform_list_disappearing, \
        enemies, hp_sprites, coin_sprites, \
        costume, v, all_sprites_here, \
        n1, n2, n3, players, c1, c2, a
    player = Player()
    run = True
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT // 2
    platform_list_ordinary = pygame.sprite.Group()
    platform_list_disappearing = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    hp_sprites = pygame.sprite.Group()
    coin_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    all_sprites_here = pygame.sprite.Group()

    n1, n2, n3 = Number('2'), Number('0'), Number('0')
    n1.rect = 50, 15
    n2.rect = n2.rect.width + 50, 15
    n3.rect = 2 * n3.rect.width + 50, 15

    c1, c2 = Number('0'), Number('0')
    c1.rect = 200, 15
    c2.rect = c2.rect.width + 200, 15
    all_sprites_here.add(player)
    players.add(player)
    generate_map()
    generate_clouds()
    clock = pygame.time.Clock()

    while run:
        screen.fill((40, 0, 81))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if player.money == 10:
                run = False
            if player.hp <= 0:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                    costume = True
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                    costume = True
                if event.key == pygame.K_UP:
                    if len(player.enemy_list) == 0:
                        player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.change_to_normal()
                    costume = False
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.change_to_normal()
                    costume = False
                    player.stop()
        if not costume and v % 2 == 0:
            player.image = load_image(player.images[a])
            a += 1
            a = a % 12
        if v % 17 == 0:
            Particle((random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4),
                      (random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4))),
                     random.choice(particle_v), random.choice(particle_v))
        all_sprites_here.update()
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.bottom > SCREEN_HEIGHT:
            player.rect.bottom = SCREEN_HEIGHT
        if player.rect.top < 0:
            player.rect.top = 0
        all_sprites_here.draw(screen)
        clock.tick(30)
        v += 1
        pygame.display.flip()


# диалоговое окно
class AskingTable(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('behind_text.png')
        self.rect = self.image.get_rect()
        self.count = 0


# текст в программе
class Text(pygame.sprite.Sprite):
    def __init__(self, text, text_size, color):
        super().__init__(all_sprites)
        font = pygame.font.SysFont('serif', text_size)
        self.image = font.render(text, False, color)
        self.rect = self.image.get_rect()


# всевозможные кнопки
class Button(pygame.sprite.Sprite):
    def __init__(self, answer_type):
        super().__init__(all_sprites)
        self.image = load_image(f'{answer_type}.png')
        self.rect = self.image.get_rect()

    def pressed(self, mouse_place):
        if mouse_place[0] > self.rect.topleft[0]:
            if mouse_place[1] > self.rect.topleft[1]:
                if mouse_place[0] < self.rect.bottomright[0]:
                    if mouse_place[1] < self.rect.bottomright[1]:
                        return True
                    return False
                return False
            return False
        return False


# портал - элемент графической новеллы
class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('portal.png')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 210
        self.count = 0


# кот
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.flip(load_image('cat_go.png'), True, False)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 550
        self.count = 0


# гг в графической новелле
class NovelPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('pavel.png')
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 210
        self.count = 0

    def update1(self):
        self.image = load_image('pavel_p.png')

    def update2(self):
        self.rect.x -= 10

    def update3(self):
        self.image = load_image('pavel_cat.png')
        self.rect.y = 550


# сама графическая новелла
def start_novel():
    number = 0
    running = True
    time_count = 0
    all_texts = ['Павел: Наконец я изобрел портальную пушку!',
                 'Павел: Посмотрим...',
                 'Павел: Что происходит? Почему я - кот?',
                 '*Нахождение кота в портале проивело к нестабильности пространства*',
                 '*Хотите вернуть свой человеческий облик?*',
                 'Павел: Чтобы вернуть человеческий облик...',
                 'Необходимо собрать очки человечности!',
                 'Павел: Но как их заработать?',
                 'Их можно заработать, играя в игру-платформер',
                 'У Вас уже есть 200 очков, а для дальнейшего прохождения нужно 250',
                 'А так как за каждую игру Вам даются по 10 очков,',
                 'Нужно сыграть минимум 5 раз!',
                 'Павел: Значит, у меня все же получилось!',
                 'Что получилось?',
                 'Павел: Если я поменялся телом с котом, значит пространство-время...',
                 'Павел: Действительно способно изменяться',
                 'Павел: Это значит, что точно так же',
                 'Павел: Я смогу вернуться обратно!',
                 'Да, это действительно так! Только есть одна проблема...',
                 'Павел: Какая?',
                 'Это будет не так просто, учитывая что сама игра непростая',
                 'Павел: Я же преподаватель, мне все под силу!',
                 'Павел: Как в неё играть?',
                 'Как и в любой игре-платформере, в нашей есть монеты',
                 'Необходимо "добраться" до них, то есть получить.',
                 'Однако в игре есть враг, забирающий жизни.',
                 'Но даже если он доберется до Вас - волноваться не стоит!',
                 'В игре можно пополнять здоровье, собирая монеты с крестиком.',
                 'Нажав на кнопку "back", Вы сможете перейти на начальный экран',
                 'Затем нажмите на "play", и играйте. Удачи!']
    cat = Cat()
    cat.rect.x = 0
    portal = Portal()
    table = AskingTable()
    table.rect.x = 0
    table.rect.y = SCREEN_HEIGHT - 150
    clock = pygame.time.Clock()
    back_btn = Button('back')
    back_btn.rect.x = 10
    back_btn.rect.y = 10
    btn_y = Button('yes')
    btn_n = Button('no')
    btn_y.kill()
    btn_n.kill()
    text1 = Text(all_texts[0], 40, (220, 220, 220))
    text1.rect.x = 10
    text1.rect.y = SCREEN_HEIGHT - 140
    move = False
    player = NovelPlayer()
    while running:
        if number <= 3:
            screen.fill((185, 187, 163))
        else:
            screen.fill((40, 0, 81))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if back_btn.pressed(pygame.mouse.get_pos()):
                    running = False
                    for sprite in all_sprites:
                        sprite.kill()
                    start_screen()
                elif btn_y.pressed(pygame.mouse.get_pos()):
                    btn_n.kill()
                    btn_y.kill()
                    number += 1
                elif btn_n.pressed(pygame.mouse.get_pos()):
                    sys.exit()
                else:
                    if number == 1 or number == 0:
                        number += 1
                    elif number == 2:
                        player.update1()
                        number += 1
                    elif number == 3:
                        move = True
                        text1.kill()
                        text1 = Text(all_texts[1], 40, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                    elif number == 4:
                        text1.kill()
                        text1 = Text(all_texts[3], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 5:
                        text1.kill()
                        text1 = Text(all_texts[4], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        btn_y = Button('yes')
                        btn_y.rect.x = 300
                        btn_y.rect.y = 10
                        btn_n = Button('no')
                        btn_n.rect.x = 600
                        btn_n.rect.y = 10
                    elif number == 6:
                        text1.kill()
                        text1 = Text(all_texts[5], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 7:
                        text1.kill()
                        text1 = Text(all_texts[6], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 8:
                        text1.kill()
                        text1 = Text(all_texts[7], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 9:
                        text1.kill()
                        text1 = Text(all_texts[8], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 10:
                        text1.kill()
                        text1 = Text(all_texts[9], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 11:
                        text1.kill()
                        text1 = Text(all_texts[10], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 12:
                        text1.kill()
                        text1 = Text(all_texts[11], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 13:
                        text1.kill()
                        text1 = Text(all_texts[12], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 14:
                        text1.kill()
                        text1 = Text(all_texts[13], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 15:
                        text1.kill()
                        text1 = Text(all_texts[14], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 16:
                        text1.kill()
                        text1 = Text(all_texts[15], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 17:
                        text1.kill()
                        text1 = Text(all_texts[16], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 18:
                        text1.kill()
                        text1 = Text(all_texts[17], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 19:
                        text1.kill()
                        text1 = Text(all_texts[18], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 20:
                        text1.kill()
                        text1 = Text(all_texts[19], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 10:
                        text1.kill()
                        text1 = Text(all_texts[9], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 21:
                        text1.kill()
                        text1 = Text(all_texts[20], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 22:
                        text1.kill()
                        text1 = Text(all_texts[21], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 23:
                        text1.kill()
                        text1 = Text(all_texts[22], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 24:
                        text1.kill()
                        text1 = Text(all_texts[23], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 25:
                        text1.kill()
                        text1 = Text(all_texts[24], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 26:
                        text1.kill()
                        text1 = Text(all_texts[25], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 27:
                        text1.kill()
                        text1 = Text(all_texts[26], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 28:
                        text1.kill()
                        text1 = Text(all_texts[27], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 29:
                        text1.kill()
                        text1 = Text(all_texts[28], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
                    elif number == 30:
                        text1.kill()
                        text1 = Text(all_texts[29], 30, (220, 220, 220))
                        text1.rect.x = 10
                        text1.rect.y = SCREEN_HEIGHT - 140
                        number += 1
        if move and player.rect.x >= 350:
            player.update2()
            cat.rect.x += 7
        elif move:
            move = False
            player.update3()
            text1.kill()
            portal.kill()
            cat.kill()
            text1 = Text(all_texts[2], 40, (220, 220, 220))
            text1.rect.x = 10
            text1.rect.y = SCREEN_HEIGHT - 140
            number += 1
        clock.tick(30)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        pygame.display.flip()


# начало игры
def start_game():
    global all_sprites_here
    started_screen()
    start_game1()
    game_over_screen()
    all_sprites_here = []
    if money < 250:
        start_screen()
    else:
        end_screen()


# начало описания игры
def start_description():
    running = True

    start_btn = Button('story')
    start_btn.rect.x = 100
    start_btn.rect.y = 100

    back_btn = Button('back')
    back_btn.rect.x = 100
    back_btn.rect.y = 200

    text_ins0 = 'Эта новелла о преподавателе, который превратился в кота'
    text_ins1 = 'Также к ней предлагается мини-игра, предназначенная для'
    text_ins2 = 'заработка очков внутри игры и  продвижения сюжета.'
    text_inside0 = Text(text_ins0, 26, (32, 12, 11))
    text_inside0.rect.x = 250
    text_inside0.rect.y = 100
    text_inside1 = Text(text_ins1, 26, (32, 12, 11))
    text_inside1.rect.x = 250
    text_inside1.rect.y = 140
    text_inside2 = Text(text_ins2, 26, (32, 12, 11))
    text_inside2.rect.x = 250
    text_inside2.rect.y = 180

    clock = pygame.time.Clock()
    while running:
        fon = pygame.transform.scale(load_image('description_bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.pressed(pygame.mouse.get_pos()):
                    running = False
                    start_btn.kill()
                    back_btn.kill()
                    text_inside0.kill()
                    text_inside1.kill()
                    text_inside2.kill()
                    start_novel()

                elif back_btn.pressed(pygame.mouse.get_pos()):
                    running = False
                    start_btn.kill()
                    text_inside0.kill()
                    text_inside1.kill()
                    text_inside2.kill()
                    back_btn.kill()
                    start_screen()
        clock.tick(30)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        pygame.display.flip()


# экран в конце игры
def end_screen():
    fon = pygame.transform.scale(load_image('congratulations.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
    run_ss = True
    pygame.display.set_caption('Game Over')
    clock = pygame.time.Clock()

    while run_ss:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_ss = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(30)


# стартовое окно с меню, кнопками итд
def start_screen():
    run = True

    start_btn = Button('story')
    start_btn.rect.x = 100
    start_btn.rect.y = 100

    desc_btn = Button('description')
    desc_btn.rect.x = 100
    desc_btn.rect.y = 200

    game_btn = Button('play')
    game_btn.rect.x = 100
    game_btn.rect.y = 300

    text_ins0 = f'Очки человечности: {money}'
    text_inside0 = Text(text_ins0, 26, (32, 12, 11))
    text_inside0.rect.x = 250
    text_inside0.rect.y = 100

    clock = pygame.time.Clock()
    while run:
        fon = pygame.transform.scale(load_image('empty.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.pressed(pygame.mouse.get_pos()):
                    run = False
                    start_btn.kill()
                    desc_btn.kill()
                    game_btn.kill()
                    text_inside0.kill()
                    start_novel()
                elif desc_btn.pressed(pygame.mouse.get_pos()):
                    run = False
                    start_btn.kill()
                    desc_btn.kill()
                    game_btn.kill()
                    text_inside0.kill()
                    start_description()
                elif game_btn.pressed(pygame.mouse.get_pos()):
                    run = False
                    start_btn.kill()
                    desc_btn.kill()
                    game_btn.kill()
                    text_inside0.kill()
                    start_game()
        clock.tick(30)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
