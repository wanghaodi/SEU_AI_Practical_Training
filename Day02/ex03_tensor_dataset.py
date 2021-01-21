import numpy
import cv2
import torch
import torchvision

# # 1. 加载数据集，导出图像
# t2 = torchvision.transforms.ToTensor()
# t3 = torchvision.transforms.Normalize((0.0, 0.0), (1.0, 1.0))
# t1 = torchvision.transforms.Compose([t2]) 
# mnist_train = torchvision.datasets.MNIST(root="./data", train=True,  transform=t1, download=True)
# # mnist_valid = torchvision.datasets.MNIST(root="./data", train=False, transform=t1, download=True)

# # 
# train_len = len(mnist_train)
# print(train_len)
# sample = mnist_train[0]

# data, target = sample
# print(data.shape, target)

# data = data.squeeze()
# print(data.shape)

# v_data = data.cpu().detach().numpy().copy()
# print(v_data)
# v_data = v_data * 255

# v_data = v_data.astype(numpy.uint8)
# cv2.imwrite("5.png", v_data)

# 2. 加载图像为张量，做卷积运算，结果再保存为图像
img = cv2.imread("00002.png")
# 转置运算
img = img.transpose(2, 0, 1)
# 转成张量
t_img = torch.from_numpy(img)
# t_img = t_img.float()
# t_img = torch.unsqueeze(t_img, dim=1)
t_img = t_img.view(-1, 3, 768, 1024).float()   # NCHW

kernel2d = numpy.array(
    [
        [ 1,  1,  1],
        [ 0,  0,  0],
        [-1, -1, -1]
    ]
)

kernel3d = numpy.zeros(shape=(3, 3, 3), dtype=numpy.int)
kernel3d[0] = kernel2d
kernel3d[1] = kernel2d
kernel3d[2] = kernel2d

t_kernel = torch.from_numpy(kernel3d).float()
t_kernel = t_kernel.view(-1, 3, 3, 3)

# 做卷积运算

t_out = torch.nn.functional.conv2d(input=t_img, weight=t_kernel, stride=1, padding=1)
print(t_out.shape)

t_out = t_out.squeeze()
print(t_out.shape)

out = t_out.cpu().detach().numpy().copy().astype(numpy.uint8)

cv2.imwrite("con2d.jpg", out)



