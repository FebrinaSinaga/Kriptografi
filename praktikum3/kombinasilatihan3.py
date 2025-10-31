def faktorial(x):
    """Menghitung nilai faktorial dari x."""
    if x == 0 or x == 1:
        return 1
    hasil = 1
    for i in range(2, x + 1):
        hasil *= i
    return hasil

def kombinasi(n, r):
    """Menghitung nilai kombinasi C(n, r)."""
    if r > n or r < 0 or n < 0:
        return 0 # Kombinasi tidak mungkin atau tidak valid

    # Menghitung faktorial untuk C(n, r) = n! / (r! * (n-r)!)
    faktorial_n = faktorial(n)
    faktorial_r = faktorial(r)
    faktorial_n_r = faktorial(n - r)
    
    # // untuk integer division
    return faktorial_n // (faktorial_r * faktorial_n_r)

def kombinasi_dengan_inisial():
    """Program kombinasi dengan output inisial huruf (C(n, r))."""
    print("\n--- Kombinasi Latihan 3: Output dengan Inisial Huruf ---")
    
    while True:
        try:
            n = int(input("Masukkan jumlah total objek (n): "))
            r = int(input("Masukkan jumlah objek yang dipilih (r): "))
            if n < r or n < 0 or r < 0:
                print("Input tidak valid. Pastikan 0 <= r <= n.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka bulat.")

    hasil = kombinasi(n, r)
    
    # Output yang menampilkan "inisial huruf" C(n, r)
    print(f"\nPerhitungan Kombinasi C(n, r):")
    print(f"C({n}, {r}) = {n}! / ({r}! * ({n}-{r})!)")
    print(f"C({n}, {r}) = {faktorial(n)} / ({faktorial(r)} * {faktorial(n-r)})")
    
    # Menampilkan hasil akhir
    print(f"Jumlah kombinasi C({n}, {r}) adalah: {hasil}")

kombinasi_dengan_inisial()