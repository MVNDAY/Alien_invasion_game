import pygame
from pygame.sprite import Sprite 

class Alien(Sprite):
	"""Class for one alien"""
	def __init__(self, ai_settings, screen):
		"""Initialazes an alien and sets its start position"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#Upload alien's image and appoint rect atrribute
		self.image = pygame.image.load('images/alien.png')
		self.rect = self.image.get_rect()

		#Every new alien spawns at left up corner of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Save alien position
		self.x = float(self.rect.x)

	def blitme(self):
		"""Prints an alien at the current position"""
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		"""Returns True if alien is on the edge of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def update(self):
		"""Moves an alien to the right"""
		self.x += (self.ai_settings.alien_speed_factor * 
			self.ai_settings.fleet_direction)
		self.rect.x = self.x




		