import numpy as np
import cv2

image = cv2.imread("test.jpg")
greybar = np.zeros((60, image.shape[1], 3), np.uint8)
greybar.fill(187)

for r in range(7, 54):
    for c in range(7, 54):
        greybar[r,c] = (0,0,0)

colorPicked = None
changeColor = False
imgShape = image.shape
def getBGRAtMouse(event, x, y, flags, param):
    global colorPicked
    global changeColor
    global imgShape
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr = display[y,x]
        print "({}\t{}):\t[{}\t{}\t  {}]".format(x, y, bgr[0], bgr[1], bgr[2])
        if y < imgShape[0]:
            colorPicked = bgr
            changeColor = True

while True:
    if cv2.getWindowProperty('window-name', 0) < 0:
        cv2.namedWindow('images')
        cv2.setMouseCallback('images', getBGRAtMouse)
        display = np.vstack([image, greybar])
        
    if changeColor:
        for r in range(7, 54):
            for c in range(7, 54):
                greybar[r,c] = colorPicked
        display = np.vstack([image, greybar])
        changeColor = False
        
    cv2.imshow("images", display)
    k = cv2.waitKey(10)
    if k == 13:  # PRESS ENTER TO CONFIRM COLOUR
        break
cv2.destroyAllWindows()
print "Colour picked:", colorPicked

#lower = [10, 10, 70]
#upper = [115, 100, 240]
lower = [0,0,0]
upper = [0,0,0]
r = 80
for i in range(3):
    if colorPicked[i] - r < 0:
        lower[i] = 0
    else:
        lower[i] = colorPicked[i] - r
    if colorPicked[i] + r > 255:
        upper[i] = 255
    else:
        upper[i] = colorPicked[i] + r
print "Lower:", lower
print "Upper:", upper

lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")

mask = cv2.inRange(image, lower, upper)
extract = cv2.bitwise_and(image, image, mask = mask)

'''
display = np.hstack([image, extract])
while True:    
    cv2.imshow("images", display)
    k = cv2.waitKey(0)
    if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
        break
cv2.destroyAllWindows()
'''

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
img_h, img_s, img_v = cv2.split(img_hsv)
ext_b, ext_g, ext_r = cv2.split(extract)
row,col = mask.shape

a = 40
for r in range(row):
    for c in range(col):
        hue = img_h[r,c]
        if not (ext_b[r,c] == 0 and ext_g[r,c] == 0 and ext_r[r,c] == 0):
            hue += a
            if hue >= 180:
                hue -= 180
            img_h[r,c] = hue

img_hsv = cv2.merge((img_h, img_s, img_v))
output = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

cv2.namedWindow('images')
cv2.setMouseCallback('images', getBGRAtMouse)
display = np.hstack([image, output])
while True:    
    cv2.imshow("images", display)
    k = cv2.waitKey(0)
    if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
        break
cv2.destroyAllWindows()
