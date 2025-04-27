import pygame
from math import floor
from numpy import full

CANVAS_BACKGROUND = (50, 50, 50)

class Canvas:
	"""
	Canvas class.

	Represents the drawing area.

	@param area_rect: The rectangular area where the canvas will be drawn.
	@param map: A 2D array representing the tile map.
	@param tileset

	"""
	def __init__(self, area_rect, map_array, tileset):
		self.map_array = map_array
		self.tileset = tileset

		self.scroll_offset_x = 0
		# clip to area_rect width
		width_in_tiles = self.map_array.width
		if(self.map_array.width * tileset.tiles_width > area_rect.width):
			width_in_tiles = floor(area_rect.width / tileset.tiles_width)

		self.scroll_offset_y = 0
		# clip to area_rect height
		height_in_tiles = self.map_array.height
		if( self.map_array.height * tileset.tiles_height > area_rect.height):
			height_in_tiles = floor(area_rect.height / tileset.tiles_height)

		self.surface = pygame.Surface((
			width_in_tiles * tileset.tiles_width,
			height_in_tiles * tileset.tiles_height
		)).convert()
		
		self.size_in_tiles = (width_in_tiles, height_in_tiles)

		self.rect = self.surface.get_rect()
		self.rect.center = area_rect.center
		self.surface.fill(CANVAS_BACKGROUND)

	def draw_map(self):
		"draw_map method"
		i = 0
		self.surface.fill(CANVAS_BACKGROUND)
		for row in self.map.data[self.scroll_offset_y:self.scroll_offset_y+self.size_in_tiles[1]]:
			for tile_id in row[self.scroll_offset_x:self.scroll_offset_x+self.size_in_tiles[0]]:
				if tile_id >= 0:
					px_x = (i % len(row)) * self.tileset.tiles_width
					px_y = floor(i / len(row)) * self.tileset.tiles_height
					self.surface.blit(self.tileset.tiles[tile_id], (px_x, px_y))
				i+=1

	def redraw_line(self, line_pos, line_orient):
		"redraw_line method"
		for oline_pos in range(0, self.size_in_tiles[line_orient]):
			if(line_orient>0):
				tile = self.map_array.get_at(line_pos+self.scroll_offset_x, oline_pos+self.scroll_offset_y)
				px_x = line_pos * self.tileset.tile_size[0]
				px_y = oline_pos * self.tileset.tile_size[1]
			else:
				tile = self.map_array.get_at(oline_pos+self.scroll_offset_x, line_pos+self.scroll_offset_y)
				px_x = oline_pos * self.tileset.tile_size[0]
				px_y = line_pos * self.tileset.tile_size[1]
			if(tile>=0):
				self.draw_tile(px_x, px_y, tile)
			else:
				self.erase_tile(px_x, px_y)

	def draw_tile(self, px_x, px_y, tile_id):
		"draw_tile method"
		self.surface.blit(self.tileset.tiles[tile_id], (px_x, px_y))

	def erase_tile(self, px_x, px_y):
		"erase_tile method"
		blank_tile = pygame.Surface(self.tileset.get_tile_size()).convert()
		blank_tile.fill(CANVAS_BACKGROUND)
		self.surface.blit(blank_tile, (px_x, px_y))

	def scroll_x(self, step):
		"scroll_x method"
		if(self.scroll_offset_x + step * -1 == -1) or \
		(self.scroll_offset_x + step * -1 > self.map_array.width - self.size_in_tiles[0]):
			return
		
		self.scroll_offset_x += step * -1
		self.surface.scroll(self.tileset.tiles_width * step, 0)
		if(step<0):
			self.redraw_line(floor(self.rect.width/self.tileset.tiles_width)-1, 1)
		else:
			self.redraw_line(0, 1)

	def scroll_y(self, step):
		"scroll_y method"
		if(self.scroll_offset_y + step * -1 == -1) or \
		(self.scroll_offset_y + step * -1 > self.map_array.height - self.size_in_tiles[1]):
			return
		
		self.scroll_offset_y += step * -1
		self.surface.scroll(0, self.tileset.tiles_height * step)
		if(step<0):
			self.redraw_line(floor(self.rect.height/self.tileset.tiles_height)-1, 0)
		else:
			self.redraw_line(0, 0)

	def update(self, events, selected_tile_index):
		for e in events:
			if (
				  (e.type == pygame.MOUSEBUTTONDOWN) or \
				  (e.type == pygame.MOUSEMOTION and (e.buttons[0] or e.buttons[2])) \
			) and self.rect.collidepoint(e.pos):

				map_x, map_y = self.get_tile_from_coords(e.pos)
				coord_x = map_x * self.tileset.tiles_width
				coord_y = map_y * self.tileset.tiles_height

				buttons = pygame.mouse.get_pressed()

				if buttons[0]:
					self.map_array.set_at(map_x + self.scroll_offset_x, map_y + self.scroll_offset_y, selected_tile_index)
					self.draw_tile(coord_x, coord_y, selected_tile_index)
				elif buttons[2]:
					self.map.set_at(map_x + self.scroll_offset_x, map_y + self.scroll_offset_y, -1)
					self.erase_tile(coord_x, coord_y)

			elif e.type == pygame.KEYDOWN:
				if e.key == 13:
					print(self.map_array.data)
				elif e.key == 276: #ARROW_LEFT
					self.scroll_x(1)
				elif e.key == 275: #ARROW_RIGHT
					self.scroll_x(-1)
				elif e.key == 273: #ARROW_UP
					self.scroll_y(1)
				elif e.key == 274: #ARROW_DOWN
					self.scroll_y(-1)

	
	def get_tile_from_coords(self, pos):
		"obtiene las coordenadas sobre la surface en tiles. cambiar nombre variables"
		map_x = floor((pos[0] - self.rect.x) / self.tileset.tiles_width)
		map_y = floor((pos[1] - self.rect.y) / self.tileset.tiles_height)
		return (map_x, map_y)
	

if __name__ == "__main__":
	MAP_SIZE = (10,10)

	from sys import exit
	import tileset, map
	
	pygame.init()
	screen = pygame.display.set_mode((500, 350))
	screen.fill((255,255,255))
	
	tset = tileset.Tileset('floortileset.png', 32, 32)

	canv_area = screen.get_rect()
	mapa = map.Map(MAP_SIZE)
	canv = Canvas(canv_area, mapa, tset)

	while True:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				exit()
		
		canv.update(events, 1) # selected_tile = 1
		
		screen.blit(canv.surface, canv.rect)
		pygame.display.update()
