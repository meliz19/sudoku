#%%
import pandas as pd
import numpy as np 
import random
from copy import deepcopy

def check_col(col:int) -> int:
        if col<3:
            return 1
        elif col<6:
            return 2
        else:
            return 3
def get_box_no(row:int, col:int) -> int:
    if row<3:
        return check_col(col)
    elif row<6:
        return 3 + check_col(col)
    else:
        return 6 + check_col(col)

class ArrayToCell:
    def __init__(self):
        # self.matrix = [Cell(row=row, col=col, box_no=self.get_box_no(row,col)) for row in range(9) for col in range(9)]
        self.puzzle = SudokuPuzzle()
        self.sudoku_board = [Cell(row=row_idx, col=col_idx, box_no=get_box_no(row_idx,col_idx), value=value) for row_idx, row in enumerate(self.puzzle.matrix) for col_idx, value in enumerate(row)]

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
    
class SudokuSolution:
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

    def stack(self) -> None:
        row1 = np.hstack([self.boxes[1], self.boxes[2], self.boxes[3]])
        row2 = np.hstack([self.boxes[4], self.boxes[5], self.boxes[6]])
        row3 = np.hstack([self.boxes[7], self.boxes[8], self.boxes[9]])
        self.matrix = np.vstack([row1, row2, row3])

    def unstack(self) -> None:
        row1, row2, row3 = np.vsplit(self.matrix,3)
        self.boxes[1], self.boxes[2], self.boxes[3] = np.hsplit(row1, 3)
        self.boxes[4], self.boxes[5], self.boxes[6] = np.hsplit(row2, 3)
        self.boxes[7], self.boxes[8], self.boxes[9] = np.hsplit(row3, 3)

    def print_matrix(self, matrix=None) -> None:
        if matrix is None:
            matrix = self.matrix
        for idx, row in enumerate(matrix, start=1):
            string = f'{" ".join(str(x) for x in row[0:3]): ^8} | {" ".join(str(x) for x in row[3:6]): ^8} | {" ".join(str(x) for x in row[6:]): ^8}'
            print(string)
            
            if (idx==3) or (idx==6):
                print('|'.join(['-'*9, '-'*10, '-'*9]))

        print('\n')
    
    def export_matrix(self) -> None:
        pd.DataFrame(data=self.matrix).to_csv('sudoku-puzzle.csv', header=False, index=False)
    
    def row_col_add(self, box_no: int) -> tuple[int, int]:
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

    def assign_num_to_cell(self) -> None:
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

    def remove_dummies(self) -> None:
        # reset the matrix/boxes so that other num can use the 10-filled cells
        self.stack()
        self.matrix[self.matrix==10] = 0
        self.unstack()

    def pull_back(self) -> None:
        # reset boxes to previous num and start assignments again
        self.boxes = deepcopy(self.assignments[self.num-1])
        self.stack()
        return

    def box_assignments(self) -> None:
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
        # print(f'Solution:\n')
        # self.print_matrix()

    def hide_num(self, row_idx: int, col_idx: int, num: int) -> None:
        # hide num
        self.matrix[row_idx, col_idx] = -1 * num 
        self.unstack()

    def unhide_num(self, num: int) -> None:
        # unhide num
        self.matrix[self.matrix==-1*num] = num 
        self.unstack()

class SudokuPuzzle(SudokuSolution):
    def __init__(self):
        super().__init__()
        self.solution = deepcopy(self.matrix)
        self.puzzle = None

        self.create_puzzle()
        self.solve_puzzle()
        self.check_puzzle_solution()

    def check_index(self, idx: int) -> list[int]:
        if idx<3:
            return list(range(3))
        elif idx<6:
            return list(range(3,6))
        else:
            return list(range(6,9))

    def hide_num_across_board(self, num):
        num_coordinates = np.argwhere(self.matrix==num)
        hidden_coordinates = []
        while len(hidden_coordinates) < 3:
            row_indices = num_coordinates[:,0]
            col_indices = num_coordinates[:,1]  
            row_idx, col_idx = random.choice(num_coordinates)
            hidden_coordinates.append((row_idx, col_idx))

            self.hide_num(row_idx, col_idx, num)

            coordinates_to_drop = list(
                set(np.nonzero(np.isin(row_indices, self.check_index(row_idx)))[0]).union(
                    set(np.nonzero(np.isin(col_indices, self.check_index(col_idx)))[0]))
            )
            num_coordinates = np.delete(num_coordinates, coordinates_to_drop, axis=0)

    def create_puzzle(self):
        for num in range(1,10):
            self.hide_num_across_board(num)
        self.puzzle = deepcopy(self.matrix)

    # Solve the puzzle
    def solve_puzzle(self):
        hidden_values = np.argwhere(self.matrix<0)
        while hidden_values.size>1:
            for row_idx, col_idx in hidden_values:
                row = self.matrix[row_idx,:]
                col = self.matrix[:,col_idx]

                # box indicies
                box_row = self.check_index(row_idx)
                box_row_min = min(box_row)
                box_row_max = max(box_row) + 1

                box_col = self.check_index(col_idx)
                box_col_min = min(box_col)
                box_col_max = max(box_col) + 1

                box = self.matrix[box_row_min:box_row_max, box_col_min:box_col_max]

                # num to exclude for list of options (range(1,10))
                num_to_exclude = np.hstack([row[row>0],col[col>0], box[box>0]])
                num_options = np.setdiff1d(np.arange(1,10), num_to_exclude)

                if (num_options.size<2):
                    self.matrix[row_idx, col_idx] = num_options[0]

            hidden_values = np.argwhere(self.matrix<0)

    def check_puzzle_solution(self) -> str:
        while not np.array_equal(self.matrix, self.solution):
                self.create_puzzle()
                self.solve_puzzle()
        print('Puzzle Generated!')

puzzle = SudokuPuzzle()