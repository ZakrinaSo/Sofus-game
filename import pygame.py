import pygame
mage_path = "data/data/org.test.myapp/files/app/"  # Путь к папке с ресурсами на Android
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((600, 234)) #размер экрана ШхВ
pygame.display.set_caption("sofus game ^_^") #название игры
icon = pygame.image.load( "/Users/sofiyaz/Downloads/Игра/изображения/1531899_halloween_icon.png").convert_alpha() #иконка игры
pygame.display.set_icon(icon) 

bg2= pygame.image.load( "/Users/sofiyaz/Downloads/Игра/изображения/seamless-layered-parallax-ready-runner-600nw-457397332.jpg.webp").convert() #фон игры
player= pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/игрок лево/1.png").convert_alpha() #игрок
walk_left = [
    pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/игрок лево/1.png").convert_alpha(),
    pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/игрок лево/2.png").convert_alpha(),
    pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/игрок лево/3.png").convert_alpha(),
    pygame.image.load( "/Users/sofiyaz/Downloads/Игра/изображения/игрок лево/4.png").convert_alpha(),
]

walk_right = [
    pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/игрок право/1.png").convert_alpha(),
    pygame.image.load( "/Users/sofiyaz/Downloads/Игра/изображения/игрок право/2.png").convert_alpha(),
    pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/игрок право/3.png").convert_alpha(),
    pygame.image.load( "/Users/sofiyaz/Downloads/Игра/изображения/игрок право/4.png").convert_alpha(),
]

player_anim_count=0
bg_x=0

player_speed=5
player_x= 50
player_y= 150

is_jumping = False
jump_count = 8

# Переменная для направления
last_direction = "right"  # начальное направление

bg_sound = pygame.mixer.Sound("/Users/sofiyaz/Downloads/Игра/изображения/музыка/1752137222_1nn1-1st3-c1r3c1-p4ln161-v2rs361.mp3")  #фон музыка
bg_sound.play()

vrag=pygame.image.load( "/Users/sofiyaz/Downloads/Игра/изображения/1167878.png").convert_alpha()
vrag_list_in_game=[]
vrag = pygame.transform.scale(vrag, (50,50))

vrag_timer = pygame.USEREVENT + 1 #таймер для появленика врага
pygame.time.set_timer(vrag_timer, 1700)

gameplay = True
victory = False  # Флаг победы

label = pygame.font.Font("/Users/sofiyaz/Downloads/Игра/шрифт/Kablammo-Regular-VariableFont_MORF.ttf", 30)
lose_label= label.render("Теперь ты мой раб :(", False, (255, 0, 0)) 
restart_label= label.render("Проиграть еще раз", True, (55, 10, 20)) 
restart_label_rect = restart_label.get_rect(topleft=(200, 150))

# Добавляем надпись победы
victory_label = label.render("ПОБЕДА! Ты прошел игру!", True, (0, 255, 0))
victory_restart_label = label.render("Играть еще раз", True, (255, 255, 255))
victory_restart_rect = victory_restart_label.get_rect(topleft=(200, 150))

bullet=pygame.image.load("/Users/sofiyaz/Downloads/Игра/изображения/6954583_ball_boom_game_icon.png").convert_alpha()
bullet = pygame.transform.scale(bullet, (30,25))
bullets = []
bullets_call = 3

# Переменная для отслеживания музыки
music_playing = True
music_start_time = pygame.time.get_ticks()
music_duration = 180000  # Длительность трека в миллисекундах (3 минуты)

run=True
while run:
    clock.tick(15) 
    
    # Проверка окончания музыки
    if music_playing and not pygame.mixer.get_busy():
        music_playing = False
        victory = True
        gameplay = False
    
    
    
    # Отрисовка фона
    screen.blit(bg2, (bg_x,0))
    screen.blit(bg2, (bg_x+600,0)) 

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y)) #прямоугольник игрока для столкновений
    
        if vrag_list_in_game:
            for (i,el) in enumerate(vrag_list_in_game):
                screen.blit(vrag, el)
                el.x-=10
                if el.x < -50:
                    vrag_list_in_game.pop(i)
                vrag_collision_rect = pygame.Rect(
                    el.x + 10,      # отступ слева
                    el.y + 10,      # отступ сверху
                    el.width - 20,  # ширина уменьшена на 20
                    el.height - 20  # высота уменьшена на 20
                )

                if player_rect.colliderect(el):
                    gameplay = False    

        keys=pygame.key.get_pressed() #нажатие клавиш
    
    # Движение влево
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            last_direction = "left"
    
    # Движение вправо
        elif keys[pygame.K_RIGHT] and player_x < 550:
            player_x += player_speed
            last_direction = "right"
    
    # Прыжок
        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) * 0.5
                else:
                    player_y += (jump_count ** 2) * 0.5
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 8
                player_y = 150

    # ОДНА отрисовка игрока в зависимости от направления
        if last_direction == "left":
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

    # Анимация игрока (только если движется)
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            player_anim_count += 1
            if player_anim_count >= len(walk_right):
                player_anim_count = 0
        else:
        # Если стоит на месте, показываем первый кадр
            player_anim_count = 0

    # Движение фона
        bg_x -= 5
        if bg_x <= -600:
            bg_x = 0

        
        
        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15

                if el.x > 600:
                    bullets.pop(i)

                if vrag_list_in_game:
                    for (j,vrag_el) in enumerate(vrag_list_in_game):
                        if el.colliderect(vrag_el): #проверка столкновения пули с врагом
                            vrag_list_in_game.pop(j)
                            bullets.pop(i)
                            break    

    elif victory:
        # ЭКРАН ПОБЕДЫ
        screen.fill((0, 0, 0))
        screen.blit(victory_label, (100, 100))
        screen.blit(victory_restart_label, victory_restart_rect)
        
        # Подсветка кнопки при наведении
        mouse = pygame.mouse.get_pos()
        if victory_restart_rect.collidepoint(mouse):
            highlighted_restart = label.render("Играть еще раз", True, (100, 255, 100))
            screen.blit(highlighted_restart, victory_restart_rect)

    else:
        # ЭКРАН ПРОИГРЫША
        screen.fill((0,0, 0))
        screen.blit(lose_label, (20, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True 
            player_x= 50
            vrag_list_in_game.clear()
            bullets.clear()
            bullets_call = 3
            bg_sound.stop()
            bg_sound.play()
            music_playing = True
            music_start_time = pygame.time.get_ticks()

            if pygame.mouse.get_pressed()[0]:
                # Сброс игровых переменных
                gameplay = True
                player_x = 50
                player_y = 150
                vrag_list_in_game.clear()
                player_anim_count = 0
                last_direction = "right"

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            pygame.quit()
            exit()
        if event.type == vrag_timer:
            vrag_list_in_game.append(vrag.get_rect(topleft=(600, 160)))
        
        if gameplay and event.type ==  pygame.KEYUP and event.key == pygame.K_m and bullets_call > 0: #стрельба
            bullets.append(bullet.get_rect(topleft=(player_x + 40, player_y + 15)))    
            bullets_call -= 1
        
        # Обработка клика для экрана победы
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if victory and victory_restart_rect.collidepoint(event.pos):
                # Перезапуск игры
                gameplay = True
                victory = False
                player_x = 50
                player_y = 150
                vrag_list_in_game.clear()
                bullets.clear()
                bullets_call = 3
                player_anim_count = 0
                last_direction = "right"
                bg_x = 0
                
                # Перезапуск музыки
                bg_sound.stop()
                bg_sound.play()
                music_playing = True
                music_start_time = pygame.time.get_ticks()