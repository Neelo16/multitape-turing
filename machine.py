'''
    This file is part of Multitape-Turing.

    Multitape-Turing is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Multitape-Turing is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Multitape-Turing.  If not, see <http://www.gnu.org/licenses/>.

'''
import time  # sleep
import itertools  # repeat
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

    def run(self, step=False, path=None):
        self.show()
        reset_cursor = "\033[F" * (len(self.tapes)*2 + 1 + (1 if step else 0))
        if path is None:
            path = itertools.repeat(None)
        for transition in path:
            self.delay(step)
            self.step(transition)
            print(reset_cursor, end='')
            self.show()
            if transition is None and self.state.name.startswith('halt'):
                break
        print("Final state: {}".format(self.state.name))

    def delay(self, step):
        if step:
            input('Press RETURN to step')
        else:
            time.sleep(0.05)

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
