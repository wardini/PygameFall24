import pygame

class Txt_item():
    def __init__(self,txt,position,selectable=False,action='',fontsize=28,location="topleft",font='default'):
        self.text = txt
        self.position = position
        self.selectable = selectable
        self.action = action
        self.location = location
        if font == 'default':
            self.font = pygame.font.SysFont('timesnewroman',fontsize)
        else:
            self.font = pygame.font.SysFont(font,fontsize)
        self.change_text(self.text)
        self.disabled = False
        
    def change_text(self,txt):
        self.text = txt
        self.text_surface = self.font.render(self.text, True, pygame.Color("white"))
        if self.location == "topleft":
            self.rect = self.text_surface.get_rect(topleft=(self.position))
        elif self.location == "center":
            self.rect = self.text_surface.get_rect(center=(self.position))
        self.sel_rect = pygame.Rect(self.rect[0]-4,self.rect[1]-4,self.rect[2]+8,self.rect[3]+4)

    def render(self,screen):
        screen.blit(self.text_surface,self.rect)
        if self.selectable:
            if self.disabled:
                pygame.draw.rect(screen, pygame.Color("gray20"),self.sel_rect,2)
            else:
                pygame.draw.rect(screen, pygame.Color("white"),self.sel_rect,2)

    def highlight(self,screen):
        pygame.draw.rect(screen, pygame.Color("orange"),self.sel_rect,3)

    def disable_click(self):
        self.text_surface = self.font.render(self.text, True, pygame.Color("gray20"))
        self.rect = self.text_surface.get_rect(topleft=(self.position))
        self.disabled = True

    def enable_click(self):
        self.text_surface = self.font.render(self.text, True, pygame.Color("white"))
        self.rect = self.text_surface.get_rect(topleft=(self.position))
        self.disabled = False

    def check_select(self,pos):
        if self.selectable and not self.disabled:
            return self.sel_rect.collidepoint(pos)
        else:
            return False
