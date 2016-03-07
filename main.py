#!/usr/bin/env python

import sys
import re
from collections import defaultdict, namedtuple

import machine


def process_input(path):
    extractor = re.compile('(?P<state>\S+) (?P<read>\S+) (?P<write>\S+) '
                           '(?P<move>\S+) (?P<new_state>\S+)')
    states = defaultdict(dict)
    transition = namedtuple("Transition", ["write", "move", "new_state"])
    with open(path, 'r') as f:
        for line in f:
            match = extractor.match(line.strip())
            if match is None:
                continue
            match = match.groupdict()
            state = match["state"]
            to_read = match["read"].replace('_', ' ')
            to_write = match["write"].replace('_', ' ')
            current_state = states[state]
            for character in to_read[:-1]:
                current_state[character] = {}
                current_state = current_state[character]
            current_state[to_read[-1]] = transition(to_write,
                                                  match["move"],
                                                  match["new_state"])
    turing_machine = machine.Machine("q0", states, 2)
    return turing_machine


def main():
    process_input(sys.argv[1])

if __name__ == '__main__':
    main()
