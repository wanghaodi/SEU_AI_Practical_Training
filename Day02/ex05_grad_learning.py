from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
from torchvision.transforms import Compose, ToTensor
import torch
import math
import numpy

from torch.nn.functional import conv2d, max_pool2d, relu, linear, log_softmax, cross_entropy

# 1. 加载数据集
train = MNIST(root="data", download=False, train=True, transform=Compose([ToTensor()]))
# 2. 形成批次数据集
loader = DataLoader(train, batch_size=1000, shuffle=True)  # [NCHW]

# for x, y in loader:
#     print(x.shape)

# 3. 定义卷积核，而且设置为可自动求导
w_6_1_5_5 = torch.Tensor(6, 1, 5, 5)  # 没有初始值的4维矩阵
b_6_1_5_5 = torch.Tensor(6)   # 偏置项 y = a * x + b
# 初始化
stdv = 1.0 / math.sqrt(6 * 5 * 5)
w_6_1_5_5.data.uniform_(-stdv, stdv)   # 均匀分布初始化权重矩阵
b_6_1_5_5.data.uniform_(-stdv, stdv)
# 必须是自动求导
w_6_1_5_5.requires_grad = True
b_6_1_5_5.requires_grad = True

# ----------------------------------
w_16_6_5_5 = torch.Tensor(16, 6, 5, 5)
b_16_6_5_5 = torch.Tensor(16)

stdv = 1.0 / math.sqrt(16 * 5 * 5)
w_16_6_5_5.data.uniform_(-stdv, stdv)
b_16_6_5_5.data.uniform_(-stdv, stdv)

w_16_6_5_5.requires_grad = True
b_16_6_5_5.requires_grad = True

# ----------------------------------
w_120_16_5_5 = torch.Tensor(120, 16, 5, 5)
b_120_16_5_5 = torch.Tensor(120)

stdv = 1.0 / math.sqrt(120 * 5 * 5)
w_120_16_5_5.data.uniform_(-stdv, stdv)
b_120_16_5_5.data.uniform_(-stdv, stdv)

w_120_16_5_5.requires_grad = True
b_120_16_5_5.requires_grad = True

# -----------------------------
w_120_84 = torch.Tensor(84, 120)
b_120_84 = torch.Tensor(84)

stdv = 1.0 / math.sqrt(120)
w_120_84.data.uniform_(-stdv, stdv)
b_120_84.data.uniform_(-stdv, stdv)

w_120_84.requires_grad = True
b_120_84.requires_grad = True

# --------------------------
# ------第五层logistic
w_84_10 = torch.Tensor(10, 84)
b_84_10 = torch.Tensor(10)

stdv = 1.0 / math.sqrt(84)
w_84_10.data.uniform_(-stdv, stdv)
b_84_10.data.uniform_(-stdv, stdv)

w_84_10.requires_grad = True
b_84_10.requires_grad = True


# 顶哟求导的运算
def forward(x):
    y = x
    y = conv2d(input=y, weight=w_6_1_5_5, bias=b_6_1_5_5, stride=1, padding=2)
    y = max_pool2d(y, kernel_size=(2, 2))
    y = relu(y, inplace=True)
    # --------------------
    y = conv2d(y, w_16_6_5_5, b_16_6_5_5, stride=1, padding=0)
    y = max_pool2d(y, kernel_size=(2, 2))
    y = relu(y, inplace=True)
    # --------------------
    y = conv2d(y, w_120_16_5_5, b_120_16_5_5)
    y = relu(y, inplace=True)
    # --------------
    y = y.view(-1, 120)
    # --------------
    y = linear(y, w_120_84, b_120_84)
    y = relu(y, inplace=True)
    # --------------------
    y = linear(y, w_84_10, b_84_10)

    # 
    y = log_softmax(y, dim=1)

    return y


lr = 0.1
epoch = 10
# 最后做一个验证：测试集的准确率
valid = MNIST("data", download=False, train=False, transform=Compose([ToTensor()]))
v_loader = DataLoader(valid, batch_size=10000, shuffle=False)

for e in range(epoch):
    batch = 0
    for x, y in  loader:
        batch += 1
        # 求预测值
        y_ = forward(x)
        # 求损失值
        loss = cross_entropy(y_, y, reduction="mean")
        # 计算导数
        loss.backward()
        # 更新梯度
        with torch.no_grad():
            w_6_1_5_5 -= w_6_1_5_5.grad * lr
            b_6_1_5_5 -= b_6_1_5_5.grad * lr

            w_16_6_5_5 -= w_16_6_5_5.grad * lr
            b_16_6_5_5 -= b_16_6_5_5.grad * lr 

            w_120_16_5_5 -= w_120_16_5_5.grad * lr
            b_120_16_5_5 -= b_120_16_5_5.grad * lr

            w_120_84 -= w_120_84.grad * lr
            b_120_84 -= b_120_84.grad * lr

            w_84_10 -= w_84_10.grad * lr
            b_84_10 -= b_84_10.grad * lr

            w_6_1_5_5.grad.zero_()
            b_6_1_5_5.grad.zero_()

            w_16_6_5_5.grad.zero_()
            b_16_6_5_5.grad.zero_()

            w_120_16_5_5.grad.zero_()
            b_120_16_5_5.grad.zero_()

            w_120_84.grad.zero_()
            b_120_84.grad.zero_()

            w_84_10.grad.zero_()
            b_84_10.grad.zero_()
        print(F"轮数：{e:03d}, 批次：{batch},\t损失值：{loss:8.6f}")


    # for j in range(5):
    #     t_x, t_y = valid[j]
    #     t_x = t_x.view(-1, 1, 28, 28)

    #     pred_y = forward(t_x)

    #     print("预测结果：", torch.argmax(pred_y, 1), "->", t_y)
    
    with torch.no_grad():
        for v_x, v_y in v_loader:
            v_y_ = forward(v_x)

            pred = torch.argmax(v_y_, dim=1)

            print("准确率：", (pred==v_y).float().mean().detach().item() * 100, "%")

