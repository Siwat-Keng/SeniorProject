from collections import defaultdict, deque
from heapq import heappush, heappop
from math import hypot


class LocationError(Exception):
    pass

def default_inf():
    return float('inf')


class Navigation:

    def __init__(self):
        self.graph = defaultdict(tuple)
        self.current_position = None
        self.start_direction = None
        self.goal = None
        self.final_direction = None
        self.path = deque()
        self.all_path = tuple()

    def set_position(self, x: int, y: int, z: float):
        if (x, y) not in self.graph:
            raise LocationError
        self.current_position = (x, y)
        self.start_direction = z
        return True

    def set_goal(self, x: int, y: int, z: float):
        if (x, y) not in self.graph:
            raise LocationError
        self.goal = (x, y)
        self.final_direction = z
        return True

    def add_path(self, u: tuple, v: tuple):
        self.graph[u] = self.graph[u] + (v, )

    def del_node(self, node: tuple):
        self.graph.pop(node, None)
        for point in self.graph:
            self.graph[point] = tuple(
                e for e in self.graph[point] if e != node)

    def calculate_shortest_path(self):
        if not self.current_position or not self.goal:
            return False
        backtracker = {}
        distances = defaultdict(default_inf)
        distances[self.current_position] = 0
        queue = [(0, self.current_position)]
        while queue:
            current_distance, current_position = heappop(queue)
            if current_distance <= distances[current_position]:
                for neighbor in self.graph[current_position]:
                    distance = hypot(
                        current_position[0]-neighbor[0], current_position[1]-neighbor[1])
                    if distance < distances[neighbor] and neighbor in self.graph:
                        distances[neighbor] = distance
                        backtracker[neighbor] = current_position
                        if neighbor == self.goal:
                            self.path = deque()
                            while neighbor != self.current_position:
                                self.path.appendleft(neighbor)
                                neighbor = backtracker[neighbor]
                            return True
                        heappush(queue, (distance, neighbor))
        self.path = deque()
        return False