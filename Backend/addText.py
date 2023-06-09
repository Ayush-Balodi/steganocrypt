import base64 
import hashlib
from Crypto.Cipher import DES
from PIL import Image

# making the image object
original_image = Image.open('origin.png')

# loading the pixel values of origin image, each one is pixel
original_pixelMap = original_image.load()

encrypt_image = Image.new(original_image.mode, original_image.size)
encrypt_pixelMap = encrypt_image.load()

# Reading the message from the user
msg = input("Enter the message : ")
msg_index=0

password = "Password"
salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
key = password.encode('utf-8') + salt
m = hashlib.md5(key)
key = m.digest()
(dk, iv) = (key[:8], key[8:])
crypter = DES.new(dk, DES.MODE_CBC, iv)

print("The message is : ", msg)
padding_length = 8 - len(msg)%8
padding = bytes([padding_length] * padding_length)
msg = msg.encode('utf-8')
msg += padding
ciphertext = crypter.encrypt(msg)
encode_string = base64.b32encode(ciphertext)
print("The encoded string is: ",encode_string.decode('utf-8'))
msg = encode_string.decode('utf-8')
msg_len=len(msg)

for row in range(original_image.size[0]):
    for col in range(original_image.size[1]):

        list=original_pixelMap[row, col]
        r=list[0]   # Red value
        g=list[1]   # Green value
        b=list[2]   # Blue value

        if row==0 and col==0:
            ascii=msg_len
            encrypt_pixelMap[row, col]=(ascii,g,b)
        elif msg_index<=msg_len:
            c=msg[msg_index-1]
            ascii=ord(c)
            encrypt_pixelMap[row, col]=(ascii,g,b)
        else:
            encrypt_pixelMap[row, col]=(r,g,b)
        msg_index+=1

original_image.close()

encrypt_image.show()

encrypt_image.save("encrypted_image.png")
encrypt_image.close()