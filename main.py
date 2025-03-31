import pygame
from numpy import full
from sys import exit

import tileset, tilespalette, canvas

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 350
PALETTE_COLUMNS = 4
TILESET = 'floortileset.png'
TILE_WIDTH = 32
TILE_HEIGHT = 32
MAP = full((10,10), -1)

def main():

	pygame.init()
	screen = pygame.display.set_mode((500, 350))
	print("Tileset image used in this prototype by gfx0 at OpenGameArt.Org\nhttps://opengameart.org/users/gfx0")

	tset = tileset.Tileset(TILESET, TILE_WIDTH, TILE_HEIGHT)
	tpal = tilespalette.TilesPalette(PALETTE_COLUMNS, SCREEN_HEIGHT, tset)
	canv = canvas.Canvas(tpal.surface.get_rect().topright, MAP, tset)

	while True:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.QUIT:
				exit()

		tpal.update(events)
		canv.update(events, tpal.canvas.selected_tile)

		screen.blit(tpal.surface, ((0,0)))
		screen.blit(canv.surface, canv.rect)
		pygame.display.update()

if __name__ == '__main__':
	main()