# Conway's Game of Life

A decently efficient version of the Game of Life written in Python (v3.10.4).

If you prefer a minimalist version without all the extra bells and whistles, see [ConwayTkLite](https://github.com/Skelt3r/conway-tk-lite).

## Controls

Clicking on a cell will toggle it's current state.  
All other functions are mapped to the hotkeys below and are also accessible through the menu bar.

| Function       | Hotkey |
| -------------- | ------ |
| Save Pattern   | Ctrl+S |
| Load Pattern   | Ctrl+L |
| Configure Game | Ctrl+F |
| Reset Board    | Ctrl+R |
| Clear Board    | Ctrl+C |
| Pause Game     | Space  |
| Exit Game      | Alt+F4 |

---

## Initializing

Run `py conwaytk.py` to launch with the default settings, or create your own instance:
```python
>>> from conwaytk import ConwayTk
>>> game = ConwayTk(columns=32,          # number of columns to generate
                    rows=24,             # number of rows to generate
                    interval=120,        # number of milliseconds between each life cycle
                    cell_size=1,         # number used for button scaling, accepts values of 1-10
                    live_color='orange'  # live cell color
                    dead_color='black'   # dead cell color
                    random=True)         # if True, randomly insert live cells into the data array
>>> game.run()
```

Settings can also be modified from the configuration menu within the app:  

![](https://github.com/Skelt3r/conway-tk/blob/main/screenshots/settings.png?raw=true)

Enjoy!  

![](https://github.com/Skelt3r/conway-tk/blob/main/screenshots/game-of-life.png?raw=true)
---

Inspired by [Joseph Bakulikira's](https://github.com/Josephbakulikira) [PyGame version](https://github.com/Josephbakulikira/Conway-s-Game-of-life---Python) of the Game of Life.
