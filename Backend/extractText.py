import base64
import hashlib
import time
from Crypto.Cipher import DES
from PIL import Image

start_time=time.time()

password="Password"
salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
key = password.encode('utf-8')+salt
m = hashlib.md5(key)
key = m.digest()
(dk, iv) = (key[:8], key[8:])
crypter = DES.new(dk, DES.MODE_CBC, iv)

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

encrypted_string = msg
encrypted_string = base64.b32decode(encrypted_string)
decrypted_string = crypter.decrypt(encrypted_string)
print("The original message was : ",decrypted_string.decode('utf-8'))
end_time = time.time()

print("Execution time is: ", (end_time-start_time))