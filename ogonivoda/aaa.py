import pygame

# Переменные для установки ширины и высоты окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

# Подключение фото для заднего фона
# Здесь лишь создание переменной, вывод заднего фона ниже в коде
bg = pygame.image.load('bg.jpg')


# Класс, описывающий поведение главного игрока
class Character(pygame.sprite.Sprite):
    # Изначально игрок смотрит вправо, поэтому эта переменная True
    right = True

    # Методы
    def __init__(self):
        # Стандартный конструктор класса
        # Нужно ещё вызывать конструктор родительского класса
        super().__init__()

        # Создаем изображение для игрока
        # Изображение находится в этой же папке проекта
        self.image = pygame.image.load('idle.png')

        # Установите ссылку на изображение прямоугольника
        self.rect = self.image.get_rect()

        # Задаем вектор скорости игрока
        self.change_x = 0
        self.change_y = 0


        self.in_air = True

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

        dead_blocks = pygame.sprite.spritecollide(self, self.level.dead_block_list, False)
        for block in dead_blocks:
            # Перезапуск уровня при попадании на мертвые кубы
            # Здесь можно добавить любую логику перезапуска уровня
            # Например:
            self.rect.x = 50
            self.rect.y = 500
            self.change_x = 0
            self.change_y = 0

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
        # или другими словами, не находимся ли мы в полете.
        # Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -15

    # Передвижение игрока
    def go_left(self):
        if self.in_air:
            self.change_x = -4  # Изменение скорости при движении в воздухе
        else:
            self.change_x = -8

        if self.right:
            self.flip()
            self.right = False

    def go_right(self):
        if self.in_air:
            self.change_x = 4  # Изменение скорости при движении в воздухе
        else:
            self.change_x = 8

        if not self.right:
            self.flip()
            self.right = True


    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.change_x = 0

    def flip(self):
        # переворот игрока (зеркальное отражение)
        self.image = pygame.transform.flip(self.image, True, False)



class Character1(Character):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('idle.png')

class Character2(Character):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('idle2.png')


# Класс для описания платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        # Конструктор платформ
        super().__init__()
        # Также указываем фото платформы
        self.image = pygame.image.load(image_path)

        # Установите ссылку на изображение прямоугольника
        self.rect = self.image.get_rect()


# Класс для расстановки платформ на сцене
class Level(object):
    def __init__(self, player, player2):
        # Создаем группу спрайтов (поместим платформы различные сюда)
        self.platform_list = pygame.sprite.Group()
        self.dead_block_list = pygame.sprite.Group()
        # Ссылка на основного игрока
        self.player = player
        self.player2 = player2

    # Чтобы все рисовалось, то нужно обновлять экран
    # При вызове этого метода обновление будет происходить
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


# Класс, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_01(Level):
    def __init__(self, player, player2):
        # Вызываем родительский конструктор
        Level.__init__(self, player, player2)

        # Массив с данными про платформы (разметка уровня)
        level = [
            "-------------------------",
            "-                       -",
            "-                       -",
            "-                       -",
            "-            --         -",
            "-                       -",
            "--                      -",
            "-                       -",
            "-                   --- -",
            "-                       -",
            "-                       -",
            "-      ---              -",
            "-                       -",
            "-   -----------         -",
            "-                       -",
            "-                -      -",
            "-                ddd--  -",
            "-                       -",
            "-                       -",
            "-------------------------"
        ]

        # Размеры блоков
        block_width = 32
        block_height = 32

        # Перебираем каждую строку в массиве level
        for row_idx, row in enumerate(level):
            for col_idx, col in enumerate(row):
                # Если символ в разметке level - "-", то создаем блок платформы
                if col == "-":
                    block = Platform(block_width, block_height, 'platform.png')
                    block.rect.x = col_idx * block_width
                    block.rect.y = row_idx * block_height
                    block.player = self.player
                    block.player2 = self.player2
                    self.platform_list.add(block)
        self.dead_block_list = pygame.sprite.Group()

        # Перебираем каждую строку в массиве level
        for row_idx, row in enumerate(level):
            for col_idx, col in enumerate(row):
                # Если символ в разметке level - "d", то создаем мертвый куб
                if col == "d":
                    dead_block = Platform(block_width, block_height, 'sliz.png')
                    dead_block.rect.x = col_idx * block_width
                    dead_block.rect.y = row_idx * block_height
                    dead_block.player = self.player
                    dead_block.player2 = self.player2
                    self.dead_block_list.add(dead_block)



# Основная функция прогарммы
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
    player.rect.y = 500
    player2.rect.x = 50
    player2.rect.y = 500
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

    # Корректное закртытие программы
    pygame.quit()
main()
