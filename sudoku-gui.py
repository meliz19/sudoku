import ttkbootstrap as ttk
from sudoku import Boxes

class SudokuBoard(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill='both', expand=True)

        self.create_board(master=self)
    
    def create_board(self, master, bootstyle='dark', padx=0, pady=0):
        '''create_board = vstack the boxes
        '''
        puzzle = Boxes()

        row1 = ttk.Frame(master=master, bootstyle=bootstyle)
        row1.pack(fill='both', expand=True, padx=padx, pady=pady)

        self.hstack_boxes(row_container=row1, matrix_row_contents=[
            puzzle.boxes[1], puzzle.boxes[2], puzzle.boxes[3]])

        row2 = ttk.Frame(master=master, bootstyle=bootstyle)
        row2.pack(fill='both', expand=True, padx=padx, pady=pady)
        self.hstack_boxes(row_container=row2, matrix_row_contents=[
           puzzle.boxes[4], puzzle.boxes[5], puzzle.boxes[6]])

        row3 = ttk.Frame(master=master, bootstyle=bootstyle)
        row3.pack(fill='both', expand=True, padx=padx, pady=pady)
        self.hstack_boxes(row_container=row3, matrix_row_contents=[
          puzzle.boxes[7], puzzle.boxes[8], puzzle.boxes[9]])
    
    def hstack_boxes(self, row_container, matrix_row_contents, padx=1, pady=1):
        col1 = ttk.Frame(master=row_container)
        col1.pack(side='left', fill='both', expand=True, padx=padx, pady=pady)
        self.create_box(col_container=col1, box_text=matrix_row_contents[0])

        col2 = ttk.Frame(master=row_container)
        col2.pack(side='left', fill='both', expand=True, padx=padx, pady=pady)
        self.create_box(col_container=col2, box_text=matrix_row_contents[1])

        col3 = ttk.Frame(master=row_container)
        col3.pack(side='left', fill='both', expand=True, padx=padx, pady=pady)
        self.create_box(col_container=col3, box_text=matrix_row_contents[2])

    def create_box(self, col_container, box_text):
        box = ttk.Frame(master=col_container)
        box.pack(fill='both', expand=True)

        self.create_box_row(box_container=box, row_text=box_text[0])
        self.create_box_row(box_container=box, row_text=box_text[1])
        self.create_box_row(box_container=box, row_text=box_text[2])

    def create_box_row(self, box_container, row_text, bootstyle='dark', padx=1, pady=1):
        row = ttk.Frame(master=box_container, bootstyle=bootstyle)
        row.pack(fill='both', expand=True)

        left = ttk.Label(master=row, text=row_text[0], anchor='center')
        left.pack(side='left', fill='both', expand=True, padx=padx, pady=pady)

        center = ttk.Label(master=row, text=row_text[1], anchor='center')
        center.pack(side='left', fill='both', expand=True, padx=padx, pady=pady)

        right = ttk.Label(master=row, text=row_text[2], anchor='center')
        right.pack(side='left', fill='both', expand=True, padx=padx, pady=pady)

class App(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill='both', expand=True)
    
        left_container = ttk.Frame(master=self)
        left_container.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        SudokuBoard(left_container)

        right_container = ttk.Frame(master=self)
        right_container.pack(fill='both', expand=True)

        self.settings_controls(container=right_container)

    def settings_controls(self, container, padx=5, pady=5):
        hint_toolbtn = ttk.Checkbutton(master=container, text='Hint', bootstyle='default-round-toggle')
        hint_toolbtn.pack(padx=padx, pady=pady)

        reset_board_btn = ttk.Button(master=container, text='Reset Board', bootstyle='danger')
        reset_board_btn.pack(padx=padx, pady=pady)

        new_puzzle_btn = ttk.Button(master=container, text='Generate New Puzzle', bootstyle='warning')
        new_puzzle_btn.pack(padx=padx, pady=pady)

        submit_btn = ttk.Button(master=container, text='Submit', bootstyle='success')
        submit_btn.pack(padx=padx, pady=pady)

if __name__=='__main__':
    app = ttk.Window(title='Sudoku')
    App(app)
    app.mainloop()