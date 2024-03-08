import numpy as np
import matplotlib.pyplot as plt 
import cv2

empty_canvas = np.ones((500, 1200, 3))
plt.imshow(empty_canvas)

rectangle1 = cv2.rectangle(empty_canvas, pt1 = (100,0), pt2 = (175,400), color = (0 , 0,  0), thickness = -1)
plt.imshow(empty_canvas)
clearence1 = cv2.rectangle(empty_canvas, pt1 = (95,0), pt2 = (180,405), color = (0 , 255,  0), thickness = 5)
rectangle2 = cv2.rectangle(empty_canvas, pt1 = (275,100), pt2 = (350,500), color = (0 , 0,  0), thickness = -1)
clearence1 = cv2.rectangle(empty_canvas, pt1 = (270,95), pt2 = (355,500), color = (0 , 255,  0), thickness = 5)

clearence3 = cv2.rectangle(empty_canvas, pt1 = (895,45), pt2 = (1105,130), color = (0 , 255,  0), thickness = -1)
clearence4 = cv2.rectangle(empty_canvas, pt1 = (1015,125), pt2 = (1105,450), color = (0 , 255,  0), thickness = -1)
clearence5 = cv2.rectangle(empty_canvas, pt1 = (895,370), pt2 = (1105,455), color = (0 , 255,  0), thickness = -1)

rectangle3 = cv2.rectangle(empty_canvas, pt1 = (900,50), pt2 = (1100,125), color = (0 , 0,  0), thickness = -1)
rectangle4 = cv2.rectangle(empty_canvas, pt1 = (1020,125), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)
rectangle5 = cv2.rectangle(empty_canvas, pt1 = (900,375), pt2 = (1100,450), color = (0 , 0,  0), thickness = -1)

hexagon = np.array([[500, 175],
                    [650, 100],
                    [800, 175], 
                    [800, 325], 
                    [650, 400],
                    [500, 325]

                   ])
print(hexagon.shape)
hexagon = hexagon.reshape(-1,1,2)
hexagon

clearence_hexagon = np.array([[495, 170],
                    [645, 95],
                    [805, 170], 
                    [805, 330], 
                    [655, 405],
                    [495, 330]

                   ])

clearence_hexagon = clearence_hexagon.reshape(-1,1,2)
clearence_hexagon

cv2.polylines(empty_canvas, [hexagon], isClosed = True, thickness = 4, color = (0, 0, 0))
cv2.fillPoly(empty_canvas, [hexagon], (0,0,0))
cv2.polylines(empty_canvas, [clearence_hexagon], isClosed = True, thickness = 5, color = (0, 255, 0))

plt.imshow(empty_canvas)
plt.show()



