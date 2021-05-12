from rospy import Publisher, Rate, init_node, Service, is_shutdown
from json import loads, dumps
from time import time
from math import radians

from robot_state.srv import Planning
from std_msgs.msg import Float32MultiArray

from modules.planner import Planner
from modules.navigator import Navigator
from modules.wrapper import point_wrapper, map_wrapper

# Response
IDLE = 0
WALKING = 1
PAUSED = 2

# Command
SET_GOAL = 0
MOVE = 1
SET_MAP = 2

COMMAND_PAUSE = 0
COMMAND_GO = 1
COMMAND_CANCEL = 2

# ROS Config
NODE_NAME = 'planning_runner'
SERVICE_NAME = 'planning'
PUBLISH_TO = 'robotControl'

POSITION_ERROR_THRES = 100


class POSITION_ERROR_EXCEPTOON(Exception):
    pass


def validate_planned(planned, map):
    if not planned:
        return False
    for (x, y, direction) in planned:
        if map[y][x]:
            return False
    return True


def get_angle_diff(angle1, angle2):
    return (angle1 - angle2 + 180) % 360 - 180


def decided_position(current_position, planned):
    closest = float('inf')
    index = -1
    for idx, (x, y, direction) in enumerate(planned):
        if (current_position[0] - x)**2 + (current_position[1] - y)**2 + abs(radians(get_angle_diff(current_position[2], direction))) < closest:
            closest = (current_position[0] - x)**2 + \
                (current_position[1] - y)**2 + \
                abs(radians(get_angle_diff(current_position[2], direction)))
            index = idx
    if closest > POSITION_ERROR_THRES:
        raise POSITION_ERROR_EXCEPTOON
    if index == len(planned) - 1:
        next_index = None
    else:
        next_index = index + 1
    return (index, next_index)


class Node:

    def __init__(self):
        self.planner = Planner()
        self.navigator = Navigator()
        self.status = IDLE
        self.publisher = Publisher(
            PUBLISH_TO, Float32MultiArray, queue_size=10)
        self.rate = Rate(10)
        self.goal = None

    def callback(self, request):
        commands = loads(request.req)
        response = {'status': 'type error'}
        if commands['type'] == SET_GOAL:
            self.planner.update_goal(point_wrapper(
                commands['goal'][0]), point_wrapper(commands['goal'][1]))
            self.goal = commands['goal']
            response['status'] = 'ok'
        elif commands['type'] == MOVE:
            if commands['status'] == COMMAND_PAUSE:
                self.status = PAUSED
                response['status'] = 'ok'
            elif commands['status'] == COMMAND_GO:
                self.status = WALKING
                response['status'] = 'ok'
            elif commands['status'] == COMMAND_CANCEL:
                self.planner.clear()
                self.navigator.clear()
                self.status = IDLE
                response['status'] = 'ok'
        elif commands['type'] == SET_MAP:
            self.planner.update_position(point_wrapper(commands['occupancy_grid_position'][0]), point_wrapper(
                commands['occupancy_grid_position'][1]), commands['real_position'][2])
            self.planner.update_map(map_wrapper(commands['map']))
            response['state'] = self.status
            response['target'] = self.goal
            response['path'] = self.planner.planned
            response['status'] = 'ok'
        print(response)
        return dumps(response)

    def init_node(self):
        init_node(NODE_NAME, anonymous=True)
        Service(SERVICE_NAME, Planning, self.callback)

    def operate(self):
        try:
            current_point, next_point = decided_position(
                self.planner.current_position, self.planner.planned)
        except POSITION_ERROR_EXCEPTOON:
            self.publisher.publish(Float32MultiArray(data=[0, 0]))
            print('Node : Hm... where am I?')
            self.planner.plan()
            current_point, next_point = decided_position(
                self.planner.current_position, self.planner.planned)
        if not next_point:
            self.status = IDLE
        self.publisher.publish(Float32MultiArray(data=self.navigator.get_motor_speed(
            self.planner.current_position, self.planner.planned[current_point], time())))

    def publish(self):
        while not is_shutdown():
            if self.status == IDLE or self.status == PAUSED:
                self.publisher.publish(Float32MultiArray(data=[0, 0]))
            elif self.status == WALKING:
                if not validate_planned(self.planner.planned, self.planner.map):
                    self.planner.plan()
                self.operate()
            self.rate.sleep()

    def run(self):
        self.init_node()
        self.publish()


if __name__ == '__main__':
    print('Started Planning')
    navigation_node = Node()
    navigation_node.run()
