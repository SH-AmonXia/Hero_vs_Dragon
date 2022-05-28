import time
import random
import pygame
import os
import sys
from pygame.locals import *
import threading


def clear():
    os.system("cls")


pygame.init()

bomb_sound = pygame.mixer.Sound("resources/music/特技剑.wav")
bomb_sound.set_volume(0.5)
hide_sound = pygame.mixer.Sound("resources/music/闪避.wav")
hide_sound.set_volume(0.5)
hit_sound = pygame.mixer.Sound("resources/music/击中.wav")
hit_sound.set_volume(0.5)
level_sound = pygame.mixer.Sound("resources/music/升级.wav")
level_sound.set_volume(0.5)
skill_sound = pygame.mixer.Sound("resources/music/技能.wav")
skill_sound.set_volume(0.7)
drink_sound = pygame.mixer.Sound("resources/music/drink.wav")
drink_sound.set_volume(0.5)


class Hero:
    def __init__(self, name):
        self.hp = 100
        self.name = name
        self._attack = 23
        self.defense = 15
        self.money = 0
        self.bomb = 15
        self.hide = 20
        self.upperhp = 100
        self.gold = 0
        self.wood = 0
        self.water = 0
        self.fire = 0
        self.dirt = 0
        self._skill = 1
        self.elename = {0: "（金）", 1: "（木）", 2: "（水）", 3: "（火）", 4: "（土）"}
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]
        self.glow = {2: 0, 3: 1, 1: 2, 4: 3, 0: 4}  # B生A（加成）
        self.killer = {0: 3, 1: 0, 2: 4, 3: 2, 4: 1}  # B克A(减少)

    def add_a(self, num):
        self._attack += num

    def add_d(self, num):
        self.defense += num

    def add_b(self, num):
        self.bomb -= num
        if self.bomb < 0:
            self.bomb = 1

    def add_h(self, num):
        self.hide -= num
        if self.hide < 0:
            self.hide = 1

    def add_hp(self, num):
        if self.hp + num <= 100:
            self.hp += num
        else:
            self.hp = 100

    def add_uhp(self, num):
        self.upperhp += num
        self.hp = self.upperhp

    def add_money(self, num):
        self.money += num

    def add_gold(self, num):
        self.gold += num
        if self.gold > 10:
            self.gold = 10

    def add_wood(self, num):
        self.wood += num
        if self.wood > 10:
            self.wood = 10
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]

    def add_water(self, num):
        self.water += num
        if self.water > 10:
            self.water = 10
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]

    def add_fire(self, num):
        self.fire += num
        if self.fire > 10:
            self.fire = 10
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]

    def add_dirt(self, num):
        self.dirt += num
        if self.dirt > 10:
            self.dirt = 10
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]

    def add_skill(self):
        self._skill += 1

    def add_all(self):
        self.add_uhp(50)
        self.add_a(20)
        self.add_d(15)
        self.add_b(3)
        self.add_h(3)
        self.add_money(170)
        self.add_gold(1)
        self.add_wood(1)
        self.add_water(1)
        self.add_fire(1)
        self.add_dirt(1)
        self.add_skill()
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]
        level_sound.play()

    def add_element(self):
        v = random.randint(0, 5)
        if v == 1:
            self.add_gold(1)
        elif v == 2:
            self.add_wood(1)
        elif v == 3:
            self.add_water(1)
        elif v == 4:
            self.add_fire(1)
        elif v == 5:
            self.add_dirt(1)
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]

    def add_rand(self):
        v = random.randint(0, 11)
        level_sound.play()
        if v == 0:
            self.add_a(2)
        elif v == 1:
            self.add_d(2)
        elif v == 2:
            self.add_b(1)
        elif v == 3:
            self.add_h(1)
        elif v == 4:
            self.add_uhp(5)
        elif v == 5:
            self.add_money(10)
        elif v == 6:
            self.add_gold(1)
        elif v == 7:
            self.add_wood(1)
        elif v == 8:
            self.add_water(1)
        elif v == 9:
            self.add_fire(1)
        elif v == 10:
            self.add_dirt(1)
        elif v == 11:
            self.add_skill()
        self._element = [self.gold, self.wood, self.water, self.fire, self.dirt]

    def attack(self, ob, mode, level):
        d = self._attack - ob.defense
        b = random.randint(0, self.bomb)
        c = random.randint(0, ob.hide)
        a = random.uniform(-2, 2)
        d += round(a, 2)
        d -= mode * 3

        if b == 1:
            d += 10 + 0.7 * level * (mode + 1)
            print("暴击！")
            bomb_sound.play()
        if c == 1:
            print("闪避！")
            hide_sound.play()
            d -= level * mode * 3
        obelement = ob.element()
        add = self._element[self.killer[obelement]] - ob._element[ob.element()]
        if add <= 0:
            add = 0
        add += self._element[self.glow[self.killer[obelement]]]
        d += add * 3
        d = round(d, 2)
        if d < 0:
            d = 0
        if ob.hp - d < 0:
            ob.hp = 0
        else:
            ob.hp -= d
        print("%s 对 %s%s 造成了 %s 点伤害" % (self.name, ob.name, self.elename[ob.element()], d))
        if b != 1 and c != 1:
            hit_sound.play()
        self.hp = round(self.hp, 2)
        ob.hp = round(ob.hp, 2)
        print("勇者血量：%s      怪物%s血量：%s" % (self.hp, self.elename[ob.element()], ob.hp))
        time.sleep(1.7)
        clear()

    def skill(self, ob, mode):
        cd = 25
        while True:
            cd -= 0.5
            rand = random.randint(0, 5)
            if cd <= 0 and rand == 2:
                skill_sound.play()
                print("技能发动！")
                ob.hp -= self._skill * 5 * (mode + 1)
                print("勇者血量：%s      怪物%s血量：%s" % (self.hp, self.elename[ob.element()], ob.hp))
                cd = 25
            elif cd > 0:
                print("技能cd：", cd)
            elif rand != 2:
                print("技能蓄力！")
            time.sleep(0.5)
            if ob.hp <= 0 or self.hp <= 10:
                break

    def treatment(self):
        s = input("1.包扎：加50点血  50金币\t\t2.手术：加满    160金币")
        if s == "1":
            if self.money >= 50:
                self.money -= 50
                self.add_hp(50)
                print("经过治疗，生命值恢复")
                print("当前生命值：", self.hp)
                time.sleep(1.7)
                clear()
            else:
                print("治疗失败，没钱了")
                time.sleep(1.7)
                clear()
        elif s == "2":
            if self.money >= 160:
                self.money -= 160
                self.add_hp(self.upperhp - self.hp)
                print("经过治疗，生命值恢复")
                print("当前生命值：", self.hp)
                time.sleep(1.7)
                clear()
            else:
                print("治疗失败，没钱了")
                time.sleep(1.7)
                clear()

    def show(self):
        print(self.name, "：")
        print("----------基础----------")
        print("\t血量：", self.hp, "/", self.upperhp)
        print("\t攻击：", self._attack)
        print("\t防御：", self.defense)
        print("\t金币：", self.money)
        print("\t暴击：1/", self.bomb)
        print("\t闪避：1/", self.hide)
        print("----------属性----------")
        print("\t金：", self.gold, "/10")
        print("\t木：", self.wood, "/10")
        print("\t水：", self.water, "/10")
        print("\t火：", self.fire, "/10")
        print("\t土：", self.dirt, "/10")
        time.sleep(5)
        clear()
