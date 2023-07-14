import hashlib
import time
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

start_time=time.time()
def decrypt_message(ciphertext, password):
    salt = b'\x28\xAB\xBC\xCD\xDE\xEF\x00\x33'
    key = hashlib.md5(password.encode('utf-8') + salt).digest()

    # Extract the IV and encrypted message from the base64-encoded ciphertext
    iv_and_message = base64.b64decode(ciphertext)

    # Split the IV and encrypted message
    iv = iv_and_message[:AES.block_size]
    encrypted_message = iv_and_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the encrypted message
    decrypted_message = cipher.decrypt(encrypted_message)
    unpadded_message = unpad(decrypted_message, AES.block_size)
    return unpadded_message.decode('utf-8')

encrypted_image=Image.open('encrypted_image.png')
encrypted_pixelMap=encrypted_image.load()

message=""
msg_index = 0

for row in range(encrypted_image.size[0]):
    for col in range(encrypted_image.size[1]):

        list = encrypted_pixelMap[row, col]
        r= list[0]

        if row==0 and col==0:
            msg_len=r
        elif msg_len>msg_index:
            message = message+chr(r)
            msg_index = msg_index+1

encrypted_image.close()

ciphertext = message
print("The cipher text is: ",ciphertext)
password="Password"
decrypted_message = decrypt_message(ciphertext, password)
print("Decrypted message:", decrypted_message)
end_time=time.time()
print("Execution time is: ", (end_time-start_time))