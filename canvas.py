import pygame
from math import floor
from numpy import full

CANVAS_BACKGROUND = (50, 50, 50)
MAP = full((10,10), -1)

class Canvas:
	"""
	Canvas class.

	Represents the drawing area.

	@param area_rect: The rectangular area where the canvas will be drawn.
	@param map: A 2D array representing the tile map.
	@param tileset

	"""
	def __init__(self, area_rect, map, tileset):
		self.map = map
		self.tileset = tileset
		self.surface = pygame.Surface(( 
			len(map[0]) * tileset.tiles_width, 
			len(map) * tileset.tiles_height
		)).convert()
		self.rect = self.surface.get_rect()
		self.rect.center = area_rect.center
		self.surface.fill(CANVAS_BACKGROUND)

	def draw_map(self):
		"draw_map method"
		i = 0
		self.surface.fill(CANVAS_BACKGROUND)
		for row in self.map:
			for tile_id in row:
				if tile_id >= 0:
					x = (i % len(row)) * self.tileset.tiles_width
					y = floor(i / len(row)) * self.tileset.tiles_height
					self.surface.blit(self.tileset.tiles[int(tile_id)], (x, y))

				i+=1
	
	def draw_tile(self, coord_x, coord_y, tile_index):
		"draw_tile method"
		self.surface.blit(self.tileset.tiles[tile_index], (coord_x, coord_y))

	def erase_tile(self, coord_x, coord_y):
		"erase_tile method"
		blank_tile = pygame.Surface(
				[self.tileset.tiles_width, self.tileset.tiles_height]).convert()
		blank_tile.fill(CANVAS_BACKGROUND)
		self.surface.blit(blank_tile, (coord_x, coord_y))

	def scroll_x(self, step):
		"scroll_x method"
		pass

	def scroll_y(self, step):
		"scroll_y method"
		pass

	def update(self, events, selected_tile_index):
		for e in events:
			if (
				  (e.type == pygame.MOUSEBUTTONDOWN) or \
				  (e.type == pygame.MOUSEMOTION and (e.buttons[0] or e.buttons[2])) \
			) and self.rect.collidepoint(e.pos):

				map_x, map_y = self.get_tile_from_coords(e.pos)
				coord_x = map_x * self.tileset.tiles_width
				coord_y = map_y * self.tileset.tiles_height

				buttons = [0,0,0]
				if e.type == pygame.MOUSEMOTION:
					buttons = e.buttons
				elif e.type == pygame.MOUSEBUTTONDOWN:
					buttons[e.button-1] = 1

				if buttons[0]:
					self.map[map_y][map_x] = selected_tile_index
					self.draw_tile(coord_x, coord_y, selected_tile_index)
				elif buttons[2]:
					self.map[map_y][map_x] = -1
					self.erase_tile(coord_x, coord_y)

	
	def get_tile_from_coords(self, pos):
		map_x = floor((pos[0] - self.rect.x) / self.tileset.tiles_width)
		map_y = floor((pos[1] - self.rect.y) / self.tileset.tiles_height)
		return (map_x, map_y)


if __name__ == "__main__":
	from sys import exit
	import tileset
	
	pygame.init()
	screen = pygame.display.set_mode((500, 350))
	screen.fill((255,255,255))
	
	tset = tileset.Tileset('floortileset.png', 32, 32)

	canv_area = screen.get_rect()
	canv = Canvas(canv_area, MAP, tset)

	while True:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				exit()
		
		canv.update(events, 1) # selected_tile = 1
		
		screen.blit(canv.surface, canv.rect)
		pygame.display.update()
