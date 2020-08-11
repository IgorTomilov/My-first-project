import pygame
import sys
import random
import time


class Game():
    def __init__(self):
        # Розмір екрану
        self.screen_width = 720
        self.screen_height = 460


        self.DISPLAYSURF = pygame.display.set_mode((self.screen_width,self.screen_height))

        # Кольора
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        self.darcgrey = pygame.Color( 40, 40, 40)

        # Кількість кадрів в секунду
        self.fps_controller = pygame.time.Clock()

        # Змінна результату
        # (скільки ми зїли яблук)
        self.score = 0

    def init_and_check_for_errors(self):
        """Початкова функція яка інсталює і перевіряє
           як запускається pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        """Задаєм surface(поверхність по якій буде все малюватись)
        і встановлюємо заголовок вікна"""
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('My first Game')

    def event_loop(self, change_to):
        """Функція для керування змійкою за допомогою клавіш"""
        # запускаем цикл по івентах
        for event in pygame.event.get():
           # якщо натиснути клавішу
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                # нитиснули escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to


    def refresh_screen(self):
        """Обновляєм екран і задаєм фпс"""
        pygame.display.flip()
        game.fps_controller.tick(10)

    def draw_Grid(self):
        for x in range(10, 720, 10):
            pygame.draw.rect(self.DISPLAYSURF, self.darcgrey, (x, 0, 1, 720))

        for y in range(10, 720, 10):
            pygame.draw.rect(self.DISPLAYSURF, self.darcgrey, (0, y, 720, 1))

        pygame.draw.rect(self.DISPLAYSURF, (self.red), (1, 1, 718, 458), 16)


    def show_score(self, choice=1):
        """Відображення результату гри"""
        s_font = pygame.font.SysFont('monaco', 25)
        s_surf = s_font.render('Score: {0}'.format(self.score), True, self.white)
        s_rect = s_surf.get_rect()
        # відображення результату зліва зверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_overe відображаєм результат по центру
        # під написом game over
        else:
            s_rect.midtop = (360, 120)
        # малюєм прямокутник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        """Функція для виведення напису Game Over і результату
        в випадку завершення гри чи виходу з неї"""
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()


class Snake():
    def __init__(self, snake_color):
        # позиція голови і тіла змійки
        self.snake_head_pos = [100, 50]  # [x, y]
        # голова змії - перший елемент, хвіст - останній
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # напрямок руху змійки, початково рух в право
        self.direction = "RIGHT"
        # як буде змінюватись рух змійки
        self.change_to = self.direction

    def validate_direction_and_change(self):
        """Змінюєм рух змійки лише в тому випадку, якщо
        рух рівний протилежному"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Змінюємо положення голови змійки"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):

        self.snake_body.insert(0, list(self.snake_head_pos))
        # коли зїли яблуко
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # якщо зіїли яблуко задаєм для нього наступне випадкове положення
            # збільшуємо score на один
            food_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]
            score += 1
        else:
            # якщо не знайшли яблуко, то забераємо останній сегмент,
            # для того щоб змія постійно не збільшувалась
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        """Відображення усіх сегментів змії"""
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        """Перевірка, що змія зіткнулась з рамками екрану або самою з собою"""
        if any((
            self.snake_head_pos[0] > screen_width-20
            or self.snake_head_pos[0] < 10,
            self.snake_head_pos[1] > screen_height-20
            or self.snake_head_pos[1] < 10
            )):
            game_over()
        for block in self.snake_body[1:]:
            # перевірка щоб якщо перший елемент(голова) врізалась в
            # інший елемент змії
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()

class Food():
    def __init__(self, food_color, screen_width, screen_height):
        """Ініт яблука"""
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                         random.randrange(1, screen_height/10)*10]

    def draw_food(self, play_surface):
        """Відображення яблука"""
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(game.green)
food = Food(game.brown, game.screen_width, game.screen_height)


game.init_and_check_for_errors()
game.set_surface_and_title()

while True:
    snake.change_to = game.event_loop(snake.change_to)

    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.black)
    game.draw_Grid()


    food.draw_food(game.play_surface)

    snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)


    game.show_score()
    game.refresh_screen()