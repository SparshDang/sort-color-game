import pygame
import random

pygame.init()

COLOR_DICT = {
    1: (0, 0, 255),
    2: (0, 255, 0),
    3: (0, 255, 255),
    4: (255, 0, 0),
    5: (255, 0, 255),
    6: (255, 255, 0),
}

HEIGHT = 200
WIDTH = 400

CIRCLE_RADIUS = 20
CENTER_GAP = 2*CIRCLE_RADIUS + 10
FIRST_CENTER = (WIDTH//2 - len(COLOR_DICT)*CIRCLE_RADIUS -
                (len(COLOR_DICT)-1)*5)+CIRCLE_RADIUS
CORRECT_BOX_TOP = HEIGHT//2 + CIRCLE_RADIUS + 10


class Game:
    def __init__(self):
        self.game_running = True
        self.answer = None
        self.current = None
        self.correct = 0
        self.circles = []

        self.selected = None

        pygame.display.set_caption("Sort The Color")
        self.game_window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont(None, 55)

        self.__setup_game()
        self.__check_correct()
        self.__game_loop()

    def __setup_game(self):
        self.answer = list(COLOR_DICT.keys())
        random.shuffle(self.answer)

        self.current = list(COLOR_DICT.keys())
        random.shuffle(self.current)

    def __check_correct(self):
        self.correct = 0
        for i, j in zip(self.current, self.answer):
            if i == j:
                self.correct += 1

    def __game_loop(self):
        while self.game_running:
            self.__handle_events()
            self.__fill_screen()
            if self.__is_won():
                self.__show_win()
                self.__show_play_again()
            else:
                self.__show_correct()
                self.__show_colors()
            self.__show_title()

            pygame.display.update()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.__is_won():
                    self.__handle_selection(event)
                else:
                    if self.play_again_rect.collidepoint(event.pos):
                        self.__setup_game()


    def __is_won(self):
        return self.current == self.answer

    def __handle_selection(self, event):
        pos = event.pos
        for index, circle in enumerate(self.circles):
            if circle.collidepoint(pos):
                if self.selected is None:
                    self.selected = index
                else:
                    self.current[self.selected], self.current[index] = self.current[index], self.current[self.selected]
                    self.selected = None
                    self.__check_correct()

    def __fill_screen(self):
        self.game_window.fill((0, 0, 0))

    def __show_win(self):
        rendered_text = self.font.render(f"You Won", True, (255, 0, 0))
        text_box = rendered_text.get_bounding_rect()
        text_box.centerx = WIDTH//2
        text_box.centery = HEIGHT//2

        self.game_window.blit(rendered_text, text_box)

    def __show_play_again(self):
        rendered_text = self.font.render(f"Play Again", True, (255, 255, 0))
        text_box = rendered_text.get_bounding_rect()
        text_box.centerx = WIDTH//2
        text_box.bottom = HEIGHT-30

        rect_width = text_box.width+20
        rect_height = text_box.height+20
        self.play_again_rect = pygame.rect.Rect(0, 0, 0, 0)
        self.play_again_rect.width = rect_width
        self.play_again_rect.height = rect_height
        self.play_again_rect.centerx = WIDTH//2
        self.play_again_rect.bottom = HEIGHT-20

        pygame.draw.rect(self.game_window, (255, 255, 0),
                         self.play_again_rect, 5)
        self.game_window.blit(rendered_text, text_box)

    def __show_correct(self):
        rendered_text = self.font.render(
            f"Correct : {self.correct}", True, (255, 0, 0))
        text_box = rendered_text.get_bounding_rect()
        text_box.centerx = WIDTH//2
        text_box.bottom = HEIGHT-20

        self.game_window.blit(rendered_text, text_box)

    def __show_colors(self):
        self.circles = []
        for index, num in enumerate(self.current):
            if self.selected == index:
                pygame.draw.circle(self.game_window, (255, 255, 255),
                                   (index*CENTER_GAP + FIRST_CENTER, HEIGHT//2), CIRCLE_RADIUS+5)
            circle = pygame.draw.circle(self.game_window, COLOR_DICT[num], (
                index*CENTER_GAP + FIRST_CENTER, HEIGHT//2), CIRCLE_RADIUS)
            self.circles.append(circle)

    def __show_title(self):
        rendered_text = self.font.render(
            f"Sort The Colors", True, (255, 255, 0))
        text_box = rendered_text.get_bounding_rect()
        text_box.centerx = WIDTH//2
        text_box.top = 20

        self.game_window.blit(rendered_text, text_box)


if __name__ == "__main__":
    Game()
