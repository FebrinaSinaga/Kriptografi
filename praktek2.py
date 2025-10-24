import operator

# Daftar operator yang bisa digunakan
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

while input("Apakah Anda ingin memulai operasi perhitungan? (y/n): ").lower() == 'y':
    try:
        # Input nilai a dan b
        a = float(input("Masukkan nilai a: "))
        b = float(input("Masukkan nilai b: "))

        # Input operator
        c = input("Masukkan operator (+, -, *, /): ")

        # Proses perhitungan
        hasil = ops[c](a, b)

        # Tampilkan hasil
        print(f"Hasil dari {a} {c} {b} = {hasil}")

    except KeyError:
        print("Operator tidak valid. Gunakan salah satu dari (+, -, *, /).")
    except ZeroDivisionError:
        print("Pembagian dengan nol tidak diperbolehkan.")
    except ValueError:
        print("Input harus berupa angka.")
    except Exception as e:
        print("Terjadi kesalahan:", e)

print("Program selesai. Terima kasih!")
