import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

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
# Helpers
# -----------------------------
def hex_list_str(lst):
    return " ".join(f"{b:02X}" for b in lst)

def to_bytes_from_text(s):
    return [ord(c) for c in s]

def bytes_to_state(b):
    return [[b[row + 4*col] for row in range(4)] for col in range(4)]

def state_to_bytes(state):
    return [state[col][row] for col in range(4) for row in range(4)]

def print_state_lines(state):
    lines = []
    for r in range(4):
        parts = []
        for c in range(4):
            parts.append(f"{state[c][r]:02X}")
        lines.append(" ".join(parts))
    return "\n".join(lines)

# -----------------------------
# AES operations
# -----------------------------
def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [SBOX[b] for b in word]

def xtime(a):
    return ((a << 1) & 0xFF) ^ (0x1B if (a & 0x80) else 0x00)

def mul(a, b):
    if b == 1:
        return a
    if b == 2:
        return xtime(a)
    if b == 3:
        return xtime(a) ^ a
    # fallback generic
    res = 0
    temp = a
    for i in range(8):
        if (b >> i) & 1:
            res ^= temp
        temp = xtime(temp)
    return res & 0xFF

def mix_single_column(col):
    a = col[:]
    res = [
        mul(a[0],2) ^ mul(a[1],3) ^ mul(a[2],1) ^ mul(a[3],1),
        mul(a[0],1) ^ mul(a[1],2) ^ mul(a[2],3) ^ mul(a[3],1),
        mul(a[0],1) ^ mul(a[1],1) ^ mul(a[2],2) ^ mul(a[3],3),
        mul(a[0],3) ^ mul(a[1],1) ^ mul(a[2],1) ^ mul(a[3],2),
    ]
    return [r & 0xFF for r in res]

# -----------------------------
# Key Expansion
# -----------------------------
def generate_key_schedule_and_roundkeys(key_text, log_output=None):
    if len(key_text) != 16:
        raise ValueError("CipherKey harus 16 karakter")

    key_bytes = to_bytes_from_text(key_text)
    W = [key_bytes[i*4:(i+1)*4] for i in range(4)]

    if log_output is not None:
        log_output.append("===== W1 – W4 (Initial Key) =====")
        # print as columns W0 W1 W2 W3 (row-wise)
        for r in range(4):
            row = []
            for c in range(4):
                row.append(f"{W[c][r]:02X}")
            log_output.append(" ".join(row))
        log_output.append("")

    for i in range(4, 44):
        prev = W[i-1]
        if log_output is not None:
            log_output.append(f"===== PROSES W{i} =====")
            log_output.append(f"Wi-1 : {hex_list_str(prev)}")
        if i % 4 == 0:
            rot = rot_word(prev)
            sub = sub_word(rot)
            r = RCON[(i//4)-1]
            sub[0] ^= r
            temp = sub
            if log_output is not None:
                log_output.append(f"RotWord : {hex_list_str(rot)}")
                log_output.append(f"SubWord : {hex_list_str(sub)} (setelah XOR RCON {r:02X})")
        else:
            temp = prev

        wim4 = W[i-4]
        new_w = [(temp[j] ^ wim4[j]) for j in range(4)]

        if log_output is not None:
            log_output.append("Byte-wise XOR:")
            for j in range(4):
                log_output.append(f"  byte[{j}]: {temp[j]:02X} XOR {wim4[j]:02X} = {new_w[j]:02X}")
            log_output.append(f"Hasil W{i}: {hex_list_str(new_w)}")
            log_output.append("")

        W.append(new_w)

        if (i+1) % 4 == 0 and log_output is not None:
            block = W[i-3:i+1]
            log_output.append(f"===== W{i-3} – W{i} =====")
            for r in range(4):
                row = []
                for c in range(4):
                    row.append(f"{block[c][r]:02X}")
                log_output.append(" ".join(row))
            log_output.append("")

    # Build round keys
    round_keys = []
    for r in range(11):
        words = W[4*r:4*r+4]
        rk = []
        for w in words:
            rk.extend(w)
        round_keys.append(rk)
        if log_output is not None:
            log_output.append(f"===== ROUND KEY K{r} =====")
            # print as state
            for rr in range(4):
                row = []
                for cc in range(4):
                    row.append(f"{rk[cc*4+rr]:02X}")
                log_output.append(" ".join(row))
            log_output.append("")

    return W, round_keys

# -----------------------------
# AES FAST HELPERS for rounds
# -----------------------------
def sub_bytes_state(state, log_output=None):
    new = [[SBOX[state[c][r]] for r in range(4)] for c in range(4)]
    if log_output is not None:
        log_output.append("SubBytes:")
        for c in range(4):
            log_output.append(f" Col {c}: {hex_list_str(state[c])} -> {hex_list_str(new[c])}")
        log_output.append("")
    return new

def shift_rows_state(state, log_output=None):
    rows = [[state[c][r] for c in range(4)] for r in range(4)]
    shifted = []
    for r in range(4):
        sr = rows[r][r:] + rows[r][:r]
        shifted.append(sr)
    new = [[shifted[r][c] for r in range(4)] for c in range(4)]
    if log_output is not None:
        log_output.append("ShiftRows:")
        for r in range(4):
            log_output.append(f" Row {r}: {hex_list_str(rows[r])} -> {hex_list_str(shifted[r])}")
        log_output.append("")
    return new

def mix_columns_state(state, log_output=None):
    new = []
    if log_output is not None:
        log_output.append("MixColumns:")
    for c in range(4):
        before = state[c]
        after = mix_single_column(before)
        new.append(after)
        if log_output is not None:
            log_output.append(f" Col {c}: {hex_list_str(before)} -> {hex_list_str(after)}")
    if log_output is not None:
        log_output.append("")
    return new

def add_round_key(state, round_key_bytes, log_output=None, label=None):
    rk_state = bytes_to_state(round_key_bytes)
    new = [[state[c][r] ^ rk_state[c][r] for r in range(4)] for c in range(4)]
    if log_output is not None:
        if label:
            log_output.append(label)
        log_output.append("RoundKey bytes: " + hex_list_str(round_key_bytes))
        log_output.append("Before AddRoundKey:")
        for line in print_state_lines(state).splitlines():
            log_output.append(" " + line)
        log_output.append("After AddRoundKey:")
        for line in print_state_lines(new).splitlines():
            log_output.append(" " + line)
        log_output.append("")
    return new

# -----------------------------
# Full AES-128 verbose encryption
# -----------------------------
def aes_encrypt_verbose(plaintext_text, round_keys, log_output):
    if len(plaintext_text) != 16:
        raise ValueError("Plaintext harus 16 karakter")

    pt_bytes = to_bytes_from_text(plaintext_text)
    state = bytes_to_state(pt_bytes)

    log_output.append("===== PLAINTEXT (STATE AWAL) =====")
    for line in print_state_lines(state).splitlines():
        log_output.append(line)
    log_output.append("")

    # Initial AddRoundKey (K0)
    log_output.append("===== Initial AddRoundKey (K0) =====")
    state = add_round_key(state, round_keys[0], log_output)

    # Rounds 1..9
    for r in range(1, 10):
        log_output.append(f"===== ROUND {r} =====")
        state = sub_bytes_state(state, log_output)
        for line in print_state_lines(state).splitlines(): log_output.append(" " + line)
        log_output.append("")
        state = shift_rows_state(state, log_output)
        for line in print_state_lines(state).splitlines(): log_output.append(" " + line)
        log_output.append("")
        state = mix_columns_state(state, log_output)
        for line in print_state_lines(state).splitlines(): log_output.append(" " + line)
        log_output.append("")
        state = add_round_key(state, round_keys[r], log_output, label=f"AddRoundKey (K{r}):")
        # also print W words for K r (optional)
        log_output.append(f"W words for K{r} (W{4*r}..W{4*r+3}):")
        # printed earlier during keyexpansion if needed

    # Round 10
    log_output.append("===== ROUND 10 =====")
    state = sub_bytes_state(state, log_output)
    for line in print_state_lines(state).splitlines(): log_output.append(" " + line)
    log_output.append("")
    state = shift_rows_state(state, log_output)
    for line in print_state_lines(state).splitlines(): log_output.append(" " + line)
    log_output.append("")
    state = add_round_key(state, round_keys[10], log_output, label="AddRoundKey (K10):")

    ciphertext = state_to_bytes(state)
    log_output.append("===== CIPHERTEXT (HEX) =====")
    log_output.append(hex_list_str(ciphertext))
    log_output.append("")
    return ciphertext

# -----------------------------
# Wrappers used by GUI buttons
# -----------------------------
# store last computed W and round_keys to allow pressing Rounds after generating keys
GLOBAL_STATE = {
    "W": None,
    "round_keys": None,
    "last_plaintext": None,
    "last_key": None
}

def run_key_expansion_only(key_text, text_widget):
    try:
        log = []
        W, round_keys = generate_key_schedule_and_roundkeys(key_text, log_output=log)
        GLOBAL_STATE["W"] = W
        GLOBAL_STATE["round_keys"] = round_keys
        GLOBAL_STATE["last_key"] = key_text
        # display
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "\n".join(log))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_rounds_only(plaintext_text, text_widget):
    try:
        if GLOBAL_STATE["round_keys"] is None:
            messagebox.showwarning("Warning", "Round keys belum dibuat! Jalankan Key Expansion dulu.")
            return
        log = []
        aes_encrypt_verbose(plaintext_text, GLOBAL_STATE["round_keys"], log)
        GLOBAL_STATE["last_plaintext"] = plaintext_text
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "\n".join(log))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_aes_verbose(plaintext_text, key_text, text_widget):
    try:
        # Ensure keys are generated for this key (regenerate if different key)
        if GLOBAL_STATE["round_keys"] is None or GLOBAL_STATE["last_key"] != key_text:
            log = []
            W, round_keys = generate_key_schedule_and_roundkeys(key_text, log_output=log)
            GLOBAL_STATE["W"] = W
            GLOBAL_STATE["round_keys"] = round_keys
            GLOBAL_STATE["last_key"] = key_text
            # We'll append encryption logs after this
            aes_log = []
            aes_encrypt_verbose(plaintext_text, round_keys, aes_log)
            full_log = log + [""] + aes_log
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "\n".join(full_log))
        else:
            # keys already exist
            log = []
            aes_encrypt_verbose(plaintext_text, GLOBAL_STATE["round_keys"], log)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "\n".join(log))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -----------------------------
# GUI
# -----------------------------
def save_output_to_file(text_widget):
    content = text_widget.get("1.0", tk.END)
    if not content.strip():
        messagebox.showinfo("Info", "Tidak ada output untuk disimpan.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text files","*.txt"), ("All files","*.*")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Sukses", f"Output tersimpan ke {path}")

def clear_output(text_widget):
    text_widget.delete("1.0", tk.END)

root = tk.Tk()
root.title("AES-128 — Key Expansion & Rounds (Verbose) 🎀")
root.geometry("1000x960")
root.configure(bg="#dfd7dc")

# ===============================
#  TITLE BESAR CANTIK (HEADER)
# ===============================
title_label = tk.Label(
    root,
    text="✨ AES-128 — Key Expansion & Rounds (Verbose) 🎀 ✨",
    font=("Segoe UI", 26, "bold"),
    bg="#dfd7dc",
    fg="#8B004B",
    pady=10
)
title_label.pack(pady=10)

# Input frame
frame_in = tk.LabelFrame(root, text=" Input (16 karakter) ", bg="#f6cbe3", fg="#200f18", font=("Segoe UI",10,"bold"), padx=10, pady=8)
frame_in.pack(fill="x", padx=12, pady=10)

tk.Label(frame_in, text="Plaintext:", bg="#f6cbe3", fg="#1E1018", font=("Segoe UI",10,"bold")).grid(row=0, column=0, sticky="w")
entry_plain = tk.Entry(frame_in, width=40, font=("Consolas",11))
entry_plain.insert(0, "")  # 16 chars example
entry_plain.grid(row=0, column=1, padx=6, pady=4, sticky="w")

tk.Label(frame_in, text="CipherKey:", bg="#f6cbe3", fg="#200f18", font=("Segoe UI",10,"bold")).grid(row=1, column=0, sticky="w")
entry_key = tk.Entry(frame_in, width=40, font=("Consolas",11))
entry_key.insert(0, "")  # 16 chars example
entry_key.grid(row=1, column=1, padx=6, pady=4, sticky="w")

# Buttons frame
frame_btn = tk.Frame(root, bg="#f2d7ea")
frame_btn.pack(fill="x", padx=12, pady=6)

btn_ke = tk.Button(frame_btn, text="Proses Key Expansion", width=22, command=lambda: run_key_expansion_only(entry_key.get(), text_output), bg="#c86aa6", fg="white")
btn_ke.grid(row=0, column=0, padx=6, pady=6)

btn_rounds = tk.Button(frame_btn, text="Proses AES Rounds", width=22, command=lambda: run_rounds_only(entry_plain.get(), text_output), bg="#c86aa6", fg="white")
btn_rounds.grid(row=0, column=1, padx=6, pady=6)

btn_full = tk.Button(frame_btn, text="Proses Lengkap (KeyExp + AES)", width=28, command=lambda: run_aes_verbose(entry_plain.get(), entry_key.get(), text_output), bg="#8f2f5a", fg="white")
btn_full.grid(row=0, column=2, padx=6, pady=6)

btn_clear = tk.Button(frame_btn, text="Clear Output", width=14, command=lambda: clear_output(text_output), bg="#b57aa3", fg="white")
btn_clear.grid(row=0, column=3, padx=6, pady=6)

btn_save = tk.Button(frame_btn, text="Simpan ke .txt", width=14, command=lambda: save_output_to_file(text_output), bg="#b57aa3", fg="white")
btn_save.grid(row=0, column=4, padx=6, pady=6)

# Output
text_output = ScrolledText(root, width=118, height=32, font=("Consolas",10), bg="#fff7fb", fg="#000000", wrap="none")
text_output.pack(padx=12, pady=6, fill="both", expand=True)

# Start mainloop
root.mainloop()
