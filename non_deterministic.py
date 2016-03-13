from collections import deque
import time  # sleep

tasks = deque()


def register_choices(machine, transitions):
    for transition in transitions:
        new_machine = machine.copy()
        tasks.append((new_machine, transition))


def run(initial_machine, step=False, no_output=False):
    machine = initial_machine
    previous_machine = machine
    transition = None
    is_halted = False
    if not no_output:
        machine.show()
    while not is_halted:
        if not no_output:
            if step:
                input('Press RETURN to step')
            else:
                time.sleep(0.05)
        machine.step(transition=transition)
        if not no_output:
            previous_machine.clear_output(step)
            machine.show()
            previous_machine = machine
        is_halted = machine.state.name.startswith('halt')
        if is_halted and machine.state.name == 'halt-accept':
            break
        if tasks:
            if not is_halted:
                tasks.append((machine, None))
            else:
                is_halted = False
            machine, transition = tasks.popleft()
    if not no_output:
        print('Final state: {}'.format(machine.state.name))
    return machine
