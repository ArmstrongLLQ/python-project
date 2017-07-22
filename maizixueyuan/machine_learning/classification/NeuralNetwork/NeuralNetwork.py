'''
神经网络算法模块
'''
import numpy as np

# sigmoid函数用来作为activation function
# 通常情况下使用tanh或者logistic作为sigmoid函数
def tanh(x):  # 双曲函数 (exp(x)-exp(-x))/(exp(x)+exp(-x))
    return np.tanh(x) # 调用np包中的tanh函数

def tanh_deriv(x):  # tanh函数的导数
    return 1.0 - np.tanh(x)*np.tanh(x)

def logistic(x):  # 逻辑函数 1/(1+exp(-t))
    return 1/(1 + np.exp(-x))

def logistic_derivative(x):  # 逻辑函数的导数
    return logistic(x)*(1-logistic(x))


class NeuralNetwork:   
    def __init__(self, layers, activation='tanh'):  
        """  
        :param layers: A list containing the number of units in each layer.
        Should be at least two values PS:layers是一个list，list元素为每一层神经网络的节点数 
        :param activation: The activation function to be used. Can be
        "logistic" or "tanh"  
        """  
        if activation == 'logistic':  # 使用logistic函数的话则初始化为logistic
            self.activation = logistic  
            self.activation_deriv = logistic_derivative  
        elif activation == 'tanh':  # 使用tanh函数的话则初始为tanh
            self.activation = tanh  
            self.activation_deriv = tanh_deriv
    
        self.weights = []  # 初始化每一层的权重，总层数为
        for i in range(1, len(layers) - 1):  # 分别初始化每一层神经网络的权重weights
            self.weights.append((2*np.random.random((layers[i - 1] + 1, layers[i] + 1))-1)*0.25)  
            self.weights.append((2*np.random.random((layers[i] + 1, layers[i + 1]))-1)*0.25)
            
            
    def fit(self, X, y, learning_rate=0.2, epochs=10000):   # 训练，X-训练集，y-分类的个数，分为多少个类别， epochs-训练次数      
        X = np.atleast_2d(X)       # 将X转换为nparray类型，便于计算
        temp = np.ones([X.shape[0], X.shape[1]+1])         
        temp[:, 0:-1] = X  # adding the bias unit to the input layer         
        X = temp         # 将X增加一列，即bias unit
        y = np.array(y)  # 将y转换为nparray类型
    
        for k in range(epochs):  
            i = np.random.randint(X.shape[0])  # 使用抽样的方法来进行训练，每次循环从X从随机中
            a = [X[i]]
    
            for l in range(len(self.weights)):  #going forward network, for each layer
                a.append(self.activation(np.dot(a[l], self.weights[l])))  #Computer the node value for each layer (O_i) using activation function
            error = y[i] - a[-1]  #Computer the error at the top layer
            deltas = [error * self.activation_deriv(a[-1])] #For output layer, Err calculation (delta is updated error)
            
            #Staring backprobagation
            for l in range(len(a) - 2, 0, -1): # we need to begin at the second to last layer 
                #Compute the updated error (i,e, deltas) for each node going from top layer to input layer 
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_deriv(a[l]))  
            deltas.reverse()  
            for i in range(len(self.weights)):  
                layer = np.atleast_2d(a[i])  
                delta = np.atleast_2d(deltas[i])  
                self.weights[i] += learning_rate * layer.T.dot(delta)
                
                
    def predict(self, x):         
        x = np.array(x)         
        temp = np.ones(x.shape[0]+1)         
        temp[0:-1] = x         
        a = temp         
        for l in range(0, len(self.weights)):             
            a = self.activation(np.dot(a, self.weights[l]))         
        return a

