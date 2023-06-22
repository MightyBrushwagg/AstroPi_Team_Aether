import exif
import cv2
import numpy as np
from fastiecm import fastiecm

with open(r"C:\Users\xavie\OneDrive\Desktop\Aether\Aether\aether_pictures\aether_image13.jpg", "rb") as image_file:
    myimage = exif.Image(image_file)

def convertToDecimal(long_lat, reference):
    total = long_lat[0] + long_lat[1]/60 + long_lat[2]/3600
    if reference in ["W", "S"]:
        total *= -1

    return total


print(myimage.gps_latitude)
print(myimage.gps_latitude_ref)
print(myimage.gps_longitude)
print(myimage.gps_longitude_ref)


#with open("/home/borealis/Desktop/aether pictures/image2.jpg", "rb") as image_file:
#    myimage = exif.Image(image_file)

#C:\Users\xavie\Downloads\aether_image271v3.png
#"C:\Users\xavie\OneDrive\Desktop\Aether\Aether\aether_pictures\aether_image305.jpg"
#C:\Users\xavie\OneDrive\Desktop\Aether\Aether\photoshopped pictures\aether_pictures\aether_image296.png
original = cv2.imread(r"C:\Users\xavie\OneDrive\Desktop\Aether\Aether\aether_pictures\aether_image10.jpg")
#print(original)
def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.000001
    ndvi = (b.astype(float) - r.astype(float)) / bottom
    total = 0
    count = 0
    reject = 0
    for j in range(len(ndvi)): # gives sublist index
        for i in range(len(ndvi[j])): # gives index of item in sublist
            if ndvi[j][i] <= 0.15:
                reject += 1
            else:
                count+=1
                total = total + ndvi[j][i] 
    print(total)
    print(count)
    print(total/count)
    print(ndvi)
    print(reject)
    return ndvi

def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)
    #shape = image.shape
    #height = int(shape[0] / 2)
    #width = int(shape[1] / 2)
    #image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


picture = np.zeros(shape=(720, 1080, 3))
picture = picture + 0.01

#print(picture)

display(original, 'Original')
contrasted = contrast_stretch(original)
display(contrasted, 'Contrasted original')
#cv2.imwrite('contrasted.png', contrasted)
ndvi = calc_ndvi(original)
display(ndvi, 'NDVI')
#cv2.imwrite('ndvi.png', ndvi)
ndvi_contrasted = contrast_stretch(ndvi)
display(ndvi_contrasted, 'NDVI Contrasted')
#cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)
color_mapped_prep = ndvi_contrasted.astype(np.uint8)
color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
#print(color_mapped_image)

"""
for sublist in range(len(ndvi_contrasted)): # gives sublist index
        for i in range(len(ndvi_contrasted[sublist])): # gives index of item in sublist
            if ndvi[sublist][i] <= 0.2:
                count+=1
                total = total + ndvi_contrasted[sublist][i]
            else:
                count+=1
                total = total + ndvi_contrasted[sublist][i] 
"""

display(color_mapped_image, 'Color mapped')
cv2.imwrite('color_mapped_image.png', color_mapped_image)
