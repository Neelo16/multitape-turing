## Multitape Turing Machine Simulator

Syntax inspired by http://morphett.info/turing/turing.html

Still a very early version. Input and options must be entered directly in the code, but base functionality is already implemented.

Comments in simulator programs are not implemented yet.

Current output method is temporary and will get messed up if you make it write lines longer than the terminal's width.

Simulation starts on state q0 and stops when a state starting with "halt" is reached. For now, you must declare that state even if it does nothing, for example:

```
halt-accept * * * halt-accept
halt-reject * * * halt-reject
```

