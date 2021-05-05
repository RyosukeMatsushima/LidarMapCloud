
import cv2
import numpy as np

from scipy import ndimage, misc
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10, 3))
ax1, ax2, ax3 = fig.subplots(1, 3)
img = misc.ascent()
img_45 = ndimage.rotate(img, 45, reshape=False)
full_img_45 = ndimage.rotate(img, 45, reshape=True)

print("img_45")
print(img_45)
print("img")
print(img)

test_img = np.zeros(img.shape, dtype=int)

for i in range(test_img.shape[0]):
    if i % 10 < 6:
        test_img[i,:] = 100

print("test_img")
print(test_img)

ax1.imshow(img, cmap='gray')
ax1.set_axis_off()
ax2.imshow(img_45, cmap='gray')
ax2.set_axis_off()
ax3.imshow(test_img, cmap='gray')
ax3.set_axis_off()
fig.set_tight_layout(True)
plt.show()


# open cv polar transform

#--- the following holds the square root of the sum of squares of the image dimensions ---
#--- this is done so that the entire width/height of the original image is used to express the complete circular range of the resulting polar image ---
img = test_img.astype(np.uint8)

value = np.sqrt(((img.shape[0]/2.0)**2.0)+((img.shape[1]/2.0)**2.0))

polar_image = cv2.linearPolar(img,(img.shape[0]/2, img.shape[1]/2), value, cv2.WARP_FILL_OUTLIERS)

polar_image = polar_image.astype(np.uint8)
cv2.imshow("Polar Image", polar_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("polar_image")
print(polar_image)

print("img")
print(img)


# 逆変換(リニア)
test_img = np.zeros(img.shape, dtype=float)

for i in range(test_img.shape[0]):
    test_img[i,:] = i * 2

test_img = test_img.astype(np.uint8)

img = test_img

flags = cv2.INTER_CUBIC + cv2.WARP_FILL_OUTLIERS + cv2.WARP_POLAR_LINEAR + cv2.WARP_INVERSE_MAP
linear_polar_inverse_image = cv2.warpPolar(test_img, (512, 512), (256, 256), 256, flags)

fig = plt.figure(figsize=(10, 3))
ax1, ax2, ax3 = fig.subplots(1, 3)

ax1.imshow(img, cmap='gray')
ax1.set_axis_off()
ax2.imshow(test_img, cmap='gray')
ax2.set_axis_off()
ax3.imshow(linear_polar_inverse_image, cmap='gray')
ax3.set_axis_off()
fig.set_tight_layout(True)
plt.show()

print("test_img")
print(test_img)


# normal distribution example
from scipy.stats import multivariate_normal

map_XY_resolution = 100
axis = np.linspace(-0.5, 0.5, map_XY_resolution + 1, endpoint=True)
x, y = np.meshgrid(axis, axis)
pos = np.dstack((x, y))
rv = multivariate_normal([0, 0], [[0.3, 0], [0, 0.3]])
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.contourf(x, y, rv.pdf(pos))

print("rv.pdf(pos)")
print(rv.pdf(pos))

plt.show()

# zoom
from scipy import ndimage, misc
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(121)  # left side
ax2 = fig.add_subplot(122)  # right side
ascent = misc.ascent()
result = ndimage.zoom(ascent, [0.1, 0.2])
ax1.imshow(ascent, vmin=0, vmax=255)
ax2.imshow(result, vmin=0, vmax=255)
plt.show()
