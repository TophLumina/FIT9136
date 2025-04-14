print("CAESAR CYPHER DECRYPT")

size = int(input("Input size of the alphabet: "))
encrypted = int(input("Input a number from ALPHABET TABLE: "))
caesar_shift = int(input("Input a caesar shift: "))

# DECRYPTED = (ENCRYPTED - SHIFT) mod SIZE
decrypted = (encrypted - caesar_shift) % size

left = (decrypted - 2) % size
right = (decrypted + 2) % size
print("\nThe decrypted entries in ALPHABET TABLE are:", left, decrypted, right)
