print("CAESAR CYPHER DECRYPT")

encrypted = int(input("Input a number from ALPHABET TABLE: "))
caesar_shift = int(input("Input a caesar shift: "))

# DECRYPTED = (ENCRYPTED - SHIFT) mod 26
decrypted = (encrypted - caesar_shift) % 26

left = (decrypted - 2) % 26
right = (decrypted + 2) % 26
print("\nThe decrypted entries in ALPHABET TABLE are:", left, decrypted, right)
