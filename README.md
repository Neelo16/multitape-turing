## Multitape (Deterministic/Non-deterministic) Turing Machine Simulator

Syntax inspired by http://morphett.info/turing/turing.html

This simulator allows you to write simple specifications for Turing Machines, which can optionally be non-deterministic. See __Usage__ and __Syntax__ below for more information.

Python 3 is required to run this simulator.

Still an early version. First line in input file must be the number of tapes.

So far, there is no GUI, and it can only be used in a terminal window.

Current output method is temporary and will get messed up if you make it write lines longer than the terminal's width.
It also only works well on Linux and (probably) Macs. If you're using Windows, you should probably comment out this line:
```python
print(reset_cursor, end='')
```
in __machine.py__ and replace it with
```python
os.system('cls')
```
After adding
```python
import os
```
to the top of the file.

Simulation starts on state q0 and stops when a state starting with "halt" is reached.
If using a non-deterministic machine, the accept state should be called "halt-accept", so it can know when to stop.

# Usage
After cloning the repository, run the program with `python main.py FILE`, where _FILE_ is the path to a file containing the syntax read by the simulator. There are also optional arguments you can pass to the simulator, such as --step to make it run one step at a time, asking you to press RETURN between transitions. You can check these options at any time by using the argument -h:
```
$ python3 main.py

usage: main.py [-h] [-v] [-s] [-nd] [-sc] FILE

Multitape Turing Machine Simulator

positional arguments:
  FILE                  path to program

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s, --step            enable step mode instead of running
  -nd, --non-deterministic
                        simulate a non-deterministic Turing Machine
  -sc, --skip-calculations
                        only show the final path in a non-deterministic
                        machine
```

By default, if you have two transitions for the same input, only the first one will be considered; to change this, use the `--non-deterministic` flag to make it go through all possible paths until it either exhausts all paths or accepts the input given. If the `-sc` flag is not provided, output will seem strange during calculation as it will constantly jump around states until it finds the (shortest) path to halt-accept. At the end, if it reached halt-accept, the program asks if you'd like to see it traverse through the found path. Alternatively, if you run it with the `--skip-calculations` argument, it will only display the final path. 

# Syntax
Writing a program for this simulator is simple:
```
<state> <character read> <character written> <direction to move in the tape> <state to transition into>
```
Use `_` to represent spaces, and `*` instead of a character read to mean _any character_, or instead of a character written/direction to mean _no change_. Refer to the example programs provided with the source to clarify.
