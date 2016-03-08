#!/usr/bin/env python

import sys
import re
from collections import defaultdict, namedtuple

import machine
from tape import Tape


def process_input(path):
    extractor = re.compile('(?P<state>\S+) (?P<read>\S+) (?P<write>\S+) '
                           '(?P<move>\S+) (?P<new_state>\S+)')
    states = defaultdict(list)
    transition = namedtuple("Transition",
                            ["read", "write", "move", "new_state"])
    with open(path, 'r') as f:
        num_tapes = int(f.readline())
        for line in f:
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
        tape_pointer = int(input("Tape {} starting pointer: ".format(i)))
        tape = Tape(tape_input)
        tape.pointer = tape_pointer
        tapes.append(tape)
    turing_machine = machine.Machine("q0", states, tapes)
    return turing_machine


def main():
    turing_machine = process_input(sys.argv[1])
    turing_machine.run()

if __name__ == '__main__':
    main()
