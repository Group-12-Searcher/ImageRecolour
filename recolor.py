import numpy as np
import cv2

image = cv2.imread("test.jpg")
lower = [17, 15, 100]
upper = [50, 56, 200]

lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")

mask = cv2.inRange(image, lower, upper)
#output = cv2.bitwise_and(image, image, mask = mask)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
row,col = mask.shape

a = 0
for r in range(row):
    for c in range(col):
        hue = h[r,c]
        if mask[r,c] != 0:
            hue += a
            if hue >= 180:
                hue -= 180
            h[r,c] = hue
hsv = cv2.merge((h,s,v))
bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

while True:    
    #cv2.imshow("images", np.hstack([image, output]))
    cv2.imshow("images", np.hstack([image, bgr]))
    k = cv2.waitKey(0)
    if k == 27 or cv2.getWindowProperty('window-name', 0) < 0:
        break
cv2.destroyAllWindows()
