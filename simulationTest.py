import pygame
import numpy as np
import cv2
from math import ceil, degrees, fabs, sin, cos, pi, radians, sqrt

from planner import Planner
from navigator import Navigator
from position import Position

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

M2P = 3779.52


def normalized_angle(angle):
    return (angle + pi) % (2 * pi) - pi


def build_map():
    return cv2.imread('map.png')


def get_angle_diff(angle1, angle2):
    return (angle1 - angle2 + 180) % 360 - 180


class Envir:

    def __init__(self, dimentions):
        self.height = dimentions[0]
        self.width = dimentions[1]

        pygame.display.set_caption("Simulation")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render('default', True, WHITE, BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.center = (50, dimentions[1]-30)
        self.background = pygame.image.load('map.png')

    def write_info(self, x, y, theta, _x, _y):
        txt = f"POSITION : ({x}, {y}, {round(degrees(theta), 1)}) GOAL : ({_x}, {_y})"
        self.text = self.font.render(txt, True, WHITE, BLACK)
        self.map.blit(self.text, self.textRect)
    
    def draw_background(self):
        self.map.blit(self.background, (0, 0))


class Robot:

    def __init__(self, startpos, robotImg, width):
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.theta = 0
        self.vl = 0
        self.vr = 0
        self.img = pygame.transform.scale(pygame.image.load(robotImg), (10, 10))
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def update_speed(self, vl, vr):
        self.vl = vl * M2P
        self.vr = vr * M2P

    def move(self):
        self.x += ((self.vl+self.vr)/2*cos(self.theta)*dt)
        self.y -= ((self.vl+self.vr)/2*sin(self.theta)*dt)
        self.theta += (self.vr-self.vl)/self.w*dt
        self.theta = normalized_angle(self.theta)

        self.rotated = pygame.transform.rotozoom(
            self.img, degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))


planner = Planner()
navigator = Navigator()
_map = build_map()
start = (50, 480)
goal = (50, 330)
current_position = (start[0], start[1], 0)
planner.update_map(_map)
planner.update_position(current_position)
planner.update_goal((goal[0], goal[1]))
planner.plan()
print(planner.planned)

positioner = Position()
positioner.update_plan(planner.planned)

pygame.init()
dims = (500, 500)
running = True

environment = Envir(dims)
robot = Robot(start, r"D:\Robot\navigation_upgrade\test\robot.png", 0.01 * M2P)
dt = 0
lasttime = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    position = positioner.get_position(robot.x, robot.y, degrees(robot.theta))
    if position:
        vl, vr = navigator.get_motor_speed((robot.x, 
            robot.y, degrees(robot.theta)), position, pygame.time.get_ticks())
    else:
        vl, vr = (0, 0)
    robot.update_speed(vl, vr)
    robot.move()
    dt = (pygame.time.get_ticks()-lasttime)/1000
    lasttime = pygame.time.get_ticks()
    pygame.display.update()
    environment.map.fill(BLACK)
    environment.draw_background()
    robot.draw(environment.map)
    environment.write_info(int(robot.x), int(
        robot.y), robot.theta, goal[0], goal[1])
