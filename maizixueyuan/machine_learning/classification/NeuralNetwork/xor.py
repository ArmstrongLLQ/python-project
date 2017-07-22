'''
使用神经网络算法进行
简单非线性关系数据集测试(XOR):

X:                  Y
0 0                 0
0 1                 1
1 0                 1
1 1                 0
'''
from NeuralNetwork import NeuralNetwork
import numpy as np

nn = NeuralNetwork([2,2,1], 'tanh')     
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])     
y = np.array([0, 1, 1, 0])     
nn.fit(X, y)     
for i in [[0, 0], [0, 1], [1, 0], [1,1]]:    
    print(i, nn.predict(i))