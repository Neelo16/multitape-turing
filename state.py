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
import non_deterministic


class State:
    def __init__(self, name, machine, transitions):
        self.name = name
        self.machine = machine
        self.transitions = transitions

    def _traverse_transitions(self, read):
        valid_transitions = []
        for transition in self.transitions:
            for did_read, should_read in zip(read, transition.read):
                if "*" != should_read != did_read:
                    break
            else:
                valid_transitions.append(transition)
                if self.machine.is_deterministic:
                    break
        if len(valid_transitions) == 0:
            raise ValueError("Invalid transition: "
                             "read {} in state {}".format(read, self.name))

        return valid_transitions

    def step(self, transition=None):
        if transition is None:
            read = []
            for tape in self.machine.tapes:
                read.append(tape.read())
            transition = self._traverse_transitions(read)
            if not self.machine.is_deterministic and len(transition) > 0:
                remaining_transitions = transition[1:]
                non_deterministic.register_choices(self.machine,
                                                   remaining_transitions)
            transition = transition[0]
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
        self.machine.traversed_transitions.append(transition)
