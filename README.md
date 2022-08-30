# Conway's Game of Life

A decently efficient version of the Game of Life written in Python v3.10.4.

## Hotkeys
Save Pattern   : Ctrl+S  
Load Pattern   : Ctrl+L  
Configure Game : Ctrl+F  
Reset Board    : Ctrl+R  
Clear Board    : Ctrl+C  
Pause Game     : Space  
Exit Game      : Alt+F4  

---

## Initializing

```python
game = ConwayTk(columns=36,          # number of columns to generate
                rows=24,             # number of rows to generate
                interval=120,        # number of milliseconds between each life cycle
                button_size=1,       # number used for button scaling, accepts values of 1-10
                live_color='Orange'  # live cell color
                dead_color='Black'   # dead cell color
                random=True)         # if True, randomly insert live cells into the data array            
game.run()
```

---

Inspired by [Joseph Bakulikira's](https://github.com/Josephbakulikira) [PyGame version](https://github.com/Josephbakulikira/Conway-s-Game-of-life---Python) of the Game of Life.
