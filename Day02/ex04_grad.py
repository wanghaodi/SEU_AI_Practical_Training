import torch

# # y = x^2 -2x  + 7
# x = torch.Tensor([5])
# # x2 = torch.tensor([5, 4])
# # 1. 设置属性，是的改张量的所有运算被跟踪
# x.requires_grad = True 

# # 2. 运算

# y = x ** 2
# y -= 2*x
# y += 7

# # 3. 自动求导
# y.backward()

# # 4. 获取导数
# print(x.grad)


# ----------------------------------
x = torch.Tensor([-5])
x.requires_grad = True

lr = 0.01

epoch = 10000
for e in range(epoch):
    # 运算
    y = x * x  - 2 *x + 7 
    # 求导
    y.backward()
    # 更新x
    with torch.autograd.no_grad():
        x -= x.grad * lr
        # 上次导数的清空
        x.grad.zero_()

print(x)