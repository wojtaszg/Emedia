import struct
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class Bmp:
    def __init__(self, obraz):
        """
        :param obraz:
         Konstruktor klasy.
         Odczytuje informacje zawarte w nagłówku pliku i DIB oraz
         zapisuje je do atrybutów klasy
        """
        if os.path.exists(obraz):
            self.file = obraz
            bmp = open(self.file, 'rb')
            #bmp file header
            self.header_type = bmp.read(2).decode()
            self.file_size = struct.unpack('I', bmp.read(4))[0]
            self.reserved_1 = struct.unpack('H', bmp.read(2))[0]
            self.reserved_2 = struct.unpack('H', bmp.read(2))[0]
            self.offset = struct.unpack('I', bmp.read(4))[0]
            #dib header
            self.dib_header_size = struct.unpack('I', bmp.read(4))[0]
            self.width = struct.unpack('I', bmp.read(4))[0]
            self.height = struct.unpack('I', bmp.read(4))[0]
            self.colour_planes = struct.unpack('H', bmp.read(2))[0]
            self.bits_per_pixel = int(struct.unpack('H', bmp.read(2))[0])
            self.compression_method = struct.unpack('I', bmp.read(4))[0]
            self.raw_image_size = struct.unpack('I', bmp.read(4))[0]
            self.horizontal_resolution = struct.unpack('I', bmp.read(4))[0]
            self.vertical_resolution = struct.unpack('I', bmp.read(4))[0]
            self.number_of_colours = struct.unpack('I', bmp.read(4))[0]
            self.important_colours = struct.unpack('B', bmp.read(1))[0]
            self.colour_rotation = struct.unpack('B', bmp.read(1))[0]
            self.bi_reserved = struct.unpack('H', bmp.read(2))[0]
            if self.dib_header_size == 52 or self.dib_header_size == 56 or \
                    self.dib_header_size == 108 or self.dib_header_size == 124:
                self.red_mask = struct.unpack('I', bmp.read(4))[0]
                self.green_mask = struct.unpack('I', bmp.read(4))[0]
                self.blue_mask = struct.unpack('I', bmp.read(4))[0]
                if self.dib_header_size == 56 or self.dib_header_size == 108 or self.dib_header_size == 124:
                    self.alpha_mask = struct.unpack('I', bmp.read(4))[0]
                    if self.dib_header_size == 108 or self.dib_header_size == 124:
                        self.colour_space = bmp.read(4).decode()[::-1]
                        bmp.seek(36, 1)
                        self.red_gamma = struct.unpack('I', bmp.read(4))[0]
                        self.green_gamma = struct.unpack('I', bmp.read(4))[0]
                        self.blue_gamma = struct.unpack('I', bmp.read(4))[0]
                        if self.dib_header_size == 124:
                            self.intent = struct.unpack('I', bmp.read(4))[0]
                            self.icc_data = struct.unpack('I', bmp.read(4))[0]
                            self.icc_size = struct.unpack('I', bmp.read(4))[0]
                            self.reserved = struct.unpack('I', bmp.read(4))[0]
            bmp.close()

    def header(self):
        """
        Metoda wyświetlająca informacje o obrazie odczytane
        z nagłówka pliku oraz nagłówka DIB
        """
        #bmp file header
        print('Type:' + self.header_type)
        print('Size: ' + str(self.file_size))
        print('Reserved 1: ' + str(self.reserved_1))
        print('Reserved 2: ' + str(self.reserved_2))
        print('Offset: ' + str(self.offset))
        #dib header
        print('DIB Header Size: ' + str(self.dib_header_size))
        print('Width: ' + str(self.width))
        print('Height: ' + str(self.height))
        print('Colour Planes: ' + str(self.colour_planes))
        print('Bits per Pixel: ' + str(self.bits_per_pixel))
        print('Compression Method: ' + str(self.compression_method))
        print('Raw Image Size: ' + str(self.raw_image_size))
        print('Horizontal Resolution: ' + str(self.horizontal_resolution))
        print('Vertical Resolution: ' + str(self.vertical_resolution))
        print('Number of Colours: ' + str(self.number_of_colours))
        print('Important Colours: ' + str(self.important_colours))
        print('Colour Rotation: ' + str(self.colour_rotation))
        print('BI Reserved: ' + str(self.bi_reserved))
        if self.dib_header_size == 52 or self.dib_header_size == 56 or \
                self.dib_header_size == 108 or self.dib_header_size == 124:
            print('Red mask: ' + str(self.red_mask))
            print('Green mask: ' + str(self.green_mask))
            print('Blue mask: ' + str(self.blue_mask))
            if self.dib_header_size == 56 or self.dib_header_size == 108 or self.dib_header_size == 124:
                print('Alpha mask: ' + str(self.alpha_mask))
                if self.dib_header_size == 108 or self.dib_header_size == 124:
                    print('Colour space: ' + str(self.colour_space))
                    print('Red gamma: ' + str(self.red_gamma))
                    print('Green gamma: ' + str(self.green_gamma))
                    print('Blue gamma: ' + str(self.blue_gamma))
                    if self.dib_header_size == 124:
                        print('Intent: ' + str(self.intent))
                        print('ICC Profile data: ' + str(self.icc_data))
                        print('ICC Profile size: ' + str(self.icc_size))
                        print('Reserved: ' + str(self.reserved))


    def colour_table(self):
        """
        Metoda odczytująca zawartość tablicy kolorów,
        wyświetlająca obraz utworzony z odczytanych kolorów oraz zapisująca go.
        Tablica kolorów występuje tylko dla głębi bitowej <= 8
        """
        if self.bits_per_pixel <= 8:
            x = self.number_of_colours
            colours = []
            bmp = open(self.file, 'rb')
            bmp.seek(self.dib_header_size + 14, 0)

            for i in range(x):
                bl = int(struct.unpack('B', bmp.read(1))[0])
                gr = int(struct.unpack('B', bmp.read(1))[0])
                re = int(struct.unpack('B', bmp.read(1))[0])
                al = int(struct.unpack('B', bmp.read(1))[0])
                colours.append((re, gr, bl))
            bmp.close()
            colours = (np.array(colours)).astype(np.uint8)
            title = "Colour table"
            # creating bar image
            cols = len(colours)
            rows = max([1, int(cols / 2.5)])
            # Create colour Array
            colours_data = np.tile(colours, (rows, 1)).reshape(rows, cols, 3)
            # Create Image from Array
            colours_img = Image.fromarray(colours_data, 'RGB')
            # saving image
            colours_img.save("{}.bmp".format(title))
            colours_img.show()


    def icc_profile(self):
        """
        Metoda odczytująca zawartość profilu kolorów ICC,
        wyświetlająca obraz utworzony z odczytanych kolorów oraz zapisująca go.
        Profil kolorów ICC występuje tylko w obrazach BMP z nagłówkiem DIB BITMAPV5HEADER
        """
        colours_profile = []
        bmp = open(self.file, 'rb')
        bmp.seek(self.icc_data, 0)
        x = int(self.icc_size / 4)
        for i in range(x):
            re = int(struct.unpack('B', bmp.read(1))[0])
            gr = int(struct.unpack('B', bmp.read(1))[0])
            bl = int(struct.unpack('B', bmp.read(1))[0])
            # al = int(struct.unpack('B', bmp.read(1))[0])
            colours_profile.append((re, gr, bl))
        bmp.close()
        colours = (np.array(colours_profile)).astype(np.uint8)
        title = "ICC Profile"
        # creating bar image
        cols = len(colours)
        rows = max([1, int(cols / 2.5)])
        # Create color Array
        colours_data = np.tile(colours, (rows, 1)).reshape(rows, cols, 3)
        # Create Image from Array
        colours_img = Image.fromarray(colours_data, 'RGB')
        # saving image
        colours_img.save("{}.bmp".format(title))
        colours_img.show()


    def fourier_transform(self):
        """
        Metoda wykonująca dyskretną transformatę Fouriera na podanym obrazie.
        Metoda wyświetla oryginalny obraz, monochromatyczny oraz jego moduł widma i fazę.
        """
        plt.figure(figsize=(8.4 * 5, 6.8 * 5))
        img_c = Image.open(self.file)
        img_c1 = cv2.imread(self.file, 0)
        img_c2 = np.fft.fft2(img_c1)
        img_c3 = np.fft.fftshift(img_c2)
        img_xd = np.angle(img_c2)
        plt.subplot(141), plt.imshow(img_c), plt.title("Oryginalny obraz")
        plt.subplot(142), plt.imshow(img_c1, "gray"), plt.title("Obraz czarnobiały")
        plt.subplot(143), plt.imshow(np.log(np.abs(img_c3)), "gray"), plt.title("Moduł widma")
        plt.subplot(144), plt.imshow(img_xd, "gray"), plt.title("Faza")
        plt.show()

    def anonymisation(self):
        """
        Metoda anonimizująca podany plik BMP.
        Anonimizacja polegała na zastępowaniu informacji,
        które nie było niezbędne do działania zerowymi bajtami
        oraz usuwaniu bajtów znajdujących się poza obrazem.
        """
        x = self.number_of_colours
        row = int(np.ceil(((self.bits_per_pixel * self.width) / 32) * 4))
        if row % 4 != 0:
            padding = 4 - (row % 4)
        else:
            padding = 0

        zero = (0).to_bytes(1, byteorder='little')
        file_in = open(self.file, 'rb')
        file_out = open('kopia.bmp', 'ab+')
        #bmb file header
        file_in.seek(0, 0)
        file_out.write(file_in.read(2))
        file_out.write(zero * 8)
        file_in.seek(8, 1)
        file_out.write(file_in.read(4))
        #dib header
        file_out.write(file_in.read(12))
        file_out.write(zero * 2)
        file_in.seek(2, 1)
        file_out.write(file_in.read(10))
        file_out.write(zero * 8)
        file_in.seek(8, 1)
        file_out.write(file_in.read(8))
        if self.dib_header_size == 52 or self.dib_header_size == 56:
            file_out.write(file_in.read(self.dib_header_size - 40))
        if self.dib_header_size == 108 or self.dib_header_size == 124:
            if self.compression_method != 3 and self.compression_method != 6:
                file_out.write(zero * 16)
                file_in.seek(16, 1)
            else:
                file_out.write(file_in.read(16))
            file_out.write(file_in.read(4))
            file_out.write(zero * 36)
            file_in.seek(36, 1)
            file_out.write(file_in.read(12))
        if self.dib_header_size == 124:
            file_out.write(file_in.read(12))
            file_out.write(zero * 4)
            file_in.seek(4, 1)
        #colour table
        if self.bits_per_pixel <= 8:
            for i in range(x):
                file_out.write(file_in.read(3))
                file_out.write(zero)
                file_in.seek(1, 1)
        #padding
        if padding > 0:
            for i in range(self.height):
                file_out.write(file_in.read(row))
                file_out.write(zero * padding)
                file_in.seek(padding, 1)
        else:
            file_out.write(file_in.read(self.raw_image_size))
        #icc profile
        if self.dib_header_size == 124:
            file_in.seek(self.icc_data)
            file_out.write(file_in.read(self.icc_size))
        file_out.close()
        file_in.close()
        os.system("rm " + self.file)
        os.system("mv kopia.bmp " + self.file)
        img = Image.open(self.file)
        img.show()


a = Bmp("bmp_v5.bmp")
a.header()
if a.dib_header_size == 124:
    a.icc_profile()
if a.bits_per_pixel <= 8:
    a.colour_table()
a.fourier_transform()
a.anonymisation()