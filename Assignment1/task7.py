def caesar_decryption(encrypted_msg: str, caesar_shift: int):
    A_ascii = int(ord("A"))
    for char in encrypted_msg:
        # ENCRYPTED = ascii(char) - ascii(A)
        # DECRYPTED = (ENCRYPTED - SHIFT) mod 26
        decrypted_code = (int(ord(char)) - A_ascii - caesar_shift) % 26
        # update caesar_shift
        caesar_shift = decrypted_code
        print(chr(decrypted_code + A_ascii))
    pass


print("DECRYPT STRING")

encrypted_str = input("Input encrypted string: ").replace(" ", "")
# check if the encrypted string and caesar shift are valid
if len(encrypted_str) == 0:
    print("Empty encrypted string.")
else:
    caesar_shift = int(input("Input caesar shift: "))
    if caesar_shift < 0 or caesar_shift > 25:
        print("Invalid caesar shift.")
    else:
        print("The decrypted string is:")
        caesar_decryption(encrypted_str, caesar_shift)
