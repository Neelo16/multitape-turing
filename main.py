#!/usr/bin/env python

import re
import os   # os.path.isfile
import sys  # exit
import argparse
from collections import defaultdict, namedtuple

import machine
from tape import Tape

try:
    input = raw_input
except NameError:
    pass


def parse_args():
    parser = argparse.ArgumentParser(description='Multitape Turing '
                                                 'Machine Simulator')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='alpha 0.7b')
    parser.add_argument('-s', '--step',
                        help='enable step mode instead of running',
                        action='store_true')
    parser.add_argument('file',
                        metavar='FILE',
                        type=str,
                        help='path to program')

    return parser.parse_args()


def process_input(path):
    extractor = re.compile('(?P<state>\S+)\s+(?P<read>\S+)\s+(?P<write>\S+)\s+'
                           '(?P<move>\S+)\s+(?P<new_state>\S+)')
    states = defaultdict(list)
    transition = namedtuple("Transition",
                            ["read", "write", "move", "new_state"])
    with open(path, 'r') as f:
        num_tapes = int(f.readline())
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
    tapes = []
    for i in range(num_tapes):
        tape_input = input("Tape {} input: ".format(i))
        # tape_pointer = int(input("Tape {} starting pointer: ".format(i)))
        tape = Tape(tape_input)
        # tape.pointer = tape_pointer
        tapes.append(tape)
    turing_machine = machine.Machine("q0", states, tapes)
    return turing_machine


def main():
    args = parse_args()
    if not os.path.isfile(args.file):
        sys.stderr.write('Invalid path to Turing Machine specification\n')
        sys.exit(1)
    turing_machine = process_input(args.file)
    turing_machine.run(step=args.step)

if __name__ == '__main__':
    main()
