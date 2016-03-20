#!/usr/bin/env python3
'''
    This file is part of Multitape-Turing.

    Multitape-Turing is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

'''

import re
import os    # os.path.isfile
import sys   # exit
import argparse
from collections import defaultdict, namedtuple

import machine
import non_deterministic
from tape import Tape


def parse_args():
    parser = argparse.ArgumentParser(description='Multitape Turing '
                                                 'Machine Simulator')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='alpha 0.8c')
    parser.add_argument('-s', '--step',
                        help='enable step mode instead of running',
                        action='store_true')
    parser.add_argument('file',
                        metavar='FILE',
                        type=str,
                        help='path to program')
    parser.add_argument('-nd', '--non-deterministic',
                        help='simulate a non-deterministic Turing Machine',
                        action='store_true')
    return parser.parse_args()


def process_input(path):
    extractor = re.compile('(?P<state>\S+)\s+(?P<read>\S+)\s+(?P<write>\S+)\s+'
                           '(?P<move>\S+)\s+(?P<new_state>\S+)')
    states = defaultdict(list)
    transition = namedtuple("Transition",
                            ["read", "write", "move", "new_state"])
    num_tapes = -1
    with open(path, 'r') as f:
        for line in f:
            line = line.split(';')[0]
            match = extractor.match(line.strip())
            if match is None:
                continue
            match = match.groupdict()
            state = match["state"]
            read = match["read"].replace('_', ' ')
            write = match["write"].replace('_', ' ')
            move = match["move"]
            new_state = match["new_state"]
            states[state].append(transition(read, write, move, new_state))
            if num_tapes == -1:
                num_tapes = len(match['read'])
    tapes = []
    for i in range(num_tapes):
        tape_input = input("Tape {} input: ".format(i))
        tape = Tape(tape_input)
        tapes.append(tape)
    turing_machine = machine.Machine("q0", states, tapes)
    return turing_machine, states, tapes


def main():
    args = parse_args()
    if not os.path.isfile(args.file):
        sys.stderr.write('Invalid path to Turing Machine specification\n')
        sys.exit(1)
    turing_machine, states, tapes = process_input(args.file)
    turing_machine.is_deterministic = not args.non_deterministic
    if turing_machine.is_deterministic:
        turing_machine.run(step=args.step)
    else:
        tapes = [tape.copy() for tape in tapes]
        final_machine = non_deterministic.get_final_path(turing_machine)
        winning_machine = machine.Machine('q0', states, tapes)
        winning_machine.run(step=args.step,
                            path=final_machine.traversed_transitions)

if __name__ == '__main__':
    main()
