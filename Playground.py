def count_most_frequent(container: object) -> tuple[object, int]:
    return max({e: container.count(e) for e in container}.items(), key=lambda x: x[1])

def deep_copy_list(lst: list) -> list:
    return [deep_copy_list(item) if isinstance(item, lst) else item for item in lst]

# Please enter your code that implements the magic function.
def is_magic(m: list) -> bool:
    s = sum(m[0])
    l = len(m)
    transposed_m = [[row[i] for row in m] for i in range(l)]
    for i in range(l):
        if sum(m[i]) != s or sum(transposed_m[i]) != s:
            return False
        
    dia_m = 0
    dia_tm = 0
    for i in range(l):
        dia_m += m[i][i]
        dia_tm += transposed_m[i][i]
    
    if dia_m != s or dia_tm != s:
        return False
    
    return True

test = "abcabca"
print(count_most_frequent(test))
print(is_magic([[1, 1], [1, 1]]))
