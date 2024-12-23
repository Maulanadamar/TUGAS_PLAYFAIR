import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def generate_key_matrix(key):
    key = key.upper().replace("J", "I")
    key = "".join(dict.fromkeys(key))  # Remove duplicate characters
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_matrix = list(key)

    for char in alphabet:
        if char not in key_matrix:
            key_matrix.append(char)

    return [key_matrix[i:i + 5] for i in range(0, 25, 5)]

def prepare_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    prepared_text = []

    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i + 1]:
            prepared_text.append(text[i])
            prepared_text.append('X')
            i += 1
        else:
            prepared_text.append(text[i])
            i += 1

    if len(prepared_text) % 2 != 0:
        prepared_text.append('X')

    return prepared_text

def find_position(matrix, char):
    for row_index, row in enumerate(matrix):
        if char in row:
            return row_index, row.index(char)
    return None

def playfair_cipher(matrix, text, encrypt=True):
    result = []
    step = 1 if encrypt else -1

    for i in range(0, len(text), 2):
        ch1, ch2 = text[i], text[i + 1]
        row1, col1 = find_position(matrix, ch1)
        row2, col2 = find_position(matrix, ch2)

        if row1 == row2:  # Same row
            result.append(matrix[row1][(col1 + step) % 5])
            result.append(matrix[row2][(col2 + step) % 5])
        elif col1 == col2:  # Same column
            result.append(matrix[(row1 + step) % 5][col1])
            result.append(matrix[(row2 + step) % 5][col2])
        else:  # Rectangle
            result.append(matrix[row1][col2])
            result.append(matrix[row2][col1])

    return "".join(result)

def encrypt_action():
    plain_text = plain_text_entry.get()
    key = key_entry.get()

    if not plain_text or not key:
        messagebox.showerror("Input Error", "Both Plain Text and Key are required!")
        return

    key_matrix = generate_key_matrix(key)
    prepared_text = prepare_text(plain_text)
    encrypted_text = playfair_cipher(key_matrix, prepared_text, encrypt=True)

    steps_text.delete(1.0, tk.END)
    steps_text.insert(tk.END, "Key Matrix:\n")
    for row in key_matrix:
        steps_text.insert(tk.END, f"{row}\n")

    steps_text.insert(tk.END, f"\nPrepared Text: {' '.join(prepared_text)}\n")
    steps_text.insert(tk.END, f"Encrypted Text: {encrypted_text}\n")

    result_label.config(text=f"Encrypted Text: {encrypted_text}")

def decrypt_action():
    encrypted_text = plain_text_entry.get()
    key = key_entry.get()

    if not encrypted_text or not key:
        messagebox.showerror("Input Error", "Both Encrypted Text and Key are required!")
        return

    key_matrix = generate_key_matrix(key)
    prepared_text = prepare_text(encrypted_text)
    decrypted_text = playfair_cipher(key_matrix, prepared_text, encrypt=False)

    steps_text.delete(1.0, tk.END)
    steps_text.insert(tk.END, "Key Matrix:\n")
    for row in key_matrix:
        steps_text.insert(tk.END, f"{row}\n")

    steps_text.insert(tk.END, f"\nPrepared Text: {' '.join(prepared_text)}\n")
    steps_text.insert(tk.END, f"Decrypted Text: {decrypted_text}\n")

    result_label.config(text=f"Decrypted Text: {decrypted_text}")

# Create the main window
root = tk.Tk()
root.title("Playfair Cipher")
root.geometry("800x600")
root.configure(bg="#f7f9fc")

# Title Label
title_label = tk.Label(root, text="TUGAS KRIPTOGRAFI", font=("Arial", 20, "bold"), bg="#f7f9fc", fg="#007acc")
title_label.pack(pady=15)

# Frame for input fields
input_frame = tk.Frame(root, bg="#f7f9fc")
input_frame.pack(pady=10)

# Plain Text Label and Entry
plain_text_label = tk.Label(input_frame, text="Plain Text / Encrypted Text:", bg="#f7f9fc", font=("Arial", 12))
plain_text_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
plain_text_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bd=2, relief="solid")
plain_text_entry.grid(row=0, column=1, padx=10, pady=5)

# Key Label and Entry
key_label = tk.Label(input_frame, text="Key:", bg="#f7f9fc", font=("Arial", 12))
key_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
key_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bd=2, relief="solid")
key_entry.grid(row=1, column=1, padx=10, pady=5)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f7f9fc")
button_frame.pack(pady=15)

# Encrypt and Decrypt Buttons
encrypt_button = ttk.Button(button_frame, text="Encrypt", command=encrypt_action)
encrypt_button.grid(row=0, column=0, padx=15, pady=10)

decrypt_button = ttk.Button(button_frame, text="Decrypt", command=decrypt_action)
decrypt_button.grid(row=0, column=1, padx=15, pady=10)

# Result Label
result_label = tk.Label(root, text="HASIL AKAN DITAMPILKAN DISINI", wraplength=600, bg="#f7f9fc", font=("Arial", 14), fg="#007f3f")
result_label.pack(pady=15)

# Steps Text Area
steps_label = tk.Label(root, text="Steps:", bg="#f7f9fc", font=("Arial", 12, "bold"))
steps_label.pack(pady=5)
steps_text = tk.Text(root, height=15, width=80, font=("Courier New", 10), bg="#eaf4fc", fg="#333333", wrap=tk.WORD, bd=2, relief="solid")
steps_text.pack(pady=10)

# Run the application
root.mainloop()
