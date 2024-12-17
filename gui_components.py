import pygame


class InputBox:
    def __init__(self, x, y, width, height, font_size=32, bg_color=(255, 192, 203), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("microsoftnewtailue", font_size)
        self.text = ''
        self.active = False
        self.placeholder = 'Input'
    
    def is_focused(self):
        return self.active
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.text = ""
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Return the input text when Enter is pressed.
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return None

    def draw(self, screen):
        # Draw the input box
        pygame.draw.rect(screen, self.color, self.rect)
        if self.active:
            txt_surface = self.font.render(self.text, True, self.text_color)
        else:
            if self.text:
                txt_surface = self.font.render(self.text, True, self.text_color)
            else:
                txt_surface = self.font.render(self.placeholder, True, self.text_color)
        
        # Center the text
        text_rect = txt_surface.get_rect(center=self.rect.center)
        screen.blit(txt_surface, text_rect)


class Button:
    def __init__(self, x, y, image_path, width=None, height=None, action=None):
        self.original_image = pygame.image.load(image_path)
        if width is not None and height is not None:
            self.image = pygame.transform.scale(self.original_image, (width, height))
        else:
            self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return 1


class Label:
    def __init__(self, x, y, text, font_size=36, text_color=(0, 0, 0), border_color=(255, 192, 203), border_thickness=2, is_center=0):
        self.font = pygame.font.SysFont("microsoftnewtailue", font_size)
        self.text = text
        self.text_color = text_color
        self.border_color = border_color
        self.border_thickness = border_thickness

        if is_center:
            self.rect = self.font.render(text, True, text_color).get_rect(center=(x, y))
        else:
            self.rect = self.font.render(text, True, text_color).get_rect(topleft=(x, y))

    def draw(self, surface):
        border_rect = self.rect.inflate(self.border_thickness * 2, self.border_thickness * 2)
        pygame.draw.rect(surface, self.border_color, border_rect)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, self.rect.topleft)

class ToggleButton:
    def __init__(self, x, y, image_on, image_off, width=None, height=None):
        self.image_on = pygame.transform.scale(pygame.image.load(image_on), (width, height))
        self.image_off = pygame.transform.scale(pygame.image.load(image_off), (width, height))
        self.rect = self.image_on.get_rect(topleft=(x, y))
        self.is_on = False  # 开关状态

    def draw(self, surface):
        if self.is_on:
            surface.blit(self.image_on, self.rect.topleft)
        else:
            surface.blit(self.image_off, self.rect.topleft)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.is_on = not self.is_on
            return self.is_on

class DropdownMenu:
    def __init__(self, x, y, w, h, options, place_holder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont("microsoftnewtailue", 15)
        self.color = pygame.Color('pink')
        self.options = options  # ["-1", "0", "1"]
        self.place_holder = place_holder
        self.selected = None
        self.active = False
        self.hover_index = -1

    def get_text(self):
        return self.selected if self.selected else self.place_holder

    def draw(self, screen):
        # 绘制主按钮
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.get_text(), True, pygame.Color('black'))
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

        # 如果下拉菜单被激活，绘制选项列表
        if self.active:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height,
                                        self.rect.width, self.rect.height)
                # 如果鼠标悬停在该选项上，使用白色背景
                if i == self.hover_index:
                    bg_color = pygame.Color('white')
                else:
                    bg_color = pygame.Color('gray')
                pygame.draw.rect(screen, bg_color, option_rect)
                text = self.font.render(option, True, pygame.Color('black'))
                screen.blit(text, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                # 检查是否点击了选项
                mouse_pos = event.pos
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height,
                                            self.rect.width, self.rect.height)
                    if option_rect.collidepoint(mouse_pos):
                        self.selected = option
                        self.active = False
                        return option
        
        elif event.type == pygame.MOUSEMOTION and self.active:
            # 更新鼠标悬停状态
            mouse_pos = event.pos
            self.hover_index = -1
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height,
                                        self.rect.width, self.rect.height)
                if option_rect.collidepoint(mouse_pos):
                    self.hover_index = i
                    break

        return None

class KeyMapper:
    def __init__(self):
        self.key_map = {
            pygame.K_s: 0,
            pygame.K_d: 1,
            pygame.K_f: 2,
            pygame.K_g: 3,
            pygame.K_h: 4,
            pygame.K_j: 5,
            pygame.K_k: 6,
            pygame.K_l: 7,
        }

    def get_key_value(self, event):
        if event.type == pygame.KEYDOWN:
            return self.key_map.get(event.key, None)
        return None


class Image:
    def __init__(self, x, y, image_path, width=None, height=None):
        self.original_image = pygame.image.load(image_path)
        if width is not None and height is not None:
            self.image = pygame.transform.scale(self.original_image, (width, height))
        else:
            self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def get_rect(self):
        return self.rect