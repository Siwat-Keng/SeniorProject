from queue import Queue

OBSTRUCTION = '#'
SPACE = ' '

class LocationError(Exception):
    pass

def createMaze():
    maze = []
    maze.append(["#","#", "#", "#", "#", "#","#"])
    maze.append(["#"," ", " ", " ", "#", " ","#"])
    maze.append(["#"," ", "#", " ", "#", " ","#"])
    maze.append(["#"," ", "#", " ", " ", " ","#"])
    maze.append(["#"," ", "#", "#", "#", " ","#"])
    maze.append(["#"," ", " ", " ", "#", " ","#"])
    maze.append(["#","#", "#", "#", "#", "#","#"])

    return maze

def createMaze2():
    maze = []
    maze.append(["#","#", "#", "#", "#", "#", "#", "#", "#"])
    maze.append(["#"," ", " ", " ", " ", " ", " ", " ", "#"])
    maze.append(["#"," ", "#", "#", " ", "#", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", " ", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", " ", "#"])
    maze.append(["#"," ", "#", " ", "#", " ", "#", "#", "#"])
    maze.append(["#"," ", " ", " ", " ", " ", " ", " ", "#"])
    maze.append(["#","#", "#", "#", "#", "#", "#", "#", "#"])

    return maze

def createEmptySpace(n):
    return [[" " for i in range(n)] for i in range(n)]

class Navigation:

    def __init__(self):
        self.map = None
        self.pos = None
        self.goal = None
        self.path = []

    def update_map(self, _map:list): # TODO
        self.map = _map

    def set_position(self, x:int, y:int):
        if self.map[y][x] == OBSTRUCTION:
            raise LocationError
        self.pos = (x, y)
    
    def set_goal(self, x:int, y:int):
        if self.map[y][x] == OBSTRUCTION:
            raise LocationError
        self.goal = (x, y)

    def calculate_path(self):
        if not self.pos or not self.goal:
            return
        queue = Queue()
        visited = set()
        queue.put([self.pos[0], self.pos[1], []])
        visited.add((self.pos[0], self.pos[1]))
        
        while not queue.empty():
            x, y, path = queue.get()
            if (x, y) == self.goal:
                self.path = path
                return
            if y-1 >= 0 and self.map[y-1][x] != OBSTRUCTION and (x, y-1) not in visited:
                queue.put([x, y-1, path+[(x, y-1)]])
                visited.add((x, y-1))
            if y+1 < len(self.map) and self.map[y+1][x] != OBSTRUCTION and (x, y+1) not in visited:
                queue.put([x, y+1, path+[(x, y+1)]])
                visited.add((x, y+1))
            if x-1 >= 0 and self.map[y][x-1] != OBSTRUCTION and (x-1, y) not in visited:
                queue.put([x-1, y, path+[(x-1, y)]])
                visited.add((x, y-1))
            if x+1 < len(self.map[y]) and self.map[y][x+1] != OBSTRUCTION and (x+1, y) not in visited:
                queue.put([x+1, y, path+[(x+1, y)]])
                visited.add((x+1, y))
        self.path = []

    def get_path(self): # TODO
        return self.path.pop(0)


if __name__ == '__main__':
    navigation = Navigation()
    # navigation.update_map(createMaze2())
    navigation.update_map(createEmptySpace(1000))
    navigation.set_position(1, 1)
    navigation.set_goal(999, 999)
    navigation.calculate_path()
    print(len(navigation.path))