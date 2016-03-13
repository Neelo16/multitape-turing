#!/usr/bin/env python3

import re
import os    # os.path.isfile
import sys   # exit
import time  # sleep
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
                        version='alpha 0.8')
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
    parser.add_argument('-sc', '--skip-calculations',
                        help='only show the final path in a '
                             'non-deterministic machine',
                        action='store_true')

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
        tape = Tape(tape_input)
        tapes.append(tape)
    turing_machine = machine.Machine("q0", states, tapes)
    return turing_machine, states, tapes


def display_final_path(final_machine,
                       states,
                       tapes,
                       step=False,
                       skipped=False):
    if not skipped and final_machine.state.name != 'halt-accept':
        return
    if not skipped:
        answer = input('Would you like to watch the path '
                       'to the accept state? (Y/n)')
    else:
        answer = ''
    if not answer.lower().startswith('n'):
        winning_machine = machine.Machine('q0', states, tapes)
        winning_machine.show()
        for transition in final_machine.traversed_transitions:
            if step:
                input('Press RETURN to step')
            else:
                time.sleep(0.05)
            winning_machine.clear_output(step)
            winning_machine.step(transition)
            winning_machine.show()


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
        final_machine = non_deterministic.run(turing_machine,
                                              step=args.step,
                                              no_output=args.skip_calculations)
        display_final_path(final_machine, states, tapes,
                           args.step, args.skip_calculations)

if __name__ == '__main__':
    main()
