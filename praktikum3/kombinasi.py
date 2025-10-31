def faktorial(x): # [cite: 144]
    if x == 0 or x == 1: # [cite: 145]
        return 1 # [cite: 146]
    hasil = 1 # [cite: 147]
    for i in range(2, x + 1): # [cite: 148]
        hasil *= i # [cite: 149]
    return hasil # [cite: 150]

def kombinasi(n, r): # [cite: 151]
    # Guard clause if r > n is missing the body in the source code [cite: 152, 153]
    if r > n:
        return 0 # Added for logical correctness, based on pseudocode's formula application
        
    faktorial_n = faktorial(n) # [cite: 154, 155]
    faktorial_r = faktorial(r) # [cite: 156, 157]
    faktorial_n_r = faktorial(n - r) # [cite: 158, 159]
    
    # // adalah integer division, yang sesuai untuk perhitungan kombinasi
    return faktorial_n // (faktorial_r * faktorial_n_r) # [cite: 160, 161]

# Contoh Penggunaan:
n = int(input("Masukkan jumlah total objek (n): ")) # [cite: 162]
r = int(input("Masukkan jumlah objek yang dipilih (r): ")) # [cite: 163]

hasil = kombinasi(n, r) # [cite: 164]
print("Jumlah kombinasi C({}, {}) adalah: {}".format(n, r, hasil)) # [cite: 165]