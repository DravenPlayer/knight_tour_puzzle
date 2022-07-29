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
    def __init__(self,dimensions=None, knight_pos=None):
        if dimensions is None:
            self.dimensions = self.get_dimensions()
        else :
            self.dimensions = dimensions
        self.board = np.zeros((self.dimensions[1], self.dimensions[0]))
        self.board_plan = []
        if knight_pos is None:
            self.knight = Knight(self.dimensions)
        else :
            self.knight = Knight(self.dimensions,knight_pos)
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
        self.board_plan = np.copy(board)
        for o in knight_movements:
            d= len(self.get_possible_movements((o[0]+1,o[1]+1)))
            if d==0:
                board[self.dimensions[1]-o[1]-1,o[0]]=-3
            else:
                board[self.dimensions[1]-o[1]-1,o[0]]= len(self.get_possible_movements((o[0]+1,o[1]+1)))

        return board
    def move(self, position=None):

        while True:
            if position is None:
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


                elif self.board[self.dimensions[1] - int(starting_position[1]), int(starting_position[0]) - 1] == -2:
                    print('Invalid position!')
                    continue

                starting_position = [int(i) for i in starting_position]

                if not (starting_position in self.get_possible_movements()):
                    print('Invalid move! ', end='')
                    continue
                else:
                    starting_position = tuple(int(i) for i in starting_position)
                    self.board[self.dimensions[1] - self.knight.position[1], self.knight.position[0] - 1] = -2
                    self.knight.position = starting_position
                    self.moves += 1
                    break
            else:
                starting_position = position

                self.board[self.dimensions[1] - self.knight.position[1], self.knight.position[0] - 1] = -2
                self.knight.position = starting_position.copy()
                self.moves += 1
                break

    def draw_board(self, final=False):
        x,y = self.dimensions[0],self.dimensions[1]
        if final ==False:
            board = self.get_board()
        else:
            board= self.board

        x_k , y_k = self.knight.position[0], self.knight.position[1]
        cell_size = len(str(x*y))
        cell =cell_size *'_'

        #print('\nHere are the possible moves:')
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
                    print(f"{(cell_size-len(str(int(tile))))*' '+str(int(tile))+' '}",end='')
            print('|',end='\n')
            l+=1

        print(borders)
        print(f'{" " * (len(str(y)) + 1)}', end='')
        for i in range(1, x + 1):
            print(f"{(cell_size - len(str(i)) + 1) * ' '}" + f'{str(i)}', end='')
        print('\n')


class Knight:
    def __init__(self,dimensions, position=None):
        self.dimensions = dimensions
        if position is None:
            self.position = np.array(self.get_starting_position())
        else:
            self.position = position


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
def solver(dimensions, knight_pos, animation = False, dur = 0.006):
    board = Board2(dimensions, knight_pos) #backend
    front_end = np.zeros((dimensions[1],dimensions[0]))
    knight_pos = np.array(knight_pos) - 1
    front_end[dimensions[1] - knight_pos[1] - 1, knight_pos[0]] = 1
    if animation:
        os.system("cls")
        board.draw_board()
        time.sleep(dur)

    try:
        for i in range(2, dimensions[0] * dimensions[1]+1):
            if animation:
                board.draw_board()
                time.sleep(dur)
            '''
            board.draw_board()
            time.sleep(1)
            print(front_end)
            '''
            possible_movements = [np.array(i) for i in board.get_possible_movements()]
            len_possible_movements = [len(np.array(board.get_possible_movements(i))) for i in possible_movements]

            minimum = 0
            for j in range(len(possible_movements)):
                if len_possible_movements[j] < len_possible_movements[minimum]:
                    minimum = j
            #print(possible_movements)
            #print(len_possible_movements)
            if len_possible_movements[minimum]==0:
                if len(possible_movements)>1:
                    board.move(possible_movements[minimum+1])
                '''
                except Exception as r:
                    if np.count_nonzero(board.board != -2) == 1:
                        front_end[dimensions[1] - knight_pos[1] - 1, knight_pos[0]] = i
                    return (board.moves,board,front_end)
                '''

            board.move(possible_movements[minimum])
            knight_pos = np.array(board.knight.position) - 1
            front_end[dimensions[1] - knight_pos[1] - 1, knight_pos[0]] = i

    except Exception as r:

        return (board.moves,board,front_end)
    else:

        return (board.moves,board,front_end)

    '''
    knight_pos = np.array(knight_pos)-1
    x_k , y_k=  dimensions[1]-knight_pos[1]-1, dimensions[0]-1
    board_s = np.zeros((dimensions))
    board_s[x_k,y_k]=-1
    '''

def main():
    board= Board2()
    knight_position = board.knight.position
    while True:
        answer = input('Do you want to try the puzzle? (y/n): ')
        if answer in ['y' , 'n']:
            break
        else:
            print('Invalid input!')
    check = solver(board.dimensions, knight_position, animation=False)
    check[1].board = check[2]
    if answer =='y':

        if np.count_nonzero(check[1] ==0) ==0 and check[1].moves == board.dimensions[0]*board.dimensions[1]:
            board = Board2(board.dimensions, knight_position)
            board.draw_board()
            while len(board.get_possible_movements()) != 0:
                board.move()
                board.draw_board()

            if np.count_nonzero(board.board != -2) == 1:
                print('What a great tour! Congratulations!')

            else:
                print('No more possible moves!')
                print(f'Your knight visited {board.moves} squares!')
        else:
            print('No solution exists!')
    else :
        if np.count_nonzero(check[1].board ==0) == 0 and check[1].moves == board.dimensions[0]*board.dimensions[1]:
            print('Here\'s the solution!')
            check[1].draw_board(True)
        else:
            print('No solution exists!')




    #controls(board)

if __name__=='__main__':
    main()


#Fixing ideas :
#seperate every method : input and existing variable
#every method must do one thing and only one thing
#





