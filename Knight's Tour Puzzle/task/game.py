import sys
import os
import keyboard
import time
import numpy as np
'''
with open('omgitworked.txt','w')as f:
    pass
file_path = 'omgitworked.txt'
sys.stdout = open(file_path, "w")
'''
#Version 2:
class Board2():
    def __init__(self):
        self.dimensions = self.get_dimensions()
        self.board = np.zeros((self.dimensions[1], self.dimensions[0]))
        self.knight = Knight(self.dimensions)
        self.moves = 1

    def get_dimensions(self):
        while True:
            board_dimensions = input('Enter your board dimensions: ').split()
            if len(board_dimensions) != 2:
                print('Invalid dimensions!')
                continue
            elif not (all(i.isdigit() for i in board_dimensions)):
                print('Invalid dimensions!')
                continue
            elif not (all(0<int(i) for i in board_dimensions)):
                print('Invalid dimensions!')
                continue
            else:
                board_dimensions = tuple(int(i) for i in board_dimensions)
                return board_dimensions
    def get_possible_movements(self,position=None):
        x, y = self.dimensions[0], self.dimensions[1]
        knight_pos = True
        x_knight, y_knight = self.knight.position[0], self.knight.position[1]
        if position is None:
            x_k, y_k = self.knight.position[0], self.knight.position[1]
            knight_pos = True
        else:
            x_k, y_k = position[0], position[1]
            knight_pos = False
        possible_movements = []
        if y_k+2<=y:
            if x_k+1<=x:
                if knight_pos ==False and x_k+1 == x_knight and y_k+2==y_knight:
                    pass
                else:
                    possible_movements.append([x_k+1, y_k+2])
            if x_k-1>=1:
                if knight_pos ==False and x_k-1== x_knight and y_k+2==y_knight:
                    pass
                else:
                    possible_movements.append([x_k-1, y_k+2])
        if y_k-2>=1:
            if x_k+1<=x:
                if knight_pos ==False and x_k+1== x_knight and y_k-2==y_knight:
                    pass
                else:
                    possible_movements.append([x_k+1, y_k-2])
            if x_k-1>=1:
                if knight_pos ==False and x_k-1== x_knight and y_k-2==y_knight:
                    pass
                else:
                    possible_movements.append([x_k-1, y_k-2])
        if x_k+2<=x:
            if y_k+1<=y:
                if knight_pos ==False and x_k+2== x_knight and y_k+1==y_knight:
                    pass
                else:
                    possible_movements.append([x_k+2, y_k+1])
            if y_k-1>=1:
                if knight_pos ==False and x_k+2== x_knight and y_k-1==y_knight:
                    pass
                else:
                    possible_movements.append([x_k+2, y_k-1])
        if x_k-2>=1:
            if y_k+1<=y:
                if knight_pos ==False and x_k-2== x_knight and y_k+1==y_knight:
                    pass
                else:
                    possible_movements.append([x_k-2, y_k+1])
            if y_k-1>=1:
                if knight_pos ==False and x_k-2== x_knight and y_k-1==y_knight:
                    pass
                else:
                    possible_movements.append([x_k-2, y_k-1])
        final = list(filter(lambda x:self.board[self.dimensions[1]-x[1],x[0]-1]!=-2,possible_movements))
        return final
    def get_board(self):
        board = np.array([i for i in self.board])
        knight_position = np.array([self.knight.position])-1


        knight_movements = np.array(self.get_possible_movements())-1

        for x in knight_position:
            board[self.dimensions[1]-x[1]-1,x[0]]=-1

        for o in knight_movements:
            d= len(self.get_possible_movements((o[0]+1,o[1]+1)))
            if d==0:
                board[self.dimensions[1]-o[1]-1,o[0]]=-3
            else:
                board[self.dimensions[1]-o[1]-1,o[0]]= len(self.get_possible_movements((o[0]+1,o[1]+1)))

        return board
    def move(self):
        while True:
            starting_position = input('Enter your next move: ').split()
            if len(starting_position) != 2:
                print('Invalid position!')
                continue
            elif not (all(i.isdigit() for i in starting_position)):
                print('Invalid move! ', end='')
                continue
            elif not (1 <= int(starting_position[0]) <= self.dimensions[0] and 1 <= int(starting_position[1]) <=
                      self.dimensions[1]):
                print('Invalid move! ', end='')
                continue


            elif self.board[self.dimensions[1]-int(starting_position[1]),int(starting_position[0])-1] == -2:
                print('Invalid position!')
                continue

            starting_position = [int(i) for i in starting_position]

            if not(starting_position in self.get_possible_movements()):
                print('Invalid move! ', end='')
                continue
            else:
                starting_position = tuple(int(i) for i in starting_position)
                self.board[self.dimensions[1] - self.knight.position[1] , self.knight.position[0] - 1] = -2
                self.knight.position = starting_position
                self.moves+=1
                break

    def draw_board(self):
        x,y = self.dimensions[0],self.dimensions[1]

        board = self.get_board()
        x_k , y_k = self.knight.position[0], self.knight.position[1]
        cell_size = len(str(x*y))
        cell =cell_size *'_'

        print('\nHere are the possible moves:')
        borders =f' {(x*(cell_size+1)+3)*"-"}'
        print(borders)
        y_rows = list(range(1, y+1))
        l = 0
        for i in y_rows[::-1]:
            number = ' ' * (len(str(y)) - len(str(i))) + str(i)
            begin_line =f"{number}| "
            print(begin_line, end='')
            for tile in board[l]:
                if tile ==0:
                    print(f"{cell+' '}",end='')
                elif tile == -1:
                    print(f"{(cell_size-1)*' '+'X '}",end='')
                elif tile ==-2:
                    print(f"{(cell_size - 1) * ' ' + '* '}", end='')
                elif tile ==-3:
                    print(f"{(cell_size - 1) * ' ' + '0 '}", end='')
                else:
                    print(f"{(cell_size-1)*' '+str(int(tile))+' '}",end='')
            print('|',end='\n')
            l+=1

        print(borders)
        print(f'{" " * (len(str(y)) + 1)}', end='')
        for i in range(1, x + 1):
            print(f"{(cell_size - len(str(i)) + 1) * ' '}" + f'{str(i)}', end='')
        print('\n')


class Knight:
    def __init__(self,dimensions):
        self.dimensions = dimensions
        self.position = np.array(self.get_starting_position())


    def get_starting_position(self):
        while True:
            starting_position = input('Enter the knight\'s starting position: ').split()
            if len(starting_position) != 2:
                print('Invalid position!')
                continue
            elif not (all(i.isdigit() for i in starting_position)):
                print('Invalid position!')
                continue
            elif not(1<=int(starting_position[0])<=self.dimensions[0] and 1<=int(starting_position[1])<=self.dimensions[1]):
                print('Invalid position!')
                continue
            else:
                starting_position = tuple(int(i) for i in starting_position)
                return starting_position


def controls(board):
    while True:
        time.sleep(0.01)
        try:
            if keyboard.read_key() == 'q':
                if 1<board.knight.position[0]:
                    board.knight.position = tuple([board.knight.position[0] - 1, board.knight.position[1]])
            elif keyboard.read_key() == 'd':
                if board.knight.position[0] < board.dimensions[0]:
                    board.knight.position = tuple([board.knight.position[0] + 1, board.knight.position[1]])
            elif keyboard.read_key() == 'z':
                    if board.knight.position[1]<board.dimensions[1]:
                        board.knight.position = tuple([board.knight.position[0], board.knight.position[1] + 1])
            elif keyboard.read_key() == 's':
                if 1<board.knight.position[1]:
                    board.knight.position = tuple([board.knight.position[0], board.knight.position[1] - 1])
            os.system("cls")
            board.draw_board()

        except:
            pass

def main():
    board= Board2()
    board.draw_board()
    while len(board.get_possible_movements())!=0:
        board.move()
        board.draw_board()

    if np.count_nonzero(board.board != -2)==1:
        print('What a great tour! Congratulations!')

    else:
        print('No more possible moves!')
        print(f'Your knight visited {board.moves} squares!')
    #controls(board)

if __name__=='__main__':
    main()