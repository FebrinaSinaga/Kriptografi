import tkinter as tk
from tkinter import ttk, messagebox

# ================================================================
#                     DES TABLES & CONSTANTS
# ================================================================

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

LEFT_SHIFTS = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
]

E_TABLE = [
    32, 1, 2, 3, 4, 5,
    4,  5, 6, 7, 8, 9,
    8,  9, 10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16,7,20,21,
    29,12,28,17,
    1,15,23,26,
    5,18,31,10,
    2,8,24,14,
    32,27,3,9,
    19,13,30,6,
    22,11,4,25
]

S_BOX = [[
    [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
]]

# ================================================================
# DES UTILITIES
# ================================================================
def permute(bits, table):
    return "".join(bits[i - 1] for i in table)

def left_rotate(s, n):
    return s[n:] + s[:n]

def xor(a, b):
    return "".join("1" if x != y else "0" for x, y in zip(a, b))

def sbox_substitution(bits48):
    out = ""
    for i in range(8):
        chunk = bits48[i * 6:(i + 1) * 6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        val = S_BOX[0][row][col]
        out += f"{val:04b}"
    return out


# ================================================================
#           INSERT COLOR TEXT
# ================================================================
def insert_tag(widget, text, tag="normal"):
    widget.insert("end", text + "\n", tag)
    widget.see("end")


# ================================================================
#                     MAIN DES PROCESS
# ================================================================
def process_des():

    plaintext = entry_plain.get()
    key = entry_key.get()

    if len(plaintext) != 8:
        messagebox.showerror("Error", "Plaintext harus 8 karakter!")
        return
    if len(key) != 8:
        messagebox.showerror("Error", "Key harus 8 karakter!")
        return

    txt_key.delete("1.0", "end")
    txt_rounds.delete("1.0", "end")
    txt_final.delete("1.0", "end")
    txt_summary.delete("1.0", "end")

    p_bin = ''.join(f"{ord(c):08b}" for c in plaintext)
    k_bin = ''.join(f"{ord(c):08b}" for c in key)

    insert_tag(txt_key, "=== INPUT DATA ===", "header")
    insert_tag(txt_key, f"Plaintext  : {plaintext}")
    insert_tag(txt_key, f"Binary     : {p_bin}")
    insert_tag(txt_key, f"Key        : {key}")
    insert_tag(txt_key, f"Key Binary : {k_bin}\n")

    # PC-1
    insert_tag(txt_key, "=== PC-1 ===", "header")
    key56 = permute(k_bin, PC1)
    insert_tag(txt_key, f"PC-1 (56 bit) = {key56}")

    C = key56[:28]
    D = key56[28:]

    insert_tag(txt_key, f"C0 = {C}", "meta")
    insert_tag(txt_key, f"D0 = {D}\n", "meta")

    subkeys = []

    insert_tag(txt_key, "=== SHIFT + PC-2 (K1–K16) ===", "header")
    for i, shift in enumerate(LEFT_SHIFTS, start=1):

        C = left_rotate(C, shift)
        D = left_rotate(D, shift)

        insert_tag(txt_key, f"Round {i} — Shift {shift}", "round")
        insert_tag(txt_key, f"  C{i} = {C}", "meta")
        insert_tag(txt_key, f"  D{i} = {D}", "meta")

        Ki = permute(C + D, PC2)
        subkeys.append(Ki)

        insert_tag(txt_key, f"  K{i:02} = {Ki}\n", "pc")

    insert_tag(txt_key, "=== SEMUA SUBKEY ===", "header")
    for i, k in enumerate(subkeys, start=1):
        insert_tag(txt_key, f"K{i:02}: {k}", "pc")

    # INITIAL PERMUTATION
    insert_tag(txt_rounds, "=== INITIAL PERMUTATION ===", "header")
    ip = permute(p_bin, IP)
    L = ip[:32]
    R = ip[32:]

    insert_tag(txt_rounds, f"L0 = {L}")
    insert_tag(txt_rounds, f"R0 = {R}\n")

    # ROUNDS 1–16
    for i in range(16):
        insert_tag(txt_rounds, f"=== ROUND {i+1} ===", "round")

        E = permute(R, E_TABLE)
        insert_tag(txt_rounds, f"E(R) = {E}")

        X = xor(E, subkeys[i])
        insert_tag(txt_rounds, f"XOR = {X}")

        S = sbox_substitution(X)
        insert_tag(txt_rounds, f"S-BOX = {S}")

        Pm = permute(S, P)
        insert_tag(txt_rounds, f"P = {Pm}")

        newR = xor(L, Pm)
        newL = R

        insert_tag(txt_rounds, f"L{i+1} = {newL}")
        insert_tag(txt_rounds, f"R{i+1} = {newR}")

        L, R = newL, newR

    # FINAL PERMUTATION
    insert_tag(txt_final, "=== FINAL PERMUTATION ===", "header")

    final_bin = permute(R + L, IP_INV)
    hex_out = hex(int(final_bin, 2))[2:].upper()

    insert_tag(txt_final, f"Final Binary: {final_bin}", "pc")
    insert_tag(txt_final, f"Final Hex   : {hex_out}", "pc")

    # SUMMARY
    insert_tag(txt_summary, "=== RINGKASAN HASIL ===", "header")
    insert_tag(txt_summary, f"Plaintext : {plaintext}")
    insert_tag(txt_summary, f"Key       : {key}")
    insert_tag(txt_summary, f"Cipher    : {hex_out}", "pc")


# ================================================================
#                           GUI WINDOW
# ================================================================
root = tk.Tk()
root.title("DES Complete Process — Sayangku 💙")
root.geometry("1150x770")
root.configure(bg="#F8F9FA")

style = ttk.Style()
style.theme_use("clam")

# BUTTON COLORS
style.configure("BlueRound.TButton",
                foreground="white", background="#1E90FF",
                padding=8, font=("Segoe UI", 11, "bold"))
style.configure("GreenRound.TButton",
                foreground="white", background="#28A745",
                padding=8, font=("Segoe UI", 11, "bold"))
style.configure("RedRound.TButton",
                foreground="white", background="#DC3545",
                padding=8, font=("Segoe UI", 11, "bold"))
style.configure("PurpleRound.TButton",
                foreground="white", background="#6F42C1",
                padding=8, font=("Segoe UI", 11, "bold"))

# ================================================================
#                        INPUT FRAME
# ================================================================
frm_input = tk.Frame(root, bg="#F8F9FA")
frm_input.pack(pady=10)

tk.Label(frm_input, text="Plaintext (8 char):", bg="#F8F9FA",
         font=("Segoe UI", 12)).grid(row=0, column=0, padx=5)
entry_plain = tk.Entry(frm_input, font=("Consolas", 12), width=20)
entry_plain.grid(row=0, column=1)

tk.Label(frm_input, text="Key (8 char):", bg="#F8F9FA",
         font=("Segoe UI", 12)).grid(row=1, column=0, padx=5)
entry_key = tk.Entry(frm_input, font=("Consolas", 12), width=20)
entry_key.grid(row=1, column=1)

btn_process = ttk.Button(frm_input, text="🔐 PROSES DES",
                         style="BlueRound.TButton",
                         command=process_des)
btn_process.grid(row=0, column=2, padx=10, rowspan=2)

def clear_all():
    txt_key.delete("1.0", "end")
    txt_rounds.delete("1.0", "end")
    txt_final.delete("1.0", "end")
    txt_summary.delete("1.0", "end")

btn_clear = ttk.Button(frm_input, text="🗑 Clear",
                       style="RedRound.TButton",
                       command=clear_all)
btn_clear.grid(row=2, column=0, pady=5)

btn_to_final = ttk.Button(frm_input, text="➡ Final",
                          style="PurpleRound.TButton",
                          command=lambda: nb.select(2))
btn_to_final.grid(row=2, column=1)

btn_to_summary = ttk.Button(frm_input, text="➡ Summary",
                            style="GreenRound.TButton",
                            command=lambda: nb.select(3))
btn_to_summary.grid(row=2, column=2)

# 👉 Tambahan tombol Rounds yg hilang
btn_to_rounds = ttk.Button(frm_input, text="➡ Rounds",
                           style="BlueRound.TButton",
                           command=lambda: nb.select(1))
btn_to_rounds.grid(row=2, column=3, padx=10)

# ================================================================
#                         NOTEBOOK TABS
# ================================================================
nb = ttk.Notebook(root)
nb.pack(expand=True, fill="both")

# Key Tab
tab_key = tk.Frame(nb)
txt_key = tk.Text(tab_key, font=("Consolas", 10), bg="#FFFFFF", fg="black")
txt_key.pack(expand=True, fill="both")
nb.add(tab_key, text="Key Schedule")

# Rounds Tab
tab_rounds = tk.Frame(nb)
txt_rounds = tk.Text(tab_rounds, font=("Consolas", 10), bg="#FFFFFF", fg="black")
txt_rounds.pack(expand=True, fill="both")
nb.add(tab_rounds, text="Rounds")

# Final Tab
tab_final = tk.Frame(nb)
txt_final = tk.Text(tab_final, font=("Consolas", 10), bg="#FFFFFF", fg="black")
txt_final.pack(expand=True, fill="both")
nb.add(tab_final, text="Final")

# Summary Tab
tab_summary = tk.Frame(nb)
txt_summary = tk.Text(tab_summary, font=("Consolas", 11), bg="#FFFFFF", fg="black")
txt_summary.pack(expand=True, fill="both")
nb.add(tab_summary, text="Summary")

# COLOR TAGS
for txt in (txt_key, txt_rounds, txt_final, txt_summary):
    txt.tag_configure("header", foreground="#A11F65", font=("Consolas", 11, "bold"))
    txt.tag_configure("round", foreground="#1E90FF", font=("Consolas", 10, "bold"))
    txt.tag_configure("pc", foreground="#0A640A", font=("Consolas", 10, "bold"))
    txt.tag_configure("meta", foreground="#000000", font=("Consolas", 10))
    txt.tag_configure("normal", foreground="#000000", font=("Consolas", 10))

root.mainloop()
