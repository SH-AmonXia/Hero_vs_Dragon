# -*- coding:utf-8 -*-
import time
import random
import pygame
import os


def clear():
    os.system("cls")


pygame.init()
ho_sound = pygame.mixer.Sound("resources/music/怪物.wav")
ho_sound.set_volume(0.5)
ho1_sound = pygame.mixer.Sound("resources/music/怪物1.wav")
ho1_sound.set_volume(0.5)
ho2_sound = pygame.mixer.Sound("resources/music/怪物2.ogg")
ho2_sound.set_volume(0.5)
ho = [ho_sound, ho1_sound, ho2_sound]


class Monster:
    def __init__(self, name, mode, level):
        self.name = name
        self.hp = 90 + 9.3 * level
        self._attack = 12 + 3 * level
        self.defense = 10 + 4 * level
        self.money = 38 + 4 * level * (mode + 1)
        self.bomb = 15 - (0.1 * level)
        self.hide = 20 - (0.2 * level)
        self.gold = 0
        self.wood = 0
        self.water = 0
        self.fire = 0
        self.dirt = 0
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]
        self.glow = {2: 0, 3: 1, 1: 2, 4: 3, 0: 4}  # B生A（加成）
        self.killer = {0: 3, 1: 0, 2: 4, 3: 2, 4: 1}  # B克A(减少)
        self.elename = {0: "（金）", 1: "（木）", 2: "（水）", 3: "（火）", 4: "（土）"}
        v = random.randint(1, 5)
        if v == 1:
            self.gold = 1
        elif v == 2:
            self.wood = 1
        elif v == 3:
            self.water = 1
        elif v == 4:
            self.fire = 1
        elif v == 5:
            self.dirt = 1
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]
        if self.bomb < 0:
            self.bomb = 1
        if self.hide < 0:
            self.hide = 1
        self.hide = round(self.hide, 0)
        self.bomb = round(self.bomb, 0)

    def element(self):
        if self.gold:
            return 0
        elif self.wood:
            return 1
        elif self.water:
            return 2
        elif self.fire:
            return 3
        elif self.dirt:
            return 4

    def final_attack(self, ob, mode, level):
        d = self._attack - (ob.defense - 10)
        if self.bomb - 3 <= 0:
            self.bomb = 4
        b = random.randint(0, self.bomb - 3)
        c = random.randint(0, ob.hide)
        a = random.uniform(-3, 3)
        d += round(a, 3)
        if b == 1:
            d += 10 * 0.7 * (mode + 1)
            d = round(d, 2)
            print("暴击！")
        if c == 1:
            print("闪避！")
            d -= level * (mode + 1) * 2
        d = round(d, 3)
        if d < 0:
            d = 0
        if ob.hp - d < 0:
            ob.hp = 0
        else:
            ob.hp -= d
        random.choice(ho).play()
        print("%s%s攻击了 %s ,造成了 %d 点伤害" % (self.name, self.elename[self.element()], ob.name, d))
        print("勇者血量：%s      恶龙%s血量：%s" % (ob.hp, self.elename[self.element()], self.hp))
        time.sleep(1.7)
        clear()

    def attack(self, ob, mode, level):
        d = self._attack - ob.defense
        b = random.randint(0, self.bomb)
        c = random.randint(0, ob.hide)
        a = random.uniform(-2, 2)
        d += round(a, 2)
        d += mode * 2
        if b == 1:
            d += 10
            print("暴击！")
        if c == 1:
            print("闪避！")
            d -= level * mode * 3
        d = round(d, 2)
        if d <= 0:
            d = 0
        if ob.hp - d < 0:
            ob.hp = 0
        else:
            ob.hp -= d
        random.choice(ho).play()
        print("%s%s攻击了 %s ,造成了 %d 点伤害" % (self.name, self.elename[self.element()], ob.name, d))
        self.hp = round(self.hp, 2)
        ob.hp = round(ob.hp, 2)
        print("勇者血量：%s      怪物%s血量：%s" % (ob.hp, self.elename[self.element()], self.hp))
        time.sleep(1.7)
        clear()
