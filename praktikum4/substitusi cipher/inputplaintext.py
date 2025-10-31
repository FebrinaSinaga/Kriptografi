# Aturan substitusi dari dokumen [cite: 223]
aturan_substitusi = {
    'U': 'K', # [cite: 224]
    'N': 'N', # [cite: 225, 226]
    'I': 'I', # [cite: 227, 228]
    'K': 'K', # [cite: 229, 230]
    'A': 'B'  # [cite: 231]
}

def substitusi_cipher(plaintext, aturan): # [cite: 215]
    ciphertext = '' # Berdasarkan [cite: 216]
    for char in plaintext.upper(): # [cite: 217]
        if char in aturan: # [cite: 218]
            ciphertext += aturan[char] # [cite: 219]
        else: # [cite: 221]
            ciphertext += char # [cite: 220]
    return ciphertext # [cite: 222]

plaintext = input("Masukkan plaintext: ").upper() # [cite: 233]
ciphertext = substitusi_cipher(plaintext, aturan_substitusi) # Berdasarkan [cite: 233]

print(f'Plaintext: {plaintext}') # [cite: 234]
print(f'Ciphertext: {ciphertext}') # [cite: 235]