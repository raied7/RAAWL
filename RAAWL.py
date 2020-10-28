#!/usr/local/bin/python3

# Raied Shoaib
# RAAWL: Resize And Add Watermark/Logo

import os
import sys
import PIL
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# global variable to keep the program running. Helps return to main if desired by user
keep_going = True
##################################################################################################
# Function to add a watermark to an indiviudal file
def watermark():

        # Ask if user wants to add a watermark to all the files in the directory. If yes, call doAllWatermark()
        doAllFiles = input("Would you like to add the watermark to ALL files in the current directory? (y/n)")
        if(doAllFiles.lower() == 'y'):
            doAllWatermark()

        # Ask user for the file to add the watermark to and check that it exists
        filename = input('Enter the name of the file you would like to add a watermark to: ')
        exists = os.path.isfile(filename)
        while(exists == False):
            exists = input("Please enter a file that exists! : ")

        # Create a '.png' copy of the image - PNG allows for alpha (transparency)
        im = Image.open(filename)
        imC = im.copy().convert('RGBA')
        width, height = im.size

        # Allows us to draw text on the image
        # draw = ImageDraw.Draw(imC)

        # Ask for the watermark text
        text = input('Input the text for the watermark: ')

        # Ask for a valid size for the watermark
        size = -1
        while(size <= 0 or size > width or size > height):
            print('Input the size for the watermark. Size cannot be 0 or greater than image width or length:','(',width, ',', height,')', '\n')
            size = (int)(input('Watermark size: '))

        # Ask for a valid transparency factor
        transparency = (int)(input('Enter the transparency value (0-255).\n\nEx. A value of 128 will make the watermark ~50% transparent (128 / 255 ~ 50)\n\nPlease enter the watermark transparency factor: '))
        while(transparency <=0 or transparency > 255):
            print('Please enter a value between 0 and 255!')
            transparency = (int)(input('Transparency value: '))

        # Bug with ImageFont.truetype where you have to read the font file name as bytes for it to work properly. Strange.
        # I looked for better solutions, but this was the one that worked. Found on Github.
        # https://jdhao.github.io/2018/12/04/two_issues_related_to_imagefont_pillow/
        with open('ostrich-regular.ttf', 'rb') as f:
            bytes_font = BytesIO(f.read())
        font = ImageFont.truetype(bytes_font, size)

        text_width, text_height = font.getsize(text)

        # Create a transparent canvas to place the text on
        txt = Image.new('RGBA', im.size, (255,255,255,0))
        d = ImageDraw.Draw(txt)

        # Find the center of the image and the text
        x = (int)((width/2) - (text_width/2))
        y = (int)((height/2) - (text_height/2))

        # Add the watermark text to the canvas and alpha_composite the canvas and the image
        print('\nAdding watermark to %s...\n' % (filename))
        d.text((x, y), text, fill= (255, 255, 255, transparency), font = font)
        out = Image.alpha_composite(imC, txt)

        # Save the watermarked file in a 'withWatermark folder'
        os.makedirs('withWatermark', exist_ok = True)
        # Get the file name without the extension and add '.png' to it
        filename = (os.path.splitext(filename)[0])
        out.save(os.path.join('withWatermark', filename +'.png'))

        # Ask user if they want to continue or exit
        global keep_going
        keep_going = input("Add watermark to another picture? (y/n)")
        if (keep_going.lower() != 'y'):
            menu = input('Exit or return to main? (x/m): ')
        if(menu.lower() == 'm'):
            keep_going = False
            main()
        else:
            sys.exit("Have a nice day!")
##################################################################################################
def doAllWatermark():

    # Ask for the watermark text, size, and transparency
    # The same watermark will be applied to all the images
    text = input('Input the text for the watermark: ')

    size = -1
    while(size <= 0):
        print('Input the size for the watermark. Size cannot be 0 or greater than width or length of the images!')
        size = (int)(input('Watermark size: '))

    transparency = (int)(input('Enter the transparency value (0-255).\n\nEx. A value of 128 will make the watermark ~50% transparent (128 / 255 ~ 50)\n\nPlease enter the watermark transparency factor: '))
    while(transparency <=0 or transparency > 255):
        print('Please enter a value between 0 and 255!')
        transparency = (int)(input('Transparency value: '))

    with open('ostrich-regular.ttf', 'rb') as f:
        bytes_font = BytesIO(f.read())
    font = ImageFont.truetype(bytes_font, size)

    text_width, text_height = font.getsize(text)

    # Loop through all the image files in the project directory and add the watermark to them
    # Similar to doAll() with logos and same code as addWatermark()
    for filename in os.listdir('.'):
        if not(filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg')):
            continue

        im = Image.open(filename)
        imC = im.copy().convert('RGBA')
        width, height = im.size

        x = (int)((width/2) - (text_width/2))
        y = (int)((height/2) - (text_height/2))

        draw = ImageDraw.Draw(im)

        txt = Image.new('RGBA', im.size, (255,255,255,0))
        d = ImageDraw.Draw(txt)

        print('\nAdding watermark to %s...\n' % (filename))
        d.text((x, y), text, fill= (255, 255, 255, transparency), font = font)
        out = Image.alpha_composite(imC, txt)

        os.makedirs('withWatermark', exist_ok = True)
        filename = (os.path.splitext(filename)[0])
        out.save(os.path.join('withWatermark', filename +'.png'))

    # Ask user if they want to continue or exit
    global keep_going
    menu = input('Exit or return to main? (x/m): ')
    if(menu.lower() == 'm'):
        keep_going = False
        main()
    else:
        sys.exit("Have a nice day!")

##################################################################################################
# Sub-function to literally add the logo. Allows user_input() to keep looping and ask user for indiviudal files
def add_Logo(filename, LOGO_FILENAME, logoIm):

    logoWidth, logoHeight = logoIm.size

    logoImC = logoIm.copy().convert('RGBA')
    im = Image.open(filename)

    imC = im.copy().convert('RGBA')
    width,height = imC.size

    # Add logo to the bottom right corner of the image
    print('Adding logo to %s...' % (filename))
    imC.paste(logoImC, (width - logoWidth - 5, height - logoHeight - 7), logoImC)

    filename = (os.path.splitext(filename)[0])
    imC.save(os.path.join('withLogo', filename + '.png'))

##################################################################################################
# Primary function for adding a logo
def user_input():

    global keep_going
    while keep_going:
    # Ask for the logo file's name and make sure it is a '.png' file that exists
        LOGO_FILENAME = input("Enter the logo's file name: ")

        exists = os.path.isfile(LOGO_FILENAME)

        while(exists == False):
            exists = input("Please enter a file that exists! : ")

        while not(LOGO_FILENAME.lower().endswith('.png')):
            LOGO_FILENAME = input("Please enter a valid file name (ending with .png): ")

        logoIm = Image.open(LOGO_FILENAME)
        logoWidth, logoHeight = logoIm.size

        # Ask if the user wants to add a logo to all the pictures. If yes, call the doAll function
        doAllFiles = input("Would you like to paste the logo on ALL files in the current directory? (y/n)")
        if(doAllFiles.lower() == 'y'):
            doAll(LOGO_FILENAME, logoIm)

        # While loop to keep the program running. Adds logo file by file and asks user for each new file
        # Asks and checks user input for the image file, logo width, and logo height
        # keep_going = True
        # while keep_going:
        filename = input("Enter the name of the file to add logo to: ")

        while(filename == LOGO_FILENAME):
            print('You cannot add the logo to itself')
            filename = input("Enter the file name: ")

        while(os.path.isfile(filename) == False):
            print("Please enter a file that exists!")
            filename = input("Enter the file name: ")

        while not (filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg')):
            print("Please enter a valid file name (ending with .png or .jpg) that is not the logo file!")
            filename = input("Enter the filename: ")

        im = Image.open(filename)
        width,height = im.size

        newLogoW = (int)(input("Enter logo width: "))

        while(newLogoW > width or newLogoW <= 0):
            if(newLogoW > width):
                print('Logo width cannot be greater than the picture width! -->', width)
            if(newLogoW <= 0):
                print('Logo width cannot be 0 or negative!')
            newLogoW = (int)(input("Enter logo width: "))

        newLogoH = (int)(input("Enter logo height: "))

        while(newLogoH > height or newLogoH <= 0):
            if(newLogoH > height):
                print("Logo height cannot be greater than the picture height! -->", height)
            if(newLogoH <= 0):
                print('Logo height cannot be 0 or negative!')
            newLogoH = (int)(input("Enter logo height: "))

        # Resize the logo with the new user-defined dimensions
        logoWidth = newLogoW
        logoHeight = newLogoH

        logoIm = logoIm.resize((logoWidth, logoHeight))

        # Create a folder 'withLogo' in the project directory and save the image with logos to it
        os.makedirs('withLogo', exist_ok = True)
        add_Logo(filename, LOGO_FILENAME, logoIm)

        # Ask user if they want to continue or exit

        keep_going = input("Add logo to another picture? (y/n)")
        if (keep_going.lower() != 'y'):
            menu = input('Exit or return to main? (x/m): ')
            if(menu.lower() == 'm'):
                keep_going = False
                main()
            else:
                sys.exit("Have a nice day!")

# Add the logo to all the images in the project directory
def doAll(LOGO_FILENAME, logoIm):

    # Ask for logo dimensions
    newLogoW = (int)(input("Enter logo width: "))

    while(newLogoW <= 0):
        print("Logo width cannot be 0 or negative!")
        newLogoW = (int)(input("Enter logo width: "))

    newLogoH = (int)(input("Enter logo height: "))

    while(newLogoH <= 0):
        print("Logo width cannot be 0 or negative!")
        newLogoH = (int)(input("Enter logo height: "))

    logoWidth = newLogoW
    logoHeight = newLogoH

    logoIm = logoIm.resize((logoWidth, logoHeight))

    os.makedirs('withLogo', exist_ok = True)
    # Loop through all the image files in the directory and add the logo to them
    for filename in os.listdir('.'):
        if not(filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename == LOGO_FILENAME):
            continue

        logoWidth, logoHeight = logoIm.size

        logoImC = logoIm.copy().convert('RGBA')
        im = Image.open(filename)

        imC = im.copy().convert('RGBA')
        width,height = imC.size

        # Add logo to the bottom right corner of the image
        print('Adding logo to %s...' % (filename))
        imC.paste(logoImC, (width - logoWidth - 5, height - logoHeight - 7), logoImC)

        filename = (os.path.splitext(filename)[0])
        imC.save(os.path.join('withLogo', filename + '.png'))
    # Ask user if they want to continue or exit
    global keep_going
    menu = input('Exit or return to main? (x/m): ')
    if(menu.lower() == 'm'):
        keep_going = False
        main()
    else:
        sys.exit("Have a nice day!")

##################################################################################################

# "Main Menu" - provide instructions and ask user what they want to do
def main():
    print("Hello! Welcome to RAAWL (Resize And Add Watermark/Logo)\n\nThis program allows you to add your logo or watermark to a picture of your choice\nHere are some guidelines to follow:\n1. Make sure the logo file is a .png file\n2. Make sure the picture file (the picture to add the logo/watermark to) is either a .png, .jpg, or .jpeg file\n3. Make sure all the images you want to add logo/watermark too are in the same folder as this program!\n4. Use common sense and do not enter nonsense values when prompted\n5. The logo is added to the bottom right corner of the picture and the watermark is added to the center of the picture.\n6. Follow the prompts and enjoy!\n")

    # change directory to the project directory
    abspath = os.path.abspath(sys.argv[0])
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    choice = input('Would you like to add a logo or a watermark? (w/l): ')

    global keep_going
    while (choice.lower() != 'w' or choice.lower() != 'l'):
        if(choice.lower() == 'w'):
            keep_going = True
            watermark()
        if (choice.lower() == 'l'):
            keep_going = True
            user_input()
        else:
            choice = input('Please enter a valid answer w (watermaek) or l(logo): ')

main()
