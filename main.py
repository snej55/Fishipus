import data.e.scripts as e
from data.e.scripts.env.tiles import *
from data.scripts.entities import Player, Blobbo
from data.e.scripts.tools.ui.texto import Font
#from data.scripts.sword import Sword
#from data.e.scripts.entities.paths import PathFinder

class App(e.Pygmy):
    def __init__(self):
        super().__init__(config={
            'caption': 'JINJAMIJET'
        }) # 
        self.world.tile_map.load('data/maps/0.json')
        self.world.tile_map.load_leaves('data/config/leaf.json')
        self.world.window.add_shader('background', 'frag.frag', 'vert.vert')  # add shaders with mgl stuff
        self.player = Player((200, 10), (6, 7), (-1, -1), self, vj=-4)
        self.blobbo = [Blobbo((250 + i * 10, 100), (6, 7), (-1, -1), self, 'blobbo', health=5) for i in range(30)]
        self.world.window.set_camera_target(self.player)
        self.text = Font('data/images/fonts/small_font.png')
        #self.path_finder = PathFinder(self)

    def update(self, screen, scroll):
        self.player.update()
        self.player.draw(screen, scroll)
        self.world.tile_map.leaves(screen, scroll)
        #pygame.draw.rect(screen, (255, 0, 0), self.player.rect())f
        #self.path_finder.draw(screen, scroll)
        self.text.render(self.world.window.ui_surf, f'{self.world.tick.clock.get_fps() :.1f} fps', (250, 10))

if __name__ == '__main__':
    App().run()