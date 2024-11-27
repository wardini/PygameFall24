import json
import glob
from level_objects import init_coords,Point,get_playing_surface,get_sprite
import numpy as np
from deliverable import Deliverable
import pygame
from txt_item import Txt_item
import random

class Level:
    def __init__(self,glbls,N):
        self.glbls = glbls

        self.ds = []
        self.points = []
        self.done = False

        # keeping track of score
        self.no_score = True
        self.last_del_time = 0
        self.last_paid = 0
        self.last_lost = 0
        self.last_destroyed = 0
        self.best_del_time = 0
        self.best_paid = 0
        self.best_lost = 0
        self.best_total = 0

        with open(f"levels/level_{N}.json","r") as f:
            ldict = json.load(f)

        self.nom_time = ldict['nomtime']

        self.T_last_paid = Txt_item('None',(1180,150))
        self.T_last_lost = Txt_item('None',(1180,175))
        self.T_this_time = Txt_item('None',(1114,225))
        self.T_last_bonus = Txt_item('None = None',(1120,250))
        self.T_last_total = Txt_item('None',(1180,290))

        self.T_best_paid = Txt_item('None',(1180,400))
        self.T_best_lost = Txt_item('None',(1180,425))
        self.T_best_bonus = Txt_item('None',(1180,450))
        self.T_best_total = Txt_item('None',(1180,480))

        self.inports = {}
        self.outports = {}

        S = 3
        PS = 20

        ox = self.glbls['grid_rect'][0] + 4
        oy = self.glbls['grid_rect'][1] + 4

        self.i_count_good = 0
        self.i_count_bad = 0
        self.play_insult = False
        self.insult_delay = 500
        self.insult = 'i_good_1'

        # instantiate level objects
        for i in range(64):
            # Input Ports
            if ldict["level"][0][i*2] == "v":
                pname = ldict["level"][0][i*2+1]
                self.inports[pname] = Point(i*8+ox,-S*8+oy,pname)
                self.inports[pname].new_slope(self.inports[pname].x+0,self.inports[pname].y+PS)
            if ldict["level"][65][i*2] == "^":
                pname = ldict["level"][65][i*2+1]
                self.inports[pname] = Point(i*8+ox,(63+S)*8+oy,pname)
                self.inports[pname].new_slope(self.inports[pname].x+0,self.inports[pname].y-PS)
            if ldict["level"][i+1][1] == ">":
                pname = ldict["level"][i+1][0]
                self.inports[pname] = Point(-S*8+ox,i*8+oy,pname)
                self.inports[pname].new_slope(self.inports[pname].x+PS,self.inports[pname].y+0)
            if ldict["level"][i+1][130] == "<":
                pname = ldict["level"][i+1][131]
                self.inports[pname] = Point((63+S)*8+ox,i*8+oy,pname)
                self.inports[pname].new_slope(self.inports[pname].x-PS,self.inports[pname].y+0)

        for i in range(64):
            # Output Ports
            if ldict["level"][0][i*2] == "^":
                pname = ldict["level"][0][i*2+1]
                self.outports[pname] = Point(i*8+ox,-S*8+oy,pname)
                self.outports[pname].back_linked_point = self.inports[pname]
                self.outports[pname].back_linked_point.forward_linked_point = self.outports[pname]
                self.outports[pname].new_slope(self.outports[pname].x+0,self.outports[pname].y-PS)
            if ldict["level"][65][i*2] == "v":
                pname = ldict["level"][65][i*2+1]
                self.outports[pname] = Point(i*8+ox,(63+S)*8+oy,pname)
                self.outports[pname].back_linked_point = self.inports[pname]
                self.outports[pname].back_linked_point.forward_linked_point = self.outports[pname]
                self.outports[pname].new_slope(self.outports[pname].x+0,self.outports[pname].y+PS)
            if ldict["level"][i+1][1] == "<":
                pname = ldict["level"][i+1][0]
                self.outports[pname] = Point(-S*8+ox,i*8+oy,pname)
                self.outports[pname].back_linked_point = self.inports[pname]
                self.outports[pname].back_linked_point.forward_linked_point = self.outports[pname]
                self.outports[pname].new_slope(self.outports[pname].x-PS,self.outports[pname].y+0)
            if ldict["level"][i+1][130] == ">":
                pname = ldict["level"][i+1][131]
                self.outports[pname] = Point((63+S)*8+ox,i*8+oy,pname)
                self.outports[pname].back_linked_point = self.inports[pname]
                self.outports[pname].back_linked_point.forward_linked_point = self.outports[pname]
                self.outports[pname].new_slope(self.outports[pname].x+PS,self.outports[pname].y+0)

        for p in self.inports.values():
            #p.add_items(*ldict["inports"][p.name])
            p.add_items(ldict["inports"][p.name])
        for p in self.outports.values():
            #p.add_items(*ldict["outports"][p.name],"")
            pass

        # generate velocity array from characters
        # #'s are groups - overlap not allowed currently
        # 'S#' Very Slow velocity
        # 's#' Slow velocity
        # ' .' Normal velocity
        # 'f#' Fast velocity
        # 'F#' Very Fast velocity
        self.vel_group = {}
        for y in range(64):
            for x in range(64):
                vchars = ldict["level"][y+1][x*2+2:x*2+4]
                if vchars[0] != ' ':
                    if vchars not in self.vel_group.keys():
                        self.vel_group[vchars] = Vgroup(x,y)
                    else:
                        self.vel_group[vchars].add_xy(x,y)

        self.velgrid = np.ones((64,64)) * 4
        for vi,vg in self.vel_group.items():
            for y in range(vg.miny,vg.maxy+1):
                for x in range(vg.minx,vg.maxx+1):
                    if vi[0] == 's':
                        self.velgrid[y,x] = 3.2
                    elif vi[0] == 'S':
                        self.velgrid[y,x] = 2

        # instantiate deliverables
        for ip in self.inports.values():
            cur_time = 0
            for j in range(len(ip.dstring)):
                if ip.dstring[j] in "0123456789":
                    cur_time += 100*int(ip.dstring[j])
                else:
                    s = get_sprite(self.glbls['dtrans'][ip.dstring[j]][0])
                    pay =self.glbls['dtrans'][ip.dstring[j]][1] 
                    self.ds.append(Deliverable(self.glbls,cur_time,ip,s,self.velgrid,pay))

        for d in self.ds:
            d.reset()
            d.state = 'nothing'

        self.ps = get_playing_surface(self.glbls,self.vel_group,self.ds,self.inports,self.nom_time)

    @staticmethod
    def get_levels_count():
        level_files = glob.glob("levels/level_*.json")
        return(len(level_files))

    def reset(self,stop=False):
        self.done = False
        self.last_destroyed = 0
        self.last_paid = 0
        self.last_lost = 0
        self.last_del_time = 0
        for d in self.ds:
            d.reset(stop)

    def insult_update(self,dt):
        if self.play_insult:
            self.insult_delay -= dt
            if self.insult_delay < 0:
                self.insult_delay = 500
                self.glbls[self.insult].play(0)
                self.play_insult = False

    def float_update(self,dt):
        [d.update(dt) for d in self.ds]

    def update(self,dt):
        self.done = all([d.update(dt) for d in self.ds])
        if self.done:
            num_delivered = sum([d.delivered for d in self.ds])
            #num_destroyed = len(self.ds) - num_delivered
            pct_delivered = 100.0 * num_delivered / len(self.ds)
            self.last_paid = sum([d.pay for d in self.ds if d.delivered])
            self.last_lost = sum([d.pay for d in self.ds]) - self.last_paid
            if self.last_lost == 0:
                self.last_del_time = max([d.del_time for d in self.ds])
                last_delta = max(self.nom_time - self.last_del_time,0)
                self.T_this_time.change_text(f'{self.last_del_time:>}')
                last_bonus = 10*last_delta
                self.T_last_bonus.change_text(f'{last_delta:>3d} = ${last_bonus:>}')
            else:
                self.T_this_time.change_text(f'None')
                self.T_last_bonus.change_text('None = None')
                last_bonus = 0

            self.T_last_paid.change_text(f'${self.last_paid:>}')
            self.T_last_lost.change_text(f'${self.last_lost:>}')

            total_paid = self.last_paid + last_bonus
            self.T_last_total.change_text(f'${total_paid:>}')

            if total_paid > self.best_total:
                self.glbls['s_gotzero'].play(0)
                self.best_paid = self.last_paid
                self.best_lost = self.last_lost
                self.best_del_time = self.last_del_time
                self.best_total = total_paid

                self.T_best_paid.change_text(f'${self.best_paid}')
                self.T_best_lost.change_text(f'${self.best_lost}')
                self.T_best_bonus.change_text(f'${last_bonus}')
                self.T_best_total.change_text(f'${self.best_total}')

            # criteria for insults
            if len(self.ds) > 5:
                if random.random() < 0.02:
                    if pct_delivered > 90:
                        if self.i_count_good < 2:
                            self.i_count_good += 1
                            rsel = random.randint(1,self.glbls['icount_good'])
                            self.insult = 'i_good_' + str(rsel)
                            self.play_insult = True
                    elif pct_delivered > 70:
                        if self.i_count_bad < 2:
                            self.i_count_bad += 1
                            rsel = random.randint(1,self.glbls['icount_med'])
                            self.insult = 'i_med_' + str(rsel)
                            self.play_insult = True
                    else:
                        if self.i_count_bad < 2:
                            self.i_count_bad += 1
                            rsel = random.randint(1,self.glbls['icount_bad'])
                            self.insult = 'i_bad_' + str(rsel)
                            self.play_insult = True

            return

        # look for collisions
        for i in range(len(self.ds)):
            for j in range(i+1,len(self.ds)):
                if self.ds[i].state == 'moving' and self.ds[j].state == 'moving':
                    if pygame.sprite.collide_mask(self.ds[i].sprite, self.ds[j].sprite):
                        self.ds[i].destroy()
                        self.ds[j].destroy()
                        self.last_destroyed += 2
                        self.glbls['s_explosion'].play(0)

        # collision with edges
        for i in range(len(self.ds)):
            if self.ds[i].state == 'moving':
                if not self.glbls["port_rect"].collidepoint(self.ds[i].xy):
                    self.ds[i].destroy()
                    self.last_destroyed += 1
                    self.glbls['s_explosion'].play(0)

    def render(self):
        w = self.glbls["window"]

        w.blit(self.ps,(0,0))

        for p in self.inports.values():
            p.render(w,slope_points=False)
        for p in self.outports.values():
            p.render(w,slope_points=False)

        self.T_last_paid.render(w)
        self.T_last_lost.render(w)
        self.T_this_time.render(w)
        self.T_last_bonus.render(w)
        self.T_last_total.render(w)
        self.T_best_paid.render(w)
        self.T_best_lost.render(w)
        self.T_best_bonus.render(w)
        self.T_best_total.render(w)

        for p in self.points:
            p.render(w)

        for d in self.ds:
            d.render(w)


class Vgroup:
    def __init__(self,startx,starty):
        self.minx = startx
        self.maxx = startx
        self.miny = starty
        self.maxy = starty
    def add_xy(self,x,y):
        self.minx = min(self.minx,x)
        self.miny = min(self.miny,y)
        self.maxx = max(self.maxx,x)
        self.maxy = max(self.maxy,y)

