import tkinter as tk
import random

# ======================================
# PEMBANGKIT KUNCI
# ======================================
p = 257
g = 3
x = 97
y = pow(g, x, p)

# ======================================
# WARNA TEMA
# ======================================
BG_MAIN = "#85D8ED"
BG_FRAME = "#81D9D0"
FG_TEXT = "#000003"
BTN_ENC = "#4898ca"
BTN_DEC = "#378b64"
OUT_BG = "#74dccd"

# ======================================
# ENKRIPSI
# ======================================
def encrypt():
    output.delete("1.0", tk.END)
    plaintext = entry_plain.get()
    ciphertext = []

    output.insert(tk.END, "=== PROSES PEMBANGKIT KUNCI ===\n")
    output.insert(tk.END, f"p = {p}\n")
    output.insert(tk.END, f"g = {g}\n")
    output.insert(tk.END, f"x (private) = {x}\n")
    output.insert(tk.END, f"y = g^x mod p = {y}\n\n")

    output.insert(tk.END, "=== PROSES ENKRIPSI ===\n")

    for i, char in enumerate(plaintext, start=1):
        m = ord(char)
        k = random.randint(1, p-2)

        a = pow(g, k, p)
        b = (pow(y, k, p) * m) % p

        ciphertext.append((a, b))

        output.insert(tk.END, f"\n[Blok m{i}]\n")
        output.insert(tk.END, f"Plaintext  : {char}\n")
        output.insert(tk.END, f"ASCII (m)  : {m}\n")
        output.insert(tk.END, f"k (acak)   : {k}\n")
        output.insert(tk.END, f"a = g^k mod p     : {a}\n")
        output.insert(tk.END, f"b = y^k · m mod p : {b}\n")

    entry_cipher.set(" | ".join([f"{a},{b}" for a, b in ciphertext]))

# ======================================
# DEKRIPSI
# ======================================
def decrypt():
    output.insert(tk.END, "\n\n=== PROSES DEKRIPSI ===\n")
    cipher_text = entry_cipher.get().split(" | ")
    plaintext = ""

    for i, item in enumerate(cipher_text, start=1):
        a, b = map(int, item.split(","))

        ax = pow(a, x, p)
        inverse = pow(a, p-1-x, p)
        m = (b * inverse) % p
        char = chr(m)

        plaintext += char

        output.insert(tk.END, f"\n[Cipher Blok {i}]\n")
        output.insert(tk.END, f"a = {a}, b = {b}\n")
        output.insert(tk.END, f"a^x mod p        : {ax}\n")
        output.insert(tk.END, f"(a^x)^(-1) mod p : {inverse}\n")
        output.insert(tk.END, f"m = b · inverse mod p : {m}\n")
        output.insert(tk.END, f"ASCII → Char     : {char}\n")

    entry_cipher.set(plaintext)

# ======================================
# GUI
# ======================================
root = tk.Tk()
root.title("ElGamal Encryption – Visual GUI")
root.geometry("900x720")
root.configure(bg=BG_MAIN)

tk.Label(root, text="🔐 ElGamal Encryption (ASCII)",
         font=("Segoe UI", 16, "bold"),
         bg=BG_MAIN, fg="#41175a").pack(pady=10)

frame = tk.Frame(root, bg=BG_FRAME, bd=2, relief="ridge")
frame.pack(padx=15, pady=10, fill="x")

tk.Label(frame, text="Plaintext",
         font=("Segoe UI", 11),
         bg=BG_FRAME, fg=FG_TEXT).pack(pady=5)

entry_plain = tk.Entry(frame, width=80,
                       font=("Consolas", 11))
entry_plain.pack(pady=5)

btn_frame = tk.Frame(frame, bg=BG_FRAME)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Encrypt",
          command=encrypt,
          bg=BTN_ENC, fg="black",
          font=("Segoe UI", 10, "bold"),
          width=15).pack(side="left", padx=10)

tk.Button(btn_frame, text="Decrypt",
          command=decrypt,
          bg=BTN_DEC, fg="black",
          font=("Segoe UI", 10, "bold"),
          width=15).pack(side="left", padx=10)

tk.Label(frame, text="Ciphertext / Plaintext",
         font=("Segoe UI", 11),
         bg=BG_FRAME, fg=FG_TEXT).pack(pady=5)

entry_cipher = tk.StringVar()
tk.Entry(frame, textvariable=entry_cipher,
         width=100,
         font=("Consolas", 10)).pack(pady=5)

tk.Label(root, text="📊 Proses ElGamal",
         font=("Segoe UI", 13, "bold"),
         bg=BG_MAIN, fg="#613907").pack(pady=5)

output = tk.Text(root, width=110, height=26,
                 bg=OUT_BG, fg="#0E0111",
                 font=("Consolas", 10))
output.pack(padx=15, pady=10)

root.mainloop()
