import pygame
import sys
import random
from Background import Background
from Card import Card
import math


pygame.init()


# Setting up the display
screen_width, screen_height = 540, 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Matching Maddness")

#Clock to limit FPS
clock = pygame.time.Clock()


#Setting up the background
frames = ["bg_imgs/frame_000.png","bg_imgs/frame_001.png","bg_imgs/frame_002.png","bg_imgs/frame_003.png","bg_imgs/frame_004.png","bg_imgs/frame_005.png","bg_imgs/frame_006.png","bg_imgs/frame_007.png","bg_imgs/frame_008.png","bg_imgs/frame_009.png"]
bg = Background(frames, 20, 120)

points_dict = {1:(40,170), 2:(205,170), 3:(370,170),
               4:(40,420), 5:(205,420), 6:(370,420),
               7:(40,670), 8:(205,670), 9:(370,670)}


# Set up the mixer
pygame.mixer.init()
pygame.mixer.music.load("music/SKYLINE.mp3")
pygame.mixer.music.set_volume(0.02)  # You can adjust the volume from 0.0 to 1.0
pygame.mixer.music.play(loops=-1)


# Set up the font for on screen text
font = pygame.font.Font(None, 36)  # You can choose a font and size (or use None for the default font)


#Card Arrays for game
all_cards = []
cards_in_play = []
cards_flipped = 0

#Card generator with random images
card_images = ["card_imgs/CuteCard1.jpg", "card_imgs/CuteCard2.jpg", "card_imgs/CuteCard3.jpg", "card_imgs/CuteCard4.jpg", "card_imgs/CuteCard5.jpg","card_imgs/CuteCard6.jpg","card_imgs/CuteCard7.jpg","card_imgs/CuteCard8.jpg"]
available_loc_keys = [1,2,3,4,5,6,7,8,9]

for i in range(4):
    rand_img = random.randint(0, (len(card_images) - 1))
    
    #Card 1 is generated here
    rand_keyA = random.randint(0, (len(available_loc_keys) - 1))
    A_Key = available_loc_keys[rand_keyA]
    cardA = Card("card_imgs/card_back.png", card_images[rand_img],points_dict[A_Key][0], points_dict[A_Key][1])
    available_loc_keys.pop(rand_keyA)
    all_cards.append(cardA)
    cards_in_play.append(cardA)
    
    #Card 2 matching Card 1 is generated here
    rand_keyB = random.randint(0, (len(available_loc_keys) - 1))
    B_Key = available_loc_keys[rand_keyB]
    cardB = Card("card_imgs/card_back.png", card_images[rand_img],points_dict[B_Key][0], points_dict[B_Key][1])
    available_loc_keys.pop(rand_keyB)
    all_cards.append(cardB)
    cards_in_play.append(cardB)
    
    card_images.pop(rand_img)

#Bad Card always the same image
badcard = Card("card_imgs/card_back.png","card_imgs/BadCard1.jpg",points_dict[available_loc_keys[0]][0],points_dict[available_loc_keys[0]][1])
all_cards.append(badcard)
cards_in_play.append(badcard)

# Game loop
running = True
fps = 60
delay_duration = 500  # milliseconds
set_time = 30 
introMessage = True

while introMessage:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            introMessage = False
            running = False
        if event.type == pygame.FINGERDOWN:
            pygame.time.delay(delay_duration)
            introMessage = False;
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.time.delay(delay_duration)
            introMessage = False;
            
    myMessage = pygame.image.load("msgs/MyMessage.png")
    myMessageRect = myMessage.get_rect()
    myMessageRect.x = 0
    myMessageRect.y = 0      

    screen.fill((255,255,255))
    
    screen.blit(myMessage, myMessageRect)
    
    pygame.display.flip()    
    
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            touchX, touchY = event.pos
            #print("X touch: "+ str(touchX) + "\nY touch: " + str(touchY))
            
            
            if cards_flipped < 2:    
                for card in cards_in_play:
                    if card.rect.collidepoint((touchX,touchY)):
                        card.is_flipped = True
                        cards_flipped += 1
                
                if badcard.is_flipped == True:
                    #Allows cards to be displayed to screen with delay
                    for card in cards_in_play:    
                        card.update()
                        card.draw(screen)    
                    
                    pygame.display.flip()
                    pygame.time.delay(delay_duration) 
                    
                    
                    #Bad Card resets position of all the cards in play
                    dict_keys = [1,2,3,4,5,6,7,8,9]
                    for card in cards_in_play:
                        random_num = random.randint(0,len(dict_keys) - 1)
                        card.rect.x = points_dict[dict_keys[random_num]][0]
                        card.rect.y = points_dict[dict_keys[random_num]][1]
                        dict_keys.pop(random_num)
                    
                    #Flips cards to back side and draws the shuffled cards to screen
                    for card in cards_in_play:    
                        card.is_flipped = False
                        card.update()
                        card.draw(screen)
                    
                    pygame.display.flip()    
                    cards_flipped = 0

                        
                    
            if cards_flipped == 2:
                #Stores flipped cards in array to check
                flipped_array = []
                for card in cards_in_play:
                    if card.is_flipped == True:
                        flipped_array.append(card)
                
                #Once two cards flipped we check if the cards relative path names match
                if len(flipped_array) == 2:
                    if flipped_array[0].name == flipped_array[1].name:
                        print("Match")
                        
                        #This allows cards to be shown on screen to player to check match
                        for card in flipped_array:
                            card.is_flipped = True
                            card.update()
                            card.draw(screen)
                            
                        pygame.display.flip()
                        pygame.time.delay(delay_duration)    
                        
                        for card in flipped_array:
                            if card in cards_in_play:
                                #Sets card match to True and moves card off board to allow cards space
                                card.match_found = True
                                card.rect.x = 545
                                card.rect.y = 965
                                cards_in_play.remove(card)
                                
                        for card in cards_in_play:
                            card.is_flipped = False
                        
                    else:
                        print("No match")
                        
                        #This allows cards to be shown on screen to player to check match
                        for card in flipped_array:
                            card.is_flipped = True
                            card.update()
                            card.draw(screen)
                            
                        pygame.display.flip()
                        pygame.time.delay(delay_duration)
                        
                        for card in cards_in_play:
                            card.is_flipped = False
                
                
                cards_flipped = 0
                flipped_array = []
            
                
        if event.type == pygame.FINGERDOWN:
            #print(event)
            touchX, touchY = event.x * screen_width, event.y * screen_height

            if cards_flipped < 2:    
                for card in cards_in_play:
                    if card.rect.collidepoint((touchX,touchY)):
                        card.is_flipped = True
                        cards_flipped += 1
                
                if badcard.is_flipped == True:
                    #Allows cards to be displayed to screen with delay
                    for card in cards_in_play:    
                        card.update()
                        card.draw(screen)    
                    
                    pygame.display.flip()
                    pygame.time.delay(delay_duration) 
                    
                    
                    #Bad Card resets position of all the cards in play
                    dict_keys = [1,2,3,4,5,6,7,8,9]
                    for card in cards_in_play:
                        random_num = random.randint(0,len(dict_keys) - 1)
                        card.rect.x = points_dict[dict_keys[random_num]][0]
                        card.rect.y = points_dict[dict_keys[random_num]][1]
                        dict_keys.pop(random_num)
                    
                    #Flips cards to back side and draws the shuffled cards to screen
                    for card in cards_in_play:    
                        card.is_flipped = False
                        card.update()
                        card.draw(screen)
                    
                    pygame.display.flip()    
                    cards_flipped = 0

                        
                    
            if cards_flipped == 2:
                #Stores flipped cards in array to check
                flipped_array = []
                for card in cards_in_play:
                    if card.is_flipped == True:
                        flipped_array.append(card)
                
                #Once two cards flipped we check if the cards relative path names match
                if len(flipped_array) == 2:
                    if flipped_array[0].name == flipped_array[1].name:
                        print("Match")
                        
                        #This allows cards to be shown on screen to player to check match
                        for card in flipped_array:
                            card.is_flipped = True
                            card.update()
                            card.draw(screen)
                            
                        pygame.display.flip()
                        pygame.time.delay(delay_duration)    
                        
                        for card in flipped_array:
                            if card in cards_in_play:
                                #Sets card match to True and moves card off board to allow cards space
                                card.match_found = True
                                card.rect.x = 545
                                card.rect.y = 965
                                cards_in_play.remove(card)
                                
                        for card in cards_in_play:
                            card.is_flipped = False
                        
                    else:
                        print("No match")
                        
                        #This allows cards to be shown on screen to player to check match
                        for card in flipped_array:
                            card.is_flipped = True
                            card.update()
                            card.draw(screen)
                            
                        pygame.display.flip()
                        pygame.time.delay(delay_duration)
                        
                        for card in cards_in_play:
                            card.is_flipped = False
                
                
                cards_flipped = 0
                flipped_array = []


    # Clear the screen
    screen.fill((0,0,0))
    
    
    
    #TIMER CHECK
    time_left = set_time - math.floor(pygame.time.get_ticks()/1000)
    if time_left <= 0:
        time_left = 0
    
    #TIMER RUNS OUT
    if time_left == 0:
        screen.fill((0,0,0))
        if badcard in cards_in_play:
            cards_in_play.remove(badcard)
        cards_in_play = []
        #print("GAME OVER")
        lose_msg = pygame.image.load("msgs/LoseMessage.png")
        lose_rect = lose_msg.get_rect()
        lose_width, lose_height = lose_msg.get_size()
        lose_rect.x = (screen_width - lose_width) // 2
        lose_rect.y = (screen_height - lose_height) // 2
        screen.blit(lose_msg,lose_rect)
        
        #Restart Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                touchX, touchY = event.pos
                if lose_rect.collidepoint((touchX,touchY)):
                    print(str(touchX) + " " + str(touchY))
                    dict_keys = [1,2,3,4,5,6,7,8,9]
                    for card in all_cards:
                        random_num = random.randint(0,len(dict_keys) - 1)
                        card.rect.x = points_dict[dict_keys[random_num]][0]
                        card.rect.y = points_dict[dict_keys[random_num]][1]
                        card.match_found = False
                        card.is_flipped = False
                        dict_keys.pop(random_num)
                        cards_in_play.append(card)
                    set_time = 30 + math.floor(pygame.time.get_ticks()/1000)
                    
            if event.type == pygame.FINGERDOWN:
                touchX, touchY = event.x * screen_width, event.y * screen_height
                if lose_rect.collidepoint((touchX,touchY)):
                    print(str(touchX) + " " + str(touchY))
                    dict_keys = [1,2,3,4,5,6,7,8,9]
                    for card in all_cards:
                        random_num = random.randint(0,len(dict_keys) - 1)
                        card.rect.x = points_dict[dict_keys[random_num]][0]
                        card.rect.y = points_dict[dict_keys[random_num]][1]
                        card.match_found = False
                        card.is_flipped = False
                        dict_keys.pop(random_num)
                        cards_in_play.append(card)
                    set_time = 30 + math.floor(pygame.time.get_ticks()/1000)
                
                
                
                
    #NO CARDS LEFT TO CHECK
    elif cards_in_play == [badcard] or cards_in_play == []:
        screen.fill((0,0,0))
        set_time = 10 + math.floor(pygame.time.get_ticks()/1000)
        if badcard in cards_in_play:
            cards_in_play.remove(badcard)
        cards_in_play = []
        #print("YOU WIN")
        win_msg = pygame.image.load("msgs/WinMessage.png")
        win_rect = win_msg.get_rect()
        win_width, win_height = win_msg.get_size()
        win_rect.x = (screen_width - win_width) // 2
        win_rect.y = (screen_height - win_height) // 2
        screen.blit(win_msg, win_rect)
        
        #Restart Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                touchX, touchY = event.pos
                if win_rect.collidepoint((touchX,touchY)):
                    print(str(touchX) + " " + str(touchY))
                    dict_keys = [1,2,3,4,5,6,7,8,9]
                    for card in all_cards:
                        random_num = random.randint(0,len(dict_keys) - 1)
                        card.rect.x = points_dict[dict_keys[random_num]][0]
                        card.rect.y = points_dict[dict_keys[random_num]][1]
                        card.match_found = False
                        card.is_flipped = False
                        dict_keys.pop(random_num)
                        cards_in_play.append(card)
                    set_time = 30 + math.floor(pygame.time.get_ticks()/1000)
            
            if event.type == pygame.FINGERDOWN:
                touchX, touchY = event.x * screen_width, event.y * screen_height
                if lose_rect.collidepoint((touchX,touchY)):
                    print(str(touchX) + " " + str(touchY))
                    dict_keys = [1,2,3,4,5,6,7,8,9]
                    for card in all_cards:
                        random_num = random.randint(0,len(dict_keys) - 1)
                        card.rect.x = points_dict[dict_keys[random_num]][0]
                        card.rect.y = points_dict[dict_keys[random_num]][1]
                        card.match_found = False
                        card.is_flipped = False
                        dict_keys.pop(random_num)
                        cards_in_play.append(card)
                    set_time = 30 + math.floor(pygame.time.get_ticks()/1000)        
    
        
    
        
    else:
        #Updates for sprites
        bg.update()
        for card in cards_in_play:
            if card.match_found == False:
                card.update()
        
        
        
        #Draw all sprites
        bg.draw(screen)
        for card in cards_in_play:
            if card.match_found == False:
                card.draw(screen)

        clock.tick(fps)
        
        
        
        #TIMER TEXT 
        timer_text_surface = font.render("Timer: " + str(time_left), True, (255, 255, 255))
        text_rect = timer_text_surface.get_rect(topleft=(10, 10))
        screen.blit(timer_text_surface, text_rect)


    #print(pygame.time.get_ticks())
    #Updates the screen display
    pygame.display.flip()

pygame.quit()
sys.exit()