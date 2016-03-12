from collections import deque
import time  # sleep

tasks = deque()


def register_choices(machine, transitions):
    for transition in transitions:
        new_machine = machine.copy()
        tasks.append((new_machine, transition))


def run(initial_machine, step=False):
    machine = initial_machine
    previous_machine = machine
    transition = None
    is_halted = False
    machine.show()
    while not is_halted:
        if step:
            input('Press RETURN to step')
        else:
            time.sleep(0.05)
        machine.step(transition=transition)
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
    print('Final state: {}'.format(machine.state.name))
    return machine
