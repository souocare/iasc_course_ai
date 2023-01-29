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


class Acao:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy



class MemoriaAprend:
    def atualizar(s: Estado, a: Acao, q: float):
        raise NotImplementedError

    def Q(s: Estado, a: Acao) -> float:
        raise NotImplementedError


class MemoriaEsparsa(MemoriaAprend):
    # cria 2 variaveis, o valro de omissao e uma lista de memoria
    def __init__(self, valor_omissao: float = 0):
        self.valor_omissao = valor_omissao
        self.memoria = {}

    def Q(self, s: Estado, a: Acao) -> float:
        return self.memoria.get((s, a), self.valor_omissao)

    def atualizar(self, s: Estado, a: Acao, q: float):
        self.memoria[(s, a)] = q


class SelAcao:
    def selecionar_acao(self, s: Estado) -> Acao:
        raise NotImplementedError


class EGreedy(SelAcao):
    def __init__(self, mem_aprend: MemoriaAprend, acoes: list, epsilon: float):
        self.mem_aprend = mem_aprend
        self.acoes = acoes
        self.epsilon = epsilon

    def max_acao(self, s: Estado) -> Acao:
        rnd.shuffle(self.acoes)
        return max(self.acoes, key=lambda a: self.mem_aprend.Q(s, a))

    def aproveitar(self, s: Estado) -> Acao:
        return self.max_acao(s)

    def explorar(self) -> Acao:
        return self.acoes[rnd.randint(0, len(self.acoes) - 1)]

    def selecionar_acao(self, s: Estado) -> Acao:
        if rnd.random() > self.epsilon:
            return self.aproveitar(s)
        else:
            return self.explorar()


class AprendRef:
    def __init__(self, mem_aprend: MemoriaAprend, sel_acao: SelAcao, alfa: float, gama: float):
        self.mem_aprend = mem_aprend
        self.sel_acao = sel_acao
        self.alfa = alfa
        self.gama = gama

    def aprender(s: Estado, a: Acao, r: float, sn: Estado, an: Acao = None):
        raise NotImplementedError


class QLearning(AprendRef):
    def aprender(self, s: Estado, a: Acao, r: float, sn: Estado):  # , an: Acao = None
        an = self.sel_acao.max_acao(sn)
        qsa = self.mem_aprend.Q(s, a)
        qsnan = self.mem_aprend.Q(sn, an)
        q = qsa + self.alfa * (r + self.gama * qsnan - qsa)
        self.mem_aprend.atualizar(s, a, q)


class MecanismoAprendRef:
    def __init__(self, acoes: Acao):
        self.acoes = acoes
        self.mem_aprend = MemoriaEsparsa()
        self.sel_acao = EGreedy(self.mem_aprend, self.acoes, 2)
        #self.aprend_ref = DynaQ(self.mem_aprend, self.sel_acao, 0.7, 0.95, 1000)
        self.aprend_ref = QLearning(self.mem_aprend, self.sel_acao, 0.7, 0.95)

    def aprender(self, s: Estado, a: Acao, r: float, sn: Estado):
        self.aprend_ref.aprender(s, a, r, sn)

    def selecionar_acao(self, s: Estado) -> Acao:
        return self.sel_acao.selecionar_acao(s)



class World:

    def __init__(self, nomeficheiro,  multipl_reforco: float = 10, custo_movimento: float = 0.01):
        self.nomeficheiro = nomeficheiro
        self.multipl_reforco = multipl_reforco
        self.custo_movimento = custo_movimento
        plt.ion()
    
    def getlocation(self):
        return Estado(self.locationagent.x, self.locationagent.y)

    def wheretomove(self, accao: Acao):
        reward = self.world[self.locationagent.x + accao.dx][self.locationagent.y + accao.dy]
        print(reward)

        '''
        The mover method takes an action (a: Acao) as an input and returns a tuple that contains the next state (sn) and the reward (r).

The method first calculates the next state (sn) by adding the dx and dy values of the action to the current state's x and y values. It then increments the number of moves.

It checks if the next state is within the limits of the world, but this check is commented out in the code. If the next state is out of the bounds of the world, the method would return the current state and a penalty reward (-2 * self.multiplicadorReforço)

Then it gets the information of the next position and assigns it to r.

Finally, the method checks if the next state is valid (r >= 0) and returns the next state and the reward. If the next state is not valid (r < 0), the method returns the current state and the penalty reward (-r * self.multiplicadorReforço - self.custoMover)

So, the return of this method is a tuple with 2 values:
1- The next state (sn) if the next position is valid (r >= 0) or the current state if the next position is not valid (r < 0)
2- The reward (r) if the next position is valid (r >= 0) or the penalty reward (-r * self.multiplicadorReforço - self.custoMover) if the next position is not valid (r < 0)
        '''
        if (reward >= 0):
            self.locationagent = Estado(self.locationagent.x + accao.dx, self.locationagent.y + accao.dy)
            #print(self.locationagent)
            return self.locationagent, reward
        else:
            return self.locationagent, reward * self.multipl_reforco - self.custo_movimento

    def showmtlpl(self):
        #mostrar um mundo com matplotlib
        #plt.ion()

        # plt.imshow(self.world)
        # plt.show()
        # time.sleep(0.5)

        plt.imshow(self.world)
        plt.pause(0.001)
        plt.clf()
        plt.show()

    def getdata(self):
        # abrir ficheiro
        f = open(self.nomeficheiro,'r')
        # extrair dados para matriz
        data = []
        datafinal = []
        for linha in f:
            data.append(linha.split())
        # fechando ficheiro
        linha_i = 0
        for linha in data:
            #print(linha)
            lista = []
            linha = linha[0]
            coluna_i = 0
            for coluna in linha:
                if coluna == "O":
                    lista.append(-1)
                elif coluna == ".":
                    lista.append(0)
                elif coluna == "A": #alvo
                    self.locationtarget = Estado(linha_i,coluna_i)
                    lista.append(2)
                elif coluna == ">":
                    self.locationagent = Estado(linha_i,coluna_i)
                    lista.append(1)
                else:
                    lista.append(0)
                coluna_i = coluna_i + 1
            #print(lista)
            datafinal.append(lista)
            linha_i = linha_i + 1

        f.close()
        self.world = datafinal

    def update(self, prevlocation: Estado, novalocation: Estado):
        self.locationagent = novalocation
        #print("---------")
        #print(self.world)
        self.world[prevlocation.x][prevlocation.y] = 0

        self.world[novalocation.x][novalocation.y] = 1
        #print("---------")
        #print(self.world)

        


if __name__ == '__main__':

    accoes = [Acao(0, 1), Acao(1, 0), Acao(0, -1), Acao(-1, 0)]
    mecan_aprend_ref = MecanismoAprendRef(accoes)
    filename = input("Please insert the name of the file, including the extension: ")
    try:
        mundo = World(filename)
        mundo.getdata()
    except:
        print("Error opening the file.")
        sys.exit()
    
    while True:
        mundo = World(filename)
        mundo.getdata()

        while True:
            selecaoinicial = mundo.getlocation()
            accaoselecionada = mecan_aprend_ref.selecionar_acao(mundo.getlocation()) #aqui seleciono a acao
            print(accaoselecionada.dx)
            print(accaoselecionada.dy)
            novalocalizacao, reward = mundo.wheretomove(accaoselecionada) 
            print(novalocalizacao)
            print(reward)

            mecan_aprend_ref.aprender(mundo.getlocation(), accaoselecionada, reward, novalocalizacao)
            mundo.update(selecaoinicial, novalocalizacao)
            mundo.showmtlpl()

            if (novalocalizacao == mundo.locationtarget):
                break

        #mundo.aprender(mundo.getlocation, accaoselecionada,

