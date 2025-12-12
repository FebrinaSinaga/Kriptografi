import tkinter as tk
from tkinter import ttk, messagebox
import math

# =========================
# RSA FUNCTIONS (unchanged)
# =========================

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("Tidak ada invers modular")
    return x % m

def string_to_blocks(s, n):
    data = s.encode("utf-8")
    max_bytes = max(1, (n.bit_length() - 1) // 8)
    blocks = []
    for i in range(0, len(data), max_bytes):
        chunk = data[i:i+max_bytes]
        blocks.append(int.from_bytes(chunk, 'big'))
    return blocks

def blocks_to_string(blocks, n):
    max_bytes = max(1, (n.bit_length() - 1) // 8)
    pieces = []
    for block in blocks:
        piece = block.to_bytes(max_bytes, 'big').lstrip(b'\x00')
        pieces.append(piece)
    return b''.join(pieces).decode('utf-8', errors='replace')

def rsa_encrypt(blocks, e, n):
    return [pow(m, e, n) for m in blocks]

def rsa_decrypt(blocks, d, n):
    return [pow(c, d, n) for c in blocks]


# =================================
# GUI: Blue Butterfly Elegant Theme
# =================================

def create_gradient_canvas(parent, width, height, colors):
    """Simple vertical gradient using stacked rectangles"""
    c = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    step_h = height // len(colors)
    for i, col in enumerate(colors):
        c.create_rectangle(0, i*step_h, width, (i+1)*step_h, fill=col, outline=col)
    return c

def proses_latihan1():
    # fixed parameters
    p, q, e = 17, 11, 7
    n = p * q
    phi = (p - 1) * (q - 1)
    try:
        d = modinv(e, phi)
    except Exception as ex:
        messagebox.showerror("Error", f"Gagal hitung d: {ex}")
        return

    plaintext = entry_plain.get().strip()
    if plaintext == "":
        messagebox.showerror("Input Kosong", "Masukkan plaintext terlebih dahulu.")
        return

    # proses
    blocks = string_to_blocks(plaintext, n)
    cipher = rsa_encrypt(blocks, e, n)
    decrypted = rsa_decrypt(cipher, d, n)
    hasil = blocks_to_string(decrypted, n)

    # tampilkan hasil di output
    output = (
        "╔════════════════ RSA LATIHAN 1 ════════════════╗\n"
        "               (p=17, q=11, e=7) \n"
        "╚══════════════════════════════════════════════╝\n\n"
        f"p = {p}\nq = {q}\nn = {n}\nphi(n) = {phi}\n\n"
        f"Public key (e,n): ({e}, {n})\nPrivate key (d,n): ({d}, {n})\n\n"
        "--- ENKRIPSI ---\n"
        f"Blok plaintext : {blocks}\n"
        f"Blok cipher    : {cipher}\n\n"
        "--- DEKRIPSI ---\n"
        f"Blok dekripsi  : {decrypted}\n"
        f"Hasil plaintext: {hasil}\n"
    )
    text_output.config(state="normal")
    text_output.delete("1.0", "end")
    text_output.insert("1.0", output)
    text_output.config(state="disabled")


# Build window
root = tk.Tk()
root.title("RSA Latihan 1🐳")
root.geometry("760x640")
root.resizable(False, False)

# Background gradient (frame)
bg_colors = ["#E8F6FF", "#DCEEFF", "#DAEBFD"]  # soft blue gradient
bg_canvas = create_gradient_canvas(root, 760, 640, bg_colors)
bg_canvas.place(x=0, y=0)

# White card container (center)
card = tk.Frame(root, bg="white", bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=680, height=560)

# Title + butterfly icon
title_frame = tk.Frame(card, bg="white")
title_frame.pack(fill="x", pady=(18, 6))
lbl_icon = tk.Label(title_frame, text="🦋", font=("Segoe UI Emoji", 26), bg="white")
lbl_icon.pack(side="left", padx=(18,10))
lbl_title = tk.Label(title_frame, text="RSA Latihan 1 - Don,t Forget To Smile Bg❤️",
                     font=("Segoe UI", 16, "bold"), bg="white", fg="#124E8C")
lbl_title.pack(side="left")

# separator
sep = tk.Frame(card, bg="#FFFFFF", height=2)
sep.pack(fill="x", padx=18, pady=(6, 12))

# Input area frame (rounded-like with padding)
input_frame = tk.Frame(card, bg="#FBFDFF")
input_frame.pack(padx=18, pady=8, fill="x")

lbl_plain = tk.Label(input_frame, text="Masukkan Plaintext:", bg="#FBFDFF",
                     fg="#0B3D91", font=("Segoe UI", 12))
lbl_plain.pack(anchor="w", pady=(8,4), padx=8)

entry_plain = tk.Entry(input_frame, font=("Segoe UI", 12), bd=0, relief="flat",
                       bg="#FBFCFC", fg="#091E36", insertbackground="#080B0E")
entry_plain.pack(fill="x", padx=8, pady=(0,10))

# Button row
btn_frame = tk.Frame(card, bg="white")
btn_frame.pack(padx=18, pady=(4,12), fill="x")

def on_enter(e):
    btn_proses.config(bg="#3EA0FF")
def on_leave(e):
    btn_proses.config(bg="#50B3FF")

btn_proses = tk.Button(btn_frame, text="Proses RSA", command=proses_latihan1,
                       bg="#50B3FF", fg="white", bd=0, relief="raised",
                       font=("Segoe UI Semibold", 12), padx=12, pady=8)
btn_proses.pack(side="left", padx=(8,6))
btn_proses.bind("<Enter>", on_enter)
btn_proses.bind("<Leave>", on_leave)

# Clear button
def clear_all():
    entry_plain.delete(0, "end")
    text_output.config(state="normal")
    text_output.delete("1.0", "end")
    text_output.config(state="disabled")

btn_clear = tk.Button(btn_frame, text="Clear", command=clear_all,
                      bg="#F0F4FF", fg="#0C1A2A", bd=0,
                      font=("Segoe UI", 11), padx=10, pady=8)
btn_clear.pack(side="left", padx=6)

# Output box label
lbl_out = tk.Label(card, text="Output (debug):", bg="white", fg="#022054",
                   font=("Segoe UI", 12, "bold"))
lbl_out.pack(anchor="w", padx=18, pady=(6,0))

# Output text area (styled)
text_output = tk.Text(card, bg="#F6FBFF", fg="#041A2F", font=("Consolas", 10),
                      bd=0, relief="flat", wrap="word")
text_output.pack(padx=18, pady=8, fill="both", expand=True)
text_output.config(state="disabled")

# Small footer
footer = tk.Label(card, text="p=17, q=11, e=7  •  RSA demo (enkripsi + dekripsi)",
                  bg="white", fg="#E658C0", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=8)

root.mainloop()
