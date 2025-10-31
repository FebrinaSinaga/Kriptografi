def ambil_aturan_substitusi():
    """Meminta pengguna memasukkan aturan substitusi dan mengembalikan dictionary."""
    print("\n--- Definisikan Aturan Substitusi ---")
    aturan = {}
    
    while True:
        # Menanyakan karakter asli
        char_asli = input("Masukkan karakter ASLI (contoh: A). Ketik 'selesai' untuk mengakhiri: ").upper().strip()
        
        if char_asli == 'SELESAI':
            break
        
        # Validasi input karakter asli
        if len(char_asli) != 1 or not char_asli.isalpha():
            print("Input tidak valid. Harap masukkan satu huruf alfabet saja.")
            continue

        # Menanyakan karakter pengganti
        char_ganti = input(f"Gantikan '{char_asli}' dengan karakter: ").upper().strip()
        
        # Validasi input karakter pengganti
        if len(char_ganti) != 1 or not char_ganti.isalpha():
            print("Input tidak valid. Harap masukkan satu huruf alfabet saja.")
            continue

        # Menambahkan aturan ke dictionary
        aturan[char_asli] = char_ganti
        print(f"Aturan ditambahkan: {char_asli} -> {char_ganti}")
        
    return aturan

def substitusi_cipher(plaintext, aturan):
    """Menerapkan Substitusi Cipher pada plaintext berdasarkan aturan yang diberikan."""
    ciphertext = ''
    # Pastikan plaintext diubah ke huruf besar untuk mencocokkan aturan
    teks_diproses = plaintext.upper()
    
    for char in teks_diproses: 
        if char in aturan:
            ciphertext += aturan[char]  # Ganti jika ada di aturan
        else:
            ciphertext += char         # Pertahankan karakter lain (spasi, angka, tanda baca, atau huruf yang tidak diatur)
    return ciphertext

def jalankan_substitusi_dinamis():
    """Fungsi utama untuk menjalankan program secara dinamis."""
    
    # 1. Input Plaintext
    plaintext = input("Masukkan Plaintext yang akan dienkripsi: ")
    
    # 2. Input Aturan Substitusi
    aturan_substitusi = ambil_aturan_substitusi()
    
    if not aturan_substitusi:
        print("\nTidak ada aturan substitusi yang didefinisikan. Proses dibatalkan.")
        return

    # 3. Proses Enkripsi
    ciphertext = substitusi_cipher(plaintext, aturan_substitusi)
    
    # 4. Output Hasil
    print("\n==================================================")
    print("HASIL SUBSTITUSI CIPHER")
    print("==================================================")
    print(f"Plaintext Input: {plaintext}")
    print(f"Plaintext Diproses: {plaintext.upper()}")
    print(f"Aturan Substitusi: {aturan_substitusi}")
    print(f"Ciphertext: {ciphertext}")
    print("==================================================")

# Jalankan Program
jalankan_substitusi_dinamis()
