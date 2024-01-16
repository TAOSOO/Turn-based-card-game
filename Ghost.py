import pygame
import random

pygame.init()


class Ghost:

    # I did kind of copy and paste this from the Character class.
    # Not completely sure what attributes a ghost should have and how they should differ from the characters.
    def __init__(self, name, element, health_point, strength, image, tans_color, info):
        self.name = name
        self.element = element
        self.health_point = health_point
        self.strength = strength
        self.image = image
        self.tansColor = tans_color
        self.info = info
        self.sp = 0
        self.damage_taken = 0
        self.level_downs = 0

    def __str__(self):  # character background/information
        return self.info

    def show_in_levels(self):
        pass


class SmallMonster(Ghost):
    def _init_(self, name, element, health_point, strength, image, tans_color, info):
        super().__init__(name, element, health_point, strength, image, tans_color, info)

        self.level_downs = 0
        self.damage_taken = 0
        self.sp = 0 

    def attack(self,player):

        if self.sp == 20:
            self.basicattack(player)

        elif self.sp == 50:
            self.final(player)

        else:
            self.attack1(player)

    def attack1(self,player):
        player.health_point -= self.strength * 4
        self.damage_taken += 5
        self.sp += 10

    def basicattack(self, player):
        player.health_point -= 50
        self.damage_taken += 5
        self.sp += 10

    def final(self,player):
        player.health_point -= (self.strength * 5 + self.damage_taken)
        self.sp = 0
        
class King(Ghost):

    def _init_(self, name, element, health_point, strength, image, tans_color, info):
        super().__init__(name, element, health_point, strength, image, tans_color, info)

        self.level_downs = 0
        self.damage_taken = 0
        self.sp = 0

    def attack(self,player):
        if self.sp == 20:
            self.show_of_force(player)
            self.sp += 10
        elif self.sp ==40:
            self.wrath(player)
            self.sp += 20

        elif self.sp == 70:
            self.judgement(player)
            self.sp += 20

        elif self.sp == 30:
            self.absorption(player)
            self.sp += 10

        elif self.health_point == 90:
            self.final_stand(player)
            self.sp = 0

        else:
            self.basic_attack(player)
            self.sp += 10
            
        

    def __str__(self):
        super().__str__(self)

    def final_stand(self,player):  # Only to be called when the health is below a certain point.
        self.health_point += self.strength * 0.75
        self.strength -= (self.strength * 0.75)
        player.health_point -= self.strength * 1.5

    def show_of_force(self, player):  # Intimidates the player, causing them to level down.
        player.strength -= player.strength * 0.2
        player.health_point -= 25

    def wrath(self, player):  # The less health he has, the angrier he  is, and the more damage he does.
        player.health_point -= (600-player.health_point) * 0.2

    def judgement(self, player):  # Damages the player based on the level of the player. Higher level = more damage.
        player.health_point -= player.level * 25

    def absorption(self,player):  # Heals based on damage received. Received damage resets upon use.
        player.health_point -= 30

    def basic_attack(self,player):
        player.health_point -= self.strength * 2.5


class Necromancer(Ghost):

    def __init__(self, name, element, health_point, strength, image, trans_color, info):
        super().__init__(name, element, health_point, strength, image, trans_color, info)

        self.sp = 0
        self.damage_taken = 0

    def attack(self, player):

        if self.sp == 40 or self.sp == 80:
            self.subsitute(self)

        elif self.sp == 50:
            self.poison(player)

        elif self.sp == 70:
            self.rebond(player)

        elif self.sp == 100:
            self.lock_soul(player)

        else:
            self.sorcery(player)

    def substitute(self):  # more like absorb the damage; every 40 sp
        self.sp += 10
        self.damage_taken += 5
        self.health_point += self.health_point * 1.2

    def poison(self, player):  # continuous decreasing player's health point;randomly 1/5%
        self.damage_takem += 10
        player.health_point -= self.damage_taken
        self.sp += 10

    def rebond(self, player):  # randomly 1/5%
        player.health_point -= self.damage_taken * (1/5) + 20
        self.sp += 10

    def lock_soul(self, player):  # final strike, when sp reaches a certain point;
        n = random.randrange(5, 8)
        player.health_point -= self.strength * n

    def sorcery(self, player):  # basic attack
        n = random.randrange(2, 4)
        player.health_point -= self.strength * n
        self.sp += 10


class RoseMedusa(Ghost):


    def __init__(self, name, element, health_point, strength, image, trans_color, info):
        super().__init__(name, element, health_point, strength, image, trans_color, info)

        self.sp = 0
        self.damage_taken = 0

    def attack(self, player):
        if self.sp == 20 or self.sp == 80:
            self.rose_plant(self)
        elif self.sp == 50:
            self.rose_perfume(self)
        elif self.sp == 90:
            self.languishing_eyes(self)
        elif self.sp == 100:
            self.red_rose_fragrance(player)
        else:
            self.enchantment(player)

    def enchantment(self, player):  # high-amount attack
        player.health_point -= self.strength * 2
        self.damage_taken += 5
        self.sp += 10

    def rose_perfume(self,player):  # change her type
        if self.element == "earth":
            self.element = "water"
        elif self.element == "water":
            self.element = "fire"
        elif self.element == "fire":
            self.element== "gold"
        elif self.element == "gold":
            self.element = "wood"
        else:
            self.element == "earth"
        self.sp += 10
        player.health_point -= 20

    def languishing_eyes(self,player):  # increase strength
        self.strength += self.strength * 1.2
        player.health_point -= self.strength * random.randrange(1,3)
        self.sp += 10

    def rose_plant(self,player):  # increase health_point
        self.health_point += 20
        self.sp += 10

    def red_rose_fragrance(self, player):  # final strike, when sp reaches a certain point;
        n = random.randrange(5, 8)
        player.health_point -= self.strength * n
        self.sp = 0

'''
###???  temporarily use image of  RoseMedusa  for SmallMonster.Once image file for smallmonster, just add the file and relace 
         file path and name
'''
level1_ghost = [SmallMonster('Rose','metal',500,10,pygame.image.load('images/RoseMedusa.png'),None,None),
                SmallMonster('Rose','water',600,10,pygame.image.load('images/RoseMedusa.png'),None,None),
                RoseMedusa('Rose Medusa','wood',800,20,pygame.image.load('images/RoseMedusa.png'),None,None)
                ]

'''
###???  temporarily use image of  RoseMedusa  for SmallMonster.Once image file for smallmonster, just add the file and relace 
         file path and name
###???temporarily use level1_ghost to replace level2_ghost and Level3_ghost
'''

level2_ghost = [SmallMonster('Rose','water',700,15,pygame.image.load('images/RoseMedusa.png'),None,None),
                SmallMonster('Rose','wood',900,20,pygame.image.load('images/RoseMedusa.png'),None,None),
                King('King','metal',1100,25,pygame.image.load('images/RoseMedusa.png'),None,None)
                ]


level3_ghost = [SmallMonster('Rose','earth',1100,15,pygame.image.load('images/RoseMedusa.png'),None,None),
                SmallMonster('Rose','fire',1300,20,pygame.image.load('images/RoseMedusa.png'),None,None),
                Necromancer('Necromancer','water',1500,30,pygame.image.load('images/RoseMedusa.png'),None,None)
                ]

                
ghost_list = [level1_ghost,level2_ghost,level3_ghost]

