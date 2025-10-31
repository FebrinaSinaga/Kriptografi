# Menggunakan logika pembagian blok dari versi dinamis  agar sesuai dengan hasil eksekusi[cite: 272].
def transposisi_cipher(plaintext): # [cite: 257, 274]
    # part_length = len(plaintext) // 4 
    part_length = len(plaintext) // 4
    if len(plaintext) % 4 != 0:
        part_length += 1 # Menyesuaikan jika tidak habis dibagi 4
    
    # Membagi plaintext menjadi bagian-bagian (baris) [cite: 276, 277, 293, 294]
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)]
    
    ciphertext = '' # [cite: 261, 262, 278, 279]
    
    for col in range(4): # Loop melalui 4 kolom [cite: 263, 280, 300]
        for part in parts: # Loop melalui setiap bagian (baris) [cite: 264, 281, 301]
            if col < len(part): # Cek agar tidak melewati batas kolom [cite: 265, 282, 303]
                ciphertext += part[col] # [cite: 266, 283, 304]
    
    return ciphertext # [cite: 267, 284, 307]

plaintext = "UNIKA SANTO THOMAS" # 
ciphertext = transposisi_cipher(plaintext) # [cite: 269]
print(ciphertext) # [cite: 270]
# Hasil: UANTAN THSISOOKA M [cite: 272]