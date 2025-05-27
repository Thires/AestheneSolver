import os
import tkinter as tk
import tkinter.messagebox

# Load words from file
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

# Check if a word satisfies all grid and clue constraints
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

# Solve the wordle based on input and filter valid words
def solve_wordle(file, known_letters, confirmed_letters, excluded_letters, banned_positions):
    solutions = []
    for word in load_word_list(file):
        if len(word) == 5 and is_valid_word(word, known_letters, confirmed_letters, excluded_letters, banned_positions):
            solutions.append(word)
    return solutions

# Extract letters and pattern info from the grid input box
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

# Handle the Solve button click
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

# Copy selected word as a command when clicked
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

# Clear grid and results
def reset_button_click():
    grid_text_box.delete("1.0", tk.END)
    available_letters_label.config(text=' '.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    results_text.config(state='normal')
    results_text.delete("1.0", tk.END)
    results_text.config(state='disabled')

# Entry validation for single character fields
def validate_entry(text):
    return len(text) <= 1

# Add a new word to the word list file
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

# Remove a word from the word list file
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

# Load a different word list file
def load_button_click():
    global word_list_file
    new_file = word_list_entry.get()
    if os.path.isfile(new_file):
        word_list_file = new_file
        tk.messagebox.showinfo("Success", f"Word list set to '{new_file}'")
    else:
        tk.messagebox.showerror("Error", f"File '{new_file}' not found")
    word_list_entry.delete(0, tk.END)

# Get the path of the current script and set default word list file path
script_directory = os.path.dirname(os.path.abspath(__file__))
word_list_file = os.path.join(script_directory, 'Aesthene-words.txt')

# Initialize the main Tkinter window
window = tk.Tk()

# Define color scheme for dark mode
dark_bg = "#1e1e1e"
dark_fg = "#ffffff"
entry_bg = "#2a2a2a"
highlight = "#3e3e3e"

# Apply dark background to main window
window.configure(bg=dark_bg)
window.title("Aesthene's Close Wordle")

# Define and center the window dimensions
win_w = 360
win_h = 350
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
x = (screen_w // 2) - (win_w // 2)
y = (screen_h // 2) - (win_h // 2)
window.geometry(f"{win_w}x{win_h}+{x}+{y}")
window.minsize(win_w, win_h)
window.attributes("-topmost", True)

# Input validation function registration (used to limit character entry)
vcmd = (window.register(validate_entry), '%P')

# Label showing the currently available letters
tk.Label(window, text="Available Letters:", bg=dark_bg, fg=dark_fg).pack()
available_letters_label = tk.Label(window, text=' '.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), bg=dark_bg, fg=dark_fg)
available_letters_label.pack()

# Create horizontal frame to contain both grid and results
horizontal_frame = tk.Frame(window, bg=dark_bg)
horizontal_frame.pack(pady=5, fill='both', expand=True)

# ---- Left Section: Wordle Grid Input ----
left_frame = tk.Frame(horizontal_frame, bg=dark_bg)
left_frame.pack(side=tk.LEFT, padx=5, fill='both', expand=True)
tk.Label(left_frame, text="Paste Wordle Grid:",bg=dark_bg, fg=dark_fg, activebackground=highlight, activeforeground=dark_fg
).pack()
grid_text_box = tk.Text(left_frame, height=10, width=33, bg=entry_bg, fg=dark_fg, insertbackground=dark_fg)
grid_text_box.pack(fill='both', expand=True)

# ---- Right Section: Results Output ----
right_frame = tk.Frame(horizontal_frame, bg=dark_bg)
right_frame.pack(side=tk.RIGHT, padx=5, fill='both', expand=True)
tk.Label(right_frame, text="Results:",bg=dark_bg, fg=dark_fg, activebackground=highlight, activeforeground=dark_fg
).pack()
scroll = tk.Scrollbar(right_frame, width=15, bg=dark_bg, troughcolor=highlight, activebackground=highlight)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
results_text = tk.Text(right_frame, height=10, width=10, yscrollcommand=scroll.set, bg=entry_bg, fg=dark_fg, insertbackground=dark_fg)
results_text.pack(side=tk.LEFT, fill='both', expand=True)
# Enable word copy on selection click
results_text.bind("<ButtonRelease-1>", copy_selected_word)
scroll.config(command=results_text.yview)

# ---- Solve/Reset Button Frame ----
btn_frame = tk.Frame(window, bg=dark_bg)
btn_frame.pack()
tk.Button(btn_frame, text="Solve", command=solve_button_click, width=15, bg=highlight, fg=dark_fg, activebackground=dark_fg, activeforeground=highlight).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Reset", command=reset_button_click, width=15, bg=highlight, fg=dark_fg, activebackground=dark_fg, activeforeground=highlight).pack(side=tk.RIGHT, padx=10)

# ---- Bottom Frame for Add/Remove/Load Word ----
bottom_frame = tk.Frame(window, bg=dark_bg)
bottom_frame.pack(fill='x', pady=5)

# Add Word
add_frame = tk.Frame(bottom_frame, bg=dark_bg)
add_frame.pack(side=tk.LEFT, expand=True, fill='both')
# Add spacer
spacer = tk.Frame(bottom_frame, width=20, bg=dark_bg)
spacer.pack(side=tk.LEFT)
tk.Label(add_frame, text="Add Word:",bg=dark_bg, fg=dark_fg, activebackground=highlight, activeforeground=dark_fg
).pack()
new_word_entry = tk.Entry(add_frame, width=10, bg=highlight, fg=dark_fg)
new_word_entry.pack()
tk.Button(add_frame, text="Add", command=add_word_button_click, bg=highlight, fg=dark_fg, activebackground=dark_fg, activeforeground=highlight).pack()

# Remove Word
remove_frame = tk.Frame(bottom_frame, bg=dark_bg)
remove_frame.pack(side=tk.LEFT, expand=True, fill='both')
tk.Label(remove_frame, text="Remove Word:",bg=dark_bg, fg=dark_fg, activebackground=highlight, activeforeground=dark_fg
).pack()
remove_word_entry = tk.Entry(remove_frame, width=10, bg=highlight, fg=dark_fg)
remove_word_entry.pack()
tk.Button(remove_frame, text="Remove", command=remove_word_button_click, bg=highlight, fg=dark_fg, activebackground=dark_fg, activeforeground=highlight).pack()

# Word List File
load_frame = tk.Frame(bottom_frame, bg=dark_bg)
load_frame.pack(side=tk.LEFT, expand=True, fill='both')
tk.Label(load_frame, text="Word List File:",bg=dark_bg, fg=dark_fg, activebackground=highlight, activeforeground=dark_fg
).pack()
word_list_entry = tk.Entry(load_frame, width=20, bg=highlight, fg=dark_fg)
word_list_entry.insert(0, "Aesthene-words.txt")
word_list_entry.pack()
tk.Button(load_frame, text="Load", command=load_button_click, bg=highlight, fg=dark_fg, activebackground=dark_fg, activeforeground=highlight).pack()

# Start the Tkinter event loop
window.mainloop()