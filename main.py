import tkinter as tk
from database import create_table, save_winner
from tkinter import messagebox
from board import Board
from game_logic import bfs_min_moves
import random

root = tk.Tk()
root.title("Snake & Ladder Game")
root.geometry("600x700")

# Create DB table
create_table()

# Global variables
player_name = ""
board = None
correct_answer = 0

player_pos = 1
player_token = None
current_move = 0


# -------------------- RESET GAME --------------------
def restart_game():
    global player_name, board, correct_answer, player_pos, current_move, player_token

    player_name = ""
    board = None
    correct_answer = 0
    player_pos = 1
    current_move = 0
    player_token = None

    # clear all frames
    result_frame.pack_forget()
    board_frame.pack_forget()
    size_frame.pack_forget()
    question_frame.pack_forget()

    name_entry.delete(0, tk.END)
    selected_option.set(0)

    name_frame.pack()


# -------------------- STEP 1: ENTER NAME --------------------
def start_game():
    global player_name

    player_name = name_entry.get()

    if player_name == "":
        messagebox.showerror("Error", "Enter your name")
        return

    name_frame.pack_forget()
    size_frame.pack()


# -------------------- STEP 2: SELECT BOARD SIZE --------------------
def select_size():
    global board, correct_answer, player_pos

    size = int(size_var.get())
    board = Board(size)
    player_pos = 1

    correct_answer = bfs_min_moves(board)

    size_frame.pack_forget()
    draw_board()
    show_question()


# -------------------- DRAW BOARD --------------------
def draw_board():
    canvas.delete("all")

    size = board.size
    cell_size = 500 // size

    for row in range(size):
        for col in range(size):

            if row % 2 == 0:
                cell_num = row * size + col + 1
            else:
                cell_num = row * size + (size - col)

            x1 = col * cell_size
            y1 = (size - row - 1) * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            color = "white"

            if cell_num in board.snakes:
                color = "#ff9999"
            elif cell_num in board.ladders:
                color = "#99ff99"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            canvas.create_text(x1 + 5, y1 + 5, text=str(cell_num), anchor="nw")

    for start, end in board.ladders.items():
        draw_line(start, end, "green")

    for start, end in board.snakes.items():
        draw_line(start, end, "red")

    draw_player()
    board_frame.pack()


# -------------------- DRAW LINES --------------------
def draw_line(start, end, color):
    size = board.size
    cell_size = 500 // size

    def get_center(cell):
        row = (cell - 1) // size
        col = (cell - 1) % size

        if row % 2 == 1:
            col = size - 1 - col

        x = col * cell_size + cell_size // 2
        y = (size - row - 1) * cell_size + cell_size // 2
        return x, y

    x1, y1 = get_center(start)
    x2, y2 = get_center(end)

    canvas.create_line(x1, y1, x2, y2, fill=color, width=3)


# -------------------- DRAW PLAYER --------------------
def draw_player():
    global player_token

    size = board.size
    cell_size = 500 // size

    def get_center(cell):
        row = (cell - 1) // size
        col = (cell - 1) % size

        if row % 2 == 1:
            col = size - 1 - col

        x = col * cell_size + cell_size // 2
        y = (size - row - 1) * cell_size + cell_size // 2
        return x, y

    x, y = get_center(player_pos)

    if player_token:
        canvas.delete(player_token)

    player_token = canvas.create_oval(
        x - 10, y - 10, x + 10, y + 10,
        fill="blue"
    )


# -------------------- QUESTION --------------------
def show_question():
    global options

    options = [correct_answer]

    while len(options) < 3:
        val = random.randint(correct_answer - 2, correct_answer + 2)
        if val > 0 and val not in options:
            options.append(val)

    random.shuffle(options)

    for i in range(3):
        option_buttons[i].config(text=str(options[i]), value=options[i])

    question_frame.pack()


# -------------------- CHECK ANSWER --------------------
def check_answer():
    global current_move

    selected = selected_option.get()

    current_move = 0
    question_frame.pack_forget()
    start_animation(selected)


# -------------------- ANIMATION --------------------
def start_animation(total_moves):
    global current_move
    current_move = 0
    perform_move(total_moves)


def perform_move(total_moves):
    global current_move

    if current_move >= total_moves:
        show_final_result()
        return

    dice = random.randint(1, 6)
    dice_label.config(text=f"Dice: {dice}")

    move_step_by_step(dice, total_moves)


def move_step_by_step(steps, total_moves):
    global player_pos, current_move

    if steps == 0:
        if player_pos in board.snakes:
            player_pos = board.snakes[player_pos]
        elif player_pos in board.ladders:
            player_pos = board.ladders[player_pos]

        draw_player()

        current_move += 1
        root.after(800, lambda: perform_move(total_moves))
        return

    if player_pos < board.total_cells:
        player_pos += 1

    draw_player()

    root.after(300, lambda: move_step_by_step(steps - 1, total_moves))


# -------------------- FINAL RESULT --------------------
def show_final_result():
    global player_pos  # 🔥 FIX HERE

    selected = selected_option.get()

    # apply final snake/ladder after last move
    if player_pos in board.snakes:
        player_pos = board.snakes[player_pos]
    elif player_pos in board.ladders:
        player_pos = board.ladders[player_pos]

    draw_player()

    if player_pos == board.total_cells:
        result_label.config(text=f"🎉 {player_name} Wins!")
        save_winner(player_name, correct_answer, board.size)
    else:
        result_label.config(
            text=f"❌ {player_name} Loses!\nFinal Cell: {player_pos}"
        )

    result_frame.pack()


# -------------------- UI --------------------

# NAME FRAME
name_frame = tk.Frame(root)
tk.Label(name_frame, text="Enter Name").pack()
name_entry = tk.Entry(name_frame)
name_entry.pack()
tk.Button(name_frame, text="Next", command=start_game).pack()
name_frame.pack()

# SIZE FRAME
size_frame = tk.Frame(root)
tk.Label(size_frame, text="Select Board Size (6–12)").pack()
size_var = tk.StringVar(value="6")
tk.OptionMenu(size_frame, size_var, *[str(i) for i in range(6, 13)]).pack()
tk.Button(size_frame, text="Start Game", command=select_size).pack()

# BOARD FRAME
board_frame = tk.Frame(root)
canvas = tk.Canvas(board_frame, width=500, height=500, bg="white")
canvas.pack()

# DICE LABEL
dice_label = tk.Label(root, text="Dice: -", font=("Arial", 14))
dice_label.pack()

# QUESTION FRAME
question_frame = tk.Frame(root)
tk.Label(question_frame, text="Minimum Dice Throws?").pack()

selected_option = tk.IntVar()

option_buttons = []
for i in range(3):
    btn = tk.Radiobutton(question_frame, text="", variable=selected_option)
    btn.pack()
    option_buttons.append(btn)

tk.Button(question_frame, text="Submit", command=check_answer).pack()

# RESULT FRAME
result_frame = tk.Frame(root)
result_label = tk.Label(result_frame, text="", font=("Arial", 14))
result_label.pack()

# 🔥 NEW: Restart Button
tk.Button(result_frame, text="🔄 Play Again", command=restart_game).pack(pady=10)

root.mainloop()