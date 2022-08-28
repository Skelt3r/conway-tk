from pickle import dump, load
from random import randint
from rich import print
from tkinter import Button, Frame, IntVar, Label, Menu, OptionMenu, Spinbox, StringVar, Tk, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename


class ConwayTk:
    def __init__(self, columns: int=48, rows: int=24, interval: int=100, live_color: str='white', dead_color: str='black', random: bool=False):
        """
        Accept configuration settings and initialize base variables.

        columns : number of columns to generate
        rows : number of rows to generate
        interval : number of milliseconds between each life cycle
        random : if True, randomly insert live cells into the data array
        """
        self.rows = rows
        self.columns = columns
        self.interval = interval
        self.live_color = live_color
        self.dead_color = dead_color
        self.data_array = self.create_2d_array(random=random)
        self.button_array = self.create_2d_array(value=None)
        self.paused = True
        self.colors = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'lime green', 'cyan', 'magenta', 'purple', 'brown']
    

    def create_2d_array(self, value: None|int=0, random: bool=False):
        """
        Create a two-dimensional array. Randomly populate or insert a static value.

        value : value to insert into the array
        random : if True, randomly insert live cells into the data array
        """
        return [[value if not random else randint(0, 1) for _ in range(self.rows)] for _ in range(self.columns)]

    
    def loading_screen(self):
        """Display a loading message while generating the button grid."""

        loading = Label(self.root, font=('Calibri', 36), text='Loading...')
        loading.place(relx=0.45, rely=0.4)
        self.draw_grid()
        loading.after(100, loading.destroy)


    def draw_grid(self):
        """Draw a grid of Tkinter buttons on the screen."""

        for x in range(self.rows):
            for y in range(self.columns):
                if self.data_array[y][x] == 0:
                    button = Button(self.grid_frame, bg=self.dead_color)
                else:
                    button = Button(self.grid_frame, bg=self.live_color)

                button.config(height=2, width=4, bd=1, relief='solid', command=lambda x=x, y=y, b=button: self.click(x, y, b))
                button.grid(row=x, column=y)
                self.button_array[y][x] = button

    
    def get_neighbors(self, x: int, y: int):
        """
        Return the total number neighbors for the current x-y axis.

        x : the current x-axis index
        y : the current y-axis index
        """
        total = 0

        for m in range(-1, 2):
            for n in range(-1, 2):
                x_ = (x+m+self.rows) % self.rows
                y_ = (y+n+self.columns) % self.columns
                total += self.data_array[y_][x_]

        total -= self.data_array[y][x]
        return total
    

    def click(self, x: int, y: int, button: Button):
        """
        Toggle button state when clicked.

        x : the current x-axis index
        y : the current y-axis index
        button : the current Button widget
        """
        if button['bg'] == 'white':
            self.data_array[y][x] = 0
            button['bg'] = self.dead_color
        else:
            self.data_array[y][x] = 1
            button['bg'] = self.live_color
    

    def save_pattern(self):
        """Save the current pattern."""
        filename = asksaveasfilename(defaultextension='.dat', filetypes=[('DAT Files', '*.dat')], initialdir='./patterns')
        if filename != '':
            with open(filename, 'wb') as savefile:
                dump(self.data_array, savefile)


    def load_pattern(self):
        """Load a saved pattern."""
        filename = askopenfilename(filetypes=[('DAT Files', '*.dat')], initialdir='./patterns')
        if filename != '':
            with open(filename, 'rb') as loadfile:
                self.data_array = load(loadfile)
            self.root.destroy()
            self.paused = True
            self.run()


    def configure(self):
        """Configure the game parameters."""
        def apply():
            """Apply the current configuration settings and reboot the app."""
            self.rows = num_rows.get()
            self.columns = num_cols.get()
            self.interval = int_ms.get()
            self.live_color = live_color.get()
            self.dead_color = dead_color.get()
            self.root.destroy()
            self.__init__(self.columns, self.rows, self.interval, self.live_color, self.dead_color, True)
            self.run()

        win = Toplevel(self.root)
        win.title('Settings')

        rows_label = Label(win, text='Rows:')
        cols_label = Label(win, text='Columns:')
        interval_label = Label(win, text='Interval (ms):')
        live_color_label = Label(win, text='Live Cells:')
        dead_color_label = Label(win, text='Dead Cells:')

        num_rows = IntVar(win, 24)
        num_cols = IntVar(win, 48)
        int_ms = IntVar(win, 100)
        live_color = StringVar(win, self.live_color.title())
        dead_color = StringVar(win, self.dead_color.title())

        rows_box = Spinbox(win, textvariable=num_rows, from_=2, to=100)
        cols_box = Spinbox(win, textvariable=num_cols, from_=2, to=100)
        interval_box = Spinbox(win, textvariable=int_ms, from_=1, to=5000)
        live_color_menu = OptionMenu(win, live_color, *self.colors, command=lambda _: live_color.set(live_color.get().title()))
        dead_color_menu = OptionMenu(win, dead_color, *self.colors, command=lambda _: dead_color.set(dead_color.get().title()))

        apply_button = Button(win, text='Apply', command=apply)

        rows_label.grid(row=0, column=0)
        cols_label.grid(row=1, column=0)
        interval_label.grid(row=2, column=0)
        live_color_label.grid(row=3, column=0)
        dead_color_label.grid(row=4, column=0)
        rows_box.grid(row=0, column=1)
        cols_box.grid(row=1, column=1)
        interval_box.grid(row=2, column=1)
        live_color_menu.grid(row=3, column=1)
        dead_color_menu.grid(row=4, column=1)
        apply_button.grid(row=5, column=0, columnspan=2)


    def reset(self):
        """Randomize the state of the board."""
        self.root.destroy()
        self.paused = True
        self.data_array = self.create_2d_array(random=True)
        self.run()
    

    def clear(self):
        """Clear all live cells from the board."""
        self.root.destroy()
        self.paused = True
        self.data_array = self.create_2d_array(value=0)
        self.run()


    def pause(self):
        """Pause or unpause the game."""
        self.paused = not self.paused
        self.life(self.paused)


    def life(self, paused: bool):
        """
        Process the current life cycle and begin the next.

        paused : the current pause state
        """
        next_cycle = self.create_2d_array(value=0)

        if not paused:
            while True:
                for x in range(self.rows):
                    for y in range(self.columns):
                        state = self.data_array[y][x]
                        neighbors = self.get_neighbors(x, y)

                        if state == 0 and neighbors == 3:
                            self.button_array[y][x].config(bg=self.live_color)
                            next_cycle[y][x] = 1
                        elif state == 1 and (neighbors < 2 or neighbors > 3):
                            self.button_array[y][x].config(bg=self.dead_color)
                            next_cycle[y][x] = 0
                        else:
                            next_cycle[y][x] = state

                self.data_array = next_cycle
                self.root.after(self.interval, lambda: self.life(self.paused))

                if self.root.destroy:
                    return False


    def run(self):
        """Build the GUI and start the game."""

        self.root = Tk()
        self.root.title('Conway\'s Game of Life')
        
        self.bg_frame = Frame(self.root, bg='lightgrey')
        self.grid_frame = Frame(self.bg_frame)

        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Save Pattern', command=self.save_pattern, accelerator='|   S')
        self.file_menu.add_command(label='Load Pattern', command=self.load_pattern, accelerator='|   L')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Configure', command=self.configure, accelerator='|   F')
        self.file_menu.add_command(label='Pause', command=self.pause, accelerator='|   Space')
        self.file_menu.add_command(label='Reset', command=self.reset, accelerator='|   R')
        self.file_menu.add_command(label='Clear', command=self.clear, accelerator='|   C')

        self.bg_frame.pack(expand=True, fill='both')
        self.grid_frame.pack(side='top', anchor='c')

        self.loading_screen()
        self.life(self.paused)

        self.root.bind_all('<space>', lambda _: self.pause())
        self.root.bind_all('s', lambda _: self.save_pattern())
        self.root.bind_all('S', lambda _: self.save_pattern())
        self.root.bind_all('l', lambda _: self.load_pattern())
        self.root.bind_all('L', lambda _: self.load_pattern())
        self.root.bind_all('f', lambda _: self.configure())
        self.root.bind_all('F', lambda _: self.configure())
        self.root.bind_all('r', lambda _: self.reset())
        self.root.bind_all('R', lambda _: self.reset())
        self.root.bind_all('c', lambda _: self.clear())
        self.root.bind_all('C', lambda _: self.clear())

        self.root.focus_force()
        self.root.config(menu=self.menu_bar)
        self.root.mainloop()


if __name__ == '__main__':
    game = ConwayTk(random=True)
    game.run()
