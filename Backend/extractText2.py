import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_message(ciphertext, password):
    salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
    key = hashlib.md5(password.encode('utf-8') + salt).digest()

    # Extract the IV and encrypted message from the base64-encoded ciphertext
    iv_and_message = base64.b64decode(ciphertext)

    # Split the IV and encrypted message
    iv = iv_and_message[:AES.block_size]
    encrypted_message = iv_and_message[AES.block_size:]

    # Create AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the encrypted message
    decrypted_message = cipher.decrypt(encrypted_message)

    # Unpad the decrypted message
    unpadded_message = unpad(decrypted_message, AES.block_size)

    return unpadded_message.decode('utf-8')

ciphertext = input("Enter the ciphertext: ")

password="Password"
decrypted_message = decrypt_message(ciphertext, password)
print("Decrypted message:", decrypted_message)