import itertools

def permutasi_menyeluruh_input():
    """Permutasi Menyeluruh dengan input dinamis."""
    print("\n--- 1. Permutasi Menyeluruh ---")
    data = ambil_input_data()
    # Menggunakan fungsi asli dari dokumen
    hasil = list(itertools.permutations(data))
    print(f"Permutasi Menyeluruh dari {data}:")
    print(hasil)

def permutasi_sebagian_input():
    """Permutasi Sebagian dengan input dinamis."""
    print("\n--- 2. Permutasi Sebagian ---")
    data = ambil_input_data()
    while True:
        try:
            k = int(input(f"Masukkan jumlah elemen yang dipilih (r), r harus <= {len(data)}: "))
            if 0 < k <= len(data):
                break
            else:
                print("Jumlah elemen yang dipilih (r) harus positif dan tidak melebihi jumlah total elemen.")
        except ValueError:
            print("Input tidak valid. Masukkan angka.")

    # Menggunakan fungsi asli dari dokumen
    hasil = list(itertools.permutations(data, k))
    print(f"Permutasi Sebagian C({len(data)}, {k}) dari {data}:")
    print(hasil)

def permutasi_keliling_input():
    """Permutasi Keliling dengan input dinamis."""
    print("\n--- 3. Permutasi Keliling (Circular) ---")
    data = ambil_input_data()
    
    if len(data) == 0:
        print("Data kosong, tidak ada permutasi keliling.")
        return
        
    pertama = data[0]
    # Permutasi penuh dari sisa elemen
    permutasi_penuh = list(itertools.permutations(data[1:]))
    
    # Menambahkan elemen pertama di awal setiap permutasi
    hasil = [[pertama] + list(perm) for perm in permutasi_penuh]
    
    print(f"Permutasi Keliling dari {data}:")
    print(hasil)
    # Catatan: Jumlah permutasi keliling sebenarnya adalah (n-1)!

def permutasi_berkelompok_input():
    """Permutasi Berkelompok dengan input dinamis."""
    print("\n--- 4. Permutasi Berkelompok ---")
    
    # Ini memerlukan input yang lebih kompleks: group dari group
    print("Masukkan data untuk setiap kelompok secara terpisah.")
    
    grup_utama = []
    while True:
        kelompok_str = input("Masukkan elemen kelompok (contoh: 1,2). Ketik 'selesai' untuk mengakhiri: ")
        if kelompok_str.lower() == 'selesai':
            break
        
        # Pisahkan string menjadi list elemen untuk kelompok saat ini
        kelompok_list = [item.strip() for item in kelompok_str.split(',')]
        if kelompok_list and kelompok_list != ['']:
             grup_utama.append(kelompok_list)
        
    if not grup_utama:
        print("Tidak ada kelompok yang dimasukkan.")
        return

    # Fungsi inti Permutasi Berkelompok dari dokumen
    hasil = [[]]
    for kelompok in grup_utama:
        hasil_baru = []
        for hsl in hasil:
            for perm in itertools.permutations(kelompok):
                hasil_baru.append(hsl + list(perm))
        hasil = hasil_baru
    
    print(f"Permutasi Berkelompok dari {grup_utama}:")
    print(hasil)

def jalankan_semua_permutasi():
    """Menu untuk menjalankan semua jenis permutasi."""
    print("\n=======================================================")
    print("APLIKASI PERMUTASI DENGAN INPUT KEYBOARD")
    print("=======================================================")
    
    permutasi_menyeluruh_input()
    print("\n-------------------------------------------------------")
    permutasi_sebagian_input()
    print("\n-------------------------------------------------------")
    permutasi_keliling_input()
    print("\n-------------------------------------------------------")
    permutasi_berkelompok_input()

def ambil_input_data():
    """Fungsi bantuan untuk mengambil input data."""
    data_str = input("Masukkan elemen data yang dipisahkan koma (contoh: 1,2,3 atau a,b,c): ")
    data_list = [item.strip() for item in data_str.split(',')]
    return data_list

# Jalankan Program Utama
jalankan_semua_permutasi()