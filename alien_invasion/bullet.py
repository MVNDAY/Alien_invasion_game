import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	def __init__(self,ai_settings,screen,ship):
		"""Class for bullet managment"""
		super().__init__()
		self.screen = screen

		#Create bullet in (0,0) position and appoint the right position
		self.rect = pygame.Rect(0,0,ai_settings.bullet_width, 
		ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		self.image = pygame.image.load('images/bullet.png')
		self.bullet_rect = self.image.get_rect()
		#Bullet position stored in float format
		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		"""Moves bullet up"""
		#Bullet position update in float format
		self.y -= self.speed_factor
		#Update rectangle position
		self.rect.y =self.y

	def draw_bullet(self):
		"""Display a bullet on the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)

