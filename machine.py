import time  # sleep
from tape import Tape
from state import State


class Machine:
    def __init__(self,
                 initial_state,
                 states, tapes=[Tape()],
                 is_deterministic=True):
        self.tapes = tapes
        self.is_deterministic = is_deterministic
        self.states = dict()
        for state, transitions in states.items():
            new_state = State(state, self, transitions)
            self.states[state] = new_state
        self.state = self.states[initial_state]
        self.traversed_transitions = []

    def run(self, step=False):
        self.show()
        reset_cursor = "\033[F" * (len(self.tapes)*2 + 1 + (1 if step else 0))
        while not self.state.name.startswith('halt'):
            if step:
                input('Press RETURN to step')
            else:
                time.sleep(0.05)
            self.step()
            print(reset_cursor, end='')
            self.show()
        print("Final state: {}".format(self.state.name))

    def step(self, transition=None):
        self.state.step(transition)

    def show(self):
        for tape in self.tapes:
            print(tape)
            print(' '*tape.pointer, '^', ' '*(len(tape)-tape.pointer), sep='')
        print("Current state:", self.state.name)

    def clear_output(self, step):
        reset_cursor = "\033[F" * (len(self.tapes)*2 + 1 + (1 if step else 0))
        print(reset_cursor, end='')
        for tape in self.tapes:
            print(' ' * len(tape))
            print(' ' * len(tape))
        print(' '*(len("Current state: " + self.state.name)))
        if step:
            print(' '*len('Press RETURN to step'))
        print(reset_cursor, end='')

    def copy(self):
        copied_tapes = []
        copied_states = {}
        for tape in self.tapes:
            copied_tapes.append(tape.copy())
        for name, state in self.states.items():
            copied_states[name] = state.transitions
        new_machine = Machine(self.state.name,
                              copied_states,
                              copied_tapes,
                              self.is_deterministic)
        new_machine.traversed_transitions = list(self.traversed_transitions)
        return new_machine
