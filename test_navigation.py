from Navigation import Planning, DifferentialDrive
from collections import deque

DIMENSION = 1

planner1 = Planning()
planner2 = Planning()

planner1.add_path((0, 0), (1, 1))
planner1.add_path((1, 1), (2, 2))
planner1.set_position(0, 0, 45)
planner1.set_goal(2, 2, 45)
planner1.calculate_shortest_path()

planner2.add_path((0, 0), (1, 1))
planner2.add_path((1, 1), (2, 2))
planner2.set_position(0, 0, 0)
planner2.set_goal(2, 2, 90)
planner2.calculate_shortest_path()

# Test Case1
diffdrive1 = DifferentialDrive(DIMENSION)
diffdrive1.create_robot_motion(planner1)
print(diffdrive1.robot_motion == deque([(0, 0, 45), (1, 1, 45.0), (2, 2, 45)]))

# Test Case2
diffdrive2 = DifferentialDrive(DIMENSION)
diffdrive2.create_robot_motion(planner2)
print(diffdrive2.robot_motion == deque([(0, 0, 0), (1, 1, 45.0), (2, 2, 90)]))