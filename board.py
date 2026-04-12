import random

class Board:
    def __init__(self, size):
        self.size = size
        self.total_cells = size * size
        self.snakes = {}
        self.ladders = {}
        self.generate_board()

    def generate_board(self):
        count = self.size - 2

        # Generate snakes
        while len(self.snakes) < count:
            start = random.randint(2, self.total_cells - 1)
            end = random.randint(1, start - 1)

            if start > end and start not in self.snakes:
                self.snakes[start] = end

        # Generate ladders
        while len(self.ladders) < count:
            start = random.randint(1, self.total_cells - 2)
            end = random.randint(start + 1, self.total_cells)

            if start < end and start not in self.ladders:
                self.ladders[start] = end