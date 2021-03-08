from math import atan2, degrees, radians, sin, pi,acos
from collections import deque

DEFAULT_SPEED = 1
TRUCK_LENGHT = 2
TURN_CONSTANT = 0.5

def get_angle(timer, period):
    if timer <= period/2:
        return TURN_CONSTANT*timer
    return TURN_CONSTANT*(period-timer)


class DifferentialDrive:

    def __init__(self, dimension: float):
        self.dimension = dimension
        self.robot_motion = []
        self.turn_timer = 0
        self.turn_period = None
        self.path = []

    def set_path(self, path: deque):
        self.path = list(path)

    def set_position(self, x: float, y: float, z: float):
        self.position = (x, y, z)

    def set_goal(self, x: float, y: float, z: float):
        self.goal = (x, y, z)

    def create_robot_motion(self):
        degree = None
        self.robot_motion = deque()
        for idx, path in enumerate(self.path):
            if idx+1 < len(self.path):
                degree = degrees(atan2(
                    self.path[idx+1][1]-self.path[idx][1], self.path[idx+1][0]-self.path[idx][0]))
            self.robot_motion.append(path+(degree, ))

    def get_motor_speed(self, pos_x: float, pos_y: float, direction: float, time: float, obstacle: bool = False):
        if obstacle:
            return (0, 0)
        try:
            # TODO check if location error
            if (pos_x, pos_y, direction) == self.robot_motion[0]:
                self.robot_motion.popleft()
            if direction != self.robot_motion[0][2]:
                if not self.turn_timer:
                    try:
                        self.turn_period = 2/TURN_CONSTANT*acos(1-(TURN_CONSTANT*self.dimension/(2*DEFAULT_SPEED)*radians(self.robot_motion[0][2]-direction)))
                    except ValueError:
                        self.turn_period = 2/TURN_CONSTANT*acos(1-(TURN_CONSTANT*self.dimension/(2*DEFAULT_SPEED)*radians(direction-self.robot_motion[0][2])))
                    self.turn_timer = time
                if time-self.turn_timer <= self.turn_period/2:
                    omega = DEFAULT_SPEED/TRUCK_LENGHT * \
                        sin(get_angle(time-self.turn_timer, self.turn_period)) + TURN_CONSTANT
                else:
                    omega = DEFAULT_SPEED/TRUCK_LENGHT * \
                        sin(get_angle(time-self.turn_timer, self.turn_period)) - TURN_CONSTANT
            else:
                self.turn_timer = 0
                omega = 0
            if direction > self.robot_motion[0][2]:
                omega *= -1
            return (DEFAULT_SPEED + omega*self.dimension/2, DEFAULT_SPEED - omega*self.dimension/2)
        except IndexError:
            return (0, 0)