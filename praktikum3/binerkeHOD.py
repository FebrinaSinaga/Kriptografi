# === Program Konversi Biner ke Desimal dan Hexadesimal ===

# Fungsi utama
def biner_ke_desimal_hex():
    print("=== Konversi Biner ke Desimal, Oktal dan Hexadesimal ===")
    biner = input("Masukkan bilangan biner: ")

    try:
        desimal = int(biner, 2)               # konversi ke desimal
        oktal = oct(desimal)[2:]           # konversi ke oktal
        heksa = hex(desimal)[2:].upper()      # konversi ke hex (hapus '0x')
        print(f"Desimal     : {desimal}")
        print(f"Oktal       : {oktal}")
        print(f"Hexadesimal : {heksa}")
    except ValueError:
        print("❌ Input bukan bilangan biner yang valid!")

# Program utama
if __name__ == "__main__":
    biner_ke_desimal_hex()
