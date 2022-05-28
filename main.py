import pygame
import time
import random
import pygame
from pygame.locals import *
import Enemy
import man
import threading
import sys
import os

mode = 1
level = 1
flag = 1


def clear():
    os.system("cls")


def main():
    pygame.init()
    screen_size = width, height = 470, 720
    bg = (255, 255, 255)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("勇者斗恶龙")

    pygame.mixer.init()
    pygame.mixer.music.load("resources/music/达拉崩吧1.mp3")
    pygame.mixer.music.set_volume(0.3)

    level_sound = pygame.mixer.Sound("resources/music/升级.wav")
    level_sound.set_volume(0.5)
    drink_sound = pygame.mixer.Sound("resources/music/drink.wav")
    drink_sound.set_volume(0.8)
    win_sound = pygame.mixer.Sound("resources/music/win.wav")
    win_sound.set_volume(0.5)
    run_sound = pygame.mixer.Sound("resources/music/逃跑.ogg")
    run_sound.set_volume(0.5)
    clear()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(bg)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
