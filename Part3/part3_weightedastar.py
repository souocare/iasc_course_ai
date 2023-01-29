import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import time
import sys
class Estado:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


class WeightedAStar:
    def __init__(self, world, start, end, file, heuristic="manhattan"):
        self.world = world
        self.start = start
        self.end = end
        self.file = file
        self.width, self.height = world.shape

        if heuristic == "manhattan": 
            self.heuristic = self.manhattan_distance
        elif heuristic == "euclidean":
            self.heuristic = self.euclidean_distance
    
    def load_world(self):
        with open(self.file, "r") as arquivo:
            lines = arquivo.readlines()
            mundo = np.zeros((len(lines), len(lines[0].replace('\n', ''))), dtype=int)
            m = 0
            for x in lines:
                n = 0
                for y in x[:-1]:
                    if y == 'O':
                        mundo[m][n] = -1
                    elif y == 'A':
                        mundo[m][n] = 2
                    elif y == '>':
                        mundo[m][n] = 1
                    n += 1
                m += 1
        return mundo
    
    def manhattan_distance(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    def euclidean_distance(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    def neighbors(self, cell):
        row, col = cell
        states = []
        print(self.world)
        if row > 0 and self.world[row-1][col] != "O":
            states.append((row-1, col))
        if row < self.width-1 and self.world[row+1][col] != "O":
            states.append((row+1, col))
        if col > 0 and self.world[row][col-1] != "O":
            states.append((row, col-1))
        if col < self.height-1 and self.world[row][col+1] != "O":
            states.append((row, col+1))
        return states

    def solve(self):
        open_set = set([self.start])
        closed_set = set()
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end)}

        while open_set != 0:
            current = None
            current_f_score = None

            # Get the cell with the lowest f_score
            for cell in open_set:
                if current is None or f_score[cell] < current_f_score:
                    current = cell
                    current_f_score = f_score[cell]

            # If we have reached the end, reconstruct the path
            if current == self.end:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.neighbors(current):
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.end)
        return None

    def printPath(self, path):
        w = self.load_world()
        plt.title("Weighted A*")
        plt.imshow(w)
        x, y = zip(*path)
        plt.plot(y, x, '-o', color='red')
        plt.show()




if __name__ == '__main__':
    data_mundo = None
    filename = input("Please insert the name of the file, including the extension: ")
    try:
        with open(filename, "r") as file:
            data_mundo = file.read()
    except:
        print("Error opening the file.")
        sys.exit()
    
    mundo = np.array([list(line) for line in data_mundo.split("\n") if line])
    
    getheu = input("If you want to solve the problem using the manhattan heuristic, please type 1. If you want to solve the problem using the euclidean heuristic, please type 2.")
    heuristic = "manhattan"
    if getheu == "1":
        heuristic = "manhattan"
    elif getheu == "2":
        heuristic = "euclidean"
    else:
        print("Invalid input.")
        sys.exit()
    # Initialize the AStar class with the world, start, and end coordinates, and the file name
    agente = WeightedAStar(mundo, (np.where(mundo == ">")[0][0], np.where(mundo == ">")[1][0]), (np.where(mundo == "A")[0][0], np.where(mundo == "A")[1][0]), file=filename, heuristic = heuristic)


    # Run the A* algorithm and get the path
    path = agente.solve()

    # Print the path if one is found
    if path:
        agente.printPath(path)
    else:
        print("No path found.")

