def vigenere_decryption(encrypted_msg: str, key: str):
    A_ascii = int(ord("A"))
    for i in range(0, len(encrypted_msg)):
        # notice that len(key) could be smaller than len(encrypted_msg)
        # SHIFT = ascii(key[i % len(key)]) - ascii(A)
        # ENCRYPTED = ascii(encrypted_msg[i]) - ascii(A)
        # DECRYPTED = (ENCRYPTED - SHIFT) mod 26
        decrypted_code = (int(ord(encrypted_msg[i])) - int(ord(key[i % len(key)]))) % 26
        print(chr(decrypted_code + A_ascii))
    pass


print("DECRYPT STRING")

encrypted_str = input("Input encrypted string: ").replace(" ", "")
# check if the encrypted string and caesar shift are valid and contain no space
if len(encrypted_str) == 0:
    print("Empty encrypted string.")
else:
    vkey = input("Input vigenère key: ").replace(" ", "")
    if len(vkey) == 0:
        print("Invalid vigenère key.")
    else:
        print("The decrypted string is:")
        vigenere_decryption(encrypted_str, vkey)
