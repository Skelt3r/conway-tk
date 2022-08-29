# Conway's Game of Life

A decently efficient version of the Game of Life written in Python v3.10.4.

## Hotkeys
Save Pattern   : S  
Load Pattern   : L  
Configure Game : F  
Pause Game     : Space  
Reset Board    : R  
Clear Board    : C  

---

## Initializing

```python
game = ConwayTk(columns=36,         # number of columns to generate
                rows=24,            # number of rows to generate
                interval=120,       # number of milliseconds between each life cycle
                live_color='Orange'  # live cell color
                dead_color='Black'  # dead cell color
                random=True)        # if True, randomly insert live cells into the data array            
game.run()
```

---

Inspired by [Joseph Bakulikira's](https://github.com/Josephbakulikira) [PyGame version](https://github.com/Josephbakulikira/Conway-s-Game-of-life---Python) of the Game of Life.
