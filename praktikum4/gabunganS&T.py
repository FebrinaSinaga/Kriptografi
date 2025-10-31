# === Gabungan Substitusi + Transposisi Cipher (dengan tampilan kolom) ===

def substitusi_cipher(teks):
    hasil = ""
    for ch in teks.lower():
        if ch == 'u':
            hasil += 'k'
        elif ch == 'a':
            hasil += 'b'
        elif ch.isalpha():
            hasil += ch
        else:
            pass  # abaikan spasi atau tanda baca
    return hasil

def transposisi_cipher(teks, kolom=4):
    panjang = len(teks)
    baris = (panjang + kolom - 1) // kolom
    total = baris * kolom
    teks += "x" * (total - panjang)

    matriks = [teks[i*kolom:(i+1)*kolom] for i in range(baris)]
    return matriks

def baca_per_kolom(matriks):
    kolom = len(matriks[0])
    baris = len(matriks)
    hasil = ""
    for c in range(kolom):
        for r in range(baris):
            hasil += matriks[r][c]
    return hasil

# === Input Plaintext ===
plaintext = "UNIKA SANTO THOMAS"

# === Langkah 1: Normalisasi ===
plain_clean = plaintext.replace(" ", "").lower()

# === Langkah 2: Substitusi Cipher ===
hasil_substitusi = substitusi_cipher(plain_clean)

# === Langkah 3: Transposisi Cipher (4 kolom) ===
matriks = transposisi_cipher(hasil_substitusi, kolom=4)
hasil_transposisi = baca_per_kolom(matriks)

# === TAMPILKAN HASIL ===
print("="*45)
print("      HASIL ENKRIPSI SUBSTITUSI & TRANSPOSISI")
print("="*45)
print(f"{'Plaintext':25}: {plaintext}")
print(f"{'Setelah Substitusi':25}: {hasil_substitusi}")
print("-"*45)
print("Matriks Transposisi (4 kolom):")
print("-"*45)
print("Kol1 Kol2 Kol3 Kol4")
print("-"*45)
for row in matriks:
    print("  ".join(row.upper()))
print("-"*45)
print(f"{'Ciphertext Akhir':25}: {hasil_transposisi}")
print("="*45)
