import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import numpy as np
from sudoku import SudokuPuzzle

class SudokuBoard(ttk.Frame):
    '''
    This class creates the Sudoku board (i.e., a 9x9 matrix) within a frame of the GUI.
    
    Attributes
    ----------
    boxes : dict
        A dictionary where the keys are the box numbers and the values are 3x3 numpy arrays. The box numbers range from 1 to 9. The numbering starts in the top, left quadrant and increases by one from left to right, top to bottom.

    hidden_ent : list
        A list of the enabled entries (i.e., the hidden values in the Sudoku puzzle) in the Sudoku board.
    
    hidden_solution : list
        A list of the negated hidden values in the Sudoku puzzle.

    ent_validation : tuple
        A tuple of the registered validation callback (check_value) and the substitution code (%P in this case, which indiciates that input to the check_value function will be the value of the text if keystroke is allowed.).
    
    Methods
    -------
    create_board(master):
        Vertically stacks rows of 3 boxes into the master frame. A box is a 3x3 matrix of ttkbootstrap entries.
    
    create_box(container, box_text):
        Creates a 3x3 matrix of ttkbootstrap entries. If the puzzle value is visible on the board, the entry is configured to the disabled state. If the puzzle value is hidden on the board, the entry is left in the configured state to allow for user input.

    get_box_no(col):
        Takes a row and col index in the range [0,2] and returns the box number in the range 1-9. The box numbering starts in the top, left quadrant and increases by one from left to right, top to bottom.

    check_value(cell_value):
        Validates the user Ttkbootstrap Entry's cell_value and ensures that only integers between 1 and 9 are allowed.

    '''
    def __init__(self, master, boxes, **kwargs):
        super().__init__(master, **kwargs)
        self.grid()

        self.boxes = boxes
        self.hidden_ent = []
        self.hidden_solution = []

        # register the validation callback
        self.ent_validation = (app.register(self.check_value), '%P')
        
        self.create_board(master=self)
    
    def create_board(self, master: ttk.Frame) -> None:
        '''
        Vertically stacks rows of 3 boxes into the master frame. A box is a 3x3 matrix of ttkbootstrap entries.

        Parameter
        ---------
        master : ttk.Frame
            The master frame for the board.

        Return
        ------
        None
        '''
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(master=master, highlightbackground='black', highlightthickness=1)
                frame.grid(row=i, column=j)
                box_no = self.get_box_no(row=i, col=j)
                self.create_box(
                    container=frame,
                    box_text=self.boxes[box_no]
                )

    def create_box(self, container: ttk.Frame, box_text: np.array) -> None:
        '''
        Creates a 3x3 matrix of ttkbootstrap entries. If the puzzle value is visible on the board, the entry is configured to the disabled state. If the puzzle value is hidden on the board, the entry is left in the configured state to allow for user input.

        Parameters
        ----------
        container : ttk.Frame
            The master frame for the box.
        
        box_text : np.array
            A 3x3 np.array that contains both the hidden and visible puzzle values. 

        Return
        ------
        None
        '''
        for i in range(box_text.shape[0]):
            for j in range(box_text.shape[1]):
                cell_value = '' if box_text[i][j] < 0 else box_text[i][j]
                ent = ttk.Entry(master=container, width=2)
                ent.grid(row=i, column=j)
                ent.insert('end', cell_value)
                if cell_value != '':
                    ent.configure(state='disabled')
                else:
                    ent.config(validate='key', validatecommand=self.ent_validation)
                    self.hidden_ent.append(ent)
                    self.hidden_solution.append(-1*box_text[i][j])

    def get_box_no(self, row:int, col:int) -> int:
        '''
        Takes the row and col index of a box and returns the box number. The box numbers range from 1 to 9. Numbering starts in the top, left quadrant and increases by one from left to right, top to bottom.

        Parameters
        ----------
        row : int
            The row index of the box.
        
        col : int
            The column index of the box.
        
        Return
        ------
        box_no : int
            The box number, which ranges from 1 to 9.
        '''
        return (row * 3) + (col + 1)
    
    def check_value(self, cell_value: str) -> bool:
        '''
        Validates the user Ttkbootstrap entries and ensures that only integers between 1 and 9 and empty string values are allowed.

        Parameters
        ----------
        cell_value : str
            The value entered into the cell, aka Ttkbootstrap Entry.  
        
        Returns
        -------
        A boolean value. The function returns True if the value is allowed and False otherwise. 

        '''
        if cell_value == '':
            return True
        elif cell_value.isdigit():
            if (int(cell_value) > 0) and (int(cell_value) < 10):
                return True
            else:
                return False
        else:
            return False

class App(ttk.Frame):
    '''
    This class generates the main window that a user sees when the app is opened/this file is run. The window contains two containers, a left container that holds the Sudoku board, and the right container that holds the menu buttons.

    Attributes
    ----------
    sudoku_puzzle : SudokuPuzzle 
        A SudokuPuzzle class object.
    
    sudoku_board : ttk.Frame
        The ttk.Frame that contains the board that is generated from the SudokuBoard class.
    
    left_container(master) : ttk.Frame
        This ttk.Frame that contains the sudoku_board object.
    
    right_container(master) : ttk.Frame
        This ttk.Frame that contains the menu buttons.

    Methods
    -------
    assemble_sudoku_board():
        Inserts the SudokuBoard class object into the left_container of the main window.

    settings_controls(container):
        Inserts the menu board buttons into the container of the main window.
    
    reset_board():
        Clears the board of all user input.
    
    generate_new_puzzle():
        Generates a new Sudoku puzzle.
    
    check_solution():
        Checks the user's inputs against the puzzle's solution.
    '''
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill='both', expand=True)

        self.sudoku_puzzle = SudokuPuzzle()
        self.sudoku_board = None

        self.left_container = ttk.Frame(master=self)
        self.left_container.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        self.assemble_sudoku_board()

        right_container = ttk.Frame(master=self)
        right_container.pack(fill='both', expand=True)
        self.settings_controls(container=right_container)
    
    def assemble_sudoku_board(self) -> None:
        '''Inserts the SudokuBoard class object into the left_container of the main window.'''
        self.inside_left_container = ttk.Frame(master=self.left_container)
        self.inside_left_container.pack(fill='both', expand=True)
        self.sudoku_board = SudokuBoard(self.inside_left_container, self.sudoku_puzzle.puzzle_boxes)
        
    def settings_controls(self, container: ttk.Frame, padx: int =5, pady: int =5) -> None:
        '''Inserts the menu board buttons into the container of the main window.'''
        reset_board_btn = ttk.Button(master=container, text='Reset Board', bootstyle='danger', command=self.reset_board)
        reset_board_btn.pack(padx=padx, pady=pady)

        new_puzzle_btn = ttk.Button(master=container, text='Generate New Puzzle', bootstyle='warning', command=self.generate_new_puzzle)
        new_puzzle_btn.pack(padx=padx, pady=pady)

        check_soln_btn = ttk.Button(master=container, text='Check Solution', bootstyle='success', command=self.check_solution)
        check_soln_btn.pack(padx=padx, pady=pady)
    
    def reset_board(self) -> None:
        '''Clears the board of all user input.'''
        for ent in self.sudoku_board.hidden_ent:
            ent.delete(0, 'end')
    
    def generate_new_puzzle(self) -> None:
        '''Generates a new Sudoku puzzle.'''
        self.inside_left_container.pack_forget()
        self.sudoku_puzzle = SudokuPuzzle()
        self.assemble_sudoku_board()
    
    def check_solution(self) -> None:
        '''Checks the user's inputs against the puzzle's solution.'''
        user_input = []
        for ent in self.sudoku_board.hidden_ent:
            if ent.get() == '':
                message = "Uh-oh. It looks like you're not done yet. You must fill in all the empty boxes with a number 1-9 before you can check your solution."
                Messagebox.ok(message=message, title='Finish puzzle to check solution.')
                return
            else:
                user_input.append(int(ent.get()))
        if np.array_equal(user_input, self.sudoku_board.hidden_solution):
            message = 'You Won!\n\nWould you like to play again?'
            msg_box = Messagebox.yesno(message=message, title='Congrats, you won!')
            if msg_box=='No':
                self.quit()
            else:
                self.generate_new_puzzle()
        else:
            message = 'Uh-Oh. It looks like you need to try again.'
            Messagebox.ok(message=message, title='Try Again.')

if __name__=='__main__':
    app = ttk.Window(title="Let's Play Sudoku!")
    App(app)
    app.mainloop()