from __future__ import print_function

try:
    range = xrange  # Python 2
except NameError:
    pass

import time  # sleep
from tape import Tape
from state import State


class Machine:
    def __init__(self, initial_state, states, num_tapes=1):
        self.tapes = [Tape() for i in range(num_tapes)]
        self.tapes[0] = Tape(list('101101'))
        self.states = dict()
        for state, transitions in states.items():
            new_state = State(state, self, transitions)
            self.states[state] = new_state
        self.state = self.states[initial_state]
        self.run()

    def run(self):
        self.show()
        reset_cursor = "\033[F" * (len(self.tapes)*2)
        while not self.state.name.startswith('halt'):
            time.sleep(0.05)
            self.state.step()
            print(reset_cursor, end='')
            self.show()
        print("Final state: {}".format(self.state.name))

    def show(self):
        for tape in self.tapes:
            print(tape)
            print(' '*tape.pointer, '^', ' '*(len(tape)-tape.pointer), sep='')
