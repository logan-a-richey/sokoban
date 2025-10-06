# Sokoban
## About
Work in progress implementation the puzzle game, Sokoban.

![Screenshot](screenshots/sokoban_screenshot.png)

## How to play
* The objective is to push all of the red spheres onto the green squares.
* Select a level with the **Levelset** and **Level** dropdown menus.
* Move the player with the `WASD` keys. 
* `CTRL Z` for undo move, `CTRL Y` for redo move, 
* `CTRL -` for zoom out, `CTRL +` for zoom in.
* `CTRL N` for level reset.

## Features
* Perl to parse level data and store it via a `.json` data structure.
* Persistent level progress via a `.json` config file.
* Simple GUI in `Tkinter`.
* Over 1000 levels included from the Sasquatch and Microban levelsets

## Todo
* I plan to refactor all the core game logic using `PerlTK` as a learning exercise.
* Web version
* C++ SDL version with `wxWidgets` 
* AI solver in C++, Perl, or Python

# License

MIT License (MIT)

Copyright (c) 2025 LoganARichey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


