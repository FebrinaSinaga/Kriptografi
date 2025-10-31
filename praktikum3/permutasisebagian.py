import itertools

def permutasi_sebagian(arr, k):
    return list(itertools.permutations(arr, k)) # [cite: 73]

data = [1, 2, 3, 4] # [cite: 74]
print(permutasi_sebagian(data, 2)) # [cite: 75]
# Output akan berupa list dari tuple, mengambil 2 elemen: [(1, 2), (1, 3), ...]