import tkinter as tk
from tkinter import messagebox
import random, math

# ======================================
#  FUNGSI DASAR RSA
# ======================================

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

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
    return [int.from_bytes(data[i:i+max_bytes],'big')
            for i in range(0, len(data), max_bytes)]

def blocks_to_string(blocks, n):
    max_bytes = max(1, (n.bit_length() - 1) // 8)
    parts = []
    for b in blocks:
        parts.append(b.to_bytes(max_bytes,'big').lstrip(b'\x00'))
    return b"".join(parts).decode(errors="replace")

def rsa_encrypt(blocks, e, n):
    return [pow(b, e, n) for b in blocks]

def rsa_decrypt(blocks, d, n):
    return [pow(c, d, n) for c in blocks]

# ======================================
#  GENERATE RANDOM KEY
# ======================================

def generate_key():
    primes = [x for x in range(50, 201) if is_prime(x)]
    p = random.choice(primes)
    q = random.choice(primes)
    while q == p:
        q = random.choice(primes)

    n = p * q
    phi = (p - 1) * (q - 1)

    candidates = [x for x in range(3, phi) if math.gcd(x, phi) == 1]
    e = random.choice(candidates)
    d = modinv(e, phi)

    return p, q, n, phi, e, d

# ======================================
#  PROSES LATIHAN 2
# ======================================

def proses_latihan2():
    plaintext = entry_plain.get().strip()
    if plaintext == "":
        messagebox.showerror("Error", "Masukkan plaintext!")
        return

    p, q, n, phi, e, d = generate_key()

    blocks = string_to_blocks(plaintext, n)
    cipher = rsa_encrypt(blocks, e, n)
    decrypted = rsa_decrypt(cipher, d, n)
    hasil = blocks_to_string(decrypted, n)

    output = f"""
╔══════════════════════════╗
   RSA LATIHAN 2 (Acak)
╚══════════════════════════╝

p = {p}
q = {q}
n = {n}
phi(n) = {phi}

Public key  : (e = {e}, n = {n})
Private key : (d = {d}, n = {n})

--- ENKRIPSI ---
Blok plaintext  : {blocks}
Blok cipher     : {cipher}

--- DEKRIPSI ---
Blok decrypt    : {decrypted}
Hasil plaintext : {hasil}
"""

    text_output.delete("1.0", "end")
    text_output.insert("end", output)

# ======================================
#  GUI SUPER CANTIK (perbaikan posisi)
# ======================================

root = tk.Tk()
root.title("✨ RSA Generator (Acak) ✨")
root.geometry("720x650")
root.configure(bg="#F4E8FF")  # pastel lavender

# CARD CONTAINER
frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="groove")
# Tambah height agar muat semua widget (label, entry, tombol)
frame.place(relx=0.5, rely=0.08, anchor="n", width=600, height=220)
# Pastikan frame tidak mengecil otomatis (pack/grid propagation)
frame.pack_propagate(False)

title = tk.Label(frame, text="🔐 RSA (p, q, e Acak)",
                 font=("Poppins", 18, "bold"),
                 bg="#FFFFFF", fg="#7B2CBF")
title.pack(pady=(12, 6))

label_plain = tk.Label(frame, text="Masukkan Plaintext:",
                       font=("Poppins", 12),
                       bg="#EDC7F0", fg="#5A189A")
label_plain.pack()

entry_plain = tk.Entry(frame, width=45, font=("Poppins", 12),
                       bg="#E5E2E9", fg="#240046", relief="flat",
                       highlightbackground="#7B2CBF", highlightthickness=1,
                       insertbackground="#240046")
entry_plain.pack(pady=6)

# TOMBOL
btn = tk.Button(frame, text="🚀 Generate & Proses RSA",
                font=("Poppins", 12, "bold"),
                bg="#9D4EDD", fg="white",
                activebackground="#7B2CBF",
                relief="flat", padx=15, pady=6,
                command=proses_latihan2)
btn.pack(pady=(6, 12))

# OUTPUT BOX (Console style)
# Pindahkan ke posisi lebih bawah supaya tidak menimpa frame
text_output = tk.Text(root, width=85, height=20,
                      bg="#E5DEEC", fg="#015F1D",
                      font=("Consolas", 10), relief="flat",
                      insertbackground="white")
# gunakan rely yang lebih besar agar berada di bawah frame
text_output.place(relx=0.5, rely=0.45, anchor="n")

root.mainloop()
