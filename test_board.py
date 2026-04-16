class TestBoard:
    def __init__(self):
        self.size = 8
        self.total_cells = 64
        # Fixed path: 1 + roll(3) = 4 -> Ladder to 30
        #            30 + roll(5) = 35 -> Ladder to 59
        #            59 + roll(5) = 64 (WIN)
        self.ladders = {4: 30, 35: 59}
        self.snakes = {63: 2, 31: 10, 15: 5}