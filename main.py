#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random

SCR_RECT = Rect(0, 0, 640, 480)
pygame.init()
screen = pygame.display.set_mode(SCR_RECT.size)
pygame.display.set_caption(u"Undertale")

class Undertale:
    def __init__(self):
        self.game_status = 0

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            pygame.display.update()



if __name__ == "__main__":
    Undertale()

