import pygame
import random
import Game
import Ghost

WIDTH = 1000
HEIGHT = 600

def check_events():
    quit = False
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
    return quit

class Level:
    cursor_img = pygame.image.load('images/mouse.png')
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    page = 1
    background = None
    #background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_track = 0   #keep track of the background
    text_track = 0         #keep track of text
    card_choose = []       #cards that the player can choose
    skill_choose = []      #skills that the player can choose
    ghost_track = 0        #keep track of ghost
    first = 0              #when first is equal to 7,player enter choose skill page
    
    def draw_cursor(self, x, y):
        self.screen.blit(self.cursor_img, (x, y))
        
    def __init__(self,level,player,ghosts,texts,cards,skills,backgrounds,audio):
        
        self.level = level
        self.player = player   #characte player choose for this level(class)
        self.ghosts = ghosts     #ghost list
        self.texts = texts       #list of lists of text
        self.cards = cards     #list of all the cards
        self.skills = skills   #list of passive skills
        self.backgrounds = backgrounds   #list of background used in the level
        self.audio=audio
        
        self.initial_strength = self.player.strength
        self.initial_health_point = self.player.health_point
    
    def conversation_text(self,text):
        text_box_image = pygame.image.load('level_images/text_box.png')
        text_box_image = pygame.transform.scale(text_box_image, (800, 100))  #230, 180, 0
        text_button = Button(200,400,text_box_image,text,Game.font_name, 15, (255, 255, 255), offset_y=-5)
        text_button.draw(self.screen)
        return text_button

    def choose_cards(self):

        x = 200
        y = 150

        cards_button = []
        for i in range(0,3):
            n = random.randrange(0,len(self.cards))
            card = self.cards[n]
            self.card_choose.append(card)
            card_image=pygame.transform.scale(card.image, (200, 300))  ###???
            card_button = Button(x,y,card_image," ",Game.font_name, 30, (230, 180, 0), offset_y=-5)

            ###self.screen or self.screen
            card_button.draw(self.screen)
            cards_button.append(card_button)
            ### out of range, ingnore this line
            #self.cards.pop(n)
            x += 250
        return cards_button

    def choose_skills(self):
        x = 200
        y = 150
        for i in range(0,3):
            n = random.randrange(0,len(self.skills))
            skill = self.skill[n]
            self.skill_choose.append(skill)
            skill_image=pygame.transform.scale(skill.image, (200, 300))  ###???
            skill_button = Button(x,y,skill_image," ",Game.font_name, 30, (230, 180, 0), offset_y=-5)

            ###self.screen or self.screen
            skill_button.draw(self.screen)

            skills_button.append(skill_button)

            ### out of range, ingnore this line
            #self.cards.pop(n)
            x += 250
        return skills_button

    def main_page(self):
        '''     player image
                health point bar at the top left corner
        '''
        condition_bar = pygame.image.load('level_images/health_point_bar.png')
        condition_bar = pygame.transform.scale(condition_bar,(200,60))
        self.screen.blit(condition_bar,(20,30))

        health_point_image = pygame.image.load('level_images/health_point.png')
        health_point_image = pygame.transform.scale(health_point_image,(50,50))
        self.screen.blit(health_point_image,(55,38))

        font = pygame.font.SysFont("freesansbold.ttf", 30)
        health_point = font.render(str(int(self.player.health_point)), True, (255, 255, 255))
        self.screen.blit(health_point,(120, 54))
        self.player.show_in_levels(self.screen)

        
    def game_page(self):
        #blit image of ghost
        ghost_image = self.ghosts[self.ghost_track].image
        ghost_image = pygame.transform.scale(ghost_image,(230,330))
        self.screen.blit(ghost_image,(680,50))

        #blit player
        self.player.show_in_levels_fight(self.screen)  ###

        #blit player condition bar
        condition_bar = pygame.image.load('level_images/health_point_bar.png')
        condition_bar = pygame.transform.scale(condition_bar,(200,60))
        self.screen.blit(condition_bar,(20,30))

        health_point_image = pygame.image.load('level_images/health_point.png')
        health_point_image = pygame.transform.scale(health_point_image,(50,50))
        self.screen.blit(health_point_image,(55,38))

        #blit ghost condition bar
        self.screen.blit(condition_bar,(780,30))
        self.screen.blit(health_point_image,(815,38))

        cards_button = []
        x = 250
        y = 400
        for card in self.player.cards:
            card_image = pygame.transform.scale(card.image, (100, 150))
            card_button = Button(x,y,card_image," ",Game.font_name, 30, (230, 180, 0), offset_y=-5)
            cards_button.append(card_button)
            card_button.draw(self.screen)  ###???   self.screen replacing self.background
            x += 150

        #pygame.display.flip() ###

        return cards_button
    

    def win_lost(self,ghost):
        #vin
        if self.player.health_point >= 0:
            victory_image = pygame.image.load('level_images/victory.png')
            victory_button = Button(500,300,victory_image," ",Game.font_name, 30, (230, 180, 0), offset_y=-5)
            victory_button.draw(self.screen) ###???   self.screen replacing self.background
            return victory_button    ### it should return Failure button. Just for test purpose

        #lost
        if ghost.health_point >= 0:
            victory_image = pygame.image.load('level_images/victory.png')
            victory_button = Button(450,300,victory_image," ",Game.font_name, 30, (230, 180, 0), offset_y=-5)
            victory_button.draw(self.screen) ###???   self.screen replacing self.background
            return victory_button

    def change_background(self,image):
        main_background = pygame.transform.scale(image, (WIDTH, HEIGHT))
        self.background = main_background

    def paint_background(self):
        self.screen.blit(self.background, (0, 0))

    def check_type(self,player,ghost):   ### check player and ghost relative attributes
        if player.element == "water":
            if ghost.element == "fire":
                player.strength += 10
            if ghost.element == "Earth":
                player.strength -= 10
        elif player.element == "fire":
            if ghost.element == "water":
                player.strength -= 10
            if ghost.element == "metal":
                player.strength += 10
        elif player.element == "wood":
            if ghost.element == "earth":
                player.strength += 10
            if ghost.element == "metal":
                player.strength -= 10
        elif player.element == "metal":
            if ghost.element == "wood":
                player.strangth += 10
            if ghost.element == "fire":
                player.strength -= 10
        elif player.element == "earth":
            if ghost.element == "water":
                player.strength += 10
            if ghost.element == "wood":
                player.strength -= 10
                
    def recover_initial_strength(self):
        if self.player.strength > self.initial_strength:
            self.player.strength -= 10
        if self.player.strength < self.initial_strength:
            self.player.strength += 10
        
    def run(self):
        pygame.init()
        pygame.display.set_caption('None')
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        #intial the new backgroud
        Game.Game.screen.blit(self.backgrounds[self.background_track], (0, 0))
        next_background = self.backgrounds[self.background_track]
        self.change_background(next_background)
        self.background=next_background

        #pygame.display.flip()

        # page to choose card, if player just enter the level,they get to choose one more card
        intial_flag=True                 ### flag  for   inistial cards_button ect.
        self.page = 1

        j = 3  # initialize: player could attack ghost 4 times before  the ghost attacks the player
        
        while True:     ###for every level run
            clock.tick(60)
            quit = check_events()
            if quit:
                break

            self.paint_background()
            pos = pygame.mouse.get_pos()


            #page to choose card, if player just enter the level,they get to choose one more card
            #flag=True                 ### flag  for   inistial cards_button ect.

            if self.page == 1:        ### initial  self.card_choose[]（will hold 3 cards)
                self.main_page()
                self.card_choose=[]   ###initial card_choose
                cards_button = self.choose_cards()  ### initial  self.card_choose[]（will hold 3 cards)

                for i in range(0,len(self.card_choose)):
                    if cards_button[i].collide_point(pos):
                        if pygame.mouse.get_pressed() ==(1,0,0):
                            card = self.card_choose[i]
                            self.player.cards.append(card)
                            pygame.time.delay(100)
                            self.cards.remove(card)
                            self.first += 1
                            self.page = 2

            #main page where conversation happens
            if self.page == 2:
                if self.first == 1:
                   self.page = 1 
                self.main_page()  ###initial  page 2 display

                if intial_flag==True:
                    intial_flag=False
                    i = 0        #keep track of the index of text, once player finish all the sentences in the list,
                    text = self.texts[self.text_track]
                else:           ###display  one text  by one click or prepare to move self. page 3
                    if i < len(self.texts[self.text_track]):
                        ###display  one text  by one click
                        text_button = self.conversation_text(text[i])
                        if text_button.collide_point(pos):
                            if pygame.mouse.get_pressed() == (1,0,0):
                                self.audio.set_ambiance_sound(0)
                                i += 1
                                pygame.time.delay(100)
                    else:
                        ### parepare to move self.page 3
                        self.page = 3
                        self.background_track += 1
                        self.text_track += 1
                        if self.background_track >= len(self.backgrounds):
                            victory_image = pygame.image.load('level_images/victory.png')
                            self.screen.blit(victory_image,(450,300))
                            pygame.time.delay(3000)
                            return False ### it should return Failure button. Just for test purpose
                        self.change_background(self.backgrounds[self.background_track])
                        self.first += 1
                        j = 3  ###player could attack ghost 2 times before  the ghost attacks the player

            #game page
            if self.page == 3:
                cards_button = self.game_page()  ###show cards the player has
                ghost = self.ghosts[self.ghost_track]
                self.check_type(self.player, ghost)
                skill = None

                font = pygame.font.SysFont("freesansbold.ttf", 30)
                health_point = font.render(str(int(self.player.health_point)), True, (255, 255, 255))
                self.screen.blit(health_point,(120, 54))

                health_point_ghost = font.render(str(int(ghost.health_point)), True, (255, 255, 255))
                self.screen.blit(health_point_ghost,(880, 54))

                if ghost.health_point >0 and self.player.health_point >0:  ###both true,then still fight
                    if j != 0:
                        for i in range(0, len(cards_button)):
                            if cards_button[i].collide_point(pos):
                                if pygame.mouse.get_pressed() == (1, 0, 0):
                                    self.audio.set_ambiance_sound(0)
                                    if self.player.cards[i].name == "Multiple":
                                        length = len(self.player.cards)
                                        count = 0
                                        for card in self.player.cards:
                                            if card.name == "Bleeding":
                                                self.player.cards[i].attack(ghost,self.player,card)
                                                self.audio.set_ambiance_sound(1)
                                            elif card.name != "Bleeding":
                                                count += 1
                                        if count == length:
                                            self.player.cards[i].attack1(ghost, self.player)
                                            self.audio.set_ambiance_sound(1)
                                        else:
                                            pass
                                    elif self.player.cards[i].name != "Multiple":
                                        self.player.cards[i].attack(ghost, self.player)
                                        self.audio.set_ambiance_sound(1) ### player  attack sound
                                    #pygame.time.delay(2000)

                                    #def __init__(self, x, start_y, end_x, end_y, flag, ghost, ghost_index, player,
                                    #             player_index, audio)
                                    start_x=280
                                    start_y=200
                                    end_x=750
                                    end_y=200
                                    
                                    attack_flag=1   ### the flag means the player attacks the ghost;
                                    magicast = Game.Magicasting(start_x, start_y, end_x, end_y, attack_flag, ghost, 0,self.player,1,self.audio)
                                    while magicast.state ==0:    #before magic hits the ghost, shows magic moving
                                        magicast.update()
                                        start_x=magicast.x
                                        start_y=magicast.y
                                        if start_x < end_x:
                                            magicast.draw(self.screen)
                                            pygame.time.delay(5)
                                            pygame.display.flip()
                                        else:
                                            pygame.time.delay(1000)
                                            break

                                    font = pygame.font.SysFont("freesansbold.ttf", 30)
                                    health_point = font.render(str(int(self.player.health_point)), True, (255, 255, 255))
                                    self.screen.blit(health_point,(120, 54))

                                    health_point_ghost = font.render(str(int(ghost.health_point)), True, (255, 255, 255))
                                    self.screen.blit(health_point_ghost,(880, 54))  ###???

                                    j -= 1
                                    pygame.display.flip()

                                     ### break out of the loop after click one card/ or attack once
                    else:  ###player attacks 2 rounds,then ghost's turn
                        j=3 ### initial the number of  the player to 2, which means it could attch 2 times before the ghost attachs;
                        pygame.time.delay(1000)
                        ghost.attack(self.player)
                        self.audio.set_ambiance_sound(7)  ### gohost attack sound
                        start_x =  750
                        start_y = 200
                        end_x = 280
                        end_y = 200
                        attack_flag = -1  ### the flag means the ghost attacks the players;
                        magicast = Game.Magicasting(start_x, start_y, end_x, end_y, -1, ghost, 0, self.player, 1,
                                                    self.audio)
                        while magicast.state == 0:  # before magic hits, shows magic moving
                            magicast.update()
                            start_x = magicast.x
                            start_y = magicast.y
                            if start_x > end_x:
                                magicast.draw(self.screen)
                                pygame.time.delay(10)
                                pygame.display.flip()
                            else:
                                pygame.time.delay(1000)
                                break

                        pygame.time.delay(100)


                else:         ### either of player  or ghost died
                    if self.player.health_point <=0:
                        return False 
                    self.ghost_track += 1
                    self.first += 1
                    self.recover_initial_strength()
                    for card in self.player.cards:
                        if card.name == "Bleeding":
                            card.bleed = 0
                    pygame.time.delay(1000)
        
                    self.background_track += 1
                    self.page = 1

                    if self.background_track >= len(self.backgrounds):
                        victory_image = pygame.image.load('level_images/victory.png')
                        self.screen.blit(victory_image,(450,300))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                        return False ### it should return Failure button. Just for test purpose
                        
                            
                    self.change_background(self.backgrounds[self.background_track])
                    self.page = 1





            # page that player get to choose skills
            if self.page == 4:
                self.main_page()
                skills_button = choose_skills()    ### skill_choose[] then holds 3 skills

                for i in range(0, len(self.skills_choose)):
                    if skills_button[i].collide_point(pos):
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            self.audio.set_ambiance_sound
                            self.player.skills.append(self.skills_choose[i])
                            self.skills_choose.pop(i)

                for skill in self.skills_choose:
                    self.skills.append(skill)
                self.skill_choose = []

                self.main_page()
                skills_button = choose_skills()
                for i in range(0, len(self.skills_choose)):
                    if skills_button[i].collide_point(pos):
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            audio.set_ambiance_sound
                            player.skills.append(self.skills_choose[i])
                            self.skills_choose.pop(i)
                for skill in self.skills_choose:
                    self.skills.append(skill)
                self.skill_choose = []
                self.first += 1
                self.page = 2

            if self.ghost_track > len(self.ghosts):
                victory_image = pygame.image.load('level_images/victory.png')
                victory_button = Button(500,300,victory_image," ",Game.font_name, 30, (230, 180, 0), offset_y=-5)
                victory_button.draw(self.screen) ###   self.screen replacing self.background
                if victory_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1,0,0):
                        pygame.time.delay(1000)
                        return False ### it should return Failure button. Just for test purpose

            if self.background_track > len(self.backgrounds):
                return False

            self.draw_cursor(*pos)
            pygame.display.flip()


    
class Button:

    # If there should be text on the button, then text is what will be displayed, fontType the font used,
    # fontSize the size of the text, and fontColor a tuple of RGB values. Offset parameters are to shift the text
    # left or right relative to the center.

    def __init__(self, x, y, image, text='', font_type=None, font_size=69, font_color=(0, 0, 0), offset_x=0.0,
                 offset_y=0.0):
        self.image = image
        self.position = (x, y)
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.text_center = (x + (self.rect.width / 4), y + (self.rect.height / 4))
        if text:
            if font_type not in pygame.font.get_fonts():
                raise Exception('Not an available font!')
            else:
                font_object = pygame.font.SysFont(name=font_type, size=font_size)

            self.text_surface = font_object.render(text, True, font_color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)

            self.text_rect.x += offset_x
            self.text_rect.y += offset_y

    def draw(self, screen):
        screen.blit(self.image, self.position)
        screen.blit(self.text_surface, self.text_rect)

    def collide_point(self, point):
        return self.rect.collidepoint(point)

