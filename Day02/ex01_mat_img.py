import numpy
import cv2
# 使用矩阵来创建图像
img_1 = numpy.ndarray(shape=(500, 500, 3), dtype=numpy.uint8)

img_py = [[[255, 255, 0] for y in range(250)] for x in range(500)]    # BGR
img_2 = numpy.array(img_py)

# print(img_2[slice(0, 2, 1), 0, 1 ], img_2[0][0])
# print(img_2[0:2:1, 0, 1 ], img_2[0][0])
# print(img_1)

img_1[0, 0, 0] = 0
img_1[0, 0, 1] = 255
img_1[0, 0, 2] = 0

cv2.imwrite("1.png", img_1)
cv2.imwrite("2.png", img_2)
# 加载图像

img_3 = cv2.imread("00002.png")

# img_3[:, :, 2] = 0
# img_3[:, :, 1] = 0

img_3[ img_3[:,:, 0] > 100] = 0

cv2.imwrite("3.png", img_3)
