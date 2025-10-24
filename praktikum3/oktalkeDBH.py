# === Program Konversi Oktal ke Desimal, Biner, dan Hexadesimal ===

def oktal_ke_desimal_biner_hex():
    print("=== Konversi Oktal ke Desimal, Biner, dan Hexadesimal ===")
    oktal = input("Masukkan bilangan oktal: ")

    try:
        desimal = int(oktal, 8)              # konversi ke desimal
        biner = bin(desimal)[2:]             # konversi ke biner
        heksa = hex(desimal)[2:].upper()     # konversi ke hex
        print(f"Desimal     : {desimal}")
        print(f"Biner       : {biner}")
        print(f"Hexadesimal : {heksa}")
    except ValueError:
        print("❌ Input bukan bilangan oktal yang valid!")

if __name__ == "__main__":
    oktal_ke_desimal_biner_hex()
