"""
Presenters Names:
                Eden Dadon
                Dudi Biton
                Eliran Dagan
                Avihay Maman

LSB Image Steganogrpahy Encoder and Decoder Python Program

In this code we were based on the following code:
https://github.com/djrobin17/image-stego-tool
"""

import numpy as np
import rsa
from PIL import Image


def Encode(src, message, dest, qual_secu):
    pre_message = message

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    # Improvement number 1:
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # Divide by n according to the RGB / RGBA format
    total_pixels = array.size//n

    # Improvement number 2:
    message += "$t3g0"
    encrypted_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(encrypted_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            # Our list contains small size (3) lists
            for q in range(0, 3):
                if index < req_pixels:
                    # Improvement number 3:
                    if qual_secu == '1':
                        # Change bits 7,8 (more quality - as the original lsb - as written in the article)
                        array[p][q] = int(bin(array[p][q])[7:9] + encrypted_message[index], 2)
                        index += 1
                    elif qual_secu == '2':
                        # Change bits 5,6 (more secure - as the proposed algorithm - as written in the article)
                        array[p][q] = int(bin(array[p][q])[5:7] + encrypted_message[index], 2)
                        index += 1
                    elif qual_secu == '3':
                        # Change bits 6,7 (merge between security and quality)
                        array[p][q] = int(bin(array[p][q])[6:8] + encrypted_message[index], 2)
                        index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        if verify_encryption(pre_message):
            print("Image Encoded Successfully")
        else:
            print("ERROR: Invalid option chosen")
            exit(1)


def verify_encryption(pre_message):
    """Improvement number 4:"""
    src = "encrypt_photo.png"
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # Divide by n according to the RGB / RGBA format
    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        message = message[:-5]
        if pre_message == message:
            return True
    else:
        return False


def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # Divide by n according to the RGB / RGBA format
    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")


if __name__ == "__main__":

    choice = input("""Please select an option:
- 1 for Encode.
- 2 for Decode.
""")

    if choice == '1':
        qual_secu = input("""Please choose what you prefer: 
- 1 for better quality. 
- 2 for higher security.
- 3 average.
""")

        if qual_secu != '1' and qual_secu != '2' and qual_secu != '3':
            print("ERROR: Invalid option chosen")
            exit(1)

        src = input("Enter Name Of Image (inside your project folder):")
        message = input("Enter Message to Hide:")
        dest = "encrypt_photo.png"
        print("Encoding...")
        Encode(src, message, dest, qual_secu)

    elif choice == '2':
        src = input("Enter Image Name (usually it's encrypt_photo.png): ")
        print("Decoding...")
        Decode(src)

    else:
        print("ERROR: Invalid option chosen")
        exit(1)
