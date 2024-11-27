import pygame

class PlayingSurface:
    def __init__(self,window):
        self.window = window
        self.graphic = pygame.Surface(self.window.size)
        self.graphic.fill("black")
        cx,cy = self.window.size[0]//2,self.window.size[1]//2

        r = pygame.Rect(cx-32*8,cy-32*8,64*8,64*8)
        pygame.draw.rect(self.graphic,pygame.Color('gray20'),r)

        r = pygame.Rect(cx-36*8,cy-36*8,72*8,72*8)
        pygame.draw.rect(self.graphic,pygame.Color('yellow'),r,width=2)

        for x in range(64):
            for y in range(64):
                cir_x,cir_y = cx-32*8+x*8+4,cy-32*8+y*8+4
                pygame.draw.circle(self.graphic,pygame.Color('gray40'),(cir_x,cir_y),3)

        self.le = cx-32*8
        self.re = cx-32*8+8*64
        self.te = cy-32*8
        self.be = cy-32*8+8*64

    def in_play_area(self,pos):
        return self.le < pos[0] < self.re and self.te < pos[1] < self.be

    def nearest(self,pos):
        '''
            Refine position to a grid so we are never off the grid 
            when we are inside the play area.
        '''
        nx = self.le + 8*((pos[0] - self.le) // 8) + 4
        ny = self.te + 8*((pos[1] - self.te) // 8) + 4
        return nx,ny

    def process_event(self,e):
        if self.in_play_area(e.pos):
            print("in the area")

    def render(self):
        self.window.blit(self.graphic,(0,0))


if __name__ == "__main__":
    import pygame
    import sys
    from global_dict import glbls

    glbls['Full Screen'] = False
    if len(sys.argv) > 1:
        glbls['Full Screen'] = (sys.argv[1] == 'full')
        #if len(sys.argv) > 2:
        #    glbls["start_level"] = int(sys.argv[2])



    pygame.init()

    if glbls['Full Screen']:
        window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']),flags=pygame.FULLSCREEN | pygame.SCALED)
    else:
        window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']))

    clock = pygame.time.Clock()

    ps = PlayingSurface(window)


    done = False
    while not done:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEMOTION:
                ps.process_event(event)

        #window.fill(pygame.Color("black"))

        ps.render()

        pygame.display.update()
        #await asyncio.sleep(0)

    pygame.quit()
