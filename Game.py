import pygame
import Ghost
import random
import level
from Ghost import ghost_list
import math

# this can be in main branch
WIDTH = 1000
HEIGHT = 600
transColor = pygame.Color(255, 0, 255)
font_name = "arial"


def check_events():
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
    return quit


class Game:
    cursor_img = pygame.image.load('images/mouse.png')
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    page = 1
    background = pygame.image.load('images/start_page.jpg').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    level_index = None
    character_index = None

    def draw_cursor(self, x, y):
        self.screen.blit(self.cursor_img, (x, y))

    def start(self):  # starting background
        start_button_image = pygame.image.load('images/start_button(1).png')
        pygame.transform.scale(start_button_image, (400, 100))
        start_button = Button(400, 450, start_button_image, "Play", font_name, 30, (230, 180, 0), offset_y=-5)
        start_button.draw(self.screen)
        return start_button

    def paint_background(self):
        self.screen.blit(self.background, (0, 0))

    def main_page(self):  # display main page
        character_button_image = pygame.image.load('images/start_button.png')
        character_button = Button(600, 100, character_button_image, "Character", font_name, 30, (230, 250, 250),
                                  offset_y=-5)
        character_button.draw(self.screen)
        map_button_image = pygame.image.load('images/start_button.png')
        map_button = Button(600, 250, map_button_image, "Map", font_name, 30, (230, 250, 250), offset_y=-5)
        map_button.draw(self.screen)
        return character_button, map_button

    def change_background(self, image):
        main_background = pygame.image.load(image).convert()
        main_background = pygame.transform.scale(main_background, (WIDTH, HEIGHT))
        self.background = main_background

    def show_characters(self):  # blit the characters on another background
        character_card_image = pygame.image.load('images/character_back.png')
        character_card_image = pygame.transform.scale(character_card_image, (140, 230))
        # initial x and y for image
        ''' for sure need to be check, and you may need to add button, which is the name of each character, 
        below each image, so that when you click that, it enters the specific character page'''
        x = 180
        y = 60

        exit_button_image = pygame.image.load('images/exit_button.png')
        exit_button = Button(5, 5, exit_button_image, " ", font_name, 30, (230, 180, 0), offset_y=-5)
        exit_button.draw(self.screen)

        character_button_list = []
        for character in character_list:
            character_image = character.image
            character_name = character.name
            color_key = character_image.get_at((10, 10))
            color_key_2 = character_card_image.get_at((5, 5))

            pygame.Surface.set_colorkey(character_card_image, color_key_2, pygame.RLEACCEL)
            character_image = pygame.transform.scale(character_image, (140, 180))
            self.screen.blit(character_card_image, (x + 15, y - 43))

            pygame.Surface.set_colorkey(character_image, color_key, pygame.RLEACCEL)
            self.screen.blit(character_image, (x, y))
            # characters.show_in_character(game_display, x, y)
            # depends on how big the images are, if the first colume is not enough to put all the images,
            # put the rest in the second colume
            character_button_image = pygame.image.load('images/character_button.png').convert()
            character_button_image = pygame.transform.scale(character_button_image, (148, 30))
            character_button = Button(x + 15, y + 200, character_button_image, character_name, font_name, 15,
                                      (255, 255, 255), offset_y=-5)
            character_button.draw(self.screen)
            character_button_list.append(character_button)
            if x + 200 <= 700:
                x += 250
            else:
                y += 280
                x = 180
        return character_button_list, exit_button

    def map_levels(self):
        exit_button_image = pygame.image.load('images/exit_button.png')
        exit_button_2 = Button(5, 5, exit_button_image, " ", font_name, 30, (230, 180, 0), offset_y=-5)
        exit_button_2.draw(self.screen)
        return exit_button_2

    def info_page(self, character):

        small_image = pygame.transform.scale(character.image, (460, 580))
        pygame.Surface.set_colorkey(small_image, character.tansColor, pygame.RLEACCEL)
        self.screen.blit(small_image, (5, 5))
        frame_image = pygame.image.load('images/frame.png')
        frame_image = pygame.transform.scale(frame_image, (400, 600))
        self.screen.blit(frame_image, (90, 0))
        infor_frame_image = pygame.image.load('images/infor_frame.png')
        infor_frame_image = pygame.transform.scale(infor_frame_image, (400, 600))
        self.screen.blit(infor_frame_image, (545, 0))
        exit_button_image = pygame.image.load('images/exit_button.png')

        # self.screen.blit(infor_frame_image, (545, 0))

        font = pygame.font.SysFont("freesansbold.ttf", 30)
        text1 = font.render(character.name, True, (0, 0, 0))
        self.screen.blit(text1, (700, 70))
        text2 = font.render("Health point: " + str(character.health_point), True, (0, 0, 0))
        self.screen.blit(text2, (650, 150))
        text3 = font.render("Ex: " + str(character.ex), True, (0, 0, 0))
        self.screen.blit(text3, (650, 200))
        text4 = font.render("Strength: " + str(character.strength), True, (0, 0, 0))
        self.screen.blit(text4, (650, 250))
        text5 = font.render("Level: " + str(character.level), True, (0, 0, 0))
        self.screen.blit(text5, (650, 300))
        text6 = font.render("Element: " + str(character.element), True, (0, 0, 0))
        self.screen.blit(text6, (650, 350))
        text7 = font.render("Cards: " + str(character.cards), True, (0, 0, 0))
        self.screen.blit(text7, (650, 400))

        exit_button = Button(40, 40, exit_button_image, " ", font_name, 30, (230, 180, 0), offset_y=-5)
        exit_button.draw(self.screen)
        return exit_button

    def level_enter(self):
        level_enter_image1 = pygame.image.load('images/level_one_enter.png')
        level_enter1_button = Button(100, 200, level_enter_image1, "  ", font_name, 30, (255, 255, 255), offset_y=-5)
        level_enter1_button.draw(self.screen)

        level_enter_image2 = pygame.image.load('images/level_two_enter.png')
        level_enter2_button = Button(500, 350, level_enter_image2, "  ", font_name, 30, (255, 255, 255), offset_y=-5)
        level_enter2_button.draw(self.screen)

        level_enter_image3 = pygame.image.load('images/level_three_enter.png')
        level_enter3_button = Button(700, 400, level_enter_image3, "  ", font_name, 30, (255, 255, 255), offset_y=-5)
        level_enter3_button.draw(self.screen)

        return level_enter1_button, level_enter2_button, level_enter3_button

    def enter_page(self, n):
        enter_page_image = pygame.image.load('images/enter_page.png')
        enter_page_image = pygame.transform.scale(enter_page_image, (800, 400))
        self.background.blit(enter_page_image, (105, 105))

        exit_button_image = pygame.image.load('images/exit_button.png')
        exit_button = Button(125, 125, exit_button_image, " ", font_name, 30, (230, 180, 0), offset_y=-5)
        exit_button.draw(self.screen)

        if self.character_index != None:
            choose_character_image = pygame.image.load('images/frame.png')

        else:
            choose_character_image = pygame.image.load('images/choose_character.png')

        choose_character_image = pygame.transform.scale(choose_character_image, (200, 300))
        choose_character_button = Button(200, 170, choose_character_image, " ", font_name, 30, (255, 255, 255),
                                         offset_y=-5)
        choose_character_button.draw(self.screen)

        start_button_image = pygame.image.load('images/start_button(1).png')
        start_button = Button(680, 420, start_button_image, "Start Game", font_name, 30, (230, 180, 0), offset_y=-5)
        start_button.draw(self.screen)

        return exit_button, choose_character_button, start_button

    def blit_text(self, text, x, y):
        pass

    def run(self):
        pygame.init()
        pygame.display.set_caption('None')
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        # initial background music
        ambiance_type = None  # only start to play background music
        audio = AudioController(ambiance_type)
        audio.start()  # start to play backgound music

        while True:
            clock.tick(60)
            quit = check_events()
            if quit:
                break

            self.paint_background()
            pos = pygame.mouse.get_pos()

            # start page
            if self.page == 1:
                start_button = self.start()
                if start_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/start.bmp')
                        self.page = 2
            # main page
            if self.page == 2:
                buttons = self.main_page()
                if buttons[0].collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/show_character.jpg')
                        self.page = 3
                if buttons[1].collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/map_image.png')
                        self.page = 4

            # character menu
            if self.page == 3:
                self.caracter_index = 0
                character_button_list = self.show_characters()[0]
                exit_button = self.show_characters()[1]
                if exit_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/start.bmp')
                        self.page = 2

                for i in range(0, 6):
                    if character_button_list[i].collide_point(pos):
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            # play the ambiance  sound for click the button
                            self.character_index = i
                            audio.set_ambiance_sound(0)
                            self.page = 5

            # map page
            if self.page == 4:
                exit_button = self.map_levels()
                level_button = self.level_enter()
                if exit_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/start.bmp')
                        self.page = 2

                for n in range(0, 3):
                    if level_button[n].collide_point(pos):
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            # play the ambiance  sound for click the button
                            audio.set_ambiance_sound(0)
                            self.level_index = n
                            self.enter_page(self.level_index)
                            self.page = 6

            # info page
            if self.page == 5:
                exit_button = self.info_page(character_list[self.character_index])
                if exit_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/show_character.jpg')
                        self.page = 3
            # enter page
            if self.page == 6:

                exit_button = self.enter_page(self.level_index)[0]
                choose_character_button = self.enter_page(self.level_index)[1]
                start_button = self.enter_page(self.level_index)[2]

                if exit_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/map_image.png')
                        self.page = 4
                        self.character_index = None
                        self.level_index = None

                if choose_character_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.change_background('images/show_character.jpg')
                        self.page = 7
                        self.character_index = None

                if self.character_index != None:
                    character_image = character_list[self.character_index].image
                    small_image = pygame.transform.scale(character_image, (200, 250))
                    pygame.Surface.set_colorkey(small_image, (255, 255, 255), pygame.RLEACCEL)
                    self.background.blit(small_image, (200, 220))

                if self.character_index != None:
                    if start_button.collide_point(pos):
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            audio.set_ambiance_sound(0)
                            self.page = 8
                            # start game
                            level_now = level.Level(self.level_index+1,character_list[self.character_index],ghost_list[self.level_index],
                                          dialogue[self.level_index],card_list,skill_list,background[self.level_index],audio)
                            level_now.run()
                            self.character_index = None
                            self.change_background('images/map_image.png')
                            self.page = 4



            # choose character
            if self.page == 7:

                character_button_list = self.show_characters()[0]
                exit_button = self.show_characters()[1]
                if exit_button.collide_point(pos):
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        # play the ambiance  sound for click the button
                        audio.set_ambiance_sound(0)
                        self.page = 6

                for n in range(0, 6):
                    if character_button_list[n].collide_point(pos):
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            # play the ambiance  sound for click the button
                            audio.set_ambiance_sound(0)
                            self.page = 6
                            self.character_index = n

            self.draw_cursor(*pos)
            pygame.display.flip()


class Character:
    def __init__(self, name, level, element, ex, health_point, strength, image, cards, skills, tans_color,
                 background_info):
        self.name = name
        self.level = level
        self.element = element
        self.ex = ex  # experience at this level, when it reaches a certain point,the character will be level up
        self.health_point = health_point
        self.strength = strength
        self.image = image
        self.cards = cards
        self.skills = skills
        self.tansColor = tans_color
        self.background_info = background_info

    def __str__(self):  # character background/information
        return self.background_info

    def show_in_character(self, characters_page, x, y):  # show in the character page that contains name and image of
        # the character
        character_basic_info = self.image
        small_image = pygame.transform.scale(self.image, (148, 250))
        pygame.Surface.set_colorkey(small_image, self.tansColor, pygame.RLEACCEL)
        characters_page.blit(character_basic_info, (x, y))

    def character_main_info(self):  # when you click the character's image on the character page, you can enter main
        # info page
        """what we should do here is to blit the image and text on this page"""
        pass

    def show_in_levels(self,screen):
        character_basic_info = self.image
        small_image = pygame.transform.scale(self.image, (230, 300))
        pygame.Surface.set_colorkey(small_image, self.tansColor, pygame.RLEACCEL)
        screen.blit(small_image, (0,300))

    def show_in_levels_fight(self,screen):
        character_basic_info = self.image
        small_image = pygame.transform.scale(self.image, (230, 300))
        pygame.Surface.set_colorkey(small_image, self.tansColor, pygame.RLEACCEL)
        screen.blit(small_image, (60, 60))  


'''
    def benefit_mankind(self, playername):
        playername.HP = playername.HP + 10 + self.level
        self.MP -= 10
    def graft_and_transplant(self,monster_name):
        monster_name.HP = monster_name.HP - 10 - self.level
        self.MP -= 15
        self.HP = self.HP + 5 + self.level
'''
'''
    def kaleidosope_of_death(self):
        self.MP = self.MP - 20 + self.level
        self.HP = self.HP + 10 + self.level
        if self.type == "earth":
            self.type = "water"
        elif self.type == "water":
            self.type = "fire"
        elif self.type == "fire":
            self.type == "gold"
        elif self.type == "gold":
            self.type = "wood"
        else:
            self.type == "earth"
        
    def blade_of_faith(self,monster_name):
        self.MP = self.MP - 10 + self.level
        monster_name.HP = monster_name.HP - 15 - self.level
'''
'''
    def left_eye(self,monster_name):
        self.MP = self.MP - 15 + self.level
        monster_name.HP = monster_name.HP - 20 - self.level
        self.HP += 3
    def right_eye(self,monster_name):
        self.MP = self.MP - 15 + self.level
        monster_name.HP = monster_name.HP - 3 - self.level
        self.HP += 15
'''
'''It's not the explosion that damages the ghosts, but the loud noise dynamite produces, allowing for multiple 
spirits to be affected at once.' def dynamite (self, monsters): self.MP = self.MP - 25 + self.level for _ in 
monsters: _.HP = _.HP - 10 - self.level 'Arma is always one to be prepared, making sure to bring extra supplies, 
allowing his team to continue fighting.' def ressuply (self,playername): playername.MP = playername.MP + self.level '''


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


# put all character in a list which can be used in the loop for some def

character_list = [Character('Elysia', 1, 'water', 0, 500, 20, pygame.image.load('images/Elysia.png').convert(), [], [],
                            pygame.image.load('images/Elysia.png').convert().get_at((10, 10)), '''Elysia is a gift 
                            from God to the people, unawaring of her position as a God's messenger. She leaves her 
                            hometown and journeys to the outer world in search of her origins.'''),
                  Character('Jin(瑾)', 1, 'Metal', 0, 500, 20, pygame.image.load('images/Jin.png'), [], [],
                            (0, 0, 0), '''The girl from the East has never been out of the mountains since she 
                            followed her master to practice in the mountains. But on her twentieth birthday, 
                            everyone in the mountains disappeared, leaving only a letter and an old pocket watch. In 
                            order to find the missing brothers and masters, Jin embarked on an endless journey'''),
                  Character("Elf Emma", 1, 'water', 0, 500, 20, pygame.image.load('images/Emma.png'), [], [], None,
                            """When Odin killed the giant Emir, elves were born from the giant's corpse. 
                            They have beautiful faces, pointed ears, light wings and eternal life.
                            At first, they lived in a remote land with beautiful mountains and rivers, 
                            being in isolation; 
                            Until one day, a woman appeared and the elves' peaceful days were broken.
                            She often sat on a rock far away from the sea, singing a charming song when the fog was 
                            everywhere. 
                            It is said that someone seemed to see a mermaid tail through the fog.
                            Once an spirit who was attracted entered the fog and went in the direction of the woman, he 
                            never came out of the fog.
                            Emma, the Elven princess, hearing stories told by bards when growing up. Since one day her 
                            childhood sweetheart stepped into the fog and never came home, she decided to go alone to 
                            the strange world to find the answer to the salvation of the people."""),
                  Character("Bard Jack", 1, 'earth', 0, 800, 15, pygame.image.load('images/Jack.png'), [], [], None,
                            """It seems that Jack was already in existence when Chaos, the god of Chaos, created Gaea, 
                            the Mother of Earth. At first, Jack wandered in the world in the way of soul, 
                            and gradually became sentient and subsistent.
                            He witnessed the vicissitudes of life from generation to generation, and experienced a cycle
                            of birth and death.After the ghosts of the past were destroyed by gods and men, he trekked about as a wandering
                            bard, telling posterity happened before.
                            Until one day, the monsters that had disappeared reappear one by one, and Jack gradually 
                            realizes something.
                            He decided to change the world disrupted by his behavior, and recruited partners, in order 
                            to let those ghosts completely leave the world."""),
                  Character("Garderner Taweel", 1, 'wood', 0, 1000, 15, pygame.image.load('images/Taweel.png'), [], [],
                            None,
                            """Taweel was an ordinary gardener living an ordinary life, growing a large number of 
                            ordinary roses for sale in his ordinary garden.
                            Until one day, when he picked a seemingly ordinary rose as usual, a beauty with a human head
                            and a snake body appeared before him.
                            Taweel right eye feels like a petrified pain as he makes an unsuspecting eye contact.
                            Women disappear, and everything becomes normal again. Thinking he was hallucinating, Taweel
                             swallowed the discomfort in his right eye and went on to pick the next rose.
                            It is only when the woman reappears in front of Taweel, smiling at him, then Taweel begins 
                            to change his firmly materialistic worldview.
                            He remembered the stories of the wandering poets he had met, and one of them was exactly 
                            like the one he had just seen.
                            He threw away all the roses he had gathered and began his journey to find the wandering poet
                             and the cure.
                            At that moment, Taweel saw in the woman smiling eyes the virtual image of his right eye, 
                            where a rose bud had just emerged from the ground and was ready to blossom.
                            """),
                  Character("Arma", 1, 'powder', 0, 750, 30, pygame.image.load('images/Arma.png'), [], [], None,
                            '''Before being recruited to combat the supernatural, Arma was a lowly laborer employed 
                            in one of several mines scattered througout the mountains oustide of the kingodom, 
                            slowly working his days away in the dark subterranean environment. In the hopes of 
                            increasing efficiency, Arma took it upon himself to study the secrets of explosive 
                            gunpowder for use in the mines. In truth, he was discovered by the team accidentally as 
                            they were traveling through the mountains. But his innovation attracted the attention of 
                            the group, who were interested by his invention, a form of dynamite. Arma was offered a 
                            spot on the team. Seeing an opportunity to secure a better life for himself, he accepted 
                            without hesitation.''')
                  ]


# Character is the character player chose, so it is a variable of class
class Card:
    def __init__(self, name, image, description):
        self.name = name
        self.image = image
        self.description = description
        self.multiple = 1
        self.added_strength = 0

    def show(self, x, y, background):
        card_image = self.image
        small_image = pygame.transform.scale(card_image, (40, 60))
        pygame.Surface.set_colorkey(small_image, self.tansColor, pygame.RLEACCEL)
        background.blit(small_image, (x, y))


class Card1(Card):  # basic attack
    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def attack(self, ghost, player):
        ghost.health_point -= player.strength * 3


class Card2(Card):  # cause ghost to have less damage

    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def attack(self, ghost, player):
        ghost.strength -= 1
        ghost.health_point -= player.strength * 1.5


class Card3(Card):  # The card that bleeds the ghost's health.
    def __init__(self, name, image, description):
        super().__init__(name, image, description)
        self.bleed = 0

    def attack(self, ghost, player):
        # When this card is used, don't delete it right away, but make it uncallable.
        # Every time a turn is taken by either side, call this method to make the ghost lose health.
        # turns_passed records the amount of turns that have passed since the card was used.
        # maximum_turns determines the amount of turns that can pass after use before the card's effect expires.
        # Once turns_passed exceeds maximum_turns, the effect no longer occurs.

        self.bleed = self.bleed + 10
        ghost.health_point -= (player.strength * 0.75 + self.bleed)



class Card4(Card):  # Vulnerability.
    def __init__(self, name, image, description):
        super().__init__(name, image, description)
        

    def attack(self, ghost, player):
        ghost.strength = ghost.strength - 10
        ghost.health_point -= player.strength * 2 


class Card5(Card):  # clear multiple, cause damage

    def __init__(self, name, image, description):
        super().__init__(name, image, description)
        self.multiples = 0

    def attack(self, ghost, player,card):
        self.multiples = card.bleed
        ghost.health_point -= (player.strength * 2 + self.multiples * 2)
        self.multiple = 0
        card.bleed = 0

    def attack1(self,ghost,player):
        ghost.health_point -= (player.strength * 2 + self.multiples * 2)
        


class Card6(Card):  # change the type
    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def attack(self, ghost,player):
        if player.element == "earth":
            player.element = "water"
        elif player.element == "water":
            player.element = "fire"
        elif player.element == "fire":
            player.element == "gold"
        elif player.element == "gold":
            player.element = "wood"
        else:
            player.element == "earth"


class Card7(Card):  # heal
    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def attack(self,ghost,player):
        player.health_point = player.health_point * 1.2


card_list = [Card1('Basic Attack',pygame.image.load('images/cards_designs/basic_attack_card.png'),'Basic attack that damages the ghost.'),
             Card2('Weakening',pygame.image.load('images/cards_designs/bash_attack_card.png'),'Decreases the damage taken from ghosts.'),
             Card3('Bleeding', pygame.image.load('images/cards_designs/drain_attack_card.png'),'Causes the ghost to gradually lose health over multiple turns.'),
             Card4('Vulnerbility',pygame.image.load('images/cards_designs/vulnerability_card.png'),'This card increases the damage taken by the ghost.'),
             Card5("Multiple", pygame.image.load('images/cards_designs/multiple_attack_card.png'),"This card deals multiple damage."),
             Card6("Change Type", pygame.image.load('images/cards_designs/change_type_card.png'), "Switch to a different elemental base."),
             Card7("Change Type", pygame.image.load('images/cards_designs/heal_card.png'), "Use this card to heal your warrior.")]



class Skills:

    def __init__(self, name, image, description):
        self.name = name
        self.image = image
        self.description = description


class Skill1(Skills):
    # increase 50% pf damage when player's health point is above 80%.
    initial_health_point = None

    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def skill(self, ghost, player, level):
        self.initial_health_point = level.initial_health_point
        if player.health_point >= 0.8 * self.initial_health_point:
            player.strength = player.strength * 1.5

    def show(self):
        card_image = self.image
        small_image = pygame.transform.scale(card, (40, 60))
        pygame.Surface.set_colorkey(small_image, self.tansColor, pygame.RLEACCEL)
        background.blit(small_image, (x, y))


class Skill2(Skills):  # increase health point afterwards
    initial_health_point = None

    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def blood(self, ghost, player, level):
        self.initial_health_point = level.initial_health_point
        if player.health_point >= 0.9 * self.initial_health_point:
            player.health_point += 0.1 * player.health_point + player.health_point

        elif player.health_point < 0.9 * self.initial_health_point:
            player.health_point += 0.25 * player.health_point + player.health_point

        elif player.health_point <= 0.5 * self.initial_health_point:
            player.health_point += 0.5 * player.health_point + player.health_point


class Skill3(Skills):  # The skill that regains health when enough cards are used.
    def __init__(self, name, image, description):
        super().__init__(name, image, description)
        self.cards_used = 0

    def skill(self, ghost, player):
        if self.cards_used >= 7:
            player.health += 3
            self.cards_used = 0


class Skill4(Skills):  # block the blood

    def __init__(self, name, image, description):
        super().__init__(name, image, description)
        self.time = 1

    def skill(self, ghost, player):
        if player.health_point <= 0.05 * self.initial_health_point:
            store = ghost.strength
            if self.time == 1:
                ghost.strength = 0
                self.time = 0
            else:
                ghost.strength = store


class Skill5(Skills):  # bounce the attack

    def __init__(self, name, image, description):
        super().__init__(name, image, description)

    def skill(self, ghost, player):
        store = ghost.strength
        ghost.health_point -= ghost.strength * 0.5



skill_list = [

Skill1("Boost Damage", "images/cards_designs/boost_damage_skill.png", "When your health is above 80%, you warrior deals 50% more damage."),
Skill2("Boost Health", "images/cards_designs/boost_health_skill.png", "After a victorious battle, your experienced fighter will recieve extra health in the next mission."),
Skill3("Redeem Health", "images/cards_designs/return_health_skill.png", "Use cards to heal your character."),
Skill4("Last Stand", "images/cards_designs/lock_health_skill.png", "Your character recieves a surge of energy when their health drops below 5%, granting them temporary invicincibility."),
Skill5("Reflect Damage", "images/cards_designs/mirror_attack_skill.png", "Damage dealt to your warrior is automatically dealt to the attacker.")

]



class AudioController:
    backgrounds = [{'filename': 'JDB - Traveling.wav', 'sound': None}]
    menu_click = [{'filename': 'mouse_click.wav', 'sound': None}]
    ambiances = [{'filename': 'cast_magic1.flac', 'sound': None},
                 {'filename': 'cast_magic2.mp3', 'sound': None},
                 {'filename': 'cast_magic3.wav', 'sound': None},
                 {'filename': 'cast_magic4.wav', 'sound': None},
                 {'filename': 'cast_magic5.wav', 'sound': None},
                 {'filename': 'cast_magic6.wav', 'sound': None},
                 {'filename': 'cast_magic7.wav', 'sound': None}
                 ]

    def __init__(self, ambiance_type):
        self.volume = 0.5
        self.right_channel = 0.5

        self.background = None
        self.background_channel = pygame.mixer.Channel(0)
        self.set_volume_pan()

        self.playing_ambiance = None
        self.amb_channel = pygame.mixer.Channel(2)

    def start(self):
        self.set_background_sound()
        # self.set_ambiance_sound(None)

    def set_ambiance_sound(self, ambiance_type):  # ambiance type by 0, 1,2,3,4,5,6,7
        '''
        while one of  chars cast its magic skill,  the def will play  the relative sound
        param casting_char: 1,2,3,4,5,6,7;
        0 for click menu
        1~6 for 1~6 player cast
        7 for ghost cast
        return:
        '''
        pan = random.uniform(.5, 1.0)
        self.amb_channel.set_volume(pan, 1 - pan)
        self.amb_channel.stop()    # first to  stop the ambiance channel(stop the previous sound)

        if ambiance_type == 0:  # click menu button and has a click sound out
            chosen_ambiance=self.menu_click[0]
            filename=chosen_ambiance['filename']
            self.playing_ambiance = pygame.mixer.Sound(f'assets/sounds/{filename}')

        elif 0 < ambiance_type < 8:  # one of chars casts  magic  and has sound out
                chosen_ambiance = AudioController.ambiances[ambiance_type - 1]
                filename = chosen_ambiance['filename']
                self.playing_ambiance = pygame.mixer.Sound(f'assets/sounds/{filename}')

        self.amb_channel.play(self.playing_ambiance)
        self.playing_ambiance = True

    def set_background_sound(self):
        '''
        if number != self.background:  # Don't restart the file when the same button is clicked
            if self.background:
                self.background_channel.stop()
        '''
        filename = AudioController.backgrounds[0]['filename']
        self.background_sound = pygame.mixer.Sound(f'assets/sounds/{filename}')
        self.background_channel.play(self.background_sound, -1)
        self.background = 0

    def set_volume_pan(self):
        left = (1 - self.right_channel) * self.volume
        right = self.right_channel * self.volume
        self.background_channel.set_volume(left, right)

    def update(self, ambiance_type):  # update ambiance when there is a  corrent  click
        if not self.amb_channel.get_busy():
            self.set_ambiance_sound(self,ambiance_type)
            self.amb_channel.play(self.background_sound)
        self.set_volume_pan()

        if new_ambiance:
            self.set_ambiance_sound()


'''
demo code: calling from level.py  while  ghost or player cast magic skill

self.audio.set_ambiance_sound(ghost_index)   #ghost_index from 7~10 standing for ambiance_type; start to play the ghost sound
magicast=Magicasting.__init__(x,start_y,end_x,end_y, 1, ghost, None, None,audio  #ghost attack player
magicast.update()
magicast.draw(surface)

self.audio.set_ambiance_sound(player_index)   #play_index from 1~6 standing for ambiance_type; start to play  player's sound
magicast=Magicasting.__init__(x,start_y,end_x,end_y, 0, None, player, play_index,audio)  #player attack  ghost 
magicast.update()
magicast.draw(surface)

'''

class Magicasting:
    #ghost/player cast magic skill with sound
    #flag=1, ghost attacks player; flag=2, player attcks ghost
    #player_index:  which players in the list
    #audio:Instance of class Audocontroller

    def __init__(self, start_x, start_y, end_x, end_y,  flag,ghost,ghost_index, player,player_index,audio):
        self.x = start_x
        self.y = start_y
        self.end_y = end_y
        self.end_x=end_x
        self.flag=flag
        self.each_step=20  ###every upate, the cast magic going 20; 1 means: moving to the right;-1:moving to the left
        self.line_angel = math.atan2(self.y-self.end_y,self.end_x-self.x)
        self.delta_x=self.each_step*math.cos(self.line_angel)
        self.delta_y=self.each_step*math.sin(self.line_angel)

        self.state = 0  # 0 is inflight, 1 is playing death sound, 2 is done/ready for del
        self.audio=audio  #an object of class Audocontroller
        self.channel = pygame.mixer.Channel(4)
        #self.sound_start = pygame.mixer.Sound('assets/sounds/bullet0.wav')
        self.sound_end = pygame.mixer.Sound('assets/sounds/cast_magic5.wav')
        #self.audio.amb_channel.play(self.sound_start)

    def is_valid(self):
        return self.state < 2

    def update(self):
        if self.state == 0:
            if self.y < self.end_y:
                self.state = 1
                self.audio.amb_channel.play(self.sound_end)
                pygame.time.delay(50)  # 50ms delay
                self.audio.amb_channel.stop()    #when stop the sound    right away?
            else:
                self.x +=self.delta_x
                self.y -=self.delta_y
        elif self.state == 1:
            if not self.audio.amb_channel.get_busy():
                self.state = 2

    def draw(self, surface):
        if self.state == 0:
            if self.flag==1:
                pygame.draw.circle(surface, (100, 220, 240), (self.x, self.y), 15)   ###player casts magic
            else:
                pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), 10) ###ghost casts magic



dialogue1 = [['The last touch of the sun exiles the left warmth.','The wind sweeps the petals into the sky, then they fall to dust.',
            'Jack walks on the road of the main city and looks at the passers and the galloping carriages around him.',
            'He puts on the clothes he had bought from the equipment merchant a few days earlier and the weapons Arma had made.',
            'A day of investigation of monster rumors slowed him down.',
            'After discussing with the team members, he was amazed to find that all the stories he told were exactly the same as what happened in this world.',
            'As he pondered the next steps, a voice sounded behind him.','Unknown: Mr.Bard!',
            'Jack looks around and sees a white-haired boy with a look of panic and joy.','Jack：Who are you？',
            'Unknown: My name is Taweel and I am here to ask for your help.',
            'Taweel adjusts his short breathing due to the run and then tells Jack everything he hss been through.',
            'Taweel was an ordinary gardener living an ordinary life, growing a large number of ordinary roses for sale in his ordinary garden.',
            'Until one day, when he picked a seemingly ordinary rose as usual, a beauty with a human head and a snake body appeared before him.',
            'Taweel right eye feels like a petrified pain as he makes an unsuspecting eye contact.',
            'Women disappear, and everything becomes normal again.',
            'Women disappear, and everything becomes normal again. Thinking he was hallucinating,',
            'Taweel swallowed the discomfort in his right eye and went on to pick the next rose.',
            'It is only when the woman reappears in front of Taweel, smiling at him, then Taweel begins to change his firmly materialistic worldview.',
            'He remembered the stories of the wandering poets he had met, and one of them was exactly like the one he had just seen.',
            'He threw away all the roses he had gathered and began his journey to find the wandering poet and the cure.',
            'Taweel: At that moment, I saw in the woman smiling eyes the virtual image of my right eye, where a rose bud had just emerged from the ground and was ready to blossom.',
            'Jack: OK, I will try my best to help you and make up for the mistake I made.',
            'Taweel does not speak, as if he is confused as to why this is a mistake made by the person in front of him,',
            "Jack looks into Taweel's intact eyes",
            'Jack: Do you have any other clues about this monster?',
            "Taweel: Well, I thought I heard a voice around my ear that said 'don't use your right eye to show your desire.'",
            "Jack: All right. I have to get back to the team base. That's where the team is. You can drop by our place if you need.",
            'Taweel: Thank you very much.',
            'Jack takes Taweel back to the base.',
            'Jack: My friends, tomorrow our journey will begin with our new friend Taweel, who will lead us to the site of our first heresy.',
            'Emma：Hello Mr.Taweel! Nice to meet you!',
            'Elysia: Glad to see you.',
            'Jin: Good evening~ Hope we will all solve our problems by fighting together.',
            'Arma: Nice to meet you Taweel.',
            'Taweel: Nice to meet you too.',
            'After a while, they begin to discuss about the implicit meaning of that sentence.',
            'Emma: Do not use your right eye to show desire... What does it mean?',
            'Jin: What about the left eye?',
            'Jack: Maybe it means that ...',
            'The next day.',
            'When the first ray of sunshine in the morning reflects into the eyes of Jack and his party through the dewdrops on the rose petals.',
            'The air is filled with the attractive aroma of the rose, and the birdsong seems to be heard in the distance.',
            'Jack：Do not use your right eye to show desire.',
            'They take out one side glasses made by Arma and cover their right eyes.',
            'Jack: Use your left eye to peep the truth.',
            'It is as if at this moment the thousands of acres of flowers have shrivelled after their brief existence.',
            "The smell of roses has turned to a rotting stench. In addition, they see branches and petals spreading out under Taweel's glasses",
            'Not only that, but in the flower fields not far away, two monsters appear.',
            "They're like petri dishes for roses. Their bodies twist at a strange angle after being wrapped by the rose.",
            "Elysia: Looks like we'll have to deal with them first."],

            ['They walk on until they reach the area where Taweel had met the monster and also see the woman with the snake body.',
            'Rose Medusa. Jack says to himself.',
            'The woman turns slowly and begins to move closer to them.',
            'Arma: Go!'],

            ['Taweel: Thank you very much!',
            'The rose on his right eye disappears when the woman fall down.',
            'Jack: That is all right. Hope that we will meet again in the future. See you.',
            'Taweel: Well, may I stay and work together with you to fight monsters?',
            'Jack: Sure!']]

dialogue2 = [['text'],['text'],['text']]
dialogue3  = [['text'],['text'],['text']]
dialogue = [dialogue1,dialogue2,dialogue3]

background1 = [pygame.image.load('level_one_images/background1.jpg'),
               pygame.image.load('level_one_images/background2.jpg'),
               pygame.image.load('level_one_images/background3.jpg'),
               pygame.image.load('level_one_images/background4.jpg'),
               pygame.image.load('level_one_images/background2.jpg'),
               pygame.image.load('level_one_images/background1.jpg')]
background2 = [pygame.image.load('level_two_images/background1.jpeg'),
               pygame.image.load('level_two_images/background2.jpeg'),
               pygame.image.load('level_two_images/background3.jpeg'),
               pygame.image.load('level_two_images/background4.jpeg'),
               pygame.image.load('level_two_images/background2.jpeg'),
               pygame.image.load('level_two_images/background1.jpeg')]
background3 = [pygame.image.load('level_three_images/background1.webp'),
               pygame.image.load('level_three_images/background2.webp'),
               pygame.image.load('level_three_images/background3.jpeg'),
               pygame.image.load('level_three_images/background4.jpeg'),
               pygame.image.load('level_three_images/background2.webp'),]

background = [background1,background2,background3]



if __name__ == "__main__":
    game = Game()
    game.run()
    
