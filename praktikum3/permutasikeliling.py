import itertools # (Asumsi import itertools ada, karena digunakan di dalamnya)

def permutasi_keliling(arr):
    if len(arr) == 1: # [cite: 94]
        return [arr] # [cite: 95]
    pertama = arr[0] # [cite: 96]
    permutasi_penuh = list(itertools.permutations(arr[1:])) # [cite: 97]
    return [[pertama] + list(perm) for perm in permutasi_penuh] # [cite: 98, 99]

data = [1, 2, 3] # [cite: 100]
print(permutasi_keliling(data)) # [cite: 101]