import pygame
from button import Button
from tilespalettecanvas import TilesPaletteCanvas

PALETTE_SCROLL_BUTTON_HEIGHT = 32
PALETTE_COLUMNS = 4 #__name__=="__main__"

class TilesPalette:
	"""TilesPalette class"""
	def __init__(self, width, height, tileset):
		self.button_up = Button(0, 0, width, PALETTE_SCROLL_BUTTON_HEIGHT)		
		self.button_down = Button(0, height-PALETTE_SCROLL_BUTTON_HEIGHT, width, PALETTE_SCROLL_BUTTON_HEIGHT)
		self.canvas = TilesPaletteCanvas(0, PALETTE_SCROLL_BUTTON_HEIGHT, width, height, tileset)
		self.canvas.load_tiles()
		
		self.surface = pygame.Surface((width, height)).convert()
		
		#self.surface.blit(self.canvas.surface, (0, PALETTE_SCROLL_BUTTON_HEIGHT))

	def update(self, events):
		canvas_event = self.canvas.update(events)
		button_up_event = self.button_up.update(events)
		button_down_event = self.button_down.update(events)
		
		self.surface.blit(self.canvas.surface, self.canvas.rect)
		self.surface.blit(self.button_up.surface, self.button_up.rect)
		self.surface.blit(self.button_down.surface, self.button_down.rect)
		
		if button_up_event == pygame.MOUSEBUTTONDOWN:
			self.canvas.scroll(-1)
		elif button_down_event == pygame.MOUSEBUTTONDOWN:
			self.canvas.scroll( 1)
		
	
if __name__ == "__main__":
	from sys import exit
	import tileset
	
	pygame.init()
	screen = pygame.display.set_mode((500, 350))
	screen.fill((255,255,255))
	
	tset = tileset.Tileset('floortileset.png', 32, 32)
	tpal = TilesPalette(PALETTE_COLUMNS*tset.tiles_width, 350, tset)
	
	print("Tileset image used in this prototype by gfx0 at OpenGameArt.Org\nhttps://opengameart.org/users/gfx0")
	
	while True:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				exit()
		
		tpal.update(events)
		
		screen.blit(tpal.surface, ((0,0)))
		pygame.display.update()	
