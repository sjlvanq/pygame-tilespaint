import pygame
from pygame.locals import *

class Tileset:
	"""
	Class Tileset.

	Represents a tileset.

	This class loads a tileset image and provides methods to divide it
	into individual tiles and retrieve them.

	"""
	def __init__(self, filename, tile_width, tile_height):
		self.tileset = pygame.image.load(filename).convert()
		self.tiles_width, self.tiles_height = tile_width, tile_height
		tileset_width, tileset_height = self.tileset.get_rect().size
		self.tileset_cols = int(tileset_width / tile_width)
		self.tileset_rows = int(tileset_height / tile_height)
		self.tiles = []
		self.load_tiles(tile_width, tile_height)
		
	def load_tiles(self, tile_width, tile_height):
		for col in range(0, self.tileset_cols):
			for row in range(0, self.tileset_rows):
				self.tiles.append(self.get_tile(row, col, tile_width, tile_height))
				
	def get_tile(self, x, y, width, height):
		tile = pygame.Surface([width, height]).convert()
		tile.blit(self.tileset, (0, 0), (x*width, y*height, x*width+width, y*height+height))
		return tile


if __name__ == "__main__":
	"""Test"""
	from math import floor
	from sys import exit
	
	pygame.init()
	screen = pygame.display.set_mode((500, 350))
	screen.fill((255,255,255))

	tileset = Tileset("numeros.png", 48, 48)
	totalcols = int(500 / 48)
	totalrows = int(350 / 48)
	
	clock = pygame.time.Clock()

	frame = 0
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
		

		x = (frame % totalcols) * 48
		y = ((floor(frame / totalcols) % totalrows) * 48 ) % 350
		#print('x: %s, y: %s' % (x,y))
		
		screen.blit(tileset.tiles[frame%len(tileset.tiles)], ((x,y)))
		pygame.display.update()
		frame+=1
		
		clock.tick(20)
