import pygame
from math import floor
from button import Button

SCROLL_BUTTON_HEIGHT = 32
PALETTE_BACKGROUND = (50,50,50)
PALETTE_COLUMNS = 4

class TilesPalette:
	"""TilesPalette class"""
	def __init__(self, width, height, tileset):
		self.scroll_offset = 0
		self.tileset = tileset
		
		self.button_up = Button(0, 0, width, SCROLL_BUTTON_HEIGHT)		
		self.button_down = Button(0, height-SCROLL_BUTTON_HEIGHT, width, SCROLL_BUTTON_HEIGHT)
		
		self.surface = pygame.Surface((width, height)).convert()
		self.palette_surface = pygame.Surface((width, height - SCROLL_BUTTON_HEIGHT*2)).convert()
		self.palette_surface.fill(PALETTE_BACKGROUND)
		
		self.load_tiles()
				
	def load_tiles(self):
		"load_tiles method"
		i = 0
		self.palette_surface.fill(PALETTE_BACKGROUND)
		for tile in self.tileset.tiles[self.scroll_offset*PALETTE_COLUMNS:]:
			x = (i % PALETTE_COLUMNS) * self.tileset.tiles_width
			y = (floor(i / PALETTE_COLUMNS) * self.tileset.tiles_height )
			self.palette_surface.blit(tile, (x, y))
			i+=1
		
		self.surface.blit(self.palette_surface, (0, SCROLL_BUTTON_HEIGHT))
				
	def scroll(self, step):
		"scroll method"
		self.scroll_offset += step
		if self.scroll_offset < 0:
			self.scroll_offset = 0
		self.load_tiles()
		
	def update(self, events):
		button_up = self.button_up.update(events)
		button_down = self.button_down.update(events)
		self.surface.blit(self.button_up.surface, self.button_up.rect)
		self.surface.blit(self.button_down.surface, self.button_down.rect)
		
		if button_up == pygame.MOUSEBUTTONDOWN:
			self.scroll(-1)
		elif button_down == pygame.MOUSEBUTTONDOWN:
			self.scroll(1)
	
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
