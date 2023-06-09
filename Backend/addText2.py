import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def encrypt_message(message, password):
    # Generate salt
    salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'

    # Derive key from password and salt using MD5
    key = hashlib.md5(password.encode('utf-8') + salt).digest()

    # Create AES cipher object with CBC mode
    cipher = AES.new(key, AES.MODE_CBC)

    # Pad the message
    padded_message = pad(message.encode('utf-8'), AES.block_size)

    # Encrypt the padded message
    encrypted_message = cipher.encrypt(padded_message)

    # Concatenate the IV and encrypted message
    iv_and_message = cipher.iv + encrypted_message

    # Return the base64-encoded ciphertext
    return base64.b64encode(iv_and_message).decode('utf-8')

message = input("Enter the message: ")
password = "Password"

encrypted_message = encrypt_message(message, password)
print("Encrypted message:", encrypted_message)