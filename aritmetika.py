
x = 'y'

while x == 'y':
    print('Opsi: ')
    print('1. Penjumlahan')
    print('2. Pengurangan')
    print('3. Perkalian')
    print('4. Pembagian')
    print('5. Modulus')

    y = int(input('Masukkan nilai: '))

    a = int(input('Masukkan nilai a: '))
    b = int(input('Masukkan nilai b: '))

    if y == 1:

        r = a + b
        print ('Hasilnya adalah ', r)
    
    elif y == 2: 
        r = a - b
        print ('Hasilnya adalah ', r)

    elif y == 3:
        r = a * b
        print ('Hasilnya adalah ', r)
    
    elif y == 4:
        r = a / b
        print ('Hasilnya adalah ', r)
    
    elif y == 5:
        r = a % b
        print ('Hasilnya adalah ', r)

    x = input('Ingin melanjutkan? (y/n)').lower()