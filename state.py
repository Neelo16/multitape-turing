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
        read = ''.join(read)
        reading = read
        for i in range(len(read)):
            for transition in self.transitions:
                if transition == reading:
                    transition = self.transitions[transition]
                    break
            else:
                reading = '*' * (i+1) + read[i+1:]
                continue
            break
        else:
            raise ValueError("Invalid read")
        for tape, movement,  symbol in zip(self.machine.tapes,
                                           transition.move,
                                           transition.write):
            if symbol != '*':
                tape.write(symbol)
            if movement == "l":
                tape.left()
            elif movement == "r":
                tape.right()
        if transition.new_state.startswith('halt'):
            self.machine.state = State(transition.new_state,
                                       self.machine,
                                       None)
        else:
            self.machine.state = self.machine.states[transition.new_state]
