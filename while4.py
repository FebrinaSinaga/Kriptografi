# Statement 'while' bisa juga 
# dilakukan bersamaan dengan variabel

# Aturannya bisa diatur sesuai keinginan
# bisa string/teks, atau integer/angka
a = input('Masukkan nilai: ')

while a == 'y':
    print('Hello World')

    # Kenapa dengan fungsi .lower()?
    # Tujuannya hanya membuat jawaban konsisten huruf kecil.
    # Penulisan kondisi statement diatas akan menghasilkan nilai false
    # ketika perbandingannya seperti ini 'y' == 'Y'
    # Fungsi .lower() akan mengubah semua masukan(input) menjadi huruf kecil.
    # Sebaliknya .upper() akan menjadikannya huruf besar
    
    a = input("Masukkan nilai: ")

print('Berakhir')