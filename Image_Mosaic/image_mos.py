import math
import random
import os
from PIL import Image
import numpy as np

class img :
    original = ""
    images = ""
    grid = []
    output = ""

def image_info(mos):
    mos.original = input("Enter the path address of the image to be mosaiced:")
    mos.images = input("Enter the Folder address of sample images:")
    x=input("Enter the grid size for the output image:")
    x,y = x.split()
    mos.grid.append(int(x))
    mos.grid.append(int(y))
    mos.output = input("Enter the address and name of the mosaiced image:")
    return mos

def List_images(dir):
    files = os.listdir(dir)
    sample_imgs = []
    for i in files:
        fileP = os.path.abspath(os.path.join(dir, i))
        try:
            fp = open(fileP, "rb")
            im = Image.open(fp)
            sample_imgs.append(im)
            im.load()
            fp.close()
        except:
            print("Invalid image: {}".format(fileP))
    return (sample_imgs)

def Final_image(Output_tiled, d):
    l=grid[0]
    b=grid[1]
    length=max([i.size[0] for i in Output_tiled])
    breadth=max([i.size[1] for i in Output_tiled])
    mosaiced_img = Image.new('RGB',(b*length,l*breadth))
    for i in range(len(Output_tiled)):
        r= int(i/b)
        c= i-b*r
        mosaiced_img.paste(Output_tiled[i],(c*length,r*breadth))
    return (mosaiced_img)

'''
Beginning
'''

#Taking Information from user about images
img_details = img()
mos = image_info(img_details)

original_img = Image.open(mos.original)
# list of sample images
sample_imgs = List_images(mos.images)

# check if any valid input images found
if sample_imgs == []:
    print('Folder of sample images is empty in {}. \nFinishing the program'.format(mos.images))
    exit()

# size of grid
grid = (int(mos.grid[1]), int(mos.grid[0]))

# Storing address for output image
output_filename = mos.output

# shuffling the list of images
random.shuffle(sample_imgs)

# resize the input to fit original image size
print('Resizing the sample images according to the given grid size')
d = (int(original_img.size[0] / grid[1]),
        int(original_img.size[1] / grid[0]))
print("Dimension of Biggest tile possible: {}".format(d))
# resolution adjustment by resizing image
for i in sample_imgs:
    i.thumbnail(d)
'''
Starting the process for conversion of image into mosaic
'''
#Divide the original_img
list = []
Length = original_img.size[0]
Breadth = original_img.size[1]
tile_length = int(Length / grid[1])
tile_breadth = int(Breadth / grid[0])
for i in range(grid[0]):
    for j in range(grid[1]):
        list.append(original_img.crop((j*tile_length, i*tile_breadth, (j+1)*tile_length, (i+1)*tile_breadth)))
Tiled_image =list

Output_tiled = []
c=0
Turn = int(len(Tiled_image) / 5)
sample_img_val = []
for i in sample_imgs:
    #Avg_RGB
    try:
        ar = np.array(i)
        l,b,dim=ar.shape
        t=(tuple(np.average(ar.reshape(l * b, dim), axis=0)))
        sample_img_val.append(t)
    except ValueError:
        continue

print("Total number of tiles: {}".format(len(Tiled_image)))
for i in Tiled_image:
    #Avg_RGB
    ar = np.array(i)
    l,b,dim=ar.shape
    curr_tile_val=(tuple(np.average(ar.reshape(l * b, dim), axis=0)))
    #Finding the most matching sample image for the particular tile
    ind = 0
    min = 0
    min_dist = math.inf
    for d in sample_img_val:
        #Eucledian Distance
        dist = math.sqrt((((d[0]-curr_tile_val[0])**2)+((d[1]-curr_tile_val[1])**2)+((d[2]-curr_tile_val[2])**2)))
        if dist < min_dist:
            min_dist = dist
            min = ind
        ind += 1
    matched = min

    Output_tiled.append(sample_imgs[matched])
    if (c>0)and(Turn>5)and(c%Turn==0):
        print('Number of Tiles converted:{}'.format(c))
    c+= 1

mosaic_image = Final_image(Output_tiled, grid)
# write out mosaic
mosaic_image.save(output_filename, 'jpeg')

print("saved output to {}".format(output_filename))
print('done.')
img = Image.open(mos.original)
img.show()
img=Image.open(output_filename)
img.show()
