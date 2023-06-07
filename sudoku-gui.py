import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import numpy as np
from sudoku import SudokuPuzzle

class SudokuBoard(ttk.Frame):
    '''
    This class creates the Sudoku board (i.e., a 9x9 matrix) within the GUI.
    
    Attributes
    ----------
    boxes : dict
        A dictionary with keys 1-9 that correspond to the "boxes" in the matrix. The numbers 
    hidden_ent : list
    hidden_solution : list

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
    
    def create_board(self, master, padx=0, pady=0):
        '''create_board = vstack the boxes
        '''
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(master=master, highlightbackground='black', highlightthickness=1)
                frame.grid(row=i, column=j, padx=padx, pady=pady)
                box_no = self.get_box_no(row=i, col=j)
                self.create_box(
                    container=frame,
                    box_text=self.boxes[box_no]
                )

    def create_box(self, container, box_text):
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

    def check_col(self, col:int) -> int:
            if col<1:
                return 1
            elif col<2:
                return 2
            else:
                return 3
    def get_box_no(self, row:int, col:int) -> int:
        if row<1:
            return self.check_col(col)
        elif row<2:
            return 3 + self.check_col(col)
        else:
            return 6 + self.check_col(col)
    
    def check_value(self, value):
        if value == '':
            return True
        elif value.isdigit():
            if (int(value) > 0) and (int(value) < 10):
                return True
            else:
                return False
        else:
            return False

class App(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill='both', expand=True)

        self.hint_var = ttk.IntVar()
        self.sudoku_puzzle = SudokuPuzzle(); self.sudoku_puzzle.print_matrix()
        self.sudoku_board = None

        self.left_container = ttk.Frame(master=self)
        self.left_container.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.assemble_sudoku_board()

        right_container = ttk.Frame(master=self)
        right_container.pack(fill='both', expand=True)
        self.settings_controls(container=right_container)
    
    def assemble_sudoku_board(self):
        self.inside_left_container = ttk.Frame(master=self.left_container)
        self.inside_left_container.pack(fill='both', expand=True)
        self.sudoku_board = SudokuBoard(self.inside_left_container, self.sudoku_puzzle.puzzle_boxes)
        
    def settings_controls(self, container, padx=5, pady=5):
        # hint_toolbtn = ttk.Checkbutton(master=container, text='Hint', variable=self.hint_var, bootstyle='default-round-toggle', command=self.on_hint)
        # hint_toolbtn.pack(padx=padx, pady=pady)

        reset_board_btn = ttk.Button(master=container, text='Reset Board', bootstyle='danger', command=self.reset_board)
        reset_board_btn.pack(padx=padx, pady=pady)

        new_puzzle_btn = ttk.Button(master=container, text='Generate New Puzzle', bootstyle='warning', command=self.generate_new_puzzle)
        new_puzzle_btn.pack(padx=padx, pady=pady)

        submit_btn = ttk.Button(master=container, text='Submit', bootstyle='success', command=self.on_submit)
        submit_btn.pack(padx=padx, pady=pady)

    # def on_hint(self):
    #     if self.hint_var.get()==1:
    #         print('hint==ON')
    #     else:
    #         print('hint==OFF')
        #     if ent != cell_solution:
        #         ent.config(bordercolor='red')
        #     elif ent == '':
        #         ent.config(bordercolor='default')
    
    def reset_board(self):
        for ent in self.sudoku_board.hidden_ent:
            ent.delete(0, 'end')
    
    def generate_new_puzzle(self):
        self.inside_left_container.pack_forget()
        self.sudoku_puzzle = SudokuPuzzle()
        self.assemble_sudoku_board()
    
    def on_submit(self):
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
            message = 'Uh-Oh. It looks like you need to try again.' # If you need a hint, turn the Hint button on.'
            Messagebox.ok(message=message, title='Try Again.')

if __name__=='__main__':
    app = ttk.Window(title='Sudoku')
    App(app)
    app.mainloop()