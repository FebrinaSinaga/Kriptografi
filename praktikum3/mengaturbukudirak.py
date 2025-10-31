def atur_buku_di_rak():
    """Menghitung dan mencetak jumlah cara mengatur n buku di r bagian rak."""
    print("\n--- Permutasi Latihan 2: Mengatur Buku di Rak ---")
    
    while True:
        try:
            n = int(input("Masukkan jumlah buku (n): "))
            if n < 0:
                print("Jumlah buku harus bilangan non-negatif.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka bulat.")

    while True:
        try:
            r = int(input("Masukkan jumlah bagian rak (r): "))
            if r <= 0:
                print("Jumlah bagian rak harus lebih besar dari nol.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka bulat.")

    # Formula untuk Permutasi dengan Pengulangan: r^n
    jumlah_cara = r ** n
    
    print(f"\nJumlah buku (n): {n}")
    print(f"Jumlah bagian rak (r): {r}")
    
    print(f"Setiap buku memiliki {r} pilihan bagian rak.")
    print(f"Total cara mengatur {n} buku di {r} bagian rak (r^n) adalah:")
    print(f"Hasil: {r}^{n} = {jumlah_cara} cara.")

atur_buku_di_rak()