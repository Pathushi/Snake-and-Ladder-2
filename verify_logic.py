from game_logic import bfs_min_moves, dijkstra_min_moves
from test_board import TestBoard

def verify_logic():
    mock_board = TestBoard()
    
    print("--- SNAKE & LADDER ALGORITHM VALIDATION ---")
    print(f"Testing {mock_board.total_cells}-cell board.")
    print("Expected Path: 1 -> 4(L30) -> 35(L59) -> 64")
    print("-" * 45)
    
    # Test BFS
    moves_bfs, path_bfs, time_bfs = bfs_min_moves(mock_board)
    print(f"Algorithm 1 (BFS):      {moves_bfs} moves in {time_bfs:.6f}s")
    
    # Test Dijkstra
    moves_dijk, time_dijk = dijkstra_min_moves(mock_board)
    print(f"Algorithm 2 (Dijkstra): {moves_dijk} moves in {time_dijk:.6f}s")

    # Final Validation
    if moves_bfs == 3 and moves_dijk == 3:
        print("\n✅ SUCCESS: Both algorithms identified the optimal 3-move path.")
        print(f"BFS Path Trace: {path_bfs}")
    else:
        print("\n❌ FAILED: Algorithm mismatch or incorrect calculation.")

if __name__ == "__main__":
    verify_logic()