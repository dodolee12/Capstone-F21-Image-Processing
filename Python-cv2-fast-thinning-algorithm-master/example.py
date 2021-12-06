import numpy as np
import cv2
import ftlib as ft
import matplotlib.pyplot as plt

img = cv2.imread('signature.PNG',0) #binary image
thinned_image = ft.fastThin(img)

#cv2.imshow('original image',img)
#cv2.imshow('thinned image',thinned_image)



denoised_image = cv2.fastNlMeansDenoising(thinned_image,h=70)

#cv2.imshow("denoised",denoised_image)
cv2.imwrite('denoised_signature.png',denoised_image)
indices = np.where(denoised_image < [250])

#for some reason this allows to to be right side up.
x_coords = indices[1]
y_coords = -indices[0]
plt.scatter(x_coords,y_coords)

num_points = len(x_coords)
id_to_coord = {}

for i in range(num_points):
    id_to_coord[i] = (x_coords[i],y_coords[i])



#plt.show()
cv2.waitKey(0) # press any key to close
cv2.destroyAllWindows()

