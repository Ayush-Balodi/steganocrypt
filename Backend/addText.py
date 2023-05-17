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