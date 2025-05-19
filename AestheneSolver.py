import os
import tkinter as tk
import tkinter.messagebox

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def is_valid_word(word, known_letters, confirmed_letters, excluded_letters, banned_positions):
    word = word.upper()
    for i in range(5):
        if confirmed_letters[i] != '_' and word[i] != confirmed_letters[i]:
            return False
    if any(letter in word for letter in excluded_letters):
        return False
    for letter in known_letters:
        if not any(word[i] == letter and letter not in banned_positions[i] for i in range(5)):
            return False
    for i in range(5):
        if word[i] in banned_positions[i]:
            return False
    return True

def solve_wordle(file, known_letters, confirmed_letters, excluded_letters, banned_positions):
    solutions = []
    for word in load_word_list(file):
        if len(word) == 5 and is_valid_word(word, known_letters, confirmed_letters, excluded_letters, banned_positions):
            solutions.append(word)
    return solutions

def extract_grid_info():
    grid_text = grid_text_box.get("1.0", "end-1c")

    lines = grid_text.strip().split("\n")

    confirmed_letters = ['_'] * 5
    known_letters = set()
    excluded_letters = set()
    banned_positions = {i: set() for i in range(5)}

    for line in lines:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) != 5:
            continue
        for i, cell in enumerate(cells):
            if len(cell) == 3 and cell[0] == cell[2] and cell[0] in '*_+':
                letter = cell[1].upper()
                if cell[0] == '+':
                    confirmed_letters[i] = letter
                elif cell[0] == '_':
                    known_letters.add(letter)
                    banned_positions[i].add(letter)
                elif cell[0] == '*':
                    excluded_letters.add(letter)

    return known_letters, confirmed_letters, excluded_letters, banned_positions

def solve_button_click():
    known_letters, confirmed_letters, excluded_letters, banned_positions = extract_grid_info()

    available = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for ch in known_letters.union(excluded_letters).union(set(confirmed_letters)):
        if ch in available and ch != '_':
            available.remove(ch)
    available_letters_label.config(text=' '.join(available))

    solutions = solve_wordle(word_list_file, known_letters, confirmed_letters, excluded_letters, banned_positions)

    results_text.config(state='normal')
    results_text.delete("1.0", tk.END)
    results_text.insert(tk.END, '\n'.join(solutions) if solutions else "No solutions found.")
    results_text.config(state='disabled')

def copy_selected_word(event):
    try:
        selected = results_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        if selected:
            full_command = f"whisper lock {selected}"
            window.clipboard_clear()
            window.clipboard_append(full_command)
            window.update()
            tk.messagebox.showinfo("Copied", f"Copied to clipboard:\n{full_command}")
    except tk.TclError:
        pass

def reset_button_click():
    grid_text_box.delete("1.0", tk.END)
    available_letters_label.config(text=' '.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    results_text.config(state='normal')
    results_text.delete("1.0", tk.END)
    results_text.config(state='disabled')

def validate_entry(text):
    return len(text) <= 1

def add_word_button_click():
    new_word = new_word_entry.get().upper()
    if len(new_word) != 5:
        tk.messagebox.showerror("Error", "New word must be 5 letters long")
        return
    words = load_word_list(word_list_file)
    if new_word in words:
        tk.messagebox.showerror("Error", f"Word '{new_word}' already exists")
    else:
        words.append(new_word)
        words.sort()
        with open(word_list_file, 'w') as f:
            f.write('\n'.join(words))
        tk.messagebox.showinfo("Success", f"Word '{new_word}' added")
    new_word_entry.delete(0, tk.END)

def remove_word_button_click():
    word = remove_word_entry.get().upper()
    words = load_word_list(word_list_file)
    if word not in words:
        tk.messagebox.showerror("Error", f"Word '{word}' not found")
    else:
        words.remove(word)
        with open(word_list_file, 'w') as f:
            f.write('\n'.join(words))
        tk.messagebox.showinfo("Success", f"Word '{word}' removed")
    remove_word_entry.delete(0, tk.END)

def load_button_click():
    global word_list_file
    new_file = word_list_entry.get()
    if os.path.isfile(new_file):
        word_list_file = new_file
        tk.messagebox.showinfo("Success", f"Word list set to '{new_file}'")
    else:
        tk.messagebox.showerror("Error", f"File '{new_file}' not found")
    word_list_entry.delete(0, tk.END)

script_directory = os.path.dirname(os.path.abspath(__file__))
word_list_file = os.path.join(script_directory, 'Aesthene-words.txt')

window = tk.Tk()
window.title("Aesthene's Close Wordle")
# Define size
win_w = 280
win_h = 440

# Center position
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
x = (screen_w // 2) - (win_w // 2)
y = (screen_h // 2) - (win_h // 2)

# Set geometry with position
window.geometry(f"{win_w}x{win_h}+{x}+{y}")
window.attributes("-topmost", True)

vcmd = (window.register(validate_entry), '%P')

tk.Label(window, text="Available Letters:").pack()
available_letters_label = tk.Label(window, text=' '.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
available_letters_label.pack()

tk.Label(window, text="Paste Wordle Grid:").pack()
grid_text_box = tk.Text(window, height=6, width=50)
grid_text_box.pack()

btn_frame = tk.Frame(window)
btn_frame.pack()
tk.Button(btn_frame, text="Solve", command=solve_button_click, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Reset", command=reset_button_click, width=15).pack(side=tk.RIGHT, padx=10)

results_frame = tk.Frame(window)
results_frame.pack()
scroll = tk.Scrollbar(results_frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
results_text = tk.Text(results_frame, height=10, width=35, yscrollcommand=scroll.set)
results_text.pack(side=tk.LEFT)
results_text.bind("<ButtonRelease-1>", copy_selected_word)
scroll.config(command=results_text.yview)

add_frame = tk.Frame(window)
add_frame.pack(side=tk.LEFT, padx=10)
tk.Label(add_frame, text="Add Word:").pack()
new_word_entry = tk.Entry(add_frame, width=10)
new_word_entry.pack()
tk.Button(add_frame, text="Add", command=add_word_button_click).pack()

remove_frame = tk.Frame(window)
remove_frame.pack(side=tk.LEFT, padx=10)
tk.Label(remove_frame, text="Remove Word:").pack()
remove_word_entry = tk.Entry(remove_frame, width=10)
remove_word_entry.pack()
tk.Button(remove_frame, text="Remove", command=remove_word_button_click).pack()

load_frame = tk.Frame(window)
load_frame.pack(side=tk.RIGHT, padx=10)
tk.Label(load_frame, text="Word List File:").pack()
word_list_entry = tk.Entry(load_frame, width=15)
word_list_entry.insert(0, "Aesthene-words.txt")
word_list_entry.pack()
tk.Button(load_frame, text="Load", command=load_button_click).pack()

window.mainloop()