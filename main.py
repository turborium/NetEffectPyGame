#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:
#
# Author:      crazzzypeter
#
# Created:     09.09.2021
# Copyright:   (c) crazzzypeter 2021
# Licence:     GNU GPL 3
#-------------------------------------------------------------------------------
import pygame
from pygame import gfxdraw
from dataclasses import dataclass
import random
import math

WIDTH=320*2
HEIGHT=240*2
FADEDISTANCE=100
POINTSCOUNT=50

@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    dx: float = 0.0
    dy: float = 0.0

def calc_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

points = []

def init():
    for _ in range(POINTSCOUNT):
        point = Point(x=random.uniform(0, WIDTH), y=random.uniform(0, HEIGHT))
        angle = random.uniform(0, math.pi)
        point.dx = math.cos(angle) * 4
        point.dy = math.sin(angle) * 4
        points.append(point)

def update():
    for point in points:
        # перемещаем точку в соответсвии со скоростью
        point.x = point.x + point.dx;
        point.y = point.y + point.dy;

        # обрабатываем вылет за экран
        if point.x < 0:
            point.dx = abs(point.dx)
        if point.x > WIDTH:
          point.dx = -abs(point.dx)
        if point.y < 0:
            point.dy = abs(point.dy)
        if point.y > HEIGHT:
          point.dy = -abs(point.dy)

def draw(surface):
    alpha_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for i in range(0, len(points)):
        for j in range(i + 1, len(points)):
            # вычисляем расстояние между линиями в -00 -> 0..1
            fade = -(calc_distance(points[i], points[j]) - FADEDISTANCE) / FADEDISTANCE

            # если фейд положителен рисуем
            if fade > 0:
                alpha_surface.fill([0,0,0,0])
                pygame.draw.line(
                    alpha_surface,
                    (0, 255, 0, int(fade * 255)),
                    (points[i].x, points[i].y),
                    (points[j].x, points[j].y),
                    int(fade * 5 + 1)
                )
                surface.blit(alpha_surface, (0,0))

    for point in points:
        pygame.draw.circle(surface, (0, 255, 100, 0), (point.x, point.y), 5)

def main():
    pygame.init()
    surface = pygame.display.set_mode(size=(WIDTH,HEIGHT), depth=32)
    clock = pygame.time.Clock()

    is_running = True

    init()

    while is_running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        update()

        # draw
        surface.fill([0,0,0]) # white background
        draw(surface)

        clock.tick(30)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
