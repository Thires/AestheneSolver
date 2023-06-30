import os
import tkinter as tk

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words


def is_valid_word(word, known_letters, confirmed_letters, excluded_letters):
    for letter in known_letters:
        if letter not in word:
            return False
    for i, letter in enumerate(confirmed_letters):
        if letter != '_' and letter != word[i]:
            return False
    for letter in excluded_letters:
        if letter != '_' and letter in word:
            return False
    return True


def solve_wordle(word_list_file, known_letters, confirmed_letters, excluded_letters):
    solutions = []
    with open(word_list_file, 'r') as file:
        for line in file:
            word = line.strip()
            if is_valid_word(word, known_letters, confirmed_letters, excluded_letters):
                solutions.append(word)
    return solutions


def solve_button_click():
    known_letters = known_entry.get().upper()
    confirmed_letters = (confirmed_entry_1.get() + confirmed_entry_2.get() + confirmed_entry_3.get() +
                     confirmed_entry_4.get() + confirmed_entry_5.get()).upper()
    excluded_letters = excluded_entry.get().upper()
    
    # Create a list of available letters
    available_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for letter in known_letters:
        if letter in available_letters:
            available_letters.remove(letter)
    for letter in excluded_letters:
        if letter in available_letters:
            available_letters.remove(letter)
        # Remove confirmed letters from the available letters list
    for letter in confirmed_letters:
        if letter != '_' and letter in available_letters:
            available_letters.remove(letter)        
    
    # Update the text of the available letters label
    available_letters_str = ' '.join(available_letters)
    available_letters_label.config(text=available_letters_str)
    
    solutions = solve_wordle("Aesthene-words.txt", known_letters, confirmed_letters, excluded_letters)
    if solutions:
        results_text.config(state='normal')
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, '\n'.join(solutions))
        results_text.config(state='disabled')
    else:
        results_text.config(state='normal')
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "No solutions found.")
        results_text.config(state='disabled')


def reset_button_click():
    known_entry.delete(0, tk.END)
    confirmed_entry_1.delete(0, tk.END)
    confirmed_entry_1.insert(0, '_')
    confirmed_entry_2.delete(0, tk.END)
    confirmed_entry_2.insert(0, '_')
    confirmed_entry_3.delete(0, tk.END)
    confirmed_entry_3.insert(0, '_')
    confirmed_entry_4.delete(0, tk.END)
    confirmed_entry_4.insert(0, '_')
    confirmed_entry_5.delete(0, tk.END)
    confirmed_entry_5.insert(0, '_')
    excluded_entry.delete(0, tk.END)
    
    # Reset the text of the available letters label
    available_letters_str = ' '.join(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    available_letters_label.config(text=available_letters_str)
    
    results_text.config(state='normal')
    results_text.delete(1.0, tk.END)
    results_text.config(state='disabled')

import tkinter.messagebox

def add_word_button_click():
    new_word = new_word_entry.get().upper()
    if len(new_word) == 5:
        with open(word_list_file, 'r') as file:
            words = file.read().splitlines()
        if new_word in words:
            tkinter.messagebox.showerror(title="Error", message=f"Word '{new_word}' already exists")
        else:
            words.append(new_word)
            words.sort()
            with open(word_list_file, 'w') as file:
                file.write('\n'.join(words))
            tkinter.messagebox.showinfo(title="Success", message=f"Word '{new_word}' added successfully")
    else:
        tkinter.messagebox.showerror(title="Error", message="New word must be 5 letters long")
    new_word_entry.delete(0, tk.END)

def remove_word_button_click():
    word_to_remove = remove_word_entry.get().upper()
    with open(word_list_file, 'r') as file:
        words = file.read().splitlines()
    if word_to_remove in words:
        words.remove(word_to_remove)
        with open(word_list_file, 'w') as file:
            file.write('\n'.join(words))
        tkinter.messagebox.showinfo(title="Success", message=f"Word '{word_to_remove}' removed successfully")
    else:
        tkinter.messagebox.showerror(title="Error", message=f"Word '{word_to_remove}' not found")
    remove_word_entry.delete(0, tk.END)

def on_return(event):
    focused_widget = window.focus_get()
    if focused_widget == solve_button:
        solve_button.invoke()
    elif focused_widget == reset_button:
        reset_button.invoke()
    elif focused_widget == add_word_button:
        add_word_button.invoke()

def load_button_click():
    global word_list_file
    new_word_list_file = word_list_entry.get()
    if os.path.isfile(new_word_list_file):
        word_list_file = new_word_list_file
        tkinter.messagebox.showinfo(title="Success", message=f"Word list file changed to '{word_list_file}'")
    else:
        tkinter.messagebox.showerror(title="Error", message=f"File '{new_word_list_file}' not found")
    word_list_entry.delete(0, tk.END)


def validate_entry(text):
    if len(text) > 1:
        return False
    return True



# Get the directory path of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Load word list from a file named 'Aesthene-words.txt' in the same folder as the script
word_list_file = os.path.join(script_directory, 'Aesthene-words.txt')
word_list = load_word_list(word_list_file)

# Create the GUI window
window = tk.Tk()
window.title("Aesthene's Close Wordle")
window.bind("<Return>", on_return)

vcmd = (window.register(validate_entry), '%P')
confirmed_label = tk.Label(window, text="Confirmed Letters (in their positions):")
confirmed_label.pack()
confirmed_frame = tk.Frame(window)
confirmed_frame.pack()

confirmed_entry_1 = tk.Entry(confirmed_frame, width=3, validate='key', validatecommand=vcmd)
confirmed_entry_1.insert(0, '_')
confirmed_entry_1.pack(side=tk.LEFT)
confirmed_entry_2 = tk.Entry(confirmed_frame, width=3, validate='key', validatecommand=vcmd)
confirmed_entry_2.insert(0, '_')
confirmed_entry_2.pack(side=tk.LEFT)
confirmed_entry_3 = tk.Entry(confirmed_frame, width=3, validate='key', validatecommand=vcmd)
confirmed_entry_3.insert(0, '_')
confirmed_entry_3.pack(side=tk.LEFT)
confirmed_entry_4 = tk.Entry(confirmed_frame, width=3, validate='key', validatecommand=vcmd)
confirmed_entry_4.insert(0, '_')
confirmed_entry_4.pack(side=tk.LEFT)
confirmed_entry_5 = tk.Entry(confirmed_frame, width=3, validate='key', validatecommand=vcmd)
confirmed_entry_5.insert(0, '_')
confirmed_entry_5.pack(side=tk.LEFT)

# Create labels and entry fields
known_label = tk.Label(window, text="Known Letters:")
known_label.pack()
known_entry = tk.Entry(window)
known_entry.pack()

excluded_label = tk.Label(window, text="Excluded Letters:")
excluded_label.pack()
excluded_entry = tk.Entry(window)
excluded_entry.pack()

# Create a label to display the available letters
available_label = tk.Label(window, text="Available Letters:")
available_label.pack()
available_letters_label = tk.Label(window)
available_letters_label.pack()
available_letters_str = ' '.join(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
available_letters_label.config(text=available_letters_str)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

solve_button = tk.Button(button_frame, text="Solve", command=solve_button_click, width=10, height=2)
solve_button.pack()
solve_button.pack(side=tk.LEFT, padx=5)
solve_button.pack()
solve_button.bind("<Return>", on_return)
solve_button.focus_set()

reset_button = tk.Button(button_frame, text="Reset", command=reset_button_click, width=5, height=1)
reset_button.pack()
reset_button.pack(side=tk.RIGHT, padx=5)
reset_button.pack()
reset_button.bind("<Return>", on_return)

results_frame = tk.Frame(window)
results_frame.pack()

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results_text = tk.Text(results_frame, height=10, width=35)
results_text.config(yscrollcommand=scrollbar.set)
results_text.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=results_text.yview)

add_frame = tk.Frame(window)
add_frame.pack(side=tk.LEFT, padx=10)
add_label = tk.Label(add_frame, text="Add Word:")
add_label.pack()
new_word_entry = tk.Entry(add_frame, width=10)
new_word_entry.pack()
add_word_button = tk.Button(add_frame, text="Add", command=add_word_button_click)
add_word_button.pack()

remove_frame = tk.Frame(window)
remove_frame.pack(side=tk.LEFT, padx=10)
remove_label = tk.Label(remove_frame, text="Remove Word:")
remove_label.pack()
remove_word_entry = tk.Entry(remove_frame, width=10)
remove_word_entry.pack()
remove_word_button = tk.Button(remove_frame, text="Remove", command=remove_word_button_click)
remove_word_button.pack()

load_frame = tk.Frame(window)
load_frame.pack(side=tk.RIGHT, padx=10)
word_list_label = tk.Label(load_frame, text="Word List File:")
word_list_label.pack()
word_list_entry = tk.Entry(load_frame, width=15)
word_list_entry.pack()
load_button = tk.Button(load_frame, text="Load", command=load_button_click)
load_button.pack()

# Start the GUI event loop
window.mainloop()
