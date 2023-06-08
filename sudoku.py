#%%
import pandas as pd
import numpy as np 
import random
from copy import deepcopy
    
class SudokuSolution:
    '''
    Create the solution to a valid Sudoku puzzle. 

    Attributes
    ----------
    boxes : dict
        A dictionary where the keys are the box numbers and the values are 3x3 numpy arrays. The box numbers range from 1 to 9. The numbering starts in the top, left quadrant and increases by one from left to right, top to bottom.

    matrix : np.array
        A 9x9 matrix of the form:
            boxes[1] | boxes[2] | boxes[3]
            ---------|----------|---------
            boxes[4] | boxes[5] | boxes[6]
            ---------|----------|---------
            boxes[7] | boxes[8] | boxes[9]


    Methods
    -------
    stack(): 
        Stacks the boxes such that a 9x9 matrix is generated with the form below (i.e., the matrix attribute).
                boxes[1] | boxes[2] | boxes[3]
                ---------|----------|---------
                boxes[4] | boxes[5] | boxes[6]
                ---------|----------|---------
                boxes[7] | boxes[8] | boxes[9]  
    
    unstack(): 
        Unstacks the matrix such that it is converted to a dictionary of boxes (i.e., the boxes attribute).

    print_matrix (matrix=None): 
        Prints the provided 9x9 numpy array to the command line in the form of a standard Sudoku board. If the matrix parameter is not given, the function will print the matrix attribute. 

    row_col_add(box_no): 
        Takes the box_no and returns a tuple of the form (row_add, col_add) containing values that should be added to the row index and column index, respectively, of the box (a 3x3 matrix) to account for the box's place in the 9x9 matrix. For example, the center coordintate for box number 6 has the coordinates (1,1) in the box form (a 3x3 matrix), whereas it will have the coordinates (1+3, 1+6) = (4,7) in the matrix form.

    assign_num_to_cell(available_indices, box_no, num): 
        Randomly selects a row and column index from the given available_indicies and assigns the given num to the selected row, column index. The box assignment is passed to the matrix attribute using the stack() method. Dummy values (10s) are assigned to the empty cells in the selected row and columns in the matrix to prevent an invalid number assignment. The dummy values are passed back to the box attribute using the unstack() method.   

    remove_dummies(): 
        Removes the dummies from the boxes and the matrix attributes that were assigned using the assign_num_to_cell() method.

    pull_back(num): 
        Resets the boxes and matrix attributes to the previous number iteration and starts the assignments again for the current number.
    
    box_assignments(): 
        Iterates through each possible number assignment (i.e., 1-9) and each box in boxes and assigns a number to each box until a valid Sudoku puzzle solution is generated.
    
    '''
    def __init__(self) -> None:
        self.boxes = {i:np.zeros((3,3), dtype=int) for i in range(1,10)}
        self.matrix = None
        self.assignments = {0: {i:np.zeros((3,3), dtype=int) for i in range(1,10)}}

        self.box_assignments()

    def stack(self) -> None:
        '''
        Stacks the boxes such that a 9x9 matrix is generated with the form below (i.e., the matrix attribute).
            boxes[1] | boxes[2] | boxes[3]
            ---------|----------|---------
            boxes[4] | boxes[5] | boxes[6]
            ---------|----------|---------
            boxes[7] | boxes[8] | boxes[9]
        
        Returns
        -------
        None
        '''
        row1 = np.hstack([self.boxes[1], self.boxes[2], self.boxes[3]])
        row2 = np.hstack([self.boxes[4], self.boxes[5], self.boxes[6]])
        row3 = np.hstack([self.boxes[7], self.boxes[8], self.boxes[9]])
        self.matrix = np.vstack([row1, row2, row3])

    def unstack(self) -> None:
        '''
        Unstacks the matrix such that it is converted to a dictionary of boxes (i.e., the boxes attribute).
        
        Returns
        -------
        None
        '''
        row1, row2, row3 = np.vsplit(self.matrix,3)
        self.boxes[1], self.boxes[2], self.boxes[3] = np.hsplit(row1, 3)
        self.boxes[4], self.boxes[5], self.boxes[6] = np.hsplit(row2, 3)
        self.boxes[7], self.boxes[8], self.boxes[9] = np.hsplit(row3, 3)

    def print_matrix(self, matrix: np.array = None) -> None:
        '''
        Prints the provided 9x9 numpy array to the command line in the form of a standard Sudoku board. If the matrix parameter is not given, the function will print the matrix attribute.

        Parameters
        ----------
        matrix : np.array, optional
            A 9x9 numpy array

        Returns 
        -------
        None
        '''
        if matrix is None:
            matrix = self.matrix
        for idx, row in enumerate(matrix, start=1):
            string = f'{" ".join(str(x) for x in row[0:3]): ^8} | {" ".join(str(x) for x in row[3:6]): ^8} | {" ".join(str(x) for x in row[6:]): ^8}'
            print(string)
            
            if (idx==3) or (idx==6):
                print('|'.join(['-'*9, '-'*10, '-'*9]))

        print('\n')
    
    def row_col_add(self, box_no: int) -> tuple[int, int]:
        '''
        Takes the box_no and returns a tuple of the form (row_add, col_add) containing values that should be added to the row index and column index, respectively, of the box (a 3x3 matrix) to account for the box's place in the 9x9 matrix. For example, the center coordintate for box number 6 has the coordinates (1,1) in the box form (a 3x3 matrix), whereas it will have the coordinates (1+3, 1+6) = (4,7) in the matrix form.

        Parameters
        ----------
        box_no : int
            The current box that has a number being assigned to it.
        
        Returns
        -------
        A tuple of the form row_add (int), col_add (int).
        '''
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

    def assign_num_to_cell(self, available_indices: np.array, box_no: int, num: int) -> None:
        '''
        Randomly selects a row and column index from the given available_indicies and assigns the given num to the selected row, column index. The box assignment is passed to the matrix attribute using the stack() method. Dummy values (10s) are assigned to the empty cells in the selected row and columns in the matrix to prevent an invalid number assignment. The dummy values are passed back to the box attribute using the unstack() method.

        Parameters
        ----------
        available_indices : np.array
            An Nx2 np.array with the available indicies for where a given num can be assigned in the 9x9 matrix.
        
        box_no : int
            The current box that has a number being assigned to it.

        num : int
            The current number being assigned coordinates within a box/the matrix.

        Return
        ------
        None
        
        '''
        # randomly chosen index
        row_idx, col_idx = random.choice(available_indices)
        
        # assign num to cell
        self.boxes[box_no][row_idx, col_idx] = num

        # stack the boxes into a matrix
        self.stack()

        # update randomly chosen index to get matrix index
        row_add, col_add = self.row_col_add(box_no)
        row_idx+= row_add
        col_idx+= col_add

        # rows & col no longer available to current num
        row = self.matrix[row_idx,:]
        row[row==0]=10

        col = self.matrix[:,col_idx]
        col[col==0]=10

        self.unstack()

    def remove_dummies(self) -> None:
        '''
        Removes the dummies from the boxes and the matrix attributes that were assigned using the assign_num_to_cell() method.
        
        Return
        ------
        None
        '''
        self.stack()
        self.matrix[self.matrix==10] = 0
        self.unstack()

    def pull_back(self, num: int) -> None:
        '''
        Resets the boxes and matrix attributes to the previous number iteration and starts the assignments again for the current number.
        
        Parameter
        ---------
        num : int
            The current number being assigned coordinates within a box/the matrix.

        Return
        ------
        None
        '''
        self.boxes = deepcopy(self.assignments[num-1])
        self.stack()
        return

    def box_assignments(self) -> None:
        '''
        Iterates through each possible number assignment (i.e., 1-9) and each box in boxes and assigns a number to each box until a valid Sudoku puzzle solution is generated.
        
        Return
        ------
        None
        '''
        num = 1
        box_no = 1
        while num<10:
            while box_no<10:
                box = self.boxes[box_no]
                available_indices = np.argwhere(box==0)

                if available_indices.size > 0:
                    self.assign_num_to_cell(available_indices, box_no, num)
                    box_no+=1

                else:
                    # reset boxes to previous num and start assignments again
                    num = max(1, num-1)
                    box_no = 1
                    self.pull_back(num)

            self.remove_dummies()

            self.assignments[num] = deepcopy(self.boxes)

            num+=1
            box_no=1

class SudokuPuzzle(SudokuSolution):
    '''
    Creates a valid puzzle based on the solution generated by the SudokuSolution class. 

    Attributes
    ----------
    solution : np.array
        The final, filled in 9x9 matrix generated by the SudokuSolution class. 

    puzzle : np.array
        The final 9x9 matrix-form of the Sudoku puzzle (i.e., the solution matrix with hidden values).

    puzzle_boxes : dict
        The final dictionary-form of the Sudoku puzzle (i.e., contains hidden values).

    Methods
    -------
    other_indices_in_box(idx): 
        Takes the given index and returns a list of indices (integers) that are also within that box. For example, if 7 is the given index (either row or column), the other indicies in that box are 6 and 8. 
    
    hide_num(row_idx, col_idx, num):
        Hides the num (by negating it) at coordinates row_idx, col_idx in the 9x9 matrix.
    
    unhide_nums(num):
        Unhides all the negated num's in the 9x9 matrix by setting them back to the (positive) num value.
    
    hide_num_across_board(num):
        Applies a simple algorithm to hide 3 instances of the given num across the matrix.
    
    create_puzzle():
        Iterates through each possible number (1-9) and runs the hide_num_across_board() method on each number. Assigns the final solution to the puzzle attribute (i.e., the 9x9 matrix-form of the Sudoku puzzle) and the box attribute (i.e., the dictionary-form of the Sudoku puzzle).

    solve_puzzle():
        Applies a simple algorithm to solve the created puzzle.

    check_puzzle_solution():
        Regenerates a Sudoku puzzle until the solve_puzzle solution matches the solution generated by the SudokuSolution class.
    '''
    def __init__(self):
        super().__init__()
        self.solution = deepcopy(self.matrix)
        self.puzzle = None
        self.puzzle_boxes = None

        self.create_puzzle()
        self.solve_puzzle()
        self.check_puzzle_solution()

    def other_indices_in_box(self, idx: int) -> list[int, int, int]:
        '''
        Takes the given index and returns a list of indices (integers) that are also within that box. For example, if 7 is the given index (either row or column), the other indicies in that box are 6 and 8. 

        Parameters
        ----------
        idx : int
            An index of the matrix attribute. Range: [0,9).

        Return
        ------
        A list of 3 integers.
        '''
        if idx<3:
            return list(range(3))
        elif idx<6:
            return list(range(3,6))
        else:
            return list(range(6,9))

    def hide_num(self, row_idx: int, col_idx: int, num: int) -> None:
        '''
        Hides the num (by negating it) at coordinates row_idx, col_idx in the 9x9 matrix.

        Parameters
        ----------
        row_idx : int
            A row index of the matrix attribute. Range: [0,9).
        
        col_idx : int
            A column index of the matrix attribute. Range: [0,9).
        
        num : int
            The current number being hidden. Range: [1,9].

        Return
        ------
        None
        '''
        self.matrix[row_idx, col_idx] = -1 * num 
        self.unstack()

    def unhide_nums(self, num: int) -> None:
        '''
        Unhides all the negated num's in the 9x9 matrix by setting them back to the (positive) num value.

        Parameters
        ----------
        
        num : int
            The current number being unhidden. Range: [1,9].

        Return
        ------
        None
        '''
        self.matrix[self.matrix==-1*num] = num 
        self.unstack()

    def hide_num_across_board(self, num):
        '''
        Applies a simple algorithm to hide 3 instances of the given num across the matrix.

        Parameters
        ----------
        
        num : int
            The current number being unhidden. Range: [1,9].

        Return
        ------
        None
        '''
        num_coordinates = np.argwhere(self.matrix==num)
        hidden_coordinates = []
        while len(hidden_coordinates) < 3:
            row_indices = num_coordinates[:,0]
            col_indices = num_coordinates[:,1]  
            row_idx, col_idx = random.choice(num_coordinates)
            hidden_coordinates.append((row_idx, col_idx))

            self.hide_num(row_idx, col_idx, num)

            coordinates_to_drop = list(
                set(np.nonzero(np.isin(row_indices, self.other_indices_in_box(row_idx)))[0]).union(
                    set(np.nonzero(np.isin(col_indices, self.other_indices_in_box(col_idx)))[0]))
            )
            num_coordinates = np.delete(num_coordinates, coordinates_to_drop, axis=0)

    def create_puzzle(self):
        '''
        Iterates through each possible number (1-9) and runs the hide_num_across_board() method on each number. Assigns the final solution to the puzzle attribute (i.e., the 9x9 matrix-form of the Sudoku puzzle) and the box attribute (i.e., the dictionary-form of the Sudoku puzzle).

        Parameters
        ----------
        None

        Return
        ------
        None
        '''
        for num in range(1,10):
            self.hide_num_across_board(num)
        self.puzzle = deepcopy(self.matrix)

        self.unstack()
        self.puzzle_boxes = deepcopy(self.boxes)

    def solve_puzzle(self):
        '''
        Applies a simple algorithm to solve the created puzzle.

        Parameters
        ----------
        None

        Return
        ------
        None
        '''
        hidden_values = np.argwhere(self.matrix<0)
        while hidden_values.size>1:
            for row_idx, col_idx in hidden_values:
                row = self.matrix[row_idx,:]
                col = self.matrix[:,col_idx]

                # box indicies
                box_row = self.other_indices_in_box(row_idx)
                box_row_min = min(box_row)
                box_row_max = max(box_row) + 1

                box_col = self.other_indices_in_box(col_idx)
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
        '''
        Regenerates a Sudoku puzzle until the solve_puzzle solution matches the solution generated by the SudokuSolution class.

        Parameters
        ----------
        None

        Return
        ------
        None
        '''
        while not np.array_equal(self.matrix, self.solution):
                self.create_puzzle()
                self.solve_puzzle()
