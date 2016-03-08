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
        for transition in self.transitions:
            for read, should_read in zip(read, transition.read):
                if should_read == '*':
                    continue
                elif should_read != read:
                    break
            else:
                break
        else:
            raise ValueError("Invalid transition: "
                             "read {} in state {}".format(read, self.name))
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
