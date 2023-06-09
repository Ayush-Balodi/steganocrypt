import hashlib
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def encrypt_message(message, password):

    salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
    key = hashlib.md5(password.encode('utf-8') + salt).digest()

    # Create the cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)

    # Concatenate the IV and encrypted message
    iv_and_message = cipher.iv + encrypted_message
    return base64.b64encode(iv_and_message).decode('utf-8')

original_image = Image.open('origin.png')
original_pixelMap = original_image.load()

encrypt_image = Image.new(original_image.mode, original_image.size)
encrypt_pixelMap = encrypt_image.load()

message = input("Enter the message: ")
password = "Password"
msg_len = len(message)
msg_index = 0

encrypted_message = encrypt_message(message, password)
print("Encrypted message:", encrypted_message)

for row in range(original_image.size[0]):
    for col in range(original_image.size[1]):

        list = original_pixelMap[row, col]
        r = list[0]
        g = list[1]
        b = list[2]

        if row==0 and col==0 :
            ascii = msg_len
            encrypt_pixelMap[row, col] = (ascii, g, b)
        elif msg_index<=msg_len:
            c=message[msg_index-1]
            ascii = ord(c)
            encrypt_pixelMap[row, col] = (ascii, g, b)
        else:
            encrypt_pixelMap[row, col] = (r, g, b)
        msg_index+=1

original_image.close()
encrypt_image.show()

encrypt_image.save("encrypted_image.png")
encrypt_image.close()