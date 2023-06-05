#%%
import pandas as pd
import numpy as np 
import random
from copy import deepcopy

class ArrayToCell:
    def __init__(self):
        # self.matrix = [Cell(row=row, col=col, box_no=self.get_box_no(row,col)) for row in range(9) for col in range(9)]
        self.puzzle = SudokuPuzzle()
        self.sudoku_board = [Cell(row=row_idx, col=col_idx, box_no=self.get_box_no(row_idx,col_idx), value=value) for row_idx, row in enumerate(self.puzzle.matrix) for col_idx, value in enumerate(row)]

    def check_col(self, col:int) -> int:
        if col<3:
            return 1
        elif col<6:
            return 2
        else:
            return 3
    def get_box_no(self, row:int, col:int) -> int:
        if row<3:
            return self.check_col(col)
        elif row<6:
            return 3 + self.check_col(col)
        else:
            return 6 + self.check_col(col)

class Cell:
    def __init__(self, row: int, col: int, box_no: int, value: int = 0, guesses: list[int] = None, hidden: bool = False, helper:bool = False) -> None:
        self.row = row
        self.col = col
        self.value = value
        self.box_no = box_no
        self.hidden = hidden
        self.guesses = guesses
        self.helper = helper

    def get_coordinates(self):
        return (self.row,self.col)
    
    def get_value(self):
        return self.value
    
    def get_box_no(self):
        return self.box_no
    
class SudokuPuzzle:
    def __init__(self) -> None:
        self.boxes = {i:np.zeros((3,3), dtype=int) for i in range(1,10)}
        self.matrix = None
        self.assignments = {i:None for i in range(0,10)}
        self.assignments[0] = {i:np.zeros((3,3), dtype=int) for i in range(1,10)}

        self.num = 1
        self.box_no = 1
        self.max_range = 2
        self.available_indices = None

        self.box_assignments()

    def stack(self):
        row1 = np.hstack([self.boxes[1], self.boxes[2], self.boxes[3]])
        row2 = np.hstack([self.boxes[4], self.boxes[5], self.boxes[6]])
        row3 = np.hstack([self.boxes[7], self.boxes[8], self.boxes[9]])
        self.matrix = np.vstack([row1, row2, row3])

    def unstack(self):
        row1, row2, row3 = np.vsplit(self.matrix,3)
        self.boxes[1], self.boxes[2], self.boxes[3] = np.hsplit(row1, 3)
        self.boxes[4], self.boxes[5], self.boxes[6] = np.hsplit(row2, 3)
        self.boxes[7], self.boxes[8], self.boxes[9] = np.hsplit(row3, 3)

    def print_matrix(self):
        for idx, row in enumerate(self.matrix, start=1):
            string = f'{" ".join(str(x) for x in row[0:3]): ^8} | {" ".join(str(x) for x in row[3:6]): ^8} | {" ".join(str(x) for x in row[6:]): ^8}'
            print(string)
            
            if (idx==3) or (idx==6):
                print('|'.join(['-'*9, '-'*10, '-'*9]))

        print('\n')
    
    def export_matrix(self):
        pd.DataFrame(data=self.matrix).to_csv('sudoku-puzzle.csv', header=False, index=False)
    
    def row_col_add(self, box_no):
        # amount to add to box index to get matrix index
        row_add = 0; col_add = 0
        if box_no in [2,5,8]:
            col_add = 3
        elif box_no in [3,6,9]:
            col_add = 6

        if box_no in range(4,7):
            row_add = 3
        elif box_no in range(7,10):
            row_add = 6
        
        return row_add, col_add

    def assign_num_to_cell(self):
        # randomly chosen index
        row_idx, col_idx = random.choice(self.available_indices)
        
        # assign num to cell
        self.boxes[self.box_no][row_idx, col_idx] = self.num

        # stack the boxes into a matrix
        self.stack()

        # update randomly chosen index to get matrix index
        row_add, col_add = self.row_col_add(self.box_no)
        row_idx+= row_add
        col_idx+= col_add

        # rows & col no longer available to current num
        row = self.matrix[row_idx,:]
        row[row==0]=10

        col = self.matrix[:,col_idx]
        col[col==0]=10

        self.unstack()

    def remove_dummies(self):
        # reset the matrix/boxes so that other num can use the 10-filled cells
        self.stack()
        self.matrix[self.matrix==10] = 0
        self.unstack()

    def pull_back(self):
        # reset boxes to previous num and start assignments again
        self.boxes = deepcopy(self.assignments[self.num-1])
        self.stack()
        return

    def box_assignments(self):
        while self.num<10:
            while self.box_no<10:
                box = self.boxes[self.box_no]

                self.available_indices = np.argwhere(box==0)

                if self.available_indices.size > 0:
                    self.assign_num_to_cell()
                    self.box_no+=1

                else:
                    # reset boxes to previous num and start assignments again
                    self.num = max(1, self.num-1)
                    self.box_no = 1
                    self.pull_back()

            self.remove_dummies()

            self.assignments[self.num] = deepcopy(self.boxes)

            self.num+=1
            self.box_no=1
       
        # final product
        self.print_matrix()

# Boxes().export_matrix()
# %%
# # Available values in each row/col
# row_values = {idx:list(range(1,10)) for idx in range(9)}
# col_values = {idx:list(range(1,10)) for idx in range(9)}
# box_values = {idx:list(range(1,10)) for idx in range(9)}



#     def print(self):
#         print(f'Box: {self.box}\nCell: ({self.row, self.col})\nValue: {self.value}')

# class Suduko:
#     def __init__(self):

#         # Indices Per Box
#         matrix_idx = np.arange(9).reshape(3,3)

#         unique_combinations = []
#         for i in range(3):
#             for j in range(3):
#                 unique_combinations.append((matrix_idx[i], matrix_idx[j]))

#         boxes={box:indices for box,indices in enumerate(unique_combinations)}
#         box_indices = {}
#         for box_no, (row_indices, col_indices) in boxes.items():
#             box_indices[box_no] = [(row, col) for row in row_indices for col in col_indices]
#             # print(f'box_no: {box_no}\trow: {row_indices}\tcol: {col_indices}')
#         # print(box_indices)

#         cells = {}
#         for box_no, indices in box_indices.items():
#             for row,col in indices:
#                 cells[(row, col)] = Cell()
#                 cells[(row, col)].row = row
#                 cells[(row, col)].col = col
#                 cells[(row, col)].box = box_no

#                 available_values = (
#                     set(box_values[box_no])
#                         .intersection(set(row_values[row]))
#                         .intersection(set(col_values[col]))
#                 )
#                 cells[(row, col)].value = random.choice(available_values)

