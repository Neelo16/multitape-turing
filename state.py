try:
    from itertools import izip as zip  # Python 2
except ImportError:
    pass


class State:
    def __init__(self, name, machine, transitions):
        self.name = name
        self.machine = machine
        self.transitions = transitions

    def step(self):
        read = []
        for tape in self.machine.tapes:
            read.append(tape.read())
        transition = self.transitions
        for character in read:
            try:
                transition = transition[character]
            except KeyError:
                transition = transition['*']
        for tape, movement,  symbol in zip(self.machine.tapes,
                                           transition.move,
                                           transition.write):
            if symbol != '*':
                tape.write(symbol)
            if movement == "l":
                tape.left()
            elif movement == "r":
                tape.right()
        self.machine.state = self.machine.states[transition.new_state]
