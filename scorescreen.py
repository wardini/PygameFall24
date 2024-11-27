import pygame
from txt_item import Txt_item

class ScoreScreen:
    def __init__(self,glbls):
        self.glbls = glbls
        self.quit = False
        self.done = False
        self.next_state = 'GamePlay'

        self.T_Back = Txt_item('Back',(550,700),selectable=True,action='back')

    def startup(self):
        gp = self.glbls['STATES']['GamePlay']

        # create high score texts
        self.T_hs = Txt_item('Bests       Paid  Lost Bonus Total',(400,40),font='courier')

        self.T_lscores = []
        total_total = 0
        for i in range(len(gp.levels)):
            best_paid = f'${gp.levels[i].best_paid:<}'
            best_lost = f'${gp.levels[i].best_lost:<}'
            if gp.levels[i].best_paid > 0 and gp.levels[i].best_lost == 0:
                vbonus = 10*max(gp.levels[i].nom_time - gp.levels[i].best_del_time,0)
                best_bonus = f'${vbonus:<}'
            else:
                best_bonus = f'{0:>5d}'
            total_total += gp.levels[i].best_total
            best_total = f'${gp.levels[i].best_total:<}'
            btext = f'{best_paid:>5} {best_lost:>5} {best_bonus:>5} {best_total:>5}'
            self.T_lscores.append(Txt_item(f'Level {i+1:>2d}: {btext}',(400,70+25*i),font='courier'))


        self.liney = 70+25*(i+1) + 2
        total_text = f'${total_total:<}'
        self.T_score = Txt_item(f'Total: {total_text:>25}',(400,2+70+25*(i+1)),font='courier')


    def process_event(self,event):
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.T_Back.check_select(event.pos):
                self.done = True

    def update(self,dt):
        pass

    def draw(self,window):
        window.fill(pygame.Color("black"))

        self.T_hs.render(window)
        pygame.draw.line(window,pygame.Color("white"),(370,67),(1000,67),width=2)
        for t in self.T_lscores:
            t.render(window)
        pygame.draw.line(window,pygame.Color("white"),(370,self.liney),(1000,self.liney),width=2)
        self.T_score.render(window)
        self.T_Back.render(window)
