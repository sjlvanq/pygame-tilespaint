import pygame
from math import floor

PALETTE_SCROLL_BUTTON_HEIGHT = 32
PALETTE_COLUMNS = 4
PALETTE_BACKGROUND = (50, 50, 50)
PALETTE_BOOKMARK_COLOR = (255, 255, 255, 128)

class TilesPaletteCanvas:
	"""
	Class TilesPaletteCanvas.

	Represents a canvas that displays tiles in a palette.

	@param x
	@param y
	@param width
	@param height
	@param tileset

	"""
	def __init__(self, x, y, width, height, tileset):
		self.selected_tile = 0
		self.scroll_offset = 0
		self.tileset = tileset
		self.surface = pygame.Surface((width, height - PALETTE_SCROLL_BUTTON_HEIGHT*2)).convert()
		self.rect = self.surface.get_rect()
		self.rect.topleft = (x, y)
		
		self.surface.fill(PALETTE_BACKGROUND)

	def load_tiles(self):
		"load_tiles method"
		i = 0
		self.surface.fill(PALETTE_BACKGROUND)
		for tile in self.tileset.tiles[self.scroll_offset*PALETTE_COLUMNS:]:
			x = (i % PALETTE_COLUMNS) * self.tileset.tiles_width
			y = (floor(i / PALETTE_COLUMNS) * self.tileset.tiles_height )
			self.surface.blit(tile, (x, y))
			if(self.selected_tile == i+self.scroll_offset*PALETTE_COLUMNS):
				pygame.draw.polygon( self.surface,
					PALETTE_BOOKMARK_COLOR,
					[
						(x+(self.tileset.tiles_width/2),y),
						(x+self.tileset.tiles_width, y),
						(x+self.tileset.tiles_width,y+self.tileset.tiles_height/2)
					]
				)
			i+=1

	def scroll(self, step):
		"scroll method"
		self.scroll_offset += step
		if self.scroll_offset < 0:
			self.scroll_offset = 0
		self.load_tiles()

	def update(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos):
				map_x, map_y = self.get_tile_from_coords(e.pos)
				self.selected_tile = (self.scroll_offset * PALETTE_COLUMNS) + map_y * PALETTE_COLUMNS + map_x
				self.load_tiles()

	def get_tile_from_coords(self, pos):
		map_x = floor((pos[0] - self.rect.x) / self.tileset.tiles_width)
		map_y = floor((pos[1] - self.rect.y) / self.tileset.tiles_height)
		return (map_x, map_y)
