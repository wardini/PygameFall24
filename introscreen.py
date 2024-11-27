import pygame
from txt_item import Txt_item

class IntroScreen:
    def __init__(self,glbls):
        self.glbls = glbls
        self.quit = False
        self.done = False
        self.next_state = 'GamePlay'
        #self.title_text1 = Txt_item('Contract',(self.glbls['WIDTH']//2,15),location="center",fontsize=16)
        #self.title_text2 = Txt_item('Adventure',(self.glbls['WIDTH']//2,30),location="center",fontsize=16)
        #self.instr3 = Txt_item('The Family',(self.glbls['WIDTH']//2,49),location="center")
        #self.music_txt = Txt_item('Press M for music on off',(self.glbls['WIDTH']//2,165),location="center")
        self.start_text = Txt_item('Click to start',(self.glbls['WIDTH']//2,140),location="center")
        self.yes_text = Txt_item('Agree',(self.glbls['WIDTH']//2-50,595),selectable=True,action='yes',location="center")
        self.no_text = Txt_item('No!',(self.glbls['WIDTH']//2+50,595),selectable=True,action='yes',location="center")

        self.g_contract = pygame.image.load('graphics/contract.png').convert()
        self.g_contract_yes = pygame.image.load('graphics/contract_yes.png').convert()

        #self.music = False
        #self.first_music=True

        self.s_welcome = pygame.mixer.Sound("audio/welcome.ogg")
        self.s_welcome.set_volume(0.8)

        self.s_excellent = pygame.mixer.Sound("audio/excellent.ogg")

    def startup(self):
        self.gp = self.glbls['STATES']['GamePlay']
        self.countdown = 3000
        self.state = 'start'



    #def music_on_off(self):
    #    if self.music:
    #        pygame.mixer.music.play(-1)
    #    else:
    #        pygame.mixer.music.stop()

    def process_event(self,event):
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.s_welcome.stop()
                self.done = True
            #elif event.key == pygame.K_m:
            #    self.music = not self.music
            #    self.music_on_off()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == 'start':
                self.s_welcome.play(0)
                self.start_text.change_text('Sign to start')
                self.state = 'waiting'
            elif self.state == 'waiting':
                if self.yes_text.check_select(event.pos):
                    self.state = 'checked'
                elif self.no_text.check_select(event.pos):
                    self.state = 'checked'


    def update(self,dt):
        if self.state == 'checked':
            if pygame.mixer.get_busy():
                return
            else:
                self.state = 'excellent'
                self.s_excellent.play(0)
        elif self.state == 'excellent':
            self.countdown -= dt
            if self.countdown < 0:
                self.done = True

    def draw(self,window):
        window.fill(pygame.Color("black"))

        #self.title_text1.render(window)
        #self.title_text2.render(window)

        #self.g_contract.render(window)

        #self.instr3.render(window)
        #self.music_txt.render(window)
        self.start_text.render(window)

        if self.state == 'waiting':
            self.yes_text.render(window)
            self.no_text.render(window)

        if self.state in ['start','waiting']:
            window.blit(self.g_contract,(self.glbls['WIDTH']//2-160,150,0,0),(0,0,320,420))
        elif self.state in ['checked','excellent']:
            window.blit(self.g_contract_yes,(self.glbls['WIDTH']//2-160,150,0,0),(0,0,320,420))

