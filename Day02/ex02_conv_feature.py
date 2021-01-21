import numpy as np
import cv2

in_img = cv2.imread("00002.png")

# sobel一阶导数运算（任意阶导数）
# out_img = cv2.Sobel(in_img, -1, 1, 1, ksize=3, scale=1.0, delta=128)

# laplace二阶导数运算
# out_img = cv2.Laplacian(in_img, -1, ksize=3, delta=0.0)


# 高斯模糊运算
out_img = cv2.GaussianBlur(in_img, ksize=(21, 21), sigmaX=90)
# 卷积运算
# kernel_x = np.array([
#     [1, 0, -1],
#     [1, 0, -1],
#     [1, 0, -1]
# ])
# kernel_y = np.array([
#     [ 1,  1,  1],
#     [ 0,  0,  0],
#     [-1, -1, -1]
# ])
# out_img_x = cv2.filter2D(in_img, -1, kernel_x, delta=0.0)
# out_img_y = cv2.filter2D(in_img, -1, kernel_y, delta=0.0)

# out_img = np.sqrt(out_img_x ** 2 + out_img_y ** 2)

cv2.imwrite("gauss.png", out_img)


