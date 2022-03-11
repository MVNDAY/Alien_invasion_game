import pygame
import sys
from button import Button

def run_game():
	#Initializes the game and creates the screen object
	pygame.init()
	screen = pygame.display.set_mode((1200,800))
	pygame.display.set_caption("Main Menu")
	clock = pygame.time.Clock()
	bg_color = (11,46,67)
	bg_image = pygame.image.load('images/bg.png')

	#Main Game Loop
	while True:
		clock.tick(60)
		screen.fill((11,46,67))
		screen.blit(bg_image, (0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
	# Show the last screen
	pygame.display.flip()

run_game()
