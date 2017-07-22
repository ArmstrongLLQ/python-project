'''
K-means聚类算法

'''

import numpy as np
 
# Function: K Means
# -------------
# K-Means is an algorithm that takes in a dataset and a constant
# k and returns k centroids (which define clusters of data in the
# dataset which are similar to one another).

def kmeans(X, k, maxIt):    # X-数据集，k-分类数， maxIt-最大迭代次数
    # 现将数据集X进行转换，转换为nparray类型，然后矩阵的加入一列，为数据的分类类型
    numPoints, numDim = X.shape # 得到X的行和列
    
    dataSet = np.zeros((numPoints, numDim + 1)) #创建一个零矩阵，比X多一列
    dataSet[:, :-1] = X     #将X的值赋给dataset
    
    # Initialize centroids randomly
    centroids = dataSet[np.random.randint(numPoints, size = k), :]  # 从所有的行里面随机选取K个值为中心点
    #centroids = dataSet[0:2, :]
    #Randomly assign labels to initial centorid
    centroids[:, -1] = range(1, k +1)   # 将K个中心点的最后一列赋值为类别
    
    # Initialize book keeping vars.
    iterations = 0
    oldCentroids = None
    
    # Run the main k-means algorithm
    while not shouldStop(oldCentroids, centroids, iterations, maxIt):
        print("iteration: \n", iterations)
        print("dataSet: \n", dataSet)
        print("centroids: \n", centroids)
        # Save old centroids for convergence test. Book keeping.
        oldCentroids = np.copy(centroids)
        iterations += 1
        
        # Assign labels to each datapoint based on centroids
        updateLabels(dataSet, centroids)
        
        # Assign centroids based on datapoint labels
        centroids = getCentroids(dataSet, k)
        
    # We can get the labels too by calling getLabels(dataSet, centroids)
    return dataSet
# Function: Should Stop
# -------------
# Returns True or False if k-means is done. K-means terminates either
# because it has run a maximum number of iterations OR the centroids
# stop changing.
def shouldStop(oldCentroids, centroids, iterations, maxIt):
    if iterations > maxIt:
        return True # 如果超过迭代次数就退出
    return np.array_equal(oldCentroids, centroids)  # 判断新的中心点和原来的中心点是否一样，一样的话退出迭代
# Function: Get Labels
# -------------
# Update a label for each piece of data in the dataset. 
def updateLabels(dataSet, centroids):
    # For each element in the dataset, chose the closest centroid. 
    # Make that centroid the element's label.
    numPoints, numDim = dataSet.shape
    for i in range(0, numPoints):
        dataSet[i, -1] = getLabelFromClosestCentroid(dataSet[i, :-1], centroids)
    
    
def getLabelFromClosestCentroid(dataSetRow, centroids):
    # 归类，将传入的行与每一个中心点的距离进行计算，然后将这一行归类为距离最小的label
    label = centroids[0, -1];
    minDist = np.linalg.norm(dataSetRow - centroids[0, :-1])
    for i in range(1 , centroids.shape[0]):
        dist = np.linalg.norm(dataSetRow - centroids[i, :-1]) # np的内建函数，用来计算两个点之间的距离
        if dist < minDist:
            minDist = dist
            label = centroids[i, -1]
    print("minDist:", minDist)
    return label
    
        
    
# Function: Get Centroids
# -------------
# Returns k random centroids, each of dimension n.
def getCentroids(dataSet, k):
    # 重新得到新的中心点
    # Each centroid is the geometric mean of the points that
    # have that centroid's label. Important: If a centroid is empty (no points have
    # that centroid's label) you should randomly re-initialize it.
    result = np.zeros((k, dataSet.shape[1]))
    for i in range(1, k + 1):
        oneCluster = dataSet[dataSet[:, -1] == i, :-1] # 得到一个类别里面所有的点
        result[i - 1, :-1] = np.mean(oneCluster, axis = 0) # np的内建函数，计算传入的矩阵oneCluster的平均值，axis=0则按行计算平均值，axis=1则按列计算
        result[i - 1, -1] = i
    
    return result
    
    
x1 = np.array([1, 1])
x2 = np.array([2, 1])
x3 = np.array([4, 3])
x4 = np.array([5, 4])
testX = np.vstack((x1, x2, x3, x4)) # 将四个点组成矩阵
 
result = kmeans(testX, 2, 10)
print("final result:")
print(result)