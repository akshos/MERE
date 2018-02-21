import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from sklearn import preprocessing
import binarize

#digits = datasets.load_digits()

##print(digits.data)
##print(digits.target)

#clf = svm.SVC(gamma=0.001, C=100)
#img = digits.images[2]
#print img


#binr = preprocessing.binarize(img, threshold=10, copy=True)
#inv = 1-binr
#print binr


#print 'data : ', digits.data[2]
#plt.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
#plt.show()
#plt.imshow(inv, cmap=plt.cm.gray_r, interpolation='nearest')
#plt.show()
#X,y = digits.data, digits.target

##for im in digits.data :
##	X[i] = binarize.binarize(im)
##	X[i] = X[i]/255



##clf.fit(X,y)

##print clf.predict([digits.data[-5]])

digits = datasets.load_digits()
images = digits.images

X = []
y = digits.target

for image in images:
	binr = preprocessing.binarize(image, threshold=10, copy=True)
	inv = 1-binr
	inv = inv.flatten()
	X.append(inv)

#print len(X)
#print len(y)
#	
#print X[1]
#print y[1]


clf = svm.SVC(gamma=0.001, C=100)
clf.fit(X,y)

print clf.predict([X[1]])
print y[1]
