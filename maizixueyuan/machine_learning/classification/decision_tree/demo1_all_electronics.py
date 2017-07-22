from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import preprocessing
from sklearn import tree
from sklearn.externals.six import StringIO

# read in the csv file and put features in a list of dict and list of class label
allElectronicsData = open('mydata1.csv')
readers = csv.reader(allElectronicsData)
for i, each in zip(range(0, 1),readers):
    if i == 0:
        header = each

print(header)

featureList = []
labelList = []

for row in readers:
    labelList.append(row[len(row) - 1])
    rowDict = {}
    for i in range(1, len(row) - 1):
        # print(row[i])
        rowDict[header[i]] = row[i]
        # print(rowDict)

    featureList.append(rowDict)

print(labelList)
print(featureList)

# vectorize features
vec = DictVectorizer()
dummyX = vec.fit_transform(featureList).toarray()

print('dummX:' + str(dummyX))

# vectorize class labels
lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
print('dummyY:' + str(dummyY))

# using decision tree for classfication
clf = tree.DecisionTreeClassifier(criterion='entropy')
clf = clf.fit(dummyX, dummyY)
print('clf:' + str(clf))

#visulize model
with open('visible.dot', 'w') as f:
    f = tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file=f)

ownRowX = dummyX[0, :]
print('newRowX:' + str(ownRowX))

newRowX = ownRowX

newRowX[0] = 1
newRowX[2] = 0
print('newRowX:' + str(newRowX))

predictedY = clf.predict(newRowX)
print('predictedY:' + str(predictedY))