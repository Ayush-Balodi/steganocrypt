from PIL import Image

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

print("The hidden message is : ", msg)
