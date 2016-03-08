import itertools  # chain


class Tape:
    def __init__(self, contents=' '):
        self.right_side = list(contents)
        self.left_side = list()
        self._pointer = 0
        if len(self.right_side) == 0:
            self.right_side.append(' ')

    def read(self):
        if self._pointer >= 0:
            return self.right_side[self._pointer]
        # Position -1 is actually index 0 of left_side
        return self.left_side[abs(self._pointer + 1)]

    def write(self, value):
        if self._pointer >= 0:
            current_side = self.right_side
            pointer = self._pointer
        else:
            current_side = self.left_side
            pointer = abs(self._pointer + 1)
        if pointer >= len(current_side):
            current_side.append(value)
        else:
            current_side[pointer] = value

    def left(self):
        self._pointer -= 1
        if self._pointer < 0 and abs(self._pointer+1) >= len(self.left_side):
            self.left_side.append(' ')

    def right(self):
        self._pointer += 1
        if self._pointer >= len(self.right_side):
            self.right_side.append(' ')

    @property
    def pointer(self):
        return len(self.left_side) + self._pointer

    @pointer.setter
    def pointer(self, value):
        self._pointer = value - len(self.left_side)

    def __iter__(self):
        return itertools.chain(reversed(self.left_side), self.right_side)

    def __repr__(self):
        return ''.join(self)

    def __len__(self):
        return len(self.left_side) + len(self.right_side)
