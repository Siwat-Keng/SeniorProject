#!/usr/bin/env python3

import json
import queue
import rospy
import threading
from datetime import datetime

from robot_state.srv import *

def robot_state_callback(req):

    print(type(req.req))
    return str(datetime.now().timestamp())

def main():

    rospy.init_node('planning_runner', anonymous=True)
    
    rospy.Service('planning', Planning, robot_state_callback)
    
    rospy.spin()


if __name__ == "__main__":
    print('started planning')
    main()

    
