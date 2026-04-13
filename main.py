import tkinter as tk
from database import create_table, save_winner
from tkinter import messagebox
from board import Board
from game_logic import bfs_min_moves
import random
import math

# --- UI CONFIGURATION ---
BG_COLOR = "#2c3e50"
BOARD_COLOR_1 = "#ffffff"
BOARD_COLOR_2 = "#f1f2f6"
PRIMARY_FONT = ("Helvetica", 12)
HEADER_FONT = ("Helvetica", 18, "bold")

root = tk.Tk()
root.title("Snake & Ladder Master")
root.geometry("600x900")
root.configure(bg=BG_COLOR)

create_table()

# Global variables
player_name = ""
board = None
correct_answer = 0
player_pos = 1
player_token = None
current_move = 0

# -------------------- DRAWING ASSETS (NO IMAGES NEEDED) --------------------

def draw_asset(start, end, type):
    x1, y1 = get_cell_coords(start)
    x2, y2 = get_cell_coords(end)

    if type == "ladder":
        # Calculate angle to offset rails properly even for horizontal ladders
        angle = math.atan2(y2 - y1, x2 - x1)
        offset_x = 8 * math.sin(angle)
        offset_y = 8 * math.cos(angle)

        # Draw two side rails
        canvas.create_line(x1 - offset_x, y1 + offset_y, x2 - offset_x, y2 + offset_y, fill="#8B4513", width=3)
        canvas.create_line(x1 + offset_x, y1 - offset_y, x2 + offset_x, y2 - offset_y, fill="#8B4513", width=3)
        
        # Draw rungs along the length
        num_rungs = 7
        for i in range(num_rungs + 1):
            frac = i / num_rungs
            lx = (x1 - offset_x) + frac * (x2 - x1)
            ly = (y1 + offset_y) + frac * (y2 - y1)
            rx = (x1 + offset_x) + frac * (x2 - x1)
            ry = (y1 - offset_y) + frac * (y2 - y1)
            canvas.create_line(lx, ly, rx, ry, fill="#A0522D", width=2)

    elif type == "snake":
        # Draw thick body
        canvas.create_line(x1, y1, x2, y2, fill="#2ecc71", width=10, capstyle=tk.ROUND, joinstyle=tk.ROUND)
        
        # Draw head at the start (top)
        canvas.create_oval(x1-9, y1-9, x1+9, y1+9, fill="#27ae60", outline="#1e8449")
        
        # Draw eyes and pupils
        canvas.create_oval(x1-4, y1-4, x1-1, y1-1, fill="white")
        canvas.create_oval(x1+1, y1-4, x1+4, y1-1, fill="white")
        canvas.create_oval(x1-3, y1-3, x1-2, y1-2, fill="black")
        canvas.create_oval(x1+2, y1-3, x1+3, y1-2, fill="black")

# -------------------- CORE GAME FUNCTIONS --------------------

def restart_game():
    global player_name, board, correct_answer, player_pos, current_move, player_token
    player_name = ""
    board = None
    correct_answer = 0
    player_pos = 1
    current_move = 0
    player_token = None
    
    for frame in [result_frame, board_frame, size_frame, question_frame, dice_label]:
        frame.pack_forget()
    
    name_entry.delete(0, tk.END)
    selected_option.set(0)
    name_frame.pack(pady=50)

def start_game():
    global player_name
    player_name = name_entry.get().strip()
    if not player_name:
        messagebox.showerror("Error", "Enter your name!")
        return
    name_frame.pack_forget()
    size_frame.pack(pady=50)

def select_size():
    global board, correct_answer, player_pos
    size = int(size_var.get())
    board = Board(size)
    player_pos = 1
    correct_answer = bfs_min_moves(board)
    size_frame.pack_forget()
    dice_label.pack(pady=10)
    draw_board()
    show_question()

def get_cell_coords(cell_num):
    size = board.size
    cell_size = 500 // size
    row = (cell_num - 1) // size
    col = (cell_num - 1) % size
    if row % 2 == 1:
        col = size - 1 - col
    x = col * cell_size + cell_size // 2
    y = (size - row - 1) * cell_size + cell_size // 2
    return x, y

def draw_board():
    canvas.delete("all")
    size = board.size
    cell_size = 500 // size

    for row in range(size):
        for col in range(size):
            cell_num = (row * size + col + 1) if row % 2 == 0 else (row * size + (size - col))
            x1, y1 = col * cell_size, (size - row - 1) * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#dcdde1")
            canvas.create_text(x1 + 5, y1 + 5, text=str(cell_num), anchor="nw", font=("Arial", 8))

    for s, e in board.ladders.items(): draw_asset(s, e, "ladder")
    for s, e in board.snakes.items(): draw_asset(s, e, "snake")
    
    draw_player()
    board_frame.pack(pady=10)

def draw_player():
    global player_token
    x, y = get_cell_coords(player_pos)
    if player_token: canvas.delete(player_token)
    player_token = canvas.create_oval(x-12, y-12, x+12, y+12, fill="#e74c3c", outline="white", width=2)

def show_question():
    global options
    options = [correct_answer]
    while len(options) < 3:
        val = random.randint(max(1, correct_answer - 3), correct_answer + 3)
        if val not in options: options.append(val)
    random.shuffle(options)
    for i in range(3):
        option_buttons[i].config(text=f" {options[i]} Throws ", value=options[i], indicatoron=0, width=15)
    question_frame.pack(pady=10)

def check_answer():
    if selected_option.get() == 0: return
    question_frame.pack_forget()
    perform_move(selected_option.get())

def perform_move(total_moves):
    global current_move
    if current_move >= total_moves:
        show_final_result()
        return
    dice = random.randint(1, 6)
    dice_label.config(text=f"🎲 Dice: {dice}", fg="#f1c40f")
    move_step_by_step(dice, total_moves)

def move_step_by_step(steps, total_moves):
    global player_pos, current_move
    if steps == 0:
        if player_pos in board.snakes: player_pos = board.snakes[player_pos]
        elif player_pos in board.ladders: player_pos = board.ladders[player_pos]
        draw_player()
        current_move += 1
        root.after(600, lambda: perform_move(total_moves))
        return
    if player_pos < board.total_cells:
        player_pos += 1
        draw_player()
        root.after(200, lambda: move_step_by_step(steps - 1, total_moves))

def show_final_result():
    if player_pos == board.total_cells:
        result_label.config(text=f"🏆 WINNER! {player_name} reached the top!", fg="#2ecc71")
        save_winner(player_name, correct_answer, board.size)
    else:
        # UPDATED: Now shows the correct answer when the player loses
        result_label.config(
            text=f"💀 Game Over! You finished at {player_pos}\nCorrect Answer was: {correct_answer}", 
            fg="#e74c3c",
            justify="center"
        )
    result_frame.pack(pady=20)

# -------------------- UI COMPONENTS --------------------

name_frame = tk.Frame(root, bg=BG_COLOR)
tk.Label(name_frame, text="SNAKE & LADDER", font=("Impact", 35), bg=BG_COLOR, fg="#ecf0f1").pack(pady=20)
name_entry = tk.Entry(name_frame, font=HEADER_FONT, justify='center')
name_entry.pack(pady=10)
tk.Button(name_frame, text="START", command=start_game, bg="#27ae60", fg="white", font=PRIMARY_FONT).pack()
name_frame.pack(pady=100)

size_frame = tk.Frame(root, bg=BG_COLOR)
tk.Label(size_frame, text="Select Board Size", font=HEADER_FONT, bg=BG_COLOR, fg="white").pack()
size_var = tk.StringVar(value="8")
tk.OptionMenu(size_frame, size_var, *[str(i) for i in range(6, 13)]).pack(pady=10)
tk.Button(size_frame, text="Generate Board", command=select_size).pack()

board_frame = tk.Frame(root, bg="#34495e", padx=5, pady=5)
canvas = tk.Canvas(board_frame, width=500, height=500, bg="white", highlightthickness=0)
canvas.pack()

dice_label = tk.Label(root, text="Dice: -", font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg="white")

question_frame = tk.Frame(root, bg=BG_COLOR)
tk.Label(question_frame, text="Guess the minimum moves to win:", font=PRIMARY_FONT, bg=BG_COLOR, fg="#bdc3c7").pack()
selected_option = tk.IntVar()
btn_container = tk.Frame(question_frame, bg=BG_COLOR)
btn_container.pack(pady=10)
option_buttons = [tk.Radiobutton(btn_container, text="", variable=selected_option, font=PRIMARY_FONT) for _ in range(3)]
for b in option_buttons: b.pack(side=tk.LEFT, padx=5)
tk.Button(question_frame, text="Confirm Prediction", command=check_answer, bg="#2980b9", fg="white").pack()

result_frame = tk.Frame(root, bg=BG_COLOR)
result_label = tk.Label(result_frame, text="", font=HEADER_FONT, bg=BG_COLOR)
result_label.pack()
tk.Button(result_frame, text="Play Again", command=restart_game).pack(pady=10)

root.mainloop()