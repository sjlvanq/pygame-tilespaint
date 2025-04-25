import pygame
from numpy import full
from sys import exit

import tileset, tilespalette, canvas

PALETTE_COLUMNS = 4
TILESET = 'floortileset.png'
TILE_WIDTH = 32
TILE_HEIGHT = 32
MAP = full((6,10), -1)

def main():
	pygame.init()
	print("Tileset image used in this prototype by gfx0 at OpenGameArt.Org\nhttps://opengameart.org/users/gfx0")

	screen = pygame.display.set_mode((500, 350))
	screen_rect = screen.get_rect()

	tset = tileset.Tileset(TILESET, TILE_WIDTH, TILE_HEIGHT)
	tpal = tilespalette.TilesPalette(PALETTE_COLUMNS, screen_rect.height, tset)

	canv_area = pygame.Rect(
		0, 0, # Initial position, will be updated in the next instruction
		screen_rect.width - tpal.rect.width,
		screen_rect.height)
	canv_area.topleft = tpal.rect.topright

	canv = canvas.Canvas(canv_area, MAP, tset)

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