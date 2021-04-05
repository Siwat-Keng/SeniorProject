#!/usr/bin/env python3

import json
import rospy

from modules.Navigation import *
from robot_state.srv import *

SET_GOAL = 0
MOVE = 1
SET_MAP = 2

ROBOT_DIMENSION = 1

navigation = Planning()
diffdrive = DifferentialDrive(ROBOT_DIMENSION)
memory = []

def robot_state_callback(req):

    commands = json.loads(req.req)
    response = {}
    if commands['type'] == SET_GOAL:
        pass
    elif commands['type'] == MOVE:
        pass
    elif commands['type'] == SET_MAP:
        pass
    return json.dumps(response)

def main():

    rospy.init_node('planning_runner', anonymous=True)
    rospy.Service('planning', Planning, robot_state_callback)
    
    rospy.spin()


if __name__ == "__main__":
    print('started planning')
    main()