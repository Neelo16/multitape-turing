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
from collections import deque

tasks = deque()


def register_choices(machine, transitions):
    for transition in transitions:
        new_machine = machine.copy()
        tasks.append((new_machine, transition))


def get_final_path(initial_machine):
    machine = initial_machine
    transition = None
    is_halted = False
    while not is_halted:
        machine.step(transition=transition)
        is_halted = machine.state.name.startswith('halt')
        if is_halted and machine.state.name == 'halt-accept':
            break
        if tasks:
            if not is_halted:
                tasks.append((machine, None))
            else:
                is_halted = False
            machine, transition = tasks.popleft()
    return machine
