from random import randint
from tkinter import Button, Frame, Label, Menu, Tk


class ConwayTk:
    def __init__(self, columns: int=48, rows: int=24, interval: int=100, random: bool=False):
        """
        Initialize base variables.

        columns : number of columns to generate
        rows : number of rows to generate
        interval : number of milliseconds between each life cycle
        random : if True, randomly insert live cells into the data array
        """
        self.rows = rows
        self.columns = columns
        self.interval = interval
        self.data_array = self.create_2d_array(random=random)
        self.button_array = self.create_2d_array(value=None)
        self.paused = True
    

    def create_2d_array(self, value: None|int=0, random: bool=False):
        """
        Create a two-dimensional array.

        value : value to insert into the array
        random : if True, randomly insert live cells into the data array
        """
        return [[value if not random else randint(0, 1) for _ in range(self.rows)] for _ in range(self.columns)]


    def draw_grid(self):
        """Draw a grid of Tkinter buttons on the screen."""

        for x in range(self.rows):
            for y in range(self.columns):
                if self.data_array[y][x] == 0:
                    button = Button(self.grid_frame, bg='black')
                else:
                    button = Button(self.grid_frame, bg='white')

                button.config(height=2, width=4, bd=1, relief='solid', command=lambda x=x, y=y, b=button: self.click(x, y, b))
                button.grid(row=x, column=y)
                self.button_array[y][x] = button

    
    def get_neighbors(self, x: int, y: int):
        """
        Return the total number neighbors to the current x-y axis.

        x : the current x-axis integer
        y : the current y-axis integer
        """
        total = 0

        for m in range(-1, 2):
            for n in range(-1, 2):
                _x = (x+m+self.rows) % self.rows
                _y = (y+n+self.columns) % self.columns
                total += self.data_array[_y][_x]

        total -= self.data_array[y][x]
        return total
    

    def click(self, x: int, y: int, button: Button):
        """
        Toggle button state when clicked.

        x : the current x-axis integer
        y : the current y-axis integer
        button : the current Button widget
        """
        if button['bg'] == 'white':
            self.data_array[y][x] = 0
            button['bg'] = 'black'
        else:
            self.data_array[y][x] = 1
            button['bg'] = 'white'
    

    def save_pattern(self):
        """Save the current pattern."""


    def load_pattern(self):
        """Load a saved pattern."""


    def configure(self):
        """Configure the game parameters."""
    

    def pause(self):
        """Pause or unpause the game."""
        self.paused = not self.paused
        self.life(self.paused)


    def life(self, paused: bool):
        """
        Process the current life cycle and begin the next.

        paused : the current pause state
        """
        next = self.create_2d_array(value=0)

        if not paused:
            while True:
                for x in range(self.rows):
                    for y in range(self.columns):
                        state = self.data_array[y][x]
                        neighbors = self.get_neighbors(x, y)

                        if state == 0 and neighbors == 3:
                            self.button_array[y][x].config(bg='white')
                            next[y][x] = 1
                        elif state == 1 and (neighbors < 2 or neighbors > 3):
                            self.button_array[y][x].config(bg='black')
                            next[y][x] = 0
                        else:
                            next[y][x] = state

                self.data_array = next
                self.root.after(self.interval, lambda: self.life(self.paused))

                if self.root.destroy:
                    return False


    def run(self):
        """Build the GUI and start the game."""

        self.root = Tk()
        self.root.title('Conway\'s Game of Life')
        self.root.geometry('1920x1080')
        
        self.bg_frame = Frame(self.root, bg='lightgrey')
        self.grid_frame = Frame(self.bg_frame)

        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Save Pattern', command=None, accelerator='|   S')
        self.file_menu.add_command(label='Load Pattern', command=None, accelerator='|   L')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Pause', command=self.pause, accelerator='|   Space')
        self.file_menu.add_command(label='Reset', command=self.pause, accelerator='|   R')
        self.file_menu.add_command(label='Configure', command=None, accelerator='|   C')

        self.bg_frame.pack(expand=True, fill='both')
        self.grid_frame.pack(side='top', anchor='c', padx=5, pady=20)

        self.draw_grid()
        self.life(self.paused)

        self.root.bind_all('<space>', lambda _: self.pause())
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()


if __name__ == '__main__':
    game = ConwayTk(random=True)
    game.run()
