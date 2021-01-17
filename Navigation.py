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
    
    def set_goal(self, x:int, y:int):
        if (x, y) not in self.graph:
            raise LocationError
        self.goal = (x, y)

    def add_path(self, u:tuple, v:tuple):
        self.graph[u].append(v)
    
    def del_path(self, u:tuple, v:tuple):
        self.graph[u].remove(v)

    def calculate_path(self):
        if not self.current_position or not self.goal:
            return
        visited = set()
        queue = Queue()
        queue.put((self.current_position, []))
        visited.add(self.current_position)
        while not queue.empty():
            (x, y), path = queue.get()
            if (x, y) == self.goal:
                self.path = path
                return
            for p in filter(lambda point: point not in visited, self.graph[(x, y)]):
                queue.put((p, path+[p]))
                visited.add(p)

if __name__ == '__main__':
    def createDummy(x, n):
        for i in range(n):
            for j in range(n):
                if i>0 and j>0 and i<n-1 and j<n-1:
                    x.add_path((i, j), (i-1,j))
                    x.add_path((i, j), (i+1,j))
                    x.add_path((i, j), (i,j-1))
                    x.add_path((i, j), (i,j+1))
                elif i==0 and j==0 and n>1:
                    x.add_path((0, 0), (0, 1))
                    x.add_path((0, 0), (1, 0))
                elif i==0 and j==n-1 and n>1:
                    x.add_path((i, j), (i+1, j))
                    x.add_path((i, j), (i, j-1))
                elif i==n-1 and j==0 and n>1:
                    x.add_path((i, j), (i-1, j))
                    x.add_path((i, j), (i, j+1))
                elif i==n-1 and j==n-1 and n>1:
                    x.add_path((i, j), (i-1, j))
                    x.add_path((i, j), (i, j-1))
                elif i==0 and j!=n-1 and j!=0 and n>1:
                    x.add_path((i, j), (i+1, j))
                    x.add_path((i, j), (i, j-1))
                    x.add_path((i, j), (i, j+1))
                elif j==0 and i!=n-1 and i!=0 and n>1:
                    x.add_path((i, j), (i-1, j))
                    x.add_path((i, j), (i+1, j))
                    x.add_path((i, j), (i, j+1))
                elif i==n-1 and j!=n-1 and j!=0 and n>1:
                    x.add_path((i, j), (i-1, j))
                    x.add_path((i, j), (i, j-1))
                    x.add_path((i, j), (i, j+1))
                elif j==n-1 and i!=n-1 and i!=0 and n>1:
                    x.add_path((i, j), (i-1, j))
                    x.add_path((i, j), (i+1, j))
                    x.add_path((i, j), (i, j-1))
    import time
    navigation = Navigation()
    createDummy(navigation, 100)
    navigation.set_position(0, 0)
    navigation.set_goal(99,99)
    t = time.time()
    navigation.calculate_path()
    print(time.time()-t)