def transposisi_cipher(plaintext): # [cite: 291]
    part_length = len(plaintext) // 4 # [cite: 292]
    if len(plaintext) % 4 != 0:
        part_length += 1 # Menyesuaikan jika tidak habis dibagi 4
        
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)] # [cite: 293, 294]
    
    print("Bagian plaintext:") # [cite: 295]
    for i, part in enumerate(parts): # [cite: 296]
        print(f"Bagian {i + 1}: '{part}'") # [cite: 297]
        
    ciphertext = '' # [cite: 298, 299]
    
    for col in range(4): # [cite: 300]
        for part in parts: # [cite: 301]
            # [cite: 303]
            if col < len(part):
                ciphertext += part[col] # [cite: 304]
                # Menampilkan proses penambahan
                print(f"Menambahkan '{part[col]}' dari Bagian {parts.index(part) + 1} ke ciphertext.") # [cite: 305, 306]
    
    return ciphertext # [cite: 307]

plaintext = input("Masukkan plaintext: ") # [cite: 308]
ciphertext = transposisi_cipher(plaintext) # Berdasarkan [cite: 308]
print(f"Ciphertext: '{ciphertext}'") # Berdasarkan [cite: 308]