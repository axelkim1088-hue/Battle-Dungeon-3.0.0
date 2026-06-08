import pygame
import Classes

play_img = pygame.image.load('Play button.png').convert_alpha()
play_button = Classes.Buttons(100, 200, play_img, 10)

exit_img = pygame.image.load('Exit button.png').convert_alpha()
exit_button = Classes.Buttons(500, 200, exit_img, 10)

info_img = pygame.image.load('Info button.png').convert_alpha()
info_button = Classes.Buttons(300, 400, info_img, 10)
