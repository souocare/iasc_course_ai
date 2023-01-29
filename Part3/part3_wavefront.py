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

class Wavefront:
    def __init__(self, nomeArquivo: str, mostrarGrafico: bool = True):
        self.mundo, self.s, self.alvo = self.load_world(nomeArquivo)
        self.mostrarGrafico = mostrarGrafico
        self.valorMundo = self.propagate_value([self.alvo])
        self.path = []

    def load_world(self, nomeArquivo: str):
        with open(nomeArquivo, "r") as file:
            lines = file.readlines()
            world: list[list[int]] = np.zeros((len(lines), len(lines[0].replace('\n', ""))), dtype=int)

            initial_state = Estado(0, 0)
            target = Estado(0, 0)

            m = 0
            for x in lines:
                n = 0
                for y in x[:-1]:
                    if y.__eq__('O'):
                        world[m][n] = -1
                    elif y.__eq__('A'):
                        world[m][n] = 2
                        target = Estado(n, m)
                    elif y.__eq__('>'):
                        initial_state = Estado(n, m)
                    n += 1
                m += 1

            print(world)
            print(initial_state, 'Start')
            print(target, 'End')
            return world, initial_state, target

    def show(self, s):
        #print(self.s)
        path = []
        print(self.adjacent(s))
        while s != self.alvo:
            path.append(s)
            max_value = -float('inf')
            max_s = None
            for next_s in self.adjacent(s):
                if self.valorMundo[next_s] > max_value:
                    max_value = self.valorMundo[next_s]
                    max_s = next_s

            s = max_s
            #s = sn

        mundo = [[x for x in y] for y in self.mundo]
        for v in self.valorMundo:
            mundo[v.y][v.x] = self.valorMundo[v]

        for s in path:
            mundo[s.y][s.x] = -5
        
        
        plt.imshow(mundo)
        plt.show()

    def propagate_value(self, objectives, gain: int = 10):
        V = {}
        wavefront = []
        gamma = len(self.mundo)/(len(self.mundo)+1)  # Gamma proportional to world

        for o in objectives:
            V[o] = gain
            wavefront.append(o)

        while len(wavefront) > 0:  # While there are states in the wavefront
            s = wavefront.pop(0)
            for a in self.adjacent(s):
                v = V[s] * gamma  # Attenuates the value
                if v > V.get(a, -1):  # If there is a worse value in the adjacent state, replaces and adds to wavefront
                    V[a] = v
                    wavefront.append(a)
        return V

    def adjacent(self, s: Estado):
        # Adjacent states only in vertical and horizontal avoiding obstacles
        adjacent = []
        if s.x > 0:
            e = Estado(s.x - 1, s.y)
            if self.mundo[e.y][e.x] != -1:
                adjacent.append(e)
        if s.x < len(self.mundo[0]) - 1:
            e = Estado(s.x + 1, s.y)
            if self.mundo[e.y][e.x] != -1:
                adjacent.append(e)
        if s.y > 0:
            e = Estado(s.x, s.y - 1)
            if self.mundo[e.y][e.x] != -1:
                adjacent.append(e)
        if s.y < len(self.mundo) - 1:
            e = Estado(s.x, s.y + 1)
            if self.mundo[e.y][e.x] != -1:
                adjacent.append(e)
        return adjacent

if __name__ == '__main__':

    filename = input("Please insert the name of the file, including the extension: ")
    try:
        wavefront = Wavefront(filename)  # Carrega o mundo, colocando o agente de volta ao início
        wavefront.show(wavefront.s)
    except:
        print("Error opening the file.")
        sys.exit()
    

