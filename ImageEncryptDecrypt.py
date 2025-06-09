def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)  # Just reverse the shift

def main():
    print("=== Caesar Cipher Tool ===")
    choice = input("Choose mode (encrypt/decrypt): ").strip().lower()
    
    if choice not in ['encrypt', 'decrypt']:
        print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")
        return

    message = input("Enter the message: ")
    try:
        shift = int(input("Enter the shift value (e.g., 3): "))
    except ValueError:
        print("Shift must be an integer.")
        return

    if choice == 'encrypt':
        encrypted = caesar_encrypt(message, shift)
        print("Encrypted message:", encrypted)
    else:
        decrypted = caesar_decrypt(message, shift)
        print("Decrypted message:", decrypted)

if __name__ == "__main_":
    main()