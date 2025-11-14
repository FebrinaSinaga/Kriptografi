import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# =========================
# Kelas Vigenere Cipher (Logika)
# =========================
class VigenereCipher:
    def __init__(self, key: str):
        self.key = key.upper()

    def _format_text(self, text: str) -> str:
        return ''.join(filter(str.isalpha, text.upper()))

    def _generate_key(self, text: str) -> str:
        key = self.key
        if len(key) < len(text):
            key = (key * (len(text) // len(key) + 1))[:len(text)]
        return key

    def encrypt(self, plaintext: str):
        plain = self._format_text(plaintext)
        key = self._generate_key(plain)
        ciphertext = []
        detail = []

        for i, ch in enumerate(plain):
            p = ord(ch) - 65
            k = ord(key[i]) - 65
            c = (p + k) % 26
            cipher_char = chr(c + 65)
            ciphertext.append(cipher_char)
            detail.append(f"{ch}({p}) + {key[i]}({k}) = {cipher_char}({c})")

        return ''.join(ciphertext), key, detail

    def decrypt(self, ciphertext: str):
        cipher = self._format_text(ciphertext)
        key = self._generate_key(cipher)
        plaintext = []
        detail = []

        for i, ch in enumerate(cipher):
            c = ord(ch) - 65
            k = ord(key[i]) - 65
            p = (c - k + 26) % 26
            plain_char = chr(p + 65)
            plaintext.append(plain_char)
            detail.append(f"{ch}({c}) - {key[i]}({k}) = {plain_char}({p})")

        return ''.join(plaintext), key, detail


# =========================
# GUI FEMINIM — Pinky Girl Theme 💖
# =========================
class ModernCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💖 Vigenère Cipher — Pinky Girl Edition")
        self.root.geometry("830x670")
        self.root.configure(bg="#FFE4EC")  # pastel pink background

        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        style = ttk.Style(self.root)
        # gunakan tema clam, aman di semua OS
        style.theme_use("clam")

        # Warna utama pink lembut dan putih
        style.configure("TLabel", background="#FFE4EC", font=("Inter", 11), foreground="#7A255D")
        style.configure("Title.TLabel", font=("Poppins", 20, "bold"), foreground="#D63384", background="#FFE4EC")
        style.configure("Sub.TLabel", font=("Inter", 10), foreground="#A34E75", background="#FFE4EC")
        style.configure("Card.TFrame", background="#FFF0F5", relief="flat")

        self.title_font = ("Poppins", 20, "bold")
        self.input_font = ("Inter", 12)
        self.mono_font = ("Courier New", 11)
        self.result_font = ("Inter", 14, "bold")

    def _build_ui(self):
        # Judul di tengah
        title_label = ttk.Label(self.root, text="💌 VIGENÈRE CIPHER 💌", style="Title.TLabel")
        title_label.place(relx=0.5, y=25, anchor="center")

        # Card Input
        input_card = ttk.Frame(self.root, style="Card.TFrame", padding=14)
        input_card.place(x=28, y=80, width=770, height=160)

        ttk.Label(input_card, text="Teks (plaintext/ciphertext):", font=self.input_font).place(x=10, y=8)
        self.entry_text = ttk.Entry(input_card, font=self.input_font, width=65)
        self.entry_text.place(x=10, y=36)

        ttk.Label(input_card, text="Key:", font=self.input_font).place(x=10, y=72)
        self.entry_key = ttk.Entry(input_card, font=self.input_font, width=65)
        self.entry_key.place(x=10, y=100)

        # Tombol aksi utama — feminin pastel
        btn_frame = ttk.Frame(self.root, style="Card.TFrame")
        btn_frame.place(x=28, y=265, width=770, height=65)

        self.btn_encrypt = tk.Button(btn_frame, text="💝 Enkripsi", font=("Inter", 12, "bold"),
                                     bg="#FF9EC4", fg="white", bd=0, activebackground="#F178B6",
                                     cursor="hand2", command=self.on_encrypt)
        self.btn_encrypt.place(x=20, y=10, width=220, height=45)

        self.btn_decrypt = tk.Button(btn_frame, text="🌸 Dekripsi", font=("Inter", 12, "bold"),
                                     bg="#FFB6C1", fg="white", bd=0, activebackground="#F497B6",
                                     cursor="hand2", command=self.on_decrypt)
        self.btn_decrypt.place(x=260, y=10, width=220, height=45)

        self.btn_clear = tk.Button(btn_frame, text="🧼 Bersihkan", font=("Inter", 12, "bold"),
                                   bg="#F8A1C4", fg="white", bd=0, activebackground="#E47BA0",
                                   cursor="hand2", command=self.on_clear)
        self.btn_clear.place(x=500, y=10, width=120, height=45)

        # Hasil akhir
        # Label hasil akhir dengan warna lebih kontras dan jarak sedikit lebih lebar
        self.label_result_title = ttk.Label(self.root, text="✨ Hasil Akhir :", font=self.result_font,
                                    foreground="#8E195E", background="#FFE4EC")
        self.label_result_title.place(x=28, y=340)

        self.label_result_text = ttk.Label(self.root, text="-", font=("Inter", 14, "bold"),
                                   background="#FFE4EC", foreground="#3A003A")
        self.label_result_text.place(x=180, y=340)  # digeser agar tidak menimpa label sebelumnya


        # Tombol salin kecil
        self.btn_copy = tk.Button(self.root, text="📋 Salin", font=("Inter", 10),
                                  bg="#FDEEF4", fg="#C2185B", bd=1, relief="ridge",
                                  activebackground="#FFD9E8", cursor="hand2",
                                  command=self.copy_result)
        self.btn_copy.place(x=720, y=338, width=70, height=28)

        # Card hasil detail
        result_card = ttk.Frame(self.root, style="Card.TFrame", padding=12)
        result_card.place(x=28, y=380, width=770, height=220)

        ttk.Label(result_card, text="💞 DETAIL PROSES 💞", style="Title.TLabel").place(x=10, y=4)

        self.text_detail = tk.Text(result_card, bg="#FFF7FA", fg="#6B214E", font=self.mono_font,
                                   wrap="word", bd=0)
        self.text_detail.place(x=10, y=34, width=745, height=170)
        self.text_detail.configure(state="disabled")

        footer = ttk.Label(self.root, text="🌷 Dibuat oleh Febrina Yohana Sinaga — PBO Project 🌷", style="Sub.TLabel")
        footer.place(relx=0.5, y=645, anchor="center")

    # =====================
    # Fungsi tombol
    # =====================
    def on_encrypt(self):
        txt = self.entry_text.get().strip()
        key = self.entry_key.get().strip()
        if not txt or not key:
            messagebox.showwarning("Peringatan", "Masukkan teks dan key terlebih dahulu!")
            return

        cipher = VigenereCipher(key)
        ciphertext, used_key, detail = cipher.encrypt(txt)

        self.label_result_text.config(text=ciphertext)
        self._update_detail("ENKRIPSI", txt, used_key, detail)

    def on_decrypt(self):
        txt = self.entry_text.get().strip()
        key = self.entry_key.get().strip()
        if not txt or not key:
            messagebox.showwarning("Peringatan", "Masukkan teks dan key terlebih dahulu!")
            return

        cipher = VigenereCipher(key)
        plaintext, used_key, detail = cipher.decrypt(txt)

        self.label_result_text.config(text=plaintext)
        self._update_detail("DEKRIPSI", txt, used_key, detail)

    def on_clear(self):
        self.entry_text.delete(0, tk.END)
        self.entry_key.delete(0, tk.END)
        self.label_result_text.config(text="-")
        self._write_textbox("")

    def _update_detail(self, mode, original, used_key, detail):
        text = f"Mode        : {mode}\n"
        text += f"Teks Asli   : {original}\n"
        text += f"Key Dipakai : {used_key}\n"
        text += "-" * 45 + "\n\n"
        for d in detail:
            text += d + "\n"
        text += "-" * 45 + "\n"
        text += f"Waktu proses: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        self._write_textbox(text)

    def _write_textbox(self, text):
        self.text_detail.configure(state="normal")
        self.text_detail.delete("1.0", tk.END)
        self.text_detail.insert(tk.END, text)
        self.text_detail.configure(state="disabled")

    def copy_result(self):
        result = self.label_result_text.cget("text")
        if result and result != "-":
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Salin", "Hasil berhasil disalin ke clipboard! 💕")
        else:
            messagebox.showwarning("Salin", "Tidak ada hasil untuk disalin.")


# =====================
# Main
# =====================
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCipherApp(root)
    root.mainloop()