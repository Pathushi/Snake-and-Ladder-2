import random
from collections import deque

def bfs_min_moves(board):
    visited = set([1])
    queue = deque([(1, 0)])

    while queue:
        cell, moves = queue.popleft()

        if cell == board.total_cells:
            return moves

        for dice in range(1, 7):
            next_cell = cell + dice

            if next_cell > board.total_cells:
                continue

            # handle snake/ladder repeatedly
            while next_cell in board.snakes or next_cell in board.ladders:
                if next_cell in board.snakes:
                    next_cell = board.snakes[next_cell]
                elif next_cell in board.ladders:
                    next_cell = board.ladders[next_cell]

            if next_cell not in visited:
                visited.add(next_cell)
                queue.append((next_cell, moves + 1))