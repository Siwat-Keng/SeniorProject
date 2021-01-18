from collections import defaultdict, deque
from itertools import chain

class LocationError(Exception):
    pass

class Navigation:

    def __init__(self):
        self.graph = defaultdict(tuple)
        self.current_position = None
        self.goal = None
        self.path = None

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
        self.graph[u] = self.graph[u] + (v, )

    def del_path(self, u:tuple, v:tuple):
        self.graph[u] = (e for e in self.graph[u] if e!=v)
    
    def del_all_path(self, node:tuple):
        self.graph.pop(node, None)
        for (x, y) in self.graph:
            self.graph[(x, y)] = (e for e in self.graph[(x, y)] if e!=node)

    def calculate_path(self):
        if not self.current_position or not self.goal:
            return False
        visited = set()
        queue = deque()
        queue.append((self.current_position, tuple()))
        visited.add(self.current_position)
        while len(queue):
            (x, y), path = queue.popleft()
            if (x, y) == self.goal:
                self.path = deque(path)
                return True
            for p in self.graph[(x, y)]:
                if p not in visited:
                    queue.append((p, chain(path, (p, ))))
                    visited.add(p)
        self.path = None
        return False

    def navigate(self):
        try:
            past_position = self.current_position
            self.current_position = self.path.popleft()
            return (past_position, self.current_position)
        except (IndexError, AttributeError):
            return (self.current_position, self.current_position)

    def at_destination(self):
        return self.current_position == self.goal and self.current_position != None