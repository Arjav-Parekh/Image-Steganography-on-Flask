#!/usr/bin/env python

import click
from PIL import Image
import cv2
import numpy as np
import types
class SteganographyDOI:
    
    @staticmethod
    def messageToBinary(message):
        if type(message) == str:
            return ''.join([ format(ord(i), "08b") for i in message ])
        elif type(message) == bytes or type(message) == np.ndarray:
            return [ format(i, "08b") for i in message ]
        elif type(message) == int or type(message) == np.uint8:
            return format(message, "08b")
        else:
            raise TypeError("Input type not supported")


    @staticmethod
    def hideData(image, secret_message):

        # calculate the maximum bytes to encode
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes to encode:", n_bytes)

        #Check if the number of bytes to encode is less than the maximum bytes in the image
        if len(secret_message) > n_bytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
        
        secret_message += "#####" # you can use any string as the delimeter

        data_index = 0
        # convert input data to binary format using messageToBinary() fucntion
        binary_secret_msg = SteganographyDOI.messageToBinary(secret_message)

        data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
        for values in image:
            for pixel in values:
                # convert RGB values to binary format
                r, g, b = SteganographyDOI.messageToBinary(pixel)
                # modify the least significant bit only if there is still data to store
                if data_index < data_len:
                    # hide the data into least significant bit of red pixel
                    pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # hide the data into least significant bit of green pixel
                    pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # hide the data into least significant bit of  blue pixel
                    pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                # if data is encoded, just break out of the loop
                if data_index >= data_len:
                    break

        return image

    @staticmethod
    def showData(image):

        binary_data = ""
        for values in image:
            for pixel in values:
                r, g, b = SteganographyDOI.messageToBinary(pixel) #convert the red,green and blue values into binary format
                binary_data += r[-1] #extracting data from the least significant bit of red pixel
                binary_data += g[-1] #extracting data from the least significant bit of red pixel
                binary_data += b[-1] #extracting data from the least significant bit of red pixel
        # split by 8-bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        # convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
                break
        #print(decoded_data)
        return decoded_data[:-5] #remove the delimeter to show the original hidden message


    @staticmethod
    # Encode data into image 
    def encode_text(image_name,data,filename):
        # image_name = input("Enter image name(with extension): ") 
        image = cv2.imread(image_name) # Read the input image using OpenCV-Python.
        #It is a library of Python bindings designed to solve computer vision problems. 
        
        #details of the image
        print("The shape of the image is: ",image.shape) #check the shape of image to calculate the number of bytes in it
        print("The original image is as shown below: ")
        resized_image = cv2.resize(image, (500, 500)) #resize the image as per your requirement

        


        # data = input("Enter data to be encoded : ") 

        if (len(data) == 0): 
            raise ValueError('Data is empty')
        
        # filename = input("Enter the name of new encoded image(with extension): ")
        encoded_image = SteganographyDOI.hideData(image, data) # call the hideData function to hide the secret message into the selected image
        cv2.imwrite(filename, encoded_image)


    @staticmethod
    # Decode the data in the image 
    def decode_text(image_name):
        # read the image that contains the hidden image
        # image_name = input("Enter the name of the steganographed image that you want to decode (with extension) :") 
        image = cv2.imread(image_name)  #read the image using cv2.imread() 

        print("The Steganographed image is as shown below: ")
        resized_image = cv2.resize(image, (500, 500)) #resize the original image as per your requirement
        # cv2.imshow("Decrypted Image",resized_image) #display the Steganographed image
            
        text = SteganographyDOI.showData(image)
        return text

    # Image Steganography     
    # @staticmethod    
    # def Steganography(): 
    #     a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: ")
    #     userinput = int(a)
    #     if (userinput == 1):
    #         print("\nEncoding....")
    #         SteganographyDOI.encode_text() 
            
    #     elif (userinput == 2):
    #         print("\nDecoding....") 
    #         print("Decoded message is " + SteganographyDOI.decode_text()) 
    #     else: 
    #         raise Exception("Enter correct input")
          


class SteganographyIOI:

    @staticmethod
    def __int_to_bin(rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        """
        r, g, b = rgb
        return (f'{r:08b}',
                f'{g:08b}',
                f'{b:08b}')

    @staticmethod
    def __bin_to_int(rgb):
        """Convert a binary (string) tuple to an integer tuple.

        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.

        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    @staticmethod
   
    def merge(img1, img2):
        """Merge two images. The second one will be merged into the first one.

        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """
        
        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = SteganographyIOI.__int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = SteganographyIOI.__int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = SteganographyIOI.__int_to_bin(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = SteganographyIOI.__merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = SteganographyIOI.__bin_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        """Unmerge an image.

        :param img: The input image.
        :return: The unmerged/extracted image.
        """

        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = SteganographyIOI.__int_to_bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = SteganographyIOI.__bin_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image


# @click.group()
# def cli():
#     pass



# @cli.command()
# @click.option('--img1', required=True, type=str, help='Image that will hide another image')
# @click.option('--img2', required=True, type=str, help='Image that will be hidden')
# @click.option('--output', required=True, type=str, help='Output image')
def merge(img1, img2, output):
    merged_image = SteganographyIOI.merge(Image.open(img1), Image.open(img2))
    merged_image.save(output)
  


# @cli.command()
# @click.option('--img', required=True, type=str, help='Image that will be hidden')
# @click.option('--output', required=True, type=str, help='Output image')
def unmerge(img, output2):
    unmerged_image = SteganographyIOI.unmerge(Image.open(img))
    unmerged_image.save(output2)

# a = int(input("1. IOI   \n 2. DOI"))
# if(a==1):

#     x=int(input("Enter 1. merge  2.unmerge"))
#     if(x==1):
#         img1=input("enter name and extension: ")
#         img2=input("enter name and extension: ")
#         output=input("enter output and extension: ")

#         merge(img1,img2,output)
#     elif(x==2):
#         img=input("name and png file to be unmerged: ")
#         output=input("enter output and extension: ")
#         unmerge(img, output)

# elif(a==2):
#     y=int(input("Enter 1. encode  2.decode"))
#     if(y==1):
#         img=input("enter name and extension: ")
#         data=input("enter data to be encoded: ")
#         output=input("enter output and extension: ")

#         SteganographyDOI.encode_text(img,data,output)
#     elif(y==2):
#         img=input("enter name and extension of image to be decoded: ")
       

#         SteganographyDOI.decode_text(img)





# if __name__ == '__main__':
#     cli()
