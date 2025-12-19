import tkinter as tk

# =============================
# WARNA & FONT
# =============================
BG_MAIN = "#b2c9fe"
BG_CARD = "#8cb8ff"
BG_OUTPUT = "#6FE7F5"
FG_TITLE = "#141519"
FG_TEXT = "#1e2231"

BTN_ENC = "#38bdf8"
BTN_DEC = "#4ade80"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_INPUT = ("Segoe UI", 10)
FONT_OUTPUT = ("Consolas", 10)

# =============================
# ENKRIPSI
# =============================
def encrypt():
    output.delete("1.0", tk.END)

    p = int(entry_p.get())
    g = int(entry_g.get())
    x = int(entry_x.get())
    k = int(entry_k.get())
    plaintext = entry_plain.get()

    y = pow(g, x, p)
    cipher = []

    output.insert(tk.END, "=== PEMBANGKITAN KUNCI ===\n")
    output.insert(tk.END, f"p = {p}\n")
    output.insert(tk.END, f"g = {g}\n")
    output.insert(tk.END, f"x = {x}\n")
    output.insert(tk.END, f"y = g^x mod p = {y}\n\n")

    output.insert(tk.END, "=== PROSES ENKRIPSI ===\n")

    for i, ch in enumerate(plaintext, 1):
        m = ord(ch)
        if m >= p:
            output.insert(tk.END,
                f"ERROR: ASCII '{ch}' = {m} ≥ p ({p})\n")
            return

        a = pow(g, k, p)
        b = (pow(y, k, p) * m) % p
        cipher.append((a, b))

        output.insert(tk.END, f"\nBlok {i}\n")
        output.insert(tk.END, f"Plaintext : {ch}\n")
        output.insert(tk.END, f"ASCII     : {m}\n")
        output.insert(tk.END, f"a = g^k mod p = {a}\n")
        output.insert(tk.END, f"b = y^k·m mod p = {b}\n")

    entry_cipher.delete(0, tk.END)
    entry_cipher.insert(0, " | ".join(f"{a},{b}" for a, b in cipher))

# =============================
# DEKRIPSI
# =============================
def decrypt():
    output.insert(tk.END, "\n\n=== PROSES DEKRIPSI ===\n")

    p = int(entry_p.get())
    x = int(entry_x.get())
    cipher = entry_cipher.get().split(" | ")

    plaintext = ""

    for i, c in enumerate(cipher, 1):
        a, b = map(int, c.split(","))
        inv = pow(a, p-1-x, p)
        m = (b * inv) % p
        ch = chr(m)

        plaintext += ch

        output.insert(tk.END, f"\nCipher {i}\n")
        output.insert(tk.END, f"a = {a}, b = {b}\n")
        output.insert(tk.END, f"(a^x)^-1 mod p = {inv}\n")
        output.insert(tk.END, f"m = {m} → '{ch}'\n")

    entry_cipher.delete(0, tk.END)
    entry_cipher.insert(0, plaintext)

# =============================
# GUI
# =============================
root = tk.Tk()
root.title("ElGamal – Manual Parameter (Rapi)")
root.geometry("1000x800")
root.configure(bg=BG_MAIN)

# ===== JUDUL =====
tk.Label(root, text="🔐 ELGAMAL ENCRYPTION & DECRYPTION",
         bg=BG_MAIN, fg=FG_TITLE,
         font=FONT_TITLE).pack(pady=10)

# ===== FRAME PARAMETER =====
frame = tk.Frame(root, bg=BG_CARD)
frame.pack(padx=20, pady=1, fill="x")

tk.Label(frame, text="Parameter ElGamal",
         bg=BG_CARD, fg=FG_TEXT,
         font=("Segoe UI", 20, "bold")).pack(pady=8)

def labeled_entry(parent, label):
    tk.Label(parent, text=label,
             bg=BG_CARD, fg=FG_TEXT,
             font=FONT_LABEL).pack(anchor="w", padx=20)
    e = tk.Entry(parent, font=FONT_INPUT, width=25)
    e.pack(padx=20, pady=2, anchor="w")
    return e

entry_p = labeled_entry(frame, "p (prima)")
entry_g = labeled_entry(frame, "g")
entry_x = labeled_entry(frame, "x (private)")
entry_k = labeled_entry(frame, "k (enkripsi)")

# ===== PLAINTEXT =====
tk.Label(root, text="Plaintext",
         bg=BG_MAIN, fg=FG_TEXT,
         font=FONT_LABEL).pack(anchor="w", padx=30)

entry_plain = tk.Entry(root, width=120, font=FONT_INPUT)
entry_plain.pack(padx=30, pady=5)

# ===== TOMBOL =====
btn = tk.Frame(root, bg=BG_MAIN)
btn.pack(pady=10)

tk.Button(btn, text="ENCRYPT",
          bg=BTN_ENC, fg="black",
          font=("Segoe UI", 11, "bold"),
          width=18,
          command=encrypt).grid(row=0, column=0, padx=15)

tk.Button(btn, text="DECRYPT",
          bg=BTN_DEC, fg="black",
          font=("Segoe UI", 11, "bold"),
          width=18,
          command=decrypt).grid(row=0, column=1, padx=15)

# ===== CIPHERTEXT =====
tk.Label(root, text="Ciphertext / Plaintext",
         bg=BG_MAIN, fg=FG_TEXT,
         font=FONT_LABEL).pack(anchor="w", padx=30)

entry_cipher = tk.Entry(root, width=120, font=("Consolas", 10))
entry_cipher.pack(padx=30, pady=5)

# ===== OUTPUT =====
tk.Label(root, text="📊 Proses ElGamal (Step-by-Step)",
         bg=BG_MAIN, fg="#463c15",
         font=("Segoe UI", 13, "bold")).pack(pady=5)

output = tk.Text(root, width=120, height=28,
                 bg=BG_OUTPUT, fg="#000b21",
                 font=FONT_OUTPUT)
output.pack(padx=20, pady=10)

root.mainloop()
