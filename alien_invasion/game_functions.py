import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame import mixer

def check_keydown_events(event,ai_settings,sb, screen, ship,bullets):
	"""Reacts on key presses"""
	if event.key == pygame.K_d:
		ship.moving_right = True
	elif event.key == pygame.K_a:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sb.game_active = False
		pygame.mouse.set_visible(True)

def check_keyup_events(event,ship):
	if event.key == pygame.K_d:
		ship.moving_right = False
	elif event.key == pygame.K_a:
		ship.moving_left = False

def check_events(ai_settings,screen, sb, ship, aliens, bullets):
	"""Tracing mouse and keyboard events"""
	for event in pygame.event.get():
		if event.type == pygame.K_q:
			sys.exit()
		elif event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings, sb, screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)


def update_screen(ai_settings,screen, sb, ship,aliens, bullets,):
	"""Updates screen images and shows the new screen"""
	#Every iteration will redraw the screen
	screen.fill(ai_settings.bg_color)
	screen.blit(ai_settings.bg_image, (0,0))
	#All bullets display behind the ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	#Print score
	sb.show_score()
	sb.show_high_score()
	sb.show_level()
	sb.show_ships()

	# Show the last screen
	pygame.display.flip()

def ship_hit(ai_settings,screen,sb, ship,aliens, bullets):
	"""Proccess ship hit by alien"""
	if sb.ships_left > 0:
		#Ships_left decrease
		sb.ships_left -= 1
		sb.show_ships()
		#Delete aliens and bullets
		aliens.empty()
		bullets.empty()

		#Create new fleet and place a new ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#Pause
		sleep(1)
	else:
		sb.game_active = False
		pygame.mouse.set_visible(True)
		if sb.score == sb.high_score:
			sb.write_high_score()

def update_bullets(ai_settings, screen, sb, ship, aliens, bullets):
	"""Updates bullets positions and deletes old ones"""
	#Bullet position update
	bullets.update()
	#Delete bullets out of screen
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen,sb, ship, aliens, bullets):
	"""Bullet-alien collisions proccesing"""
	#Delete bullets and aliens, participating in collisions
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			sb.score += ai_settings.alien_points * len(aliens)
			sb.show_score()
			check_high_score(sb)
	if len(aliens) == 0:
		#Destroy existing bullets, increase speed and create new fleet
		bullets.empty()
		ai_settings.increase_speed()

		#Level up
		sb.level += 1 
		sb.show_level()
		create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
	"""Fires a bullets if max is not reached"""
	#Create new bullet and add to 'bullets' group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen,ship)
		bullets.add(new_bullet)
		
def get_number_aliens_x(ai_settings, alien_width):
	"""Calculates aliens's quantity in a row"""
	avialable_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avialable_space_x / (2*alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number, row_number):
	"""Create an alien and place it in a row"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship , aliens):
	"""Creates an aliens' fleet"""
	#Create an alien and calculate the aliens quantity in a row

	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)

	#Create aliens' fleet
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number, 
			row_number)

def get_number_rows(ai_settings,ship_height,alien_height):
	"""Sets the number of rows"""
	avialable_space_y = (ai_settings.screen_height -
		3 * alien_height - ship_height)
	number_rows = int(avialable_space_y / (2 * alien_height))
	return number_rows
def update_aliens(ai_settings,screen, sb, ship, aliens, bullets):
	"""Checks if fleet reached the edge"""
	"""Afterwards updates positions of all aliens"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	#Check for alien-ship collisions
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen, sb, ship,aliens, bullets)
	check_aliens_bottom(ai_settings, screen, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings,aliens):
	"""Reacts on alien reched the edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Moves the fleet down and changes its direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings. fleet_direction *= -1

def check_aliens_bottom(ai_settings,screen,sb, ship, aliens, bullets):
	"""Check if aliens reached the bottom"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Reset the game
			ship_hit(ai_settings, screen,sb, ship, aliens, bullets)
			break

def check_high_score(sb):
	"""Check if highscore was reached"""
	if sb.score > sb.high_score:
		sb.high_score = sb.score
		sb.show_high_score()

def main_menu(ai_settings,screen,sb,new_game_button,dev_button, exit_button,ship, aliens, bullets):
	#Show main menu
	screen.blit(ai_settings.bg_image, (0,0))
	show_dev = False
	new_game_button.draw_button()
	exit_button.draw_button()
	dev_button.draw_button()
	main_menu_events(ai_settings,screen,sb,new_game_button,dev_button, exit_button,ship, aliens, bullets)
	pygame.display.flip()

def main_menu_events(ai_settings,screen,sb, new_game_button,dev_button, exit_button,ship, aliens, bullets):
	#Check for button collisions
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			
			#Check if any button was clicked
			mouse_x, mouse_y = pygame.mouse.get_pos()
			game_button_clicked = new_game_button.rect.collidepoint(mouse_x, mouse_y)
			exit_button_clicked = exit_button.rect.collidepoint(mouse_x,mouse_y)
			dev_button_clicked = dev_button.rect.collidepoint(mouse_x,mouse_y)

			#New game button was clicked
			if game_button_clicked and not sb.game_active:
				start_new_game(ai_settings,screen,sb,ship, aliens, bullets)
			
			#Exit button was clicked
			elif exit_button_clicked and not sb.game_active:
				sys.exit()
			
			#Developers button was clicked
			elif dev_button_clicked and not sb.game_active:
				show_dev = True
				while show_dev == True:
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
							main_menu(ai_settings,screen,sb,new_game_button,dev_button, exit_button,ship, aliens, bullets)
							show_dev = False
					screen.blit(ai_settings.bg_image, (0,0))
					screen.blit(ai_settings.titres_image, (0,0))
					pygame.display.flip()
				

def start_new_game(ai_settings,screen,sb,ship, aliens, bullets):
	#Reset all game settings
	ai_settings.initizalize_dynamic_settings()
	bullets.empty()
	aliens.empty()
	#Mouse poiner hides
	pygame.mouse.set_visible(False)

	sb.reset_stats()
	sb.game_active = True
	sb.load_high_score()
	sb.show_score()
	sb.show_level()
	sb.show_high_score()
	sb.show_ships()
	#Create new fleet and place new ship
	create_fleet(ai_settings, screen,ship,aliens)
	ship.center_ship()