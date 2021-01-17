from collections import defaultdict
from queue import Queue

class LocationError(Exception):
    pass

class Navigation:

    def __init__(self):
        self.graph = defaultdict(list)
        self.current_position = None
        self.goal = None
        self.path = []

    def set_position(self, x:int, y:int):
        if (x, y) not in self.graph:
            raise LocationError
        self.current_position = (x, y)
        return True

    def set_goal(self, x:int, y:int):
        if (x, y) not in self.graph:
            raise LocationError
        self.goal = (x, y)
        return True

    def add_path(self, u:tuple, v:tuple):
        try:
            self.graph[u].append(v)
            return True
        except ValueError:
            return False

    def del_path(self, u:tuple, v:tuple):
        try:
            self.graph[u].remove(v)
            return True
        except ValueError:
            return False

    def calculate_path(self):
        if not self.current_position or not self.goal:
            return False
        visited = set()
        queue = Queue()
        queue.put((self.current_position, []))
        visited.add(self.current_position)
        while not queue.empty():
            (x, y), path = queue.get()
            if (x, y) == self.goal:
                self.path = path
                return True
            for p in filter(lambda point: point not in visited, self.graph[(x, y)]):
                queue.put((p, path+[p]))
                visited.add(p)
        self.path = []
        return False

    def navigate(self):
        try:
            self.current_position = self.path.pop(0)
            return self.current_position
        except IndexError:
            return self.current_position

    def at_destination(self):
        return self.current_position == self.goal and self.current_position != None