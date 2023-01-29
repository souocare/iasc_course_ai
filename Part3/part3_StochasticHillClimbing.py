import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import time
import random
import math

import random


class StochasticHillClimbingtwo:
    def __init__(self, initial_state, cost_func, neighbor_func):
        self.initial_state = initial_state
        self.cost_func = cost_func
        self.neighbor_func = neighbor_func
        
    def search(self, max_iterations=1000):
        current_state = self.initial_state
        print(current_state)
        current_cost = self.cost_func(current_state)
        best_state = current_state
        best_cost = current_cost
        for i in range(max_iterations):
            next_state = self.neighbor_func(current_state)
            next_cost = self.cost_func(next_state)
            if next_cost < current_cost:
                current_state = next_state
                current_cost = next_cost
                if current_cost < best_cost:
                    best_state = current_state
                    best_cost = current_cost
            else:
                if random.uniform(0, 1) < 0.5:
                    current_state = next_state
                    current_cost = next_cost
        return best_state


class NQueens:
    def __init__(self, n):
        self.n = n
        self.qc = [rnd.randint(1, self.n) for i in range(self.n)]
        
    
    def neighbor(self):
        new_queens = self.qc.copy()
        i = rnd.randint(0, self.n-1)
        new_queens[i] = rnd.randint(1, self.n)
        return new_queens

    def cost(self, qc):
        cost = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                if qc[i] == qc[j]:
                    cost += 1
                elif abs(qc[i] - qc[j]) == abs(i - j):
                    cost += 1
        return cost
        
    def printState(self, state: list, msg: str = ''):
        board = [[1 if j+1 == state[i] else 0 for j in range(len(state))] for i in range(len(state))]

        plt.figure()
        plt.title(msg + '\nAttacks: ' + str(self.cost(state)))
        plt.imshow(board)
        # plt.axis(False)

        plt.show()

    def __str__(self):
        board = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                if self.qc[j] == i:
                    row.append("Q")
                else:
                    row.append(".")
            board.append(row)
        return "\n".join(["".join(row) for row in board])

        
class TravellingSalesman:
    def __init__(self, n):
        self.n = n 
        self.qc = []
        for i in range(n):
            city = (rnd.randint(0, 100), rnd.randint(0, 100))
            while city in self.qc:
                city = (rnd.randint(0, 100), rnd.randint(0, 100))

            self.qc.append(city)
    
    def printState(self, state):
        plt.figure()
        plt.title('\nDistance: ' + str(int(self.cost(state))))
        state.append(state[0])

        plt.plot(*zip(*state), 'o-')
        for i in range(len(state)-1):
            plt.annotate(f'  {i+1}', (state[i][0], state[i][1]))

        plt.show()

    def cost(self, qc):
        cost = 0
        for i in range(self.n-1):
            x1, y1 = qc[i]
            x2, y2 = qc[i+1]
            cost += math.sqrt((x2-x1)**2 + (y2-y1)**2)
        x1, y1 = qc[-1]
        x2, y2 = qc[0]
        cost += math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return cost


    def neighbor(self):
        new_tour = self.qc.copy()
        i, j = random.sample(range(len(self.qc)), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour





class StochasticHillClimbing:
    def __init__(self, problema):
        self.problema = problema
        
    def search(self, max_iterations=1000000):
        current_state = self.problema.qc
        current_cost = self.problema.cost(current_state)
        best_state = current_state
        best_cost = current_cost
        for i in range(max_iterations):
            print(i)
            next_state = self.problema.neighbor()
            next_cost = self.problema.cost(next_state)
            if next_cost < current_cost:
                current_state = next_state
                current_cost = next_cost
                if current_cost < best_cost:
                    best_state = current_state
                    best_cost = current_cost
            else:
                if random.uniform(0, 1) < 0.5:
                    current_state = next_state
                    current_cost = next_cost
        return best_state




def __main__():
    getexercise = input("If you want to play a game of NQueens, type 1\nIf you want to play Travelling Salesman, type 2\nIf you want to play both, pleas type 0.")
    if (getexercise == "1"):
        print("STARTING NQUEENS GAME")
        initial_state_queens = NQueens(8)
        initial_state_queens.printState(initial_state_queens.qc)
        shc_queens = StochasticHillClimbing(initial_state_queens)
        best_state_queens = shc_queens.search()
        print(best_state_queens)
        initial_state_queens.printState(best_state_queens)
        print("NQUEENS ENDED")
    elif (getexercise == "2"):
        print("STARTING TravellingSalesman GAME")
        tsp = TravellingSalesman(20)
        tsp.printState(tsp.qc)
        shc_tsp = StochasticHillClimbing(tsp)
        best_state_tsp = shc_tsp.search()
        tsp.printState(best_state_tsp)
        print("TravellingSalesman ENDED")

    else:
        print("STARTING NQUEENS GAME")
        initial_state_queens = NQueens(8)
        initial_state_queens.printState(initial_state_queens.qc)
        shc_queens = StochasticHillClimbing(initial_state_queens)
        best_state_queens = shc_queens.search()
        print(best_state_queens)
        initial_state_queens.printState(best_state_queens)
        print("NQUEENS ENDED")
        print("----------------------------------------------------------------")
        print("STARTING TravellingSalesman GAME")
        tsp = TravellingSalesman(20)
        tsp.printState(tsp.qc)
        shc_tsp = StochasticHillClimbing(tsp)
        best_state_tsp = shc_tsp.search()
        tsp.printState(best_state_tsp)
        print("TravellingSalesman ENDED")


    #########################


