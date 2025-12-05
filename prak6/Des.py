# des_gui_tabs.py
import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# DES tables (full)
# =========================
PC1 = [
    57,49,41,33,25,17,9,1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,3,28,15,6,21,10,
    23,19,12,4,26,8,16,7,27,20,13,2,
    41,52,31,37,47,55,30,40,51,45,33,48,
    44,49,39,56,34,53,46,42,50,36,29,32
]

LEFT_SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

IP = [
    58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7
]

IP_INV = [
    40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25
]

E = [
    32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,
    12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,
    24,25,26,27,28,29,28,29,30,31,32,1
]

P = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

S_BOX = [
    # S1
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    # S2
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    # S3
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    # S4
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    # S5
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
     [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
     [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
     [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    # S6
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
     [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
     [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
     [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    # S7
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
     [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
     [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
     [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    # S8
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
     [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
     [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
     [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

# =========================
# Utilities
# =========================
def permute(bits: str, table: list) -> str:
    return ''.join(bits[i-1] for i in table)

def left_rotate(bits: str, n: int) -> str:
    return bits[n:] + bits[:n]

def xor_bits(a: str, b: str) -> str:
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

def chunk(s: str, size: int):
    return [s[i:i+size] for i in range(0, len(s), size)]

def sbox_sub(bits48: str) -> str:
    out = ''
    blocks = chunk(bits48, 6)
    for i, blk in enumerate(blocks):
        row = int(blk[0] + blk[5], 2)
        col = int(blk[1:5], 2)
        val = S_BOX[i][row][col]
        out += f'{val:04b}'
    return out

def bitstr_to_hex(bs: str) -> str:
    return f'{int(bs,2):0{len(bs)//4}X}'

# =========================
# GUI helpers
# =========================
def insert_tagged(widget: tk.Text, text: str, tag: str = None):
    if tag:
        widget.insert('end', text + '\n', tag)
    else:
        widget.insert('end', text + '\n')
    widget.see('end')

# =========================
# Generate subkeys (single source)
# =========================
def generate_subkeys(key_bits: str):
    key56 = permute(key_bits, PC1)
    C = key56[:28]; D = key56[28:]
    subkeys = []
    Cs = [C]; Ds = [D]  # optional if want later
    for shift in LEFT_SHIFTS:
        C = left_rotate(C, shift)
        D = left_rotate(D, shift)
        Ki = permute(C + D, PC2)
        subkeys.append(Ki)
        Cs.append(C); Ds.append(D)
    return subkeys, key56, Cs, Ds

# =========================
# Main DES process
# =========================
def process_des():
    pt = entry_plain.get()
    ky = entry_key.get()

    # require 8 ASCII chars
    if len(pt) != 8 or len(ky) != 8:
        messagebox.showerror("Input error", "Plaintext dan Key harus 8 ASCII karakter masing-masing.")
        return

    # clear tabs
    for w in (text_key, text_rounds, text_final):
        w.delete("1.0", "end")

    pt_bits = ''.join(f'{ord(c):08b}' for c in pt)
    ky_bits = ''.join(f'{ord(c):08b}' for c in ky)

    # Key schedule (single generation)
    subkeys, key56, Cs, Ds = generate_subkeys(ky_bits)

    insert_tagged(text_key, "=== KEY SCHEDULE ===", "header")
    insert_tagged(text_key, f"Plaintext (bin): {pt_bits}", "meta")
    insert_tagged(text_key, f"Key (bin):       {ky_bits}", "meta")
    insert_tagged(text_key, f"PC-1 -> 56 bits: {key56}", "pc")
    insert_tagged(text_key, f"C0 = {Cs[0]}", "meta")
    insert_tagged(text_key, f"D0 = {Ds[0]}", "meta")
    for i, (c,d,k) in enumerate(zip(Cs[1:], Ds[1:], subkeys), start=1):
        insert_tagged(text_key, f"--- Round {i} (shift={LEFT_SHIFTS[i-1]}) ---", "round")
        insert_tagged(text_key, f" C{i} = {c}", "meta")
        insert_tagged(text_key, f" D{i} = {d}", "meta")
        insert_tagged(text_key, f" K{i:02} = {k}", "pc")
    insert_tagged(text_key, "\n=== ALL SUBKEYS (K1..K16) ===", "header")
    for idx,k in enumerate(subkeys, start=1):
        insert_tagged(text_key, f"K{idx:02}: {k}", "pc")
    text_key.see("end")

    # Initial Permutation
    IPout = permute(pt_bits, IP)
    L = IPout[:32]; R = IPout[32:]
    insert_tagged(text_rounds, "=== INITIAL PERMUTATION (IP) ===", "header")
    insert_tagged(text_rounds, f"After IP: {IPout}", "meta")
    insert_tagged(text_rounds, f"L0 = {L}", "meta")
    insert_tagged(text_rounds, f"R0 = {R}", "meta")

    # 16 rounds using same subkeys
    for r in range(1,17):
        insert_tagged(text_rounds, f"--- ROUND {r} ---", "round")
        Eout = permute(R, E)
        insert_tagged(text_rounds, f"E(R{r-1}) = {Eout}", "meta")
        Ki = subkeys[r-1]
        insert_tagged(text_rounds, f"Using K{r:02}: {Ki}", "pc")
        xor_out = xor_bits(Eout, Ki)
        insert_tagged(text_rounds, f"XOR with K{r:02}: {xor_out}", "xor")
        s_out = sbox_sub(xor_out)
        insert_tagged(text_rounds, f"S-box output: {s_out}", "sbox")
        p_out = permute(s_out, P)
        insert_tagged(text_rounds, f"P-permutation: {p_out}", "pbox")
        newR = xor_bits(L, p_out)
        newL = R
        insert_tagged(text_rounds, f"L{r} = {newL}", "meta")
        insert_tagged(text_rounds, f"R{r} = {newR}", "meta")
        L, R = newL, newR
    text_rounds.see("end")

    # Final
    preoutput = R + L
    finalbits = permute(preoutput, IP_INV)
    finalhex = bitstr_to_hex(finalbits)
    insert_tagged(text_final, "=== PREOUTPUT (R16||L16) ===", "header")
    insert_tagged(text_final, preoutput, "meta")
    insert_tagged(text_final, "=== FINAL PERMUTATION (IP^-1) ===", "header")
    insert_tagged(text_final, finalbits, "final")
    insert_tagged(text_final, f"Cipher (HEX): {finalhex}", "final")
    text_final.see("end")

    nb.select(1)  # show rounds tab

# =========================
# Build UI (version A: 3 tabs)
# =========================
root = tk.Tk()
root.title("DES — KeySchedule | Rounds | Final — Sayangku 💙")
root.geometry("1150x760")

top = ttk.Frame(root, padding=8)
top.pack(fill='x')

ttk.Label(top, text="Plaintext (8 ASCII):").grid(row=0, column=0, sticky='w')
entry_plain = ttk.Entry(top, width=30)
entry_plain.grid(row=0, column=1, padx=6)
entry_plain.insert(0, "")

ttk.Label(top, text="Key (8 ASCII):").grid(row=1, column=0, sticky='w')
entry_key = ttk.Entry(top, width=30)
entry_key.grid(row=1, column=1, padx=6)
entry_key.insert(0, "")

# colored button style
style = ttk.Style()
style.theme_use('clam')
style.configure("Accent.TButton", background="#1E90FF", foreground="white", padding=6, font=("Segoe UI",11,"bold"))
# (ttk buttons on some platforms ignore bg; we'll also create a tk.Button for stronger color)
btn_run = tk.Button(top, text="🔐 Proses DES", bg="#1E90FF", fg="white", font=("Segoe UI",11,"bold"), command=process_des)
btn_run.grid(row=0, column=2, rowspan=2, padx=12)

# Notebook with 3 tabs
nb = ttk.Notebook(root)
nb.pack(fill='both', expand=True, padx=8, pady=8)

text_key = tk.Text(nb, font=("Consolas", 10), wrap='none')
text_rounds = tk.Text(nb, font=("Consolas", 10), wrap='none')
text_final = tk.Text(nb, font=("Consolas", 10), wrap='none')

nb.add(text_key, text="Key Schedule")
nb.add(text_rounds, text="Rounds")
nb.add(text_final, text="Final")

# dark styling for text widgets
for w in (text_key, text_rounds, text_final):
    w.configure(bg="#1e1e1e", fg="#e6e6e6", insertbackground="#ffffff")

# text tags (colors)
styles = {
    "header": {"foreground":"#FFD087", "font":("Consolas",10,"bold")},
    "pc": {"foreground":"#7FFFD4"},
    "xor": {"foreground":"#FFD700"},
    "sbox": {"foreground":"#DA70D6"},
    "pbox": {"foreground":"#87CEFA"},
    "round": {"foreground":"#00BFFF", "font":("Consolas",10,"bold")},
    "final": {"foreground":"#98FB98", "font":("Consolas",10,"bold")},
    "meta": {"foreground":"#e6e6e6"}
}

for w in (text_key, text_rounds, text_final):
    for tag, cfg in styles.items():
        w.tag_configure(tag, **cfg)

# small helper navigation buttons under notebook
nav = ttk.Frame(root, padding=6)
nav.pack(fill='x')
ttk.Button(nav, text="➡ Key", command=lambda: nb.select(0)).pack(side='left', padx=4)
ttk.Button(nav, text="➡ Rounds", command=lambda: nb.select(1)).pack(side='left', padx=4)
ttk.Button(nav, text="➡ Final", command=lambda: nb.select(2)).pack(side='left', padx=4)

# Clear button
def clear_all():
    for w in (text_key, text_rounds, text_final):
        w.delete("1.0", "end")
ttk.Button(nav, text="Clear", command=clear_all).pack(side='right', padx=6)

root.mainloop()
