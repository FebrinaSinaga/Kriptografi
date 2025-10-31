# Menggunakan logika pembagian blok len(plaintext) // 4.
def transposisi_cipher(plaintext): # [cite: 274]
    part_length = len(plaintext) // 4 # 
    if len(plaintext) % 4 != 0:
        part_length += 1 # Menyesuaikan jika tidak habis dibagi 4
        
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)] # [cite: 276, 277]
    
    ciphertext = '' # [cite: 278, 279]
    
    for col in range(4): # [cite: 280]
        for part in parts: # [cite: 281]
            if col < len(part): # [cite: 282]
                ciphertext += part[col] # [cite: 283]
    
    return ciphertext # [cite: 284]

plaintext = input("Masukkan plaintext: ") # [cite: 285]
ciphertext = transposisi_cipher(plaintext) # [cite: 286]
print(ciphertext) # [cite: 287]
# Contoh Hasil: Masukkan plaintext: UNIKA SANTO THOMAS -> UANTAN THSISOOKA M [cite: 289]