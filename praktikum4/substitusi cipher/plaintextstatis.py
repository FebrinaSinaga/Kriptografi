# Aturan substitusi dari dokumen
aturan_substitusi = {
    'U': 'K', # [cite: 198, 199]
    'N': 'N', # [cite: 200, 201]
    'I': 'I', # [cite: 202]
    'K': 'K', # [cite: 203]
    'A': 'B'  # [cite: 204]
}

def substitusi_cipher(plaintext, aturan): # [cite: 189]
    ciphertext = '' # [cite: 190]
    for char in plaintext: # [cite: 191]
        if char in aturan: # [cite: 192]
            ciphertext += aturan[char] # [cite: 194]
        else:
            ciphertext += char # [cite: 195]
    return ciphertext # [cite: 196]

plaintext = "UNIKA" # 
ciphertext = substitusi_cipher(plaintext, aturan_substitusi) # [cite: 207]

print(f'Plaintext: {plaintext}') # [cite: 208]
print(f'Ciphertext: {ciphertext}') # Berdasarkan [cite: 209]
#Hasil: Plaintext: UNIKA, Ciphertext: KNIKB [cite: 211, 212]
