import itertools # (Asumsi import itertools ada)

def permutasi_berkelompok(grup): # [cite: 115]
    hasil = [[]] # [cite: 116]
    for kelompok in grup: # [cite: 117]
        hasil_baru = [] # [cite: 118]
        for hsl in hasil: # [cite: 119]
            for perm in itertools.permutations(kelompok): # [cite: 120]
                hasil_baru.append(hsl + list(perm)) # [cite: 121]
        hasil = hasil_baru # [cite: 122]
    return hasil # [cite: 123]

grup = [[1, 2], [3, 4]] # [cite: 125]
print(permutasi_berkelompok(grup)) # [cite: 126]
# Output akan menggabungkan permutasi dari [1, 2] dan [3, 4]