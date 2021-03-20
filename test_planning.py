from Navigation import Planning, LocationError
from collections import deque

# Test Case1
planner = Planning()
planner.add_path((0, 0), (10, 10))
planner.set_position(0, 0, 0)
planner.set_goal(10, 10, 0)
planner.calculate_shortest_path()
print(planner.path == deque([(0, 0), (10, 10)]))

# Test Case2
planner = Planning()
planner.add_path((0, 0), (10, 10))
planner.set_position(0, 0, 0)
planner.set_goal(1, 2, 0)
print(not planner.calculate_shortest_path())

# Test Case3
planner = Planning()
planner.add_path((0, 0), (5, 3))
planner.add_path((5, 3), (10, 10))
planner.set_position(0, 0, 0)
planner.set_goal(10, 10, 0)
planner.calculate_shortest_path() # deque([(0, 0), (5, 3), (10, 10)])
planner.del_node((5, 3)) # (5, 5) in deque
planner.add_path((5, 6), (0, 0)) # new path
planner.add_path((5, 6), (10, 10)) # new path
planner.calculate_shortest_path()
print(planner.path == deque([(0, 0), (5, 6), (10, 10)]))

# Test Case4
_pass = False
planner = Planning()
planner.add_path((0, 0),(10, 10))
try:
    planner.set_position(1, 1, 0)
except LocationError:
    _pass = True
print(_pass)