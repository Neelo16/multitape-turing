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
