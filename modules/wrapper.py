from math import ceil
from cv2 import resize

SCALE = 0.5
MAP_SIZE = (250, 250)

def point_wrapper(point):
    return ceil(point * SCALE)

def map_wrapper(map):
    return resize(map, MAP_SIZE)