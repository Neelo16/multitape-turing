try:
    from itertools import izip as zip  # Python 2
except ImportError:
    pass


class State:
    def __init__(self, name, machine, transitions):
        self.name = name
        self.machine = machine
        self.transitions = transitions

    def _traverse_transitions(self, read):
        result = None
        for transition in self.transitions:
            result = transition
            i = 0
            for did_read, should_read in zip(read, transition.read):
                i += 1
                if "*" != should_read != did_read:
                    result = None
                    break
            if result is not None:
                break
        if result is None:
            raise ValueError("Invalid transition: "
                             "read {} in state {}".format(read, self.name))
        return result

    def step(self):
        read = []
        for tape in self.machine.tapes:
            read.append(tape.read())
        transition = self._traverse_transitions(read)
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
