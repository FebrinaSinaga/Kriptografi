import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# AES S-BOX + RCON (standar)
# -----------------------------
SBOX = [
    0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
    0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
    0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
    0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
    0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
    0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
    0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
    0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
    0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
    0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
    0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
    0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
    0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
    0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
    0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
    0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# -----------------------------
# Helper Functions
# -----------------------------
def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [SBOX[b] for b in word]

def to_hexbytes_from_text(s):
    return [ord(c) for c in s]

def hex_list_str(lst):
    return " ".join(f"{b:02X}" for b in lst)

# -----------------------------
# PRINT W DALAM BENTUK KOLOM (BENAR!)
# -----------------------------
def print_words_column(output, block):
    output.insert(tk.END, "W4   W3   W2   W1\n")
    order = [3, 2, 1, 0]  # W3 W2 W1 W0

    for r in range(4):
        line = ""
        for c in order:
            line += f"{block[c][r]:02X} ".ljust(6)
        output.insert(tk.END, line + "\n")
    output.insert(tk.END, "\n")

# -----------------------------
# AES KEY EXPANSION (FULL PROCESS)
# -----------------------------
def generate_key_schedule_and_print(key_text, output):

    if len(key_text) != 16:
        messagebox.showerror("Error", "CipherKey harus 16 karakter!")
        return

    key_bytes = to_hexbytes_from_text(key_text)
    W = [key_bytes[i*4:(i+1)*4] for i in range(4)]

    output.insert(tk.END, "===== W0 – W3 =====\n")
    print_words_column(output, W)

    for i in range(4, 44):

        prev = W[i-1]
        output.insert(tk.END, f"===== PROSES W{i} =====\n")
        output.insert(tk.END, f"Wi-1 : {hex_list_str(prev)}\n")

        if i % 4 == 0:
            rot = rot_word(prev)
            output.insert(tk.END, f"RotWord : {hex_list_str(rot)}\n")

            sub = sub_word(rot)
            output.insert(tk.END, f"SubWord : {hex_list_str(sub)}\n")

            r = RCON[(i//4)-1]
            sub[0] ^= r
            output.insert(tk.END, f"XOR RCON ({r:02X}) : {hex_list_str(sub)}\n")

            temp = sub
        else:
            temp = prev

        wim4 = W[i-4]
        new_w = [(temp[j] ^ wim4[j]) for j in range(4)]

        output.insert(tk.END, f"Hasil W{i}: {hex_list_str(new_w)}\n\n")

        W.append(new_w)

        if (i+1) % 4 == 0:
            block = W[i-3:i+1]
            output.insert(tk.END, f"===== W{i-3} – W{i} =====\n")
            print_words_column(output, block)

# ==========================================================
# GUI — PINKI GIRL EDITION 🎀💗
# ==========================================================
root = tk.Tk()
root.title("AES Key Schedule🎀")
root.geometry("950x750")
root.configure(bg="#daa6c9")

BG_MAIN = "#cea4c1"
BG_FRAME = "#cf8ab5"
BG_TEXTBOX = "#e7e8e1"
BTN_PINK = "#05456D"
TXT_PINK = "#200f18"

title = tk.Label(
    root,
    text="✨ AES KEY SCHEDULE — PRAKTIKUM 8  ✨",
    font=("Segoe UI", 18, "bold"), bg=BG_MAIN, fg=TXT_PINK
)
title.pack(pady=15)

main_frame = tk.Frame(root, bg=BG_MAIN)
main_frame.pack(fill="both", expand=True)

input_frame = tk.LabelFrame(
    main_frame,
    text=" 🎀 Input Cipher Key 🎀 ",
    bg=BG_FRAME, fg=TXT_PINK,
    font=("Segoe UI", 12, "bold"),
    padx=10, pady=10
)
input_frame.pack(fill="x", pady=10)

label = tk.Label(
    input_frame,
    text="CipherKey (16 karakter):",
    font=("Segoe UI", 10, "bold"), bg=BG_FRAME, fg=TXT_PINK
)
label.pack(anchor="w")

entry_key = tk.Entry(
    input_frame, width=40,
    font=("Consolas", 11),
    bg="white", fg=TXT_PINK,
    insertbackground=TXT_PINK
)
entry_key.insert(0, "UNIKASANTOTHOMAS")
entry_key.pack(anchor="w", pady=5)

btn_frame = tk.Frame(main_frame, bg=BG_MAIN)
btn_frame.pack(anchor="w", pady=10)

def style(btn):
    btn.configure(
        bg=BTN_PINK, fg="white",
        activebackground="#541931",
        relief="flat",
        padx=12, pady=6,
        font=("Segoe UI", 10, "bold")
    )

def on_generate():
    output.delete("1.0", tk.END)
    generate_key_schedule_and_print(entry_key.get(), output)

btn_gen = tk.Button(btn_frame, text="GENERATE", command=on_generate)
style(btn_gen)
btn_gen.pack(side="left", padx=5)

def on_clear():
    output.delete("1.0", tk.END)

btn_clear = tk.Button(btn_frame, text="CLEAR", command=on_clear)
style(btn_clear)
btn_clear.pack(side="left", padx=5)

output_frame = tk.LabelFrame(
    main_frame,
    text=" 💗 Output Proses Key Expansion AES 💗 ",
    bg=BG_FRAME, fg=TXT_PINK,
    font=("Segoe UI", 12, "bold"),
    padx=10, pady=10
)
output_frame.pack(fill="both", expand=True)

output = tk.Text(
    output_frame, width=115, height=35,
    bg=BG_TEXTBOX, fg=TXT_PINK,
    font=("Consolas", 10),
    relief="solid", borderwidth=2,
    insertbackground=TXT_PINK
)
output.pack(fill="both", expand=True)

root.mainloop()
