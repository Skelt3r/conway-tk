from pickle import dump, load
from random import randint
from tkinter import Button, Frame, IntVar, Label, Menu, OptionMenu, Spinbox, StringVar, Tk, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename


class ConwayTk:
    def __init__(self, columns: int=32, rows: int=24, interval: int=120, live_color: str='White', dead_color: str='Black', random: bool=False):
        """
        Accept configuration settings and initialize base variables.

        columns : number of columns to generate
        rows : number of rows to generate
        interval : number of milliseconds between each life cycle
        live_color : color of live cells
        dead_color : color of dead cells
        random : if True, randomly insert live cells into the data array
        """
        try:
            with open('./settings.dat', 'rb') as file:
                self.settings = load(file)
        except FileNotFoundError:
            self.settings = {'rows': rows, 'columns': columns, 'interval': interval, 'live': live_color, 'dead': dead_color}

        self.rows = self.settings['rows']
        self.columns = self.settings['columns']
        self.interval = self.settings['interval']
        self.live_color = self.settings['live']
        self.dead_color = self.settings['dead']
        self.data_array = self.create_2d_array(random=random)
        self.button_array = self.create_2d_array(value=None)
        self.colors = ['Black', 'White', 'Red', 'Green', 'Blue', 'Yellow', 'Lime Green', 'Cyan', 'Magenta', 'Purple', 'Orange', 'Brown', 'Grey']
        self.paused = True


    def create_2d_array(self, value: None|int=0, random: bool=False):
        """
        Create a two-dimensional array. Randomly populate or insert a static value.

        value : value to insert into the array
        random : if True, randomly insert live cells into the data array
        """
        return [[value if not random else randint(0, 1) for _ in range(self.rows)] for _ in range(self.columns)]


    def draw_grid(self):
        """Display a loading message while drawing a grid of Tkinter buttons on the screen."""

        loading = Label(self.root, font=('Calibri', 36), text='Loading...')
        loading.place(relx=0.45, rely=0.4)
        
        for x in range(self.rows):
            for y in range(self.columns):
                if self.data_array[y][x] == 0:
                    button = Button(self.grid_frame, bg=self.dead_color)
                else:
                    button = Button(self.grid_frame, bg=self.live_color)

                button.config(height=2, width=4, bd=1, relief='solid', command=lambda x=x, y=y, b=button: self.click(x, y, b))
                button.grid(row=x, column=y)
                self.button_array[y][x] = button
        
        loading.after(100, loading.destroy)

    
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
        if button['bg'] == self.live_color:
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

        def save_config():
            """Save the current configuration settings and reboot the app."""
            self.settings['rows'] = num_rows.get()
            self.settings['columns'] = num_cols.get()
            self.settings['interval'] = int_ms.get()
            self.settings['live'] = live_color.get()
            self.settings['dead'] = dead_color.get()
            with open('./settings.dat', 'wb') as file:
                dump(self.settings, file)
            self.root.destroy()
            self.__init__(random=True)
            self.run()

        
        if self.config_win.winfo_exists():
            self.config_win.destroy()
        else:
            self.config_win = Toplevel(self.root)
            self.config_win.title('Settings')
            self.config_win.resizable(0, 0)
            self.config_win.wm_attributes('-toolwindow', True)

            rows_label = Label(self.config_win, text='Rows:')
            cols_label = Label(self.config_win, text='Columns:')
            interval_label = Label(self.config_win, text='Interval (ms):')
            live_color_label = Label(self.config_win, text='Live Cells:')
            dead_color_label = Label(self.config_win, text='Dead Cells:')

            num_rows = IntVar(self.config_win, self.rows)
            num_cols = IntVar(self.config_win, self.columns)
            int_ms = IntVar(self.config_win, self.interval)
            live_color = StringVar(self.config_win, self.live_color)
            dead_color = StringVar(self.config_win, self.dead_color)

            rows_box = Spinbox(self.config_win, textvariable=num_rows, from_=2, to=100, justify='center', width=12)
            cols_box = Spinbox(self.config_win, textvariable=num_cols, from_=2, to=100, justify='center', width=12)
            interval_box = Spinbox(self.config_win, textvariable=int_ms, from_=1, to=5000, justify='center', width=12)
            live_color_menu = OptionMenu(self.config_win, live_color, *self.colors, command=lambda _: live_color.set(live_color.get()))
            dead_color_menu = OptionMenu(self.config_win, dead_color, *self.colors, command=lambda _: dead_color.set(dead_color.get()))
            live_color_menu.config(bg='white', relief='sunken', width=10)
            dead_color_menu.config(bg='white', relief='sunken', width=10)

            save_button = Button(self.config_win, text='Save', command=save_config)
            cancel_button = Button(self.config_win, text='Cancel', command=self.config_win.destroy)

            rows_label.grid(row=0, column=0, padx=1, pady=1, sticky='e')
            cols_label.grid(row=1, column=0, padx=1, pady=1, sticky='e')
            interval_label.grid(row=2, column=0, padx=1, pady=1, sticky='e')
            live_color_label.grid(row=3, column=0, padx=1, pady=1, sticky='e')
            dead_color_label.grid(row=4, column=0, padx=1, pady=1, sticky='e')
            rows_box.grid(row=0, column=1, pady=1, sticky='w')
            cols_box.grid(row=1, column=1, pady=1, sticky='w')
            interval_box.grid(row=2, column=1, pady=1, sticky='w')
            live_color_menu.grid(row=3, column=1, pady=1, sticky='w')
            dead_color_menu.grid(row=4, column=1, pady=1, sticky='w')
            save_button.grid(row=5, column=0, pady=5, sticky='e')
            cancel_button.grid(row=5, column=1, padx=10, pady=5, sticky='w')


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
        self.root.resizable(0, 0)
        
        self.bg_frame = Frame(self.root, bg='lightgrey')
        self.grid_frame = Frame(self.bg_frame)

        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.control_menu = Menu(self.menu_bar, tearoff=0)

        self.config_win = Toplevel(self.root)
        self.config_win.destroy()

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label='Control', menu=self.control_menu)
        self.file_menu.add_command(label='Save Pattern', command=self.save_pattern, accelerator='|   S')
        self.file_menu.add_command(label='Load Pattern', command=self.load_pattern, accelerator='|   L')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Configure', command=self.configure, accelerator='|   F')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.destroy, accelerator='|   Alt+F4')
        self.control_menu.add_command(label='Pause', command=self.pause, accelerator='|   Space')
        self.control_menu.add_command(label='Reset', command=self.reset, accelerator='|   R')
        self.control_menu.add_command(label='Clear', command=self.clear, accelerator='|   C')

        self.bg_frame.pack(expand=True, fill='both')
        self.grid_frame.pack(side='top', anchor='c')

        self.draw_grid()
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
