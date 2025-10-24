import re

# Fungsi untuk mengganti semua variasi tanda minus menjadi tanda '-' biasa
def normalize_minus(expr: str) -> str:
    return re.sub(r"[\u2012\u2013\u2014\u2212]", "-", expr)

# Fungsi untuk menghitung ekspresi kiri-ke-kanan (tanpa precedence)
def eval_left_to_right(tokens):
    if not tokens:
        raise ValueError("Ekspresi kosong!")

    try:
        hasil = float(tokens[0])
    except ValueError:
        raise ValueError(f"Token pertama bukan angka: {tokens[0]}")

    proses = [tokens[0]]  # simpan langkah-langkah proses

    i = 1
    while i < len(tokens):
        if i + 1 >= len(tokens):
            raise ValueError("Operator tanpa operand di akhir!")

        op = tokens[i]
        try:
            nilai = float(tokens[i + 1])
        except ValueError:
            raise ValueError(f"Operand bukan angka: {tokens[i + 1]}")

        # simpan proses sebelum dihitung
        proses.append(op)
        proses.append(tokens[i + 1])

        if op == '+':
            hasil += nilai
        elif op == '-':
            hasil -= nilai
        elif op == '*':
            hasil *= nilai
        elif op == '/':
            if nilai == 0:
                raise ZeroDivisionError("Tidak bisa membagi dengan nol!")
            hasil /= nilai
        else:
            raise ValueError(f"Operator tidak dikenali: {op}")

        print(f"Langkah: {' '.join(proses)} = {hasil}")
        i += 2

    return hasil

# Fungsi untuk menghitung dengan precedence normal
def eval_with_precedence(expr):
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
        raise ValueError("Ekspresi mengandung karakter tidak diizinkan!")

    try:
        print(f"Ekspresi dengan precedence: {expr}")
        hasil = eval(expr, {"__builtins__": None}, {})
        if isinstance(hasil, (int, float)):
            return hasil
        else:
            raise ValueError("Hasil bukan angka.")
    except Exception as e:
        raise ValueError(f"Gagal evaluasi: {e}")

# Program utama
def kalkulator_hybrid():
    print("=== Kalkulator Hybrid (dengan Proses Perhitungan) ===")
    print("Aturan:")
    print("• Jika ada spasi  → dihitung kiri-ke-kanan (tanpa precedence)")
    print("• Jika tidak ada  → mengikuti precedence operator standar\n")

    while True:
        ekspresi = input("Masukkan ekspresi (atau ketik 'exit' untuk keluar): ").strip()
        if ekspresi.lower() == "exit":
            print("Terima kasih! Program selesai.")
            break

        if not ekspresi:
            print("⚠️  Ekspresi kosong!\n")
            continue

        ekspresi = normalize_minus(ekspresi)

        try:
            if " " in ekspresi:
                print(f"\nEkspresi kiri-ke-kanan: {ekspresi}")
                token = ekspresi.split()
                hasil = eval_left_to_right(token)
            else:
                hasil = eval_with_precedence(ekspresi)

            print(f"\n➡️  Hasil Akhir: {hasil}\n{'='*45}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

# Jalankan program
if __name__ == "__main__":
    kalkulator_hybrid()
