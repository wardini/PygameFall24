import pygame
from txt_item import Txt_item
from level import Level
from level_objects import Point,nearest
import numpy as np

class GamePlay:
    def __init__(self,glbls):
        self.glbls = glbls
        self.quit = False
        self.done = False
        self.next_state = 'ScoreScreen'

        # load levels
        self.levels = []
        N = Level.get_levels_count()
        for i in range(N):
            self.levels.append(Level(self.glbls,i))

        self.T_launch = Txt_item('Start Deliveries',(550,10),selectable=True,action='launch')
        self.T_reset = Txt_item('Reset Level',(1100,10),selectable=True,action='reset')
        self.T_destroyed = Txt_item(f'Destroyed: {0}',(450,47))
        self.T_time = Txt_item(f'Time: {0}',(730,47))
        self.T_llabel = Txt_item(f'Level Select:',(20,710))

        self.T_td = Txt_item(f'Todays Deliveries',(30,100))

        # Level Select Buttons
        self.T_levsel = []
        for i in range(N):
            self.T_levsel.append(Txt_item(f'{i+1}',(190+33*i,710),selectable=True,action=f'Level {i}'))
            self.T_levsel[-1].disable_click()

        self.T_total_score = Txt_item(f'Total Score',(190+33*(i+1),710),selectable=True,action=f'total_score')
        self.T_total_score.disable_click()

        self.change_level(self.glbls.get("start_level",0))
        self.T_levsel[self.cur_level].enable_click()

        self.zero_texts()

    def startup(self):
        self.state = 'edit'
        self.mouse_state = 'waiting'
        self.hl_state = 'nothing'

    def change_level(self,new_lev_num):
        self.cur_level = new_lev_num
        self.zero_texts()

    def zero_texts(self):
        self.T_destroyed.change_text(f'Destroyed: {0}')
        self.T_time.change_text(f'Time: {0}')

    def find_highlights(self,pos):
        # actions depend on what is hilighted
        # if nothing is hilighted, nothing happens when click
        # so look and identify something being hilighted
        # for each port check if near
        mx,my = pos

        if not self.glbls["play_rect"].collidepoint(pos):
            self.hl_state = 'outside'
            return

        for inport in self.levels[self.cur_level].inports.values():
            if inport.x - 4 < mx < inport.x + 4 and inport.y-4 < my < inport.y+4:
                self.hl_state = 'hl_port'
                self.hl = inport
                return

        for outport in self.levels[self.cur_level].outports.values():
            if outport.x - 4 < mx < outport.x + 4 and outport.y-4 < my < outport.y+4:
                self.hl_state = 'hl_port'
                self.hl = outport
                return

        if self.mouse_state not in ['move','move_slope']:
            # for each slope, check if near
            for p in self.levels[self.cur_level].points:
                if p.close_slope(pos):
                    self.hl_state = 'hl_slope'
                    self.hl = p
                    return

        # for each point, check if near
        for p in self.levels[self.cur_level].points:
            if self.mouse_state == 'move' and p == self.last_point:
                continue
            if p.close_point(pos):
                self.hl_state = 'hl_point'
                self.hl = p
                return

        if self.mouse_state == 'move':
            if self.glbls["grid_rect"].collidepoint(pos):
                gx,gy = nearest(self.glbls,pos)
                self.hl_state = 'hl_node'
                self.nx,self.ny = gx,gy
                return

        if not self.glbls["grid_rect"].collidepoint(pos):
            self.hl_state = 'nothing'
            return

        for op in self.levels[self.cur_level].outports.values():
            sp = op
            while sp.back_linked_point:
                dist = np.linalg.norm(sp.spline_points - np.array(pos),axis=1)
                e = np.argmin(dist)
                if dist[e] < 6:
                    self.hl_state = 'hl_spline'
                    self.hlspx,self.hlspy = sp.spline_points[e]
                    self.hl = sp
                    return
                sp = sp.back_linked_point

        # compute node nearest
        gx,gy = nearest(self.glbls,pos)
        self.hl_state = 'hl_node'
        self.nx,self.ny = gx,gy
        return

    def process_event(self,event):
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.done = True
                self.quit = True
                return
            elif event.key == pygame.K_SPACE:
                if self.mouse_state == 'waiting':
                    if self.state == 'edit':
                        self.T_launch.change_text('Cancel Deliveries')
                        self.state = 'prelaunch'
                        self.levels[self.cur_level].reset()
                    elif self.state == 'launch':
                        self.levels[self.cur_level].reset(stop=True)
                        self.T_launch.change_text('Start Deliveries')
                        self.state = 'edit'
            return

        if self.state == 'edit':

            if self.mouse_state == 'move':
                if event.type == pygame.MOUSEMOTION:
                    self.find_highlights(event.pos)
                    if self.hl_state == 'outside':
                        self.last_point.revert()
                        self.mouse_state = 'waiting'
                    else:
                        gx,gy = nearest(self.glbls,event.pos)
                        self.last_point.new_location(gx,gy)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.find_highlights(event.pos)
                    if self.hl_state == 'hl_node':
                        gx,gy = nearest(self.glbls,event.pos)
                        self.last_point.new_location(gx,gy)
                        self.last_point.move_end()
                        self.mouse_state = 'waiting'
                    else:
                        self.last_point.revert()
                        self.mouse_state = 'waiting'
            elif self.mouse_state == 'move_slope':
                if event.type == pygame.MOUSEMOTION:
                    self.find_highlights(event.pos)
                    if self.hl_state == 'outside':
                        self.last_point.revert_slope()
                        self.mouse_state = 'waiting'
                    else:
                        self.last_point.new_slope(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.last_point.new_slope(*event.pos)
                    self.last_point.slope_end()
                    self.mouse_state = 'waiting'
            elif self.mouse_state == 'waiting':
                if event.type == pygame.MOUSEMOTION:
                    self.find_highlights(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.find_highlights(event.pos)
                    if self.hl_state == 'hl_spline':
                        gx,gy = nearest(self.glbls,(self.hlspx,self.hlspy))
                        self.last_point = Point(gx,gy,f'_{self.hl.name}')
                        self.hl.back_linked_point.forward_linked_point = self.last_point
                        self.last_point.back_linked_point = self.hl.back_linked_point
                        self.hl.back_linked_point = self.last_point
                        self.last_point.forward_linked_point = self.hl
                        self.levels[self.cur_level].points.append(self.last_point)

                        #if self.hl not in self.levels[self.cur_level].outports.values():
                        #    dx = self.hl.x + int((self.hl.x - self.last_point.x) / 10)
                        #    dy = self.hl.y + int((self.hl.y - self.last_point.y) / 10)
                        #    self.hl.new_slope(dx,dy)

                        dx = self.last_point.x + int((self.last_point.x - self.last_point.back_linked_point.x) / 10)
                        dy = self.last_point.y + int((self.last_point.y - self.last_point.back_linked_point.y) / 10)
                        self.last_point.new_slope(dx,dy)
                        # try going straightt to move point mode
                        self.mouse_state = 'move'
                        self.last_point.move_start()
                        return
                    elif self.hl_state == 'hl_point':
                        self.mouse_state = 'move'
                        self.last_point = self.hl
                        self.last_point.move_start()
                    elif self.hl_state == 'hl_slope':
                        self.mouse_state = 'move_slope'
                        self.last_point = self.hl
                        self.last_point.slope_start()
                    elif self.hl_state == 'hl_port':
                        return
                    elif self.hl_state == 'outside':
                        if self.T_launch.check_select(event.pos):
                            self.T_launch.change_text('Cancel Deliveries')
                            self.state = 'prelaunch'
                        elif self.T_reset.check_select(event.pos):
                            for i in range(len(self.levels[self.cur_level].points)-1,-1,-1):
                                self.remove_point(self.levels[self.cur_level].points[i])
                        elif self.T_total_score.check_select(event.pos):
                            self.done = True
                        else:
                            for i in range(len(self.T_levsel)):
                                if i == self.cur_level:
                                    continue
                                elif self.T_levsel[i].check_select(event.pos):
                                    self.change_level(i)

                # delete stuff
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.find_highlights(event.pos)
                    if self.hl_state == 'hl_point':
                        self.remove_point(self.hl)
                        self.hl_state = 'nothing'

            return

        elif self.state == 'launch':
            if self.mouse_state == 'waiting':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.find_highlights(event.pos)
                    if self.T_launch.check_select(event.pos):
                        self.levels[self.cur_level].reset(stop=True)
                        self.T_launch.change_text('Start Deliveries')
                        self.state = 'edit'

    def remove_point(self,p):
        fp = p.forward_linked_point
        p.back_linked_point.forward_linked_point = fp
        bp = p.back_linked_point
        p.forward_linked_point.back_linked_point = bp
        self.levels[self.cur_level].points.remove(p)
        if fp not in self.levels[self.cur_level].outports.values():
            dx = fp.x + int((fp.x - bp.x) / 10)
            dy = fp.y + int((fp.y - bp.y) / 10)
            fp.new_slope(dx,dy)
        else:
            fp.make_spline()

    def update(self,dt):
        # make stuff follow paths
        if self.state == 'prelaunch':
            self.levels[self.cur_level].reset()
            self.showtime = 0
            self.destroyed = 0
            self.state = 'launch'
        elif self.state == 'launch':
            self.showtime += 1
            self.T_time.change_text(f'Time: {self.showtime}')
            self.levels[self.cur_level].update(dt)
            if self.levels[self.cur_level].done:
                self.state = 'edit'
                self.T_launch.change_text('Start Deliveries')
                if self.levels[self.cur_level].last_lost == 0:
                    if self.cur_level + 1 < len(self.T_levsel):
                        self.T_levsel[self.cur_level+1].enable_click()
                    else:
                        self.T_total_score.enable_click()

            self.T_destroyed.change_text(f'Destroyed: {self.levels[self.cur_level].last_destroyed}')
        elif self.state == 'edit':
            self.levels[self.cur_level].insult_update(dt)
            self.levels[self.cur_level].float_update(dt)

        return


    def draw(self,window):
        window.fill(pygame.Color("black"))

        self.levels[self.cur_level].render()

        if self.hl_state == 'hl_point':
            self.hl.highlight(window)
            self.hl.route_highlight(window)
        elif self.hl_state == 'hl_slope':
            self.hl.slope_highlight(window)
            self.hl.route_highlight(window)
        elif self.hl_state == 'hl_port':
            self.hl.highlight(window)
            self.hl.route_highlight(window)
        elif self.hl_state == 'hl_node':
            pygame.draw.circle(window,pygame.Color('gray90'),(self.nx,self.ny),3)
        elif self.hl_state == 'hl_spline':
            pygame.draw.rect(window,pygame.Color('orange'),(self.hlspx-3,self.hlspy-3,7,7),width=2)
            self.hl.route_highlight(window)

        self.T_launch.render(window)
        self.T_reset.render(window)
        self.T_time.render(window)
        self.T_destroyed.render(window)

        self.T_llabel.render(window)
        for i in range(len(self.T_levsel)):
            self.T_levsel[i].render(window)
            if i == self.cur_level:
                self.T_levsel[i].highlight(window)
        self.T_total_score.render(window)
