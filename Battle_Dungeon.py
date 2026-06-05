import pygame
import time
import random
import Classes
import Main_menu_screen as Main_menu
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battle Dungeon')

clock = pygame.time.Clock()

game_info = Classes.GameInfo()

FONT = pygame.font.SysFont('comicsans', 30)

def blit_text_centre(text):
    render = FONT.render(text, 1, (255, 255, 255))
    WIN.blit(render, (WIN.get_width()/2 - render.get_width()/2, WIN.get_height()/2 - render.get_height()/2,))


BG = pygame.transform.scale(pygame.image.load('Dungeon Floor.png'), (WIDTH, HEIGHT))

def draw(player, enemies, attack_rect, elapsed_time, game_info, hit_timer):
    WIN.blit(BG, (0, 0))

    player.draw(WIN)

    player_health = FONT.render(f'{player.health}/{player.max_health}', 1, (255, 255, 255))
    WIN.blit(player_health, (player.rect.x, player.rect.y - 20))

    for enemy in enemies:
        enemy.draw(WIN)
        enemy_health = FONT.render(f'{enemy.health}/{enemy.max_health}', 1, (255, 255, 255)) 
        WIN.blit(enemy_health, (enemy.rect.x, enemy.rect.y - 20))
        
    if player.attack_timer > 0:
        attack_rect = pygame.Rect(player.rect.x - 20, player.rect.y - 20, player.rect.width + 40, player.rect.height + 40)
        pygame.draw.rect(WIN, (255, 255, 0), attack_rect, 2)
    
    if hit_timer > 0:
        hit_rect = pygame.Rect(player.rect.x - 20, player.rect.y - 20, player.rect.width + 40, player.rect.height + 40)
        pygame.draw.rect(WIN, (200, 0, 0), hit_rect, 2)

    level_text = FONT.render(f'Level: {game_info.level}', 1, (255, 255, 255))
    WIN.blit(level_text, (550, level_text.get_height() - 30))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')
    WIN.blit(time_text, (10, 10))

def main():
    state = 'menu'
    running = True

    game_initialised = False
    
    while running:
        if state == 'menu':
            WIN.fill((150, 150, 150))

            Title = FONT.render('BATTLE DUNGEON', 1, 'white')
            WIN.blit(Title, (250, 20))

            if Main_menu.play_button.draw(WIN):
                print('Play')
                state = 'game'
            if Main_menu.exit_button.draw(WIN):
                running = False
            if Main_menu.info_button.draw(WIN):
                state = 'info'

            for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
            
            pygame.display.update()

        elif state == 'info':
            WIN.fill((150, 150, 150))

            Title_text = FONT.render('Info Screen', 1, 'white')
            WIN.blit(Title_text, (300, 20))

            Control_text = FONT.render('Controls:', 1, 'white')
            WIN.blit(Control_text, (330, 50))

            Left_text = FONT.render('To move Left: a or left arrow key', 1, 'white')
            WIN.blit(Left_text, (180, 80))

            Right_text = FONT.render('To move Right: d or right arrow key', 1, 'white')
            WIN.blit(Right_text, (160, 110))

            Up_text = FONT.render('To move Up: w or up arrow key', 1, 'white')
            WIN.blit(Up_text, (180, 140))

            Down_text = FONT.render('To move Down: s or down arrow key', 1, 'white')
            WIN.blit(Down_text, (160, 170))

            Attack_text = FONT.render('To Attack: space', 1, 'white')
            WIN.blit(Attack_text, (270, 200))

            Enemy_text = FONT.render('Enemy Information:', 1, 'white')
            WIN.blit(Enemy_text, (240, 260))

            Tanker_stats = FONT.render('Tanker stats: HP: 100, Damage: Insta-kill', 1, 'white')
            WIN.blit(Tanker_stats, (110, 290))

            Soldier_stats = FONT.render('Soldier stats: HP: 75, Damage: 40', 1, 'white')
            WIN.blit(Soldier_stats, (160, 320))

            Speedster_stats = FONT.render('Speedster stats: HP: 50, Damage: 20', 1, 'white')
            WIN.blit(Speedster_stats, (150, 350))

            Exit_text = FONT.render('Press any key to return to main menu', 1, 'white')
            WIN.blit(Exit_text, (150, 500))

            for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

                        if event.type == pygame.KEYDOWN:
                            state = 'menu'

            
            
            pygame.display.update()

        elif state == 'game':
            if not game_initialised:
                level_transition = False

                hit_cooldown = 30

                hit_timer = 0

                player = Classes.Player(380, 280, 40, 40, 6, WIDTH, HEIGHT, 100)

                start_time = time.time()

                enemies = Classes.Enemy.spawn_enemies(player, game_info.level, 40)

                game_initialised = True

            clock.tick(60)
            elapsed_time = time.time() - start_time

            if hit_cooldown > 0:
                hit_cooldown -= 1
            
            if hit_timer > 0:
                hit_timer -= 1

            if elapsed_time >= (15 + (game_info.level - 1)*5) or len(enemies) <= 0:
                level_transition = True

                draw(player, enemies, player.current_attack, elapsed_time, game_info, hit_timer)
                victory_text = (f'You beat level {game_info.level}!')
                blit_text_centre(victory_text)
                pygame.display.update()
                pygame.time.delay(3000)
                
                draw(player, enemies, player.current_attack, elapsed_time, game_info, hit_timer)

                game_info.next_level()

                player.health = 100
                
                if game_info.game_finished():
                    state = 'menu'
                    continue

                enemies = Classes.Enemy.spawn_enemies(player, game_info.level, 40)
                start_time = time.time()

                level_transition = False
                continue
            
            while not game_info.started:
                WIN.fill((0, 0, 0))
                blit_text_centre(f'Press any key to start level {game_info.level}')
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break
                    
                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()


            if player.current_attack:
                for enemy in enemies[:]:
                    if player.current_attack.colliderect(enemy.rect):
                        if enemy not in player.hit_enemies:
                            player.hit_enemies.add(enemy)
                            enemy.health -= 25
                            if enemy.health <= 0:
                                enemies.remove(enemy)

                        

            player.update_cooldown()
            
            for enemy in enemies:
                enemy.update(player.rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            keys = pygame.key.get_pressed()

            player.move(keys)
            
            hit = False


            if player.current_attack:
                player.current_attack.x = player.rect.x - 20
                player.current_attack.y = player.rect.y -20
            
            if player.attack_timer > 0:
                player.attack_timer -= 1
            else:
                player.current_attack = None

            if keys[pygame.K_SPACE] and player.attack_cooldown <= 0 and player.attack_timer == 0:
                player.start_attack()

            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    if hit_cooldown <= 0:
                        player.health -= enemy.damage
                        hit_timer = 20
                        hit_cooldown = 30
                    hit = True


            if hit:
                if player.health <= 0:
                    draw(player, enemies, player.current_attack, elapsed_time, game_info, hit_timer,)
                    lose_text = FONT.render('You Died!', 1, 'white')
                    WIN.blit(lose_text, (WIDTH/2 - lose_text.get_width()/2, HEIGHT/2 - lose_text.get_height()/2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    
                    state = 'menu'
                else:
                    pass
            
            draw(player, enemies, player.current_attack, elapsed_time, game_info, hit_timer)
            pygame.display.update()

        
    pygame.quit()

if __name__ == '__main__':
    main()