# Please enter your code here for implementing the function.
def delimiter_matcher(s: str, i: int, lst: list) -> list:
    res = []
    for delimiter in lst:
        target = s.find(delimiter, 0)
        while target >= 0 and target < len(s):
            for i in range(len(delimiter)):
                res += [target + i]
            target = s.find(delimiter, target + len(delimiter))

    res.sort()
    return res


def preprocess_string(s: str, lst: list) -> list:
    delimiters = delimiter_matcher(s, 0, lst)
    res = []
    last_d = -1
    for d in delimiters:
        if last_d != d - 1:
            res += [s[last_d + 1:d - 1]]
            last_d = d
    if delimiters[-1] < len(s) - 1:
        res += [s[delimiters[-1] + 1:]]

    return res


a = "jsjkkdk,djsljdl,dsjljdlk"
b = [',', ':']
print(preprocess_string(a, b))