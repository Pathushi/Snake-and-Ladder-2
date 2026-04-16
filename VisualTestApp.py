import tkinter as tk
from game_logic import bfs_min_moves
from test_board import TestBoard

class VisualTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logic & Movement Validator")
        self.board = TestBoard()
        self.cell_size = 60
        self.canvas_size = self.board.size * self.cell_size
        self.player_pos = 1
        self.token = None
        self.path_to_follow = [] # Stores the dice rolls from BFS
        
        # UI Layout
        self.info_label = tk.Label(root, text="Goal: Move 1 -> 4(L30) -> 35(L59) -> 64", font=("Arial", 12))
        self.info_label.pack(pady=10)
        
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(padx=20)
        
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.calc_btn = tk.Button(self.btn_frame, text="1. Run Algorithms", command=self.validate_logic)
        self.calc_btn.pack(side=tk.LEFT, padx=5)

        self.sim_btn = tk.Button(self.btn_frame, text="2. Simulate Path", command=self.start_simulation, state=tk.DISABLED)
        self.sim_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(root, text="Step: 0 | Position: 1", font=("Arial", 10))
        self.status_label.pack()

        self.draw_test_board()
        self.draw_player()

    def get_coords(self, cell_num):
        size = self.board.size
        row = (cell_num - 1) // size
        col = (cell_num - 1) % size
        if row % 2 == 1: col = size - 1 - col
        x = col * self.cell_size + self.cell_size // 2
        y = (size - row - 1) * self.cell_size + self.cell_size // 2
        return x, y

    def draw_test_board(self):
        size = self.board.size
        for row in range(size):
            for col in range(size):
                cell_num = (row * size + col + 1) if row % 2 == 0 else (row * size + (size - col))
                x1, y1 = col * self.cell_size, (size - row - 1) * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "#f1f2f6" if (row + col) % 2 == 0 else "#ffffff"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#dcdde1")
                self.canvas.create_text(x1 + 15, y1 + 15, text=str(cell_num), font=("Arial", 8))

        for s, e in self.board.ladders.items():
            x1, y1 = self.get_coords(s); x2, y2 = self.get_coords(e)
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, arrow=tk.LAST)
        for s, e in self.board.snakes.items():
            x1, y1 = self.get_coords(s); x2, y2 = self.get_coords(e)
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3, arrow=tk.LAST)

    def draw_player(self):
        x, y = self.get_coords(self.player_pos)
        if self.token: self.canvas.delete(self.token)
        self.token = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="orange", outline="black")

    def validate_logic(self):
        # Updated to handle the (moves, path, time) return structure
        moves, self.path_to_follow, time_taken = bfs_min_moves(self.board)
        self.status_label.config(text=f"Shortest Path: {moves} moves ({time_taken:.5f}s)")
        self.sim_btn.config(state=tk.NORMAL)

    def start_simulation(self):
        self.player_pos = 1
        self.current_step = 0
        self.run_step()

    def run_step(self):
        if self.current_step < len(self.path_to_follow):
            roll = self.path_to_follow[self.current_step]
            
            # Logic to calculate landing
            new_pos = self.player_pos + roll
            if new_pos in self.board.ladders: new_pos = self.board.ladders[new_pos]
            elif new_pos in self.board.snakes: new_pos = self.board.snakes[new_pos]
            
            self.player_pos = new_pos
            self.draw_player()
            self.current_step += 1
            self.status_label.config(text=f"Move {self.current_step}: Rolled {roll} -> Position {new_pos}")
            self.root.after(1000, self.run_step)
        else:
            self.status_label.config(text="Victory! Reached cell 64.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualTestApp(root)
    root.mainloop()