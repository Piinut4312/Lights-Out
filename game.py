import numpy as np
from random import sample
from itertools import product

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])
CENTER = np.array([0, 0])
DIRECTIONS = [UP, DOWN, LEFT, RIGHT, CENTER]

class Game:

    def __init__(self, shape):
        self.shape = shape
        self.board = np.zeros(shape=shape, dtype=np.int16)
        self.indices = list(product(range(shape[0]), range(shape[1])))
        self.n_cells = shape[0]*shape[1]
        self.adj_matrix = np.zeros(shape=(self.n_cells, self.n_cells), dtype=np.int8)
        for pos in self.indices:
            x, y = pos
            id = shape[1]*x+y
            for dir in DIRECTIONS:
                if self.in_range(x+dir[0], y+dir[1]):
                    id2 = shape[1]*(x+dir[0])+y+dir[1]
                    self.adj_matrix[id, id2] = 1


    def in_range(self, row, col):
        return row >= 0 and col >= 0 and row < self.shape[0] and col < self.shape[1]


    def flip(self, row, col):
        self.board[row, col] = 1-self.board[row, col]

    
    def click_at(self, row, col):
        if not self.in_range(row, col):
            raise ValueError('Invalid click position: ({x}, {y})'.format(x=row, y=col))
        for dir in DIRECTIONS:
            if self.in_range(row+dir[0], col+dir[1]):
                self.flip(row+dir[0], col+dir[1])
            
    
    def win(self):
        return np.all(self.board == 0)
    

    def randomize(self, steps=10):
        pos = sample(self.indices, k=steps)
        for p in pos:
            self.click_at(p[0], p[1])

