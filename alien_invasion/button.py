import pygame.font

class Button():

	def __init__(self,ai_settings,screen, msg,x,y):
		"""Initialazes a button"""
		self.screen = screen
		self.screen_rect = screen.get_rect()

		#Size and features of the button
		self.width, self.height = 200,50
		self.button_color = (11,46,100)
		self.text_color = (0,0,0)
		self.font = pygame.font.SysFont(None,48)

		#Create a rect for a button and place at the screen center
		self.rect = pygame.Rect(0,0, self.width, self.height)
		self.rect.y = y
		self.rect.x = x

		#Message for the button creater only once
		self.prep_msg(msg)

	def prep_msg(self,msg):
		"""Makes msg to a rect and places text at center"""
		self.msg_image = self.font.render(msg,True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.x = self.rect.x
		self.msg_image_rect.y = self.rect.y

	def draw_button(self):
		#Print a button
		self.screen.blit(self.msg_image, self.msg_image_rect)