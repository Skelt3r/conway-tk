from random import randint
from tkinter import Button, Tk


class ConwayTk:
    def __init__(self, rows: int=32, columns: int=16, interval: int=100, random: bool=False):
        self.rows = rows
        self.columns = columns
        self.interval = interval
        self.data_array = self.create_2d_array(random=random)
        self.button_array = self.create_2d_array(value=None)
        self.paused = True
    

    def create_2d_array(self, value: None|int=0, random: bool=False):
        if random:
            return [[randint(0, 1) for _ in range(self.rows)] for _ in range(self.columns)]
        else:
            return [[value for _ in range(self.rows)] for _ in range(self.columns)]


    def draw_grid(self):
        for y in range(self.columns):
            for x in range(self.rows):
                if self.data_array[y][x] == 0:
                    button = Button(self.root, bg='black')
                else:
                    button = Button(self.root, bg='white')

                button.config(height=2, width=4, bd=1, relief='solid', command=lambda x=x, y=y, b=button: self.click(x, y, b))
                button.grid(row=y, column=x)
                self.button_array[y][x] = button

    
    def get_neighbors(self, x: int, y: int):
        total = 0

        for n in range(-1, 2):
            for m in range(-1, 2):
                _x = (x+m+self.rows) % self.rows
                _y = (y+n+self.columns) % self.columns
                total += self.data_array[_y][_x]

        total -= self.data_array[y][x]
        return total
    

    def click(self, x: int, y: int, button: Button):
        if button['bg'] == 'white':
            self.data_array[y][x] = 0
            button['bg'] = 'black'
        else:
            self.data_array[y][x] = 1
            button['bg'] = 'white'
    

    def pause(self):
        self.paused = not self.paused
        self.life(self.paused)


    def life(self, paused: bool):
        next = self.create_2d_array(value=0)

        if not paused:
            while True:
                for y in range(self.columns):
                    for x in range(self.rows):
                        state = self.data_array[y][x]
                        neighbors = self.get_neighbors(x, y)

                        if state == 0 and neighbors == 3:
                            next[y][x] = 1
                            self.button_array[y][x].config(bg='white')
                        elif state == 1 and (neighbors < 2 or neighbors > 3):
                            next[y][x] = 0
                            self.button_array[y][x].config(bg='black')
                        else:
                            next[y][x] = state

                self.data_array = next
                self.root.after(self.interval, lambda: self.life(self.paused))

                if self.root.destroy:
                    return False


    def run(self):
        self.root = Tk()
        self.root.title('Conway\'s Game of Life')
        self.root.bind_all('<space>', lambda _: self.pause())
        self.draw_grid()
        self.life(self.paused)
        self.root.mainloop()


if __name__ == '__main__':
    game = ConwayTk(random=True)
    game.run()
