import itertools 
def permutasi_menyeluruh(arr): 
    return list(itertools.permutations(arr)) 
data = [1, 2, 3] 
print(permutasi_menyeluruh(data)) 