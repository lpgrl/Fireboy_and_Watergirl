import pygame

# Переменные для установки ширины и высоты окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

# Подключение фото для заднего фона
bg = pygame.image.load('bg.png')

class Character(pygame.sprite.Sprite):
    # Методы
    def __init__(self, idle_image, move_images):
        super().__init__()

        # Загрузка изображений
        self.idle_image = pygame.image.load(idle_image)
        self.move_images = [pygame.image.load(img) for img in move_images]
        self.image = self.idle_image

        self.rect = self.image.get_rect()

        # Задаем вектор скорости игрока
        self.change_x = 0
        self.change_y = 0

        self.in_air = True

        # Дополнительные переменные для анимации
        self.move_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Скорость смены кадров анимации

    def update(self):
        # В этой функции мы передвигаем игрока
        # Сперва устанавливаем для него гравитацию
        self.calc_grav()

        # Передвигаем его на право/лево
        # change_x будет меняться позже при нажатии на стрелочки клавиатуры
        self.rect.x += self.change_x

        # Следим ударяем ли мы какой-то другой объект, платформы, например
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # Перебираем все возможные объекты, с которыми могли бы столкнуться
        for block in block_hit_list:
            # Если мы идем направо,
            # устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # В противном случае, если мы движемся влево, то делаем наоборот
                self.rect.left = block.rect.right

        # Передвигаемся вверх/вниз
        self.rect.y += self.change_y

        # То же самое, вот только уже для вверх/вниз
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Останавливаем вертикальное движение
            self.change_y = 0

        # Проверка на нахождение в воздухе
        self.rect.y += 2  # Смещение немного вниз
        platforms = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2  # Возвращаемся обратно

        # Если нет коллизий, игрок в воздухе
        self.in_air = not bool(platforms)

        water_blocks = pygame.sprite.spritecollide(self, self.level.water_block_list, False)
        fire_blocks = pygame.sprite.spritecollide(self, self.level.fire_block_list, False)
        win_blocks = pygame.sprite.spritecollide(self, self.level.win_list, False)
        dead_blocks = pygame.sprite.spritecollide(self, self.level.dead_block_list, False)

        for block in dead_blocks:
            self.rect.x = 50
            self.rect.y = 585
            self.change_x = 0
            self.change_y = 0

            self.level.player2.rect.x = 50
            self.level.player2.rect.y = 585
            self.level.player2.change_x = 0
            self.level.player2.change_y = 0

            self.level.player.rect.x = 50
            self.level.player.rect.y = 585
            self.level.player.change_x = 0
            self.level.player.change_y = 0

        if water_blocks and self is self.level.player:
            self.level.player.rect.x = 50
            self.level.player.rect.y = 585
            self.level.player.change_x = 0
            self.level.player.change_y = 0

            self.level.player2.rect.x = 50
            self.level.player2.rect.y = 585
            self.level.player2.change_x = 0
            self.level.player2.change_y = 0

        elif fire_blocks and self is self.level.player2:
            self.level.player.rect.x = 50
            self.level.player.rect.y = 585
            self.level.player.change_x = 0
            self.level.player.change_y = 0

            self.level.player2.rect.x = 50
            self.level.player2.rect.y = 585
            self.level.player2.change_x = 0
            self.level.player2.change_y = 0

        # Обновление анимации
        now = pygame.time.get_ticks()
        if self.change_x < 0:  # Если игрок движется влево
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.move_frame = (self.move_frame + 1) % len(self.move_images)
                self.image = self.move_images[self.move_frame]
        elif self.change_x > 0:  # Если игрок движется вправо
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.move_frame = (self.move_frame + 1) % len(self.move_images)
                self.image = self.move_images_right[self.move_frame]
        else:  # Если игрок стоит
            self.image = self.idle_image

    def calc_grav(self):
        # Здесь мы вычисляем как быстро объект будет
        # падать на землю под действием гравитации
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # Обработка прыжка
        # Нам нужно проверять здесь, контактируем ли мы с чем-либо
        # Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -12

    # Передвижение игрока
    def go_left(self):
        if self.in_air:
            self.change_x = -4  # Изменение скорости при движении в воздухе
        else:
            self.change_x = -8

    def go_right(self):
        if self.in_air:
            self.change_x = 4  # Изменение скорости при движении в воздухе
        else:
            self.change_x = 8

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.change_x = 0

# Класс Character1
class Character1(Character):
    def __init__(self):
        super().__init__('ogon/fire.png', ['ogon/fire_left_1.png', 'ogon/fire_left_2.png', 'ogon/fire_left_3.png', 'ogon/fire_left_4.png'])
        self.move_images_right = [pygame.image.load(img) for img in ['ogon/fire_right_1.png', 'ogon/fire_right_2.png', 'ogon/fire_right_3.png', 'ogon/fire_right_4.png']]

# Класс Character2
class Character2(Character):
    def __init__(self):
        super().__init__('voda/water.png', ['voda/water_left_1.png', 'voda/water_left_2.png', 'voda/water_left_3.png', 'voda/water_left_4.png'])
        self.move_images_right = [pygame.image.load(img) for img in ['voda/water_right_1.png', 'voda/water_right_2.png', 'voda/water_right_3.png', 'voda/water_right_4.png']]

class WaterBlock(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

class FireBlock(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

class DeathBlock(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

class WinBlock(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

# Класс для описания платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

# Класс для расстановки платформ на сцене
class Level(object):
    def __init__(self, player, player2):
        # Создаем группу спрайтов (поместим платформы различные сюда)
        self.platform_list = pygame.sprite.Group()

        self.player = player
        self.player2 = player2

    def update(self):
        self.platform_list.update()
        self.dead_block_list.update()
        self.player2.update()

    # Метод для рисования объектов на сцене
    def draw(self, screen):
        # Рисуем задний фон
        screen.blit(bg, (0, 0))

        # Рисуем все платформы из группы спрайтов
        self.platform_list.draw(screen)
        self.dead_block_list.draw(screen)
        self.water_block_list.draw(screen)
        self.fire_block_list.draw(screen)
        self.win_list.draw(screen)


# Класс, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_01(Level):
    def __init__(self, player, player2):
        # Вызываем родительский конструктор
        Level.__init__(self, player, player2)

        # Массив с данными про платформы (разметка уровня)
        level = [
            "--------------------------------------------------",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-            --                                  -",
            "-                                                -",
            "--                                               -",
            "-                                                -",
            "-                    ---                         -",
            "-                                                -",
            "-                                                -",
            "-                               ---              -",
            "-                                                -",
            "-   ---- -------                                 -",
            "-                                                -",
            "-                                         -      -",
            "-                                         ddd--  -",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-                                    --          -",
            "-               -------                          -",
            "--                                               -",
            "-         ---                                    -",
            "-               -                           ---  -",
            "-                      ------                    -",
            "-               --                               -",
            "---GGG-----------------------------------        -",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "-                                              ---",
            "-                                                -",
            "-                                                -",
            "-                                                -",
            "--------------wWWWWWV----ddd----fFFFFFFP-----------"
        ]

        # Размеры блоков
        block_width = 16
        block_height = 16

        self.water_block_list = pygame.sprite.Group()
        self.fire_block_list = pygame.sprite.Group()
        self.dead_block_list = pygame.sprite.Group()
        self.win_list = pygame.sprite.Group()

        # Перебираем каждую строку в массиве level
        for row_idx, row in enumerate(level):
            for col_idx, col in enumerate(row):
                if col == "-":
                    block = Platform(block_width, block_height, 'platform.png')
                    block.rect.x = col_idx * block_width
                    block.rect.y = row_idx * block_height
                    block.player = self.player
                    block.player2 = self.player2
                    self.platform_list.add(block)
                elif col == "W":
                    water_block = WaterBlock(block_width, block_height, 'vodichka/water.png')
                    water_block.rect.x = col_idx * block_width
                    water_block.rect.y = row_idx * block_height
                    self.water_block_list.add(water_block)
                elif col == "w":
                    water_block = WaterBlock(block_width, block_height, 'vodichka/water_left.png')
                    water_block.rect.x = col_idx * block_width
                    water_block.rect.y = row_idx * block_height
                    self.water_block_list.add(water_block)
                elif col == "V":
                    water_block = WaterBlock(block_width, block_height, 'vodichka/water_right.png')
                    water_block.rect.x = col_idx * block_width
                    water_block.rect.y = row_idx * block_height
                    self.water_block_list.add(water_block)
                elif col == "F":
                    fire_block = FireBlock(block_width, block_height, 'lava/lava.png')
                    fire_block.rect.x = col_idx * block_width
                    fire_block.rect.y = row_idx * block_height
                    self.fire_block_list.add(fire_block)
                elif col == "f":
                    fire_block = FireBlock(block_width, block_height, 'lava/lava_left.png')
                    fire_block.rect.x = col_idx * block_width
                    fire_block.rect.y = row_idx * block_height
                    self.fire_block_list.add(fire_block)
                elif col == "P":
                    fire_block = FireBlock(block_width, block_height, 'lava/lava_right.png')
                    fire_block.rect.x = col_idx * block_width
                    fire_block.rect.y = row_idx * block_height
                    self.fire_block_list.add(fire_block)
                elif col == "d":
                    dead_block = DeathBlock(block_width, block_height, 'sliz.png')
                    dead_block.rect.x = col_idx * block_width
                    dead_block.rect.y = row_idx * block_height
                    self.dead_block_list.add(dead_block)
                elif col == "G":
                    win_block = WinBlock(block_width, block_height, 'lava/lava_right.png')
                    win_block.rect.x = col_idx * block_width
                    win_block.rect.y = row_idx * block_height
                    self.win_list.add(win_block)

    def check_win_condition(self):
        win_blocks_collided = pygame.sprite.spritecollide(self.player, self.win_list, False)
        win_blocks_collided2 = pygame.sprite.spritecollide(self.player2, self.win_list, False)
        return len(win_blocks_collided) > 0 and len(win_blocks_collided2) > 0

# Основная функция программы
def main():
    # Инициализация
    pygame.init()

    # Установка высоты и ширины
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # Название игры
    pygame.display.set_caption("Огонь и вода")

    # Создаем игрока
    player = Character1()
    player2 = Character2()

    # Устанавливаем текущий уровень

    current_level = Level_01(player,player2)

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player2.level = current_level

    player.rect.x = 50
    player.rect.y = 585
    player2.rect.x = 50
    player2.rect.y = 585
    active_sprite_list.add(player)
    active_sprite_list.add(player2)

    # Цикл будет до тех пор, пока пользователь не нажмет кнопку закрытия
    done = False

    # Используется для управления скоростью обновления экрана
    clock = pygame.time.Clock()

    # Основной цикл программы
    while not done:
        # Отслеживание действий
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Если закрыл программу, то останавливаем цикл
                done = True

            # Если нажали на стрелки клавиатуры, то двигаем объект
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            # Второй игрок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player2.go_left()
                if event.key == pygame.K_d:
                    player2.go_right()
                if event.key == pygame.K_w:
                    player2.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player2.change_x < 0:
                    player2.stop()
                if event.key == pygame.K_d and player2.change_x > 0:
                    player2.stop()
        if current_level.check_win_condition():
            print("Вы прошли игру! Поздравляем!")
            print()
            print('______________________¶¶¶')
            print('___________________¶¶¶¶¶')
            print('__________________¶¶¶¶¶¶')
            print('________________¶¶¶¶¶¶¶')
            print('_______________¶¶¶¶¶¶¶¶')
            print('_______________¶¶¶¶¶¶¶¶')
            print('______________¶¶¶¶¶¶¶¶¶¶')
            print('______________¶¶¶¶¶¶¶¶¶¶')
            print('______________¶¶¶¶¶¶¶¶¶¶¶______________¶¶¶')
            print('______________¶¶¶¶¶¶¶¶¶¶¶¶___________¶¶¶¶')
            print('_______¶______¶¶¶¶¶¶¶¶¶¶¶¶¶________¶¶¶¶¶¶')
            print('_______¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶¶______¶¶¶¶¶¶¶')
            print('_______¶¶¶¶¶___¶¶¶¶¶¶¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶')
            print('_______¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶¶¶¶¶¶¶')
            print('_______¶¶¶¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_______¶¶¶¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('______¶¶¶¶¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_____¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶¶______¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶___¶________¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_¶¶¶¶¶¶¶¶¶¶¶¶¶¶_____________¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶')
            print('_¶¶¶¶¶¶¶¶¶¶¶¶¶¶______________¶____¶¶¶¶¶¶¶¶¶¶¶')
            print('__¶¶¶¶¶¶¶¶¶¶¶¶_____________________¶¶¶¶¶¶¶¶¶')
            print('____¶¶¶¶¶¶¶¶¶¶_____________________¶¶¶¶¶¶¶¶')
            print('______¶¶¶¶¶¶¶¶_____________________¶¶¶¶¶¶')
            print('_________¶¶¶¶¶¶___________________¶¶¶¶')
            print('_____________¶¶¶¶¶______________¶')
            done = True

            # Обновляем игрока
        player.update()

        # Обновляем объекты на сцене
        current_level.update()

        # Если игрок приблизится к правой стороне, то дальше его не двигаем
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # Если игрок приблизится к левой стороне, то дальше его не двигаем
        if player.rect.left < 0:
            player.rect.left = 0

        if player2.rect.right > SCREEN_WIDTH:
            player2.rect.right = SCREEN_WIDTH

        # Если игрок приблизится к левой стороне, то дальше его не двигаем
        if player2.rect.left < 0:
            player2.rect.left = 0

        # Рисуем объекты на окне
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # Устанавливаем количество фреймов
        clock.tick(30)

        # Обновляем экран после рисования объектов
        pygame.display.flip()

    # Корректное закрытие программы
    pygame.quit()
main()


