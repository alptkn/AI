import argparse
import time 
import numpy as np 
import random 
from pathlib import Path
import sys 
path = str(Path(__file__).parent)
 

class Game:
    def __init__(self,file_name):
        self.initialize_game(file_name)
        self.values = np.array([1,2,3,4,5,6,7,8,9], np.int32)
        self.turn = "MAX"
    
    def initialize_game(self,file_name):
        file = open(path + "/" + str(file_name), "r")
        Lines = file.readlines()
        my_data = [[int(val) for val in line.split()] for line in Lines[0:]]
        self.board = np.array(my_data, np.int32)
        
        count = 0
        for x in range(self.board.shape[0]):
            for y in range(self.board.shape[1]):
                if self.board[x][y] == 0:
                    count = count + 1
        
        if count < 1 or count > 15:
            print("Invalid number of empty boxes")
            sys.exit()

    def print_board(self):
         for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                print('{}|'.format(self.board[i][j]), end=" ")
            print("\n--------------------------")
         print()

    def valid_moves(self,x,y):
        temp_list,temp_list_2,valid_values = list(),list(),list()
        temp = None
        if x < 3:
            if y < 3:
                for i in range(0,3):
                    for j in range(0,3):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
            elif y >= 3 and y < 6:
                for i in range(0,3):
                    for j in range(3,6):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
            else:
                for i in range(0,3):
                    for j in range(6,9):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
        
        elif x >=3 and x < 6:
             if y < 3:
                 for i in range(3,6):
                    for j in range(0,3):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
            
             elif y >= 3 and y < 6:
                for i in range(3,6):
                    for j in range(3,6):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
             else:
                for i in range(3,6):
                    for j in range(6,9):
                        if x !=i or j != y:
                           temp = self.board[i][j]
                           temp_list.append(temp)
        else:
            if y < 3:
                for i in range(6,9):
                    for j in range(0,3):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
            elif y >= 3 and y < 6:
                for i in range(6,9):
                    for j in range(3,6):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
            else:
                for i in range(6,9):
                    for j in range(6,9):
                        if x !=i or j != y:
                            temp = self.board[i][j]
                            temp_list.append(temp)
            
        temp_list = np.array(temp_list, np.int32)
        for var in self.values:
            if var not in temp_list:
                temp_list_2.append(var)
        temp_list_2 = np.array(temp_list_2, np.int32)
        for var in temp_list_2:
            flag_1, flag_2 = True, True
            for j in range(9):
                if self.board[x][j] == var:
                    flag_1 = False
                    break
            if flag_1:
                for i in range(9):
                    if self.board[i][y] == var:
                        flag_2 = False
                        break
            
            if flag_1 and flag_2:
                valid_values.append(var)
        
        
        if not valid_values:
            return valid_values, False
        else:
            return valid_values,True


    def is_end(self):
        result = np.all(self.board)
        if result:
            if self.turn == "MAX":
                return 1
            else:
                return 2
        else:
            return result
     
    def max(self):
        
        maxv = -2
        px = None
        py = None 
        temp = None
        result = self.is_end()
        
        if result == 2:
            return (1,0,0)
        elif result == 1:
            return (-1,0,0)
        
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 0:
                    moves = self.valid_moves(i, j) 
                    if not moves:
                        temp = random.choice(moves)
                        self.board[i][j] = temp
                    
                    (m, min_i, min_j,a) = self.min()
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.board[i][j] = 0
        
        return (maxv, px, py,temp)
    
    def min(self):
        minv = 2
        qx = None
        qy = None 
        temp = None
        result = self.is_end()
        
        if result == 2:
            return (-1,0,0)
        elif result == 1:
            return (1,0,0)
        
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 0:
                    moves = self.valid_moves(i, j) 
                    if not moves:
                        temp = random.choice(moves)
                        self.board[i][j] = temp
                    
                    (m, max_i, max_j,a) = self.max()
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.board[i][j] = 0
        return (minv, qx, qy,temp)
        
    def play(self):
        
        while True:
            self.print_board()
            result = self.is_end()
            
            if result:
                print(result)
            
                return 
            
            if self.turn == "MAX":
                
                start_time = time.time()
                (m, qx, qy,val) = self.max()
                end = time.time()
                self.board[qx][qy] = val
                self.player_turn = 'MIN'
        
            else:
                (m, px, py,val) = self.min()
                self.board[px][py] = val
                self.turn = "MAX"
        
        
def main():
    g = Game("input.txt")
    g.play()
if __name__ == "__main__":
    main()