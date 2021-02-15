from collections import defaultdict, deque


class LocationError(Exception):
    pass


class Navigation:

    def __init__(self):
        self.graph = defaultdict(tuple)
        self.current_position = None
        self.goal = None
        self.path = deque()
        self.all_path = tuple()

    def set_position(self, x: int, y: int):
        if (x, y) not in self.graph:
            raise LocationError
        self.current_position = (x, y)
        return True

    def set_goal(self, x: int, y: int):
        if (x, y) not in self.graph:
            raise LocationError
        self.goal = (x, y)
        return True

    def add_path(self, u: tuple, v: tuple):
        self.graph[u] = self.graph[u] + (v, )

    def del_path(self, u: tuple, v: tuple):
        self.graph[u] = tuple(e for e in self.graph[u] if e != v)

    def del_node(self, node: tuple):
        self.graph.pop(node, None)

    def remove_all_path(self, node: tuple):
        self.graph.pop(node, None)
        for point in self.graph:
            self.graph[point] = tuple(
                e for e in self.graph[point] if e != node)

    def calculate_shortest_path(self):
        if not self.current_position or not self.goal:
            return False
        backtracker = {}
        queue = deque()
        queue.append(self.current_position)
        while len(queue):
            point = queue.popleft()
            for p in self.graph[point]:
                if p not in backtracker:
                    queue.append(p)
                    backtracker[p] = point
                    if p == self.goal:
                        self.path = deque()
                        while p != self.current_position:
                            self.path.append(p)
                            p = backtracker[p]
                        return True
        self.path = deque()
        return False

    def calculate_all_path(self):
        if not self.current_position or not self.goal:
            return False
        queue = deque()
        queue.append((self.current_position, {self.current_position}, tuple()))
        found = tuple()
        while len(queue):
            point, visited, path = queue.popleft()
            if point == self.goal:
                found += (path, )
            for p in self.graph[point]:
                if p not in visited:
                    queue.append((p, visited | {p}, path+(p,)))
        if found:
            self.all_path = found
            return True
        return False