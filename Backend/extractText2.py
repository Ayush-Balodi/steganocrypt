import base64
import hashlib 
from Crypto.Cipher import AES
from PIL import Image

password="Password"
salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=16)
key = key[:16]
iv = salt
crypter = AES.new(key, AES.MODE_CBC, iv)

encrypt_image=Image.open('encrypted_image.png')

encrypt_pixelMap=encrypt_image.load()

msg=""
msg_index=0
for row in range(encrypt_image.size[0]):
    for col in range(encrypt_image.size[1]):

        list=encrypt_pixelMap[row, col]
        r=list[0]

        if row==0 and col==0:
            msg_len=r
        elif msg_len>msg_index:
            msg = msg+chr(r)
            msg_index = msg_index+1
    
encrypt_image.close()

print("The encrypted message is : ", msg)

encypted_string = msg
encypted_string = base64.b32decode(encypted_string)
decrypted_string = crypter.decrypt(encypted_string)
print("The original message was : ",decrypted_string.decode('utf-8'))