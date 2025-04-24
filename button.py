import pygame
from pygame.locals import *

BUTTON_BORDER_WEIGHT = 3
BUTTON_HIGHLIGHT_BORDER_COLOR = (200, 200, 200)
BUTTON_SHADOW_BORDER_COLOR = (100, 100, 100)
BUTTON_FACE_COLOR = (150, 150, 150)

class Button:
	"""
	Button class.

	Represents a button object.

	@param x: X coordinate from the topleft corner.
	@param y: Y coordinate from the topleft corner.
	@param width
	@param height

	"""
	def __init__(self, x, y, width, height):
		self.is_pressed = False
		self.surface = pygame.Surface((width, height)).convert()
		self._rect = self.surface.get_rect()
		self.rect = self.surface.get_rect()
		self.rect.topleft = (x, y)
		self.render()
			
	def press(self):
		self.is_pressed = True
		self.render()
		
	def release(self):
		self.is_pressed = False
		self.render()
		
	def render(self):
		border_highlight = BUTTON_HIGHLIGHT_BORDER_COLOR
		border_shadow = BUTTON_SHADOW_BORDER_COLOR
		
		if self.is_pressed:
			border_highlight, border_shadow = border_shadow, border_highlight
		
		self.surface.fill(BUTTON_FACE_COLOR)
		pygame.draw.line(self.surface, border_highlight, self._rect.topleft, self._rect.topright, BUTTON_BORDER_WEIGHT)
		pygame.draw.line(self.surface, border_shadow, self._rect.bottomright, self._rect.topright, BUTTON_BORDER_WEIGHT)
		pygame.draw.line(self.surface, border_highlight, self._rect.bottomleft, self._rect.topleft, BUTTON_BORDER_WEIGHT)
		pygame.draw.line(self.surface, border_shadow, self._rect.bottomleft, self._rect.bottomright, BUTTON_BORDER_WEIGHT)
	
	def update(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos):
				self.press()
				return pygame.MOUSEBUTTONDOWN
			elif e.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(e.pos):
				self.release()
				return pygame.MOUSEBUTTONUP


if __name__ == "__main__":
	from sys import exit
	
	pygame.init()
	screen = pygame.display.set_mode((90, 100))
	screen.fill((255,255,255))
	
	button1 = Button(20, 10, 50, 30)
	button2 = Button(10, 50, 70, 30)
	
	while True:
		events = pygame.event.get()
		for e in events:
			if e.type == QUIT:
				exit()
				
		button1.update(events)
		button2.update(events)
		
		screen.blit(button1.surface, (button1.rect))
		screen.blit(button2.surface, (button2.rect))
		
		pygame.display.update()	
