import numpy as np
from spline import Spline
import pygame
from txt_item import Txt_item

def init_coords(glbls):
    size = pygame.display.Info().current_w,pygame.display.Info().current_h
    cx,cy = int(0.5*size[0]),int(0.5*size[1])
    grid_rect = pygame.Rect(cx-32*8,cy-32*8,64*8,64*8)
    play_rect = pygame.Rect(cx-36*8,cy-36*8,72*8,72*8)
    port_rect = pygame.Rect(cx-36*8+10,cy-36*8+10,72*8-20,72*8-20)
    glbls["grid_rect"] = grid_rect
    glbls["play_rect"] = play_rect
    glbls["port_rect"] = port_rect

def get_playing_surface(glbls,vel_group,ds,inports,nom_time):
    size = pygame.display.Info().current_w,pygame.display.Info().current_h
    ps = pygame.Surface(size)
    ps.fill("black")
    #pygame.draw.rect(ps,pygame.Color('gray20'),glbls['grid_rect'])
    pygame.draw.rect(ps,pygame.Color('yellow'),glbls['play_rect'],width=2)

    # add different colors to non normal velocity areas
    for vg,vv in vel_group.items():
        if vg[0] == 's':
            sr = pygame.Rect(glbls['grid_rect'][0]+vv.minx*8,glbls['grid_rect'][1]+vv.miny*8,(vv.maxx-vv.minx+1)*8,(vv.maxy-vv.miny+1)*8)
            pygame.draw.rect(ps,pygame.Color(240,90,0),sr)
        if vg[0] == 'S':
            sr = pygame.Rect(glbls['grid_rect'][0]+vv.minx*8,glbls['grid_rect'][1]+vv.miny*8,(vv.maxx-vv.minx+1)*8,(vv.maxy-vv.miny+1)*8)
            pygame.draw.rect(ps,pygame.Color(210,40,40),sr)

    for x in range(64):
        for y in range(64):
            l,t = glbls['grid_rect'].left , glbls['grid_rect'].top
            cir_x,cir_y = l+x*8+4 , t+y*8+4
            pygame.draw.circle(ps,pygame.Color('gray40'),(cir_x,cir_y),3)

    # Draw todays deliveries info area
    T_td = Txt_item(f'Todays Deliveries',(60,100))
    T_td.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(25,130),(300,130),width=2)
    T_cl = Txt_item(f'Item Port Pay Good',(25,150),fontsize=14)
    pygame.draw.line(ps,pygame.Color("white"),(25,165),(145,165),width=1)
    T_cl.render(ps)
    column = 0
    row = 0

    if len(ds) > 42:
        RM = 20
        MaxR = 25
    else:
        RM = 25
        MaxR = 20

    for i in range(min(52,len(ds))):
        if row > MaxR:
            column = 1
            row = 0
            T_cl = Txt_item(f'Item Port Pay Good',(25+column*150,150),fontsize=14)
            pygame.draw.line(ps,pygame.Color("white"),(25+column*150,165),(145+column*150,165),width=1)
            T_cl.render(ps)
        small_image = pygame.transform.scale(ds[i].sprite.image,(24,24))
        r = small_image.get_rect(center=(37+column*150,row*RM+179))
        ps.blit(small_image,r)

        T_reward = Txt_item(f'{ds[i].sp.name:<1}'+f"{f'${ds[i].pay:<}':>5}",(80+column*150,row*RM+178),fontsize=18,location='center')
        T_reward.render(ps)

        # checkbox
        cb = pygame.Rect(120+column*150,row*RM+175,10,10)
        pygame.draw.rect(ps,pygame.Color("white"),cb,width=1)
        ds[i].check_coord = (117+column*150,row*RM+172)

        row += 1

    # draw score area
    T_score_title = Txt_item('Last Score',(1050,100))
    T_score_title.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(945,130),(1250,130),width=2)
    T_ds = Txt_item('Delivered:',(950,150))
    T_ds.render(ps)
    T_de = Txt_item('Destroyed:',(950,175))
    T_de.render(ps)
    T_at = Txt_item(f'Author Time:',(950,200))
    T_at.render(ps)
    T_nt = Txt_item(f'{nom_time:>}',(1114,200))
    T_nt.render(ps)
    T_tt = Txt_item('This Time:',(950,225))
    T_tt.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(1100,254),(1175,254),width=1)
    T_bonus = Txt_item('Bonus:  $10 x',(950,250))
    T_bonus.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(945,280),(1250,280),width=2)
    T_total = Txt_item('Total:',(950,290))
    T_total.render(ps)

    T_score_title = Txt_item('Best Score',(1050,350))
    T_score_title.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(945,380),(1250,380),width=2)
    T_ds = Txt_item('Delivered:',(950,400))
    T_ds.render(ps)
    T_de = Txt_item('Destroyed:',(950,425))
    T_de.render(ps)
    T_bonus = Txt_item('Bonus:',(950,450))
    T_bonus.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(945,480),(1250,480),width=2)
    T_total = Txt_item('Total:',(950,480))
    T_total.render(ps)

    T_help0 = Txt_item('Instructions',(10,5),fontsize=18)
    T_help0.render(ps)
    pygame.draw.line(ps,pygame.Color("white"),(5,25),(260,25),width=1)
    T_help1 = Txt_item('Click and drag to declutter routes',(10,25),fontsize=18)
    T_help1.render(ps)
    T_help2 = Txt_item('Right click to delete node',(10,45),fontsize=18)
    T_help2.render(ps)
    T_help3 = Txt_item('Click Start Deliveries to make money!',(10,65),fontsize=18)
    T_help3.render(ps)

    # input port labels
    for ip in inports.values():
        pos = (ip.x-1.1*ip.dx,ip.y-1.1*ip.dy)
        T_ipn = Txt_item(ip.name,pos,location='center',fontsize=18)
        T_ipn.render(ps)

    return ps

def nearest(glbls,pos):
    '''
        Refine position to a grid so we are never off the grid 
        when we are inside the play area.
    '''
    le = glbls["grid_rect"][0]
    te = glbls["grid_rect"][1]

    nx = le + 8*((pos[0] - le) // 8) + 4
    ny = te + 8*((pos[1] - te) // 8) + 4
    return nx,ny

def get_sprite(name):
    spr = pygame.sprite.Sprite()
    spr.image = pygame.image.load(f'graphics/{name}.png').convert_alpha()
    spr.mask = pygame.mask.from_surface(spr.image)
    spr.rect = spr.image.get_rect()
    return spr

splinegen = Spline()

class Point:
    def __init__(self,x,y,name,linked_point=None):
        self.x = x
        self.y = y
        self.name = name
        if linked_point:
            self.back_linked_point = linked_point
            self.forward_linked_point = None
            self.back_linked_point.forward_linked_point = self

            dx = self.x + int((self.x - self.back_linked_point.x) / 10)
            dy = self.y + int((self.y - self.back_linked_point.y) / 10)
            self.new_slope(dx,dy)

            bdx = self.back_linked_point.x + int((self.x - self.back_linked_point.x)/10) + self.back_linked_point.dx
            bdy = self.back_linked_point.y + int((self.y - self.back_linked_point.y)/10) + self.back_linked_point.dy
            self.back_linked_point.new_slope(bdx,bdy)

        else:
            self.back_linked_point = None
            self.forward_linked_point = None
            self.dx = 0
            self.dy = 0
            self.spline_points=np.array([])
    def __repr__(self):
        return(f'[{self.x},{self.y},{self.dx},{self.dy}]')
    def str_loc(self):
        return(f'[{self.x},{self.y}]')
    def str_slope(self):
        return(f'[{self.dx},{self.dy}]')

    #def add_items(self,qty,start_delay,delay,gname):
    def add_items(self,dstring):
        #self.qty = qty
        #self.start_delay = start_delay
        #self.delay = delay
        #self.gname = gname
        self.dstring = dstring

    def linked_count(self):
        return int(bool(self.back_linked_point)) + int(bool(self.forward_linked_point)) 
    #def make_spline(self):
    #    b=np.linalg.inv(np.array([[1,0,0,0],[1,1,1,1],[0,1,0,0],[0,1,2,3]]))
    #    u = np.linspace(0,1.0,50)
    #    uu = np.vstack((np.ones(u.shape),u,u**2,u**3)).T
    #    mult = 5.
    #
    #    c = np.array([
    #        [self.back_linked_point.x,self.back_linked_point.y],
    #        [self.x,self.y],
    #        [mult*self.back_linked_point.dx,mult*self.back_linked_point.dy],
    #        [mult*self.dx,mult*self.dy]
    #        ])
    #    d = b@c
    #    self.spline_points = uu@d

    def make_spline(self):
        self.spline_points = splinegen.get_spline_array(
            self.back_linked_point.x,self.back_linked_point.y,
            self.x,self.y,
            self.back_linked_point.dx,self.back_linked_point.dy,
            self.dx,self.dy
        )

    def move_start(self):
        self.oldx = self.x
        self.oldy = self.y

    def revert(self):
        self.new_location(self.oldx,self.oldy)

    def move_end(self):
        pass

    def slope_start(self):
        self.olddx = self.dx
        self.olddy = self.dy

    def revert_slope(self):
        self.new_slope(self.olddx+self.x,self.olddy+self.y)

    def slope_end(self):
        pass

    def new_location(self,x,y):
        self.x = x
        self.y = y
        if self.back_linked_point:
            self.make_spline()
        if self.forward_linked_point:
            self.forward_linked_point.make_spline()

    def new_slope(self,mx,my):
        self.dx = mx - self.x
        self.dy = my - self.y
        if self.back_linked_point:
            self.make_spline()
        if self.forward_linked_point:
            self.forward_linked_point.make_spline()

    def close_point(self,pos):
        dist = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
        return(dist < 8)

    def close_slope(self,pos):
        if self.back_linked_point or self.forward_linked_point:
            dist = ((self.x + self.dx - pos[0])**2 + (self.y + self.dy - pos[1])**2)**0.5
            return(dist < 8)

    def update(self,dt):
        pass

    def render(self,window,bold=0,slope_points=True):
        if (self.back_linked_point or self.forward_linked_point) and slope_points:
            pygame.draw.line(window,pygame.Color('gray40'),(self.x+self.dx,self.y+self.dy),(self.x,self.y),width=1)
            pygame.draw.rect(window, pygame.Color("green"),(self.x+self.dx-3,self.y+self.dy-3,7,7),1)
        if self.back_linked_point:
            pygame.draw.lines(window,pygame.Color('pink'),False,self.spline_points,width=2+bold*2)
        pygame.draw.rect(window, pygame.Color("yellow"),(self.x-4,self.y-4,9,9),2)
        
    def highlight(self,window):
        pygame.draw.rect(window, pygame.Color("yellow"),(self.x-6,self.y-6,11,11),4)

    def slope_highlight(self,window):
        pygame.draw.rect(window, pygame.Color("green"),(self.x+self.dx-6,self.y+self.dy-6,11,11),4)

    def route_highlight(self,window):
        # traverse all the points forwards and back and highlight them
        blp = self
        while blp.back_linked_point:
            pygame.draw.lines(window,pygame.Color('orange'),False,blp.spline_points,width=2)
            blp = blp.back_linked_point
        flp = self
        while flp.forward_linked_point:
            pygame.draw.lines(window,pygame.Color('orange'),False,flp.forward_linked_point.spline_points,width=2)
            flp = flp.forward_linked_point

