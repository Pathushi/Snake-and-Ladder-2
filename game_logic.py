import random
from collections import deque

def bfs_min_moves(board):
    # -----------------------------
    # visited keeps track of cells we already processed
    # so we don't repeat same paths again (prevents loops)
    # -----------------------------
    visited = set([1])  # start cell (1) is already visited

    # -----------------------------
    # queue stores (current_cell, number_of_dice_moves_taken)
    # BFS processes level by level (shortest path logic)
    # -----------------------------
    queue = deque([(1, 0)])  # start at cell 1 with 0 moves

    # -----------------------------
    # BFS LOOP
    # runs until there are no more paths to explore
    # -----------------------------
    while queue:

        # take the first element in queue (FIFO)
        cell, moves = queue.popleft()

        # -----------------------------
        # CHECK IF WE REACHED FINAL CELL
        # if yes, return moves immediately
        # this is guaranteed to be the shortest path
        # -----------------------------
        if cell == board.total_cells:
            return moves

        # -----------------------------
        # TRY ALL POSSIBLE DICE VALUES (1 to 6)
        # each represents one possible move from current cell
        # -----------------------------
        for dice in range(1, 7):
            next_cell = cell + dice

            # -----------------------------
            # ignore moves that go beyond board size
            # -----------------------------
            if next_cell > board.total_cells:
                continue

            # -----------------------------
            # HANDLE SNAKES AND LADDERS
            # if we land on a snake or ladder,
            # we must move immediately to new position
            # (can happen multiple times in a chain)
            # -----------------------------
            while next_cell in board.snakes or next_cell in board.ladders:

                # if snake → move down
                if next_cell in board.snakes:
                    next_cell = board.snakes[next_cell]

                # if ladder → move up
                elif next_cell in board.ladders:
                    next_cell = board.ladders[next_cell]

            # -----------------------------
            # VISITED CHECK
            # only process this cell if we haven't visited it before
            # prevents infinite loops and repeated work
            # -----------------------------
            if next_cell not in visited:

                # mark as visited
                visited.add(next_cell)

                # add to queue with +1 move (one dice throw used)
                queue.append((next_cell, moves + 1))