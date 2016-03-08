## Multitape Turing Machine Simulator

Syntax inspired by http://morphett.info/turing/turing.html

Still a very early version. First line in input file must be the number of tapes.

So far, there is no GUI, and it can only be used in a terminal window.

Current output method is temporary and will get messed up if you make it write lines longer than the terminal's width.
It also only works well on Linux and (probably) Macs. If you're using Windows, you should probably comment out this line:
```python
print(reset_cursor, end='')
```
in __machine.py__ and replacing it with
```python
os.system('clear')
```
After adding
```python
import os
```
to the top of the file.

Simulation starts on state q0 and stops when a state starting with "halt" is reached.

# Usage
After cloning the repository, run the program with `python main.py FILE`, where _FILE_ is the path to a file containing the syntax read by the simulator. There are also optional arguments you can pass to the simulator, such as --step to make it run one step at a time (in fact, this is the only option implemented so far), asking you to press RETURN between transitions. You can check these options at any time by using the argument -h:
```
$ python main.py -h
usage: main.py [-h] [-v] [-s] file

Multitape Turing Machine Simulator

positional arguments:
  file

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -s, --step     enable step mode instead of running
```

# Syntax
Writing a program for this simulator is simple:
```
<state> <character read> <character written> <direction to move in the tape> <state to transition into>
```
Use `_` to represent spaces, and `*` instead of a character read to mean _any character_, or instead of a character written/direction to mean _no change_. Refer to the example programs provided with the source to clarify.
