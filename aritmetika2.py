
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

    match y:
        case 1:
            r = a + b
            print ('Hasilnya adalah ', r)
        
        case 2:
            r = a - b
            print ('Hasilnya adalah ', r)
        
        case 3:
            r = a * b
            print ('Hasilnya adalah ', r)
        
        case 4:
            r = a / b
            print ('Hasilnya adalah ', r)
        
        case 5:
            r = a % b
            print ('Hasilnya adalah ', r)


    x = input('Ingin melanjutkan? (y/n)').lower()