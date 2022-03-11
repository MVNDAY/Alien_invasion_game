import pygame
from pygame.sprite import Group
from pygame import mixer

from settings import Setting
from ship import Ship
from scoreboard import Scoreboard
from button import Button
import game_functions as gf
def run_game():
	#Initializes the game and creates the screen object
	pygame.init()
	pygame.mixer.init(44100,16,2, 1024)
	ai_settings = Setting()
	screen = pygame.display.set_mode((ai_settings.screen_width,
	 ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	clock = pygame.time.Clock()

	#Initialize stats
	sb = Scoreboard(ai_settings, screen)
	sb.load_high_score()

	#Create main menu buttons 
	new_game_button = Button(ai_settings,screen, "NEW GAME",500,350)
	dev_button = Button(ai_settings,screen, "DEVELOPERS", 475,450)
	exit_button = Button(ai_settings,screen, "EXIT", 550, 550)
	
	#Create ship, bullets group and aliens group
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()


	#Create aliens' fleet
	gf.create_fleet(ai_settings,screen, ship, aliens)
	
	# Start the main loop for the game
	while True:
		clock.tick(60)
		if not sb.game_active:
			gf.main_menu(ai_settings,screen,sb,new_game_button,dev_button, exit_button,ship, aliens, bullets) 

		if sb.game_active:
			gf.check_events(ai_settings,screen, sb,
				ship, aliens, bullets)
			ship.update()
			gf.update_bullets(ai_settings,screen, sb, ship,
			 aliens, bullets)
			gf.update_aliens(ai_settings,screen, sb, ship
				, aliens, bullets)
			gf.update_screen(ai_settings, screen, sb, ship,aliens,
				bullets)
run_game()