# === Program Konversi Bilangan ===
# 1) Biner → Desimal, Hexadesimal
# 2) Oktal → Desimal, Biner, Hexadesimal
# 3) Hexadesimal → Desimal, Biner, Oktal

def biner_ke_desimal_dan_hex():
    print("\n=== Konversi Biner ke Desimal dan Hexadesimal ===")
    biner = input("Masukkan bilangan biner: ")
    try:
        desimal = int(biner, 2)
        oktal = oct(desimal)[2:]
        heksa = hex(desimal)[2:].upper()
        print(f"Desimal     : {desimal}")
        print(f"Oktal   : {oktal}")
        print(f"Hexadesimal : {heksa}")
        
    except ValueError:
        print("❌ Input bukan bilangan biner yang valid!")

def oktal_ke_desimal_biner_hex():
    print("\n=== Konversi Oktal ke Desimal, Biner, dan Hexadesimal ===")
    oktal = input("Masukkan bilangan oktal: ")
    try:
        desimal = int(oktal, 8)
        biner = bin(desimal)[2:]
        heksa = hex(desimal)[2:].upper()
        print(f"Desimal     : {desimal}")
        print(f"Biner       : {biner}")
        print(f"Hexadesimal : {heksa}")
    except ValueError:
        print("❌ Input bukan bilangan oktal yang valid!")

def heksa_ke_desimal_biner_oktal():
    print("\n=== Konversi Hexadesimal ke Desimal, Biner, dan Oktal ===")
    heksa = input("Masukkan bilangan hexadesimal: ")
    try:
        desimal = int(heksa, 16)
        biner = bin(desimal)[2:]
        oktal = oct(desimal)[2:]
        print(f"Desimal : {desimal}")
        print(f"Biner   : {biner}")
        print(f"Oktal   : {oktal}")
    except ValueError:
        print("❌ Input bukan bilangan hexadesimal yang valid!")

# === Menu utama ===
def main():
    while True:
        print("\n=== PROGRAM KONVERSI BILANGAN ===")
        print("1. Biner → Desimal, Hexadesimal")
        print("2. Oktal → Desimal, Biner, Hexadesimal")
        print("3. Hexadesimal → Desimal, Biner, Oktal")
        print("4. Keluar")

        pilih = input("Pilih menu (1-4): ")

        if pilih == "1":
            biner_ke_desimal_dan_hex()
        elif pilih == "2":
            oktal_ke_desimal_biner_hex()
        elif pilih == "3":
            heksa_ke_desimal_biner_oktal()
        elif pilih == "4":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("⚠️  Pilihan tidak valid, coba lagi!")

if __name__ == "__main__":
    main()
