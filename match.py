

opsi = input('Masukkan nilai: ')

# Statement 'match' mirip statement 'if-elif'
# hanya saja lebih rapi

match opsi:

    case 'a':
        print('Hello World')
    
    case 'b': 
        print('Halo Dunia')
    
    case _: 
        print('Ini nilai default')