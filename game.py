import asyncio
import pygame
from txt_item import Txt_item

class Game:
    def __init__(self, window, glbls, start_state):
        self.done = False
        self.window = window
        self.glbls = glbls
        self.state = self.glbls['STATES'][start_state]
        self.clock = pygame.time.Clock()
        #self.glbls['ti_fps'] = Txt_item('00',(self.glbls['WIDTH']-49,1))
        self.fps = 60
        self.state.startup()

    def event_loop(self):
        for event in pygame.event.get():
            self.state.process_event(event)

    def flip_state(self):
        self.state.done = False
        self.state = self.glbls['STATES'][self.state.next_state]
        self.state.startup()

    def update(self, dt):
        #self.glbls['ti_fps'].change_text(f"{self.clock.get_fps():4.1f}")
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

        self.state.update(dt)

    async def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.state.draw(self.window)
            #self.glbls['ti_fps'].render(self.window)
            pygame.display.update()
            await asyncio.sleep(0)
        pygame.quit()
