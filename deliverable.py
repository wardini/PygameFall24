import numpy as np
import pygame
import random

class Deliverable:
    def __init__(self,glbls,start_time,start_port,sprite,velgrid,pay):
        self.glbls = glbls
        self.st = start_time
        self.sp = start_port
        self.sprite = sprite
        self.velgrid = velgrid
        self.pay = pay
        self.state = 'waiting'
        self.delivered = 0
        self.check_coord = (0,0)
        self.vxy = np.array([0,0])
        self.float_image = sprite.image.copy()
        self.float_image.set_alpha(200)

    def get_grid_coord(self,x,y):
        nx = int((x - self.glbls["grid_rect"][0]) // 8)
        ny = int((y - self.glbls["grid_rect"][1]) // 8)
        return nx,ny

    def reset(self,stop=False):
        self.next_point = self.sp.forward_linked_point
        self.spi = 0
        self.xy = self.next_point.spline_points[self.spi].copy()
        self.spi = 1
        self.cur_time = 0
        if stop:
            self.state = 'nothing'
        else:
            self.state = 'waiting'
        self.delivered = 0
        self.del_time = 0

        #print("np",self.next_point.x,self.next_point.y)
        #print("sp49",self.next_point.spline_points[49])
        #print("sp0",self.next_point.spline_points[0])
        #print("xy",self.xy)
        #print("-------------")

    def destroy(self):
        self.state = 'exploding'
        self.exp_parts = []
        self.del_time = self.cur_time
        for i in range(10):
            self.exp_parts.append(Particle(self.xy[0],self.xy[1],0,pygame.Color("white")))

    def update(self,dt):
        self.cur_time += 1
        if self.state == 'waiting':
            if self.cur_time*16 > self.st:
                self.state = 'moving'
            else:
                return False
        elif self.state == 'done':
            if self.delivered:
                self.xy += self.vxy
                self.sprite.rect.center = (self.xy[0],self.xy[1])
            return True
        elif self.state == 'exploding':
            if all([p.update(dt) for p in self.exp_parts]):
                self.state = 'done'
            return False
        elif self.state == 'nothing':
            return False

        # traverse the spline
        gx,gy = self.get_grid_coord(self.xy[0],self.xy[1])
        if gx < 0 or gx > 63 or gy < 0 or gy > 63:
            D_to_travel = 4 #pixels/frame
        else:
            D_to_travel = self.velgrid[gy,gx]
        while D_to_travel > 0:
            sps = self.next_point.spline_points
            v = sps[self.spi] - self.xy
            dist = np.linalg.norm(v)
            D_to_travel -= dist
            if D_to_travel > 0:
                self.xy = self.next_point.spline_points[self.spi].copy()
                self.spi += 1
                if self.spi == sps.shape[0]:
                    if not self.next_point.forward_linked_point:
                        self.state = 'done'
                        self.delivered = 1
                        self.del_time = self.cur_time
                        self.glbls['s_delivered'].play(0)

                        # float velocity and direction generation for post graphics
                        self.vxy = np.array([self.next_point.dx/20,self.next_point.dy/20])
                        self.vxy += (np.random.random(2) - 0.5)*2
                        
                        return True
                    else:
                        self.next_point = self.next_point.forward_linked_point
                        self.spi = 0
            else:
                if dist == 0:
                    self.xy = sps[self.spi].copy()
                else:
                    self.xy = sps[self.spi].copy() + (D_to_travel/dist)*v # move back
            self.sprite.rect.center = (self.xy[0],self.xy[1])

        return False

    def render(self,window):
        if self.state =='moving':
            window.blit(self.sprite.image,self.sprite.rect)
            #pygame.draw.circle(window,pygame.Color('red'),(self.xy[0],self.xy[1]),8)
        elif self.state == 'exploding':
            for p in self.exp_parts:
                    p.render(window)

        if self.state == 'done':
            if self.delivered:
                window.blit(self.glbls['g_check'],self.check_coord)
            else:
                window.blit(self.glbls['g_x'],self.check_coord)

            # float it away here I think
            if self.delivered:
                window.blit(self.float_image,self.sprite.rect)

class Particle:
    def __init__(self,x,y,delay,color):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.delay = delay
        self.color = color

        self.dx = random.choice([1,-1])*(3*random.random()+2)
        self.dy = random.choice([1,-1])*(3*random.random()+2)

        self.start_size = 10
        self.pct_done = 0
        self.time = 0
        self.size = self.start_size

    def update(self,dt):
        self.time += dt/1000
        
        self.pct_done = 150 * max(0,self.time - self.delay)

        if self.pct_done > 50:
            return True

        self.x = self.start_x + self.pct_done * self.dx
        self.y = self.start_y + self.pct_done * self.dy
        self.size = max(1,self.start_size * (1 - self.pct_done/50))
        self.rect = pygame.Rect(self.x,self.y,self.size,self.size)

        return False

    def render(self,window):
        if self.pct_done > 0:
            pygame.draw.rect(window,self.color,self.rect)
