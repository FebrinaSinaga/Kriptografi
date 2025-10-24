# === Program Konversi Hexadesimal ke Desimal, Biner, dan Oktal ===

def heksa_ke_desimal_biner_oktal():
    print("=== Konversi Hexadesimal ke Desimal, Biner, dan Oktal ===")
    heksa = input("Masukkan bilangan hexadesimal: ")

    try:
        desimal = int(heksa, 16)           # konversi ke desimal
        biner = bin(desimal)[2:]           # konversi ke biner
        oktal = oct(desimal)[2:]           # konversi ke oktal
        print(f"Desimal : {desimal}")
        print(f"Biner   : {biner}")
        print(f"Oktal   : {oktal}")
    except ValueError:
        print("❌ Input bukan bilangan hexadesimal yang valid!")

if __name__ == "__main__":
    heksa_ke_desimal_biner_oktal()
