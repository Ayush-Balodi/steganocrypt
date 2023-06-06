import base64
import hashlib
from Crypto.Cipher import AES
from PIL import Image

# making the image object
original_image = Image.open('origin.png')

# loading the pixel values of the original image, each one is a pixel
original_pixelMap = original_image.load()

encrypt_image = Image.new(original_image.mode, original_image.size)
encrypt_pixelMap = encrypt_image.load()

# Reading the message from the user
msg = input("Enter the message: ")
msg_index = 0

password = "Password"
salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=16)
m = hashlib.md5(key)
key = m.digest()[:16]  # 16-byte key for AES

# Generate a 16-byte initialization vector (IV)
iv = hashlib.md5(salt).digest()[:16]

crypter = AES.new(key, AES.MODE_CBC, iv)

print("The message is:", msg)
padding_length = 16 - len(msg) % 16
padding = bytes([padding_length] * padding_length)
msg = msg.encode('utf-8')
msg += padding
ciphertext = crypter.encrypt(msg)
encode_string = base64.b32encode(ciphertext)
print("The encoded string is:", encode_string.decode('utf-8'))
msg = encode_string.decode('utf-8')
msg_len = len(msg)

for row in range(original_image.size[0]):
    for col in range(original_image.size[1]):

        pixel = original_pixelMap[row, col]
        r = pixel[0]  # Red value
        g = pixel[1]  # Green value
        b = pixel[2]  # Blue value

        if row == 0 and col == 0:
            ascii_val = msg_len
            encrypt_pixelMap[row, col] = (ascii_val, g, b)
        elif msg_index < msg_len:
            c = msg[msg_index]
            ascii_val = ord(c)
            encrypt_pixelMap[row, col] = (ascii_val, g, b)
        else:
            encrypt_pixelMap[row, col] = (r, g, b)
        msg_index += 1

original_image.close()

encrypt_image.show()

encrypt_image.save("encrypted_image.png")
encrypt_image.close()
