# Declare constants
A_ASCII = int(ord("A"))


def caesar_cypher(encrypted_text: str, shift: int):
    for char in encrypted_text:
        # ENCRYPTED = ascii(char) - ascii(A)
        # DECRYPTED = (ENCRYPTED - SHIFT) mod 26
        decrypted_code = (int(ord(char)) - A_ASCII - shift) % 26
        # update shift
        shift = decrypted_code
        print(chr(decrypted_code + A_ASCII))
    pass


def vigenere_cipher(encrypted_text: str, key: str):
    for i in range(0, len(encrypted_text)):
        # notice that len(key) could be smaller than len(encrypted_msg)
        # SHIFT = ascii(key[i % len(key)]) - ascii(A)
        # ENCRYPTED = ascii(encrypted_msg[i]) - ascii(A)
        # DECRYPTED = (ENCRYPTED - SHIFT) mod 26
        decrypted_code = (
            int(ord(encrypted_text[i])) - int(ord(key[i % len(key)]))
        ) % 26
        print(chr(decrypted_code + A_ASCII))
    pass


def decrypt_cypher(encrypted_text: str, key: str):
    print("The decrypted string is:")
    # if the key contains only digits, call caesar_cypher
    if key.isdigit():
        caesar_shift = int(key)
        caesar_cypher(encrypted_text, caesar_shift)
    # otherwise, call vigenere_cipher
    else:
        vigenere_cipher(encrypted_text, key)
    pass


# Decrypt text
if __name__ == "__main__":
    # Display preamble
    print("DECRYPT STRING")

    # Get encrypted text
    encrypted_str = input("Input encrypted string: ").replace(" ", "")
    if len(encrypted_str) == 0:
        print("Empty encrypted string.")
    else:
        # Get decryption key
        key = input("Input key: ").replace(" ", "")
        if len(key) == 0:
            print("Empty encrypted string.")
        else:
            # Decrypt text
            decrypt_cypher(encrypted_str, key)
