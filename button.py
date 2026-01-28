from settings import *

#mouse_x, mouse_y = pygame.mouse.get_pos()
#holding_mouse = False

font = pygame.font.Font(None, 36)

default_button_height = 50

buttons = []


class Button:
    # global mouse_x, mouse_y
    # global holding_mouse
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # holding_mouse = False

    

    def __init__(self, x, y, text, width=default_button_height, height=default_button_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = text

        self.font_size = get_perfect_font_size(text, pygame.Rect(x, y, width-4, height-4))
        # self.font_size = 5
        self.font = pygame.font.SysFont('Arial', self.font_size)

        self.border_size = 5
        self.shadow_size = 5

        black = (0, 0, 0)

        self.border_color = black
        self.fill_color = (220, 220, 220)
        self.text_color = black

        self.selected_color = (150, 150, 150)
        self.normal_color = self.fill_color
        self.pressed_color = (100, 80, 100)

        shadow_intensity = 20

        self.bright_color = (
            self.fill_color[0] + shadow_intensity,
            self.fill_color[1] + shadow_intensity,
            self.fill_color[2] + shadow_intensity,
        )

        self.dark_color = (
            self.fill_color[0] - shadow_intensity,
            self.fill_color[1] - shadow_intensity,
            self.fill_color[2] - shadow_intensity,
        )

        self.already_pressed = False


        self.mouse_x = 0
        self.mouse_y = 0
        self.holding_mouse = False

        buttons.append(self)


    def get_mouse_signal(self, mouse_x, mouse_y, holding_mouse):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.holding_mouse = holding_mouse

    def change_color(self, color):
        self.fill_color = color
        #self.text_color = text_color

        shadow_intensity = 20

        self.bright_color = (
            self.fill_color[0] + shadow_intensity,
            self.fill_color[1] + shadow_intensity,
            self.fill_color[2] + shadow_intensity,
        )

        self.dark_color = (
            self.fill_color[0] - shadow_intensity,
            self.fill_color[1] - shadow_intensity,
            self.fill_color[2] - shadow_intensity,
        )

    def mouse_in_area(self):
        if self.mouse_x >= self.x and self.mouse_x <= self.x + self.width:
            if self.mouse_y >= self.y and self.mouse_y <= self.y + self.height:
                return True
        return False

    def got_pressed(self):
        if self.holding_mouse and self.mouse_in_area():
            return True
        return False

    def check_for_presses(self):
        if self.got_pressed() and not self.already_pressed:
            self.change_color(self.pressed_color)
            self.already_pressed = True
            print('naciskam i ustawiam na true')
        elif self.mouse_in_area():
            self.change_color(self.selected_color)
            #print("Mouse in area")
        else:
            self.change_color(self.normal_color)

        if not self.holding_mouse:
            self.already_pressed = False
            print('puszczona wiec ustawiam na false')

    def draw(self):
        if self.got_pressed():
            self.change_color(self.pressed_color)
        elif self.mouse_in_area():
            self.change_color(self.selected_color)
        else:
            self.change_color(self.normal_color)

        border_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        fill_width = self.width - 2 * self.border_size
        fill_height = self.height - 2 * self.border_size

        fill_rect = pygame.Rect(
            self.x + self.border_size, self.y + self.border_size, fill_width, fill_height
        )

        shadow_bright_rect_horizontal = pygame.Rect(
            self.x + self.border_size,
            self.y + self.border_size,
            fill_width,
            self.shadow_size,
        )
        shadow_bright_rect_vertical = pygame.Rect(
            self.x + self.border_size,
            self.y + self.border_size,
            self.shadow_size,
            fill_height,
        )

        shadow_dark_rect_horizontal = pygame.Rect(
            self.x + self.border_size,
            self.y + self.border_size + fill_height - self.shadow_size,
            fill_width,
            self.shadow_size,
        )
        shadow_dark_rect_vertical = pygame.Rect(
            self.x + self.border_size + fill_width - self.shadow_size,
            self.y + self.border_size,
            self.shadow_size,
            fill_height,
        )

        pygame.draw.rect(screen, self.border_color, border_rect)
        pygame.draw.rect(screen, self.fill_color, fill_rect)

        pygame.draw.rect(screen, self.bright_color, shadow_bright_rect_horizontal)
        pygame.draw.rect(screen, self.bright_color, shadow_bright_rect_vertical)

        pygame.draw.rect(screen, self.dark_color, shadow_dark_rect_horizontal)
        pygame.draw.rect(screen, self.dark_color, shadow_dark_rect_vertical)


        # font = pygame.font.SysFont('Arial', get_perfect_font_size(self.text))
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        # text_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # text_rect.center=(self.x + self.width // 2, self.y + self.height // 2)
        screen.blit(text_surface, text_rect)

    def update(self, xmouse, ymouse, holding_mouse):
        self.get_mouse_signal(xmouse, ymouse, holding_mouse)
        self.check_for_presses()
