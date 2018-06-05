import numpy as np 
import os
import cv2
import time
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.decomposition import PCA

do_time = time.time()

def pre_processing(image):
	# opening #
	img = cv2.imread(image,0)
	img = cv2.equalizeHist(img)
	img = preprocessing.scale(img)
	img = np.reshape(img, (img.shape[0]*img.shape[1]))
	return img
 	

def renaming():
	source = "orl_faces"
	pre_image1 = os.path.join(source, 's')
	pre_image2 = pre_image1 + str(i)
	pre_image3 = os.path.join(pre_image2,str(j))
	true_image = pre_image3 + ".pgm"
	return true_image


def neural_network(num):
	mlp =  MLPClassifier(hidden_layer_sizes = (num,),activation='logistic',max_iter = 1000)
	return mlp

def neural_network3():
	mlp = MLPClassifier(hidden_layer_sizes = 3000,activation = 'logistic',max_iter = 1000)
	return mlp

def support_vector():
	mlp = SVC()
	return mlp

def support_vector2(i):
	mlp = SVC(kernel = 'poly',degree=i)
	return mlp

def support_vector3(i):
	mlp = SVC(kernel = 'rbf',gamma = i)
	return mlp

arr1 = []	
arr2 = []
arr3 = []
arr4 = []

for i in range (1,41):
	print("Opening folder of s" +str(i))
	for j in range (1,7):
		arr2.append(i)
		print("Printing image #"+str(j))
		true_image1 = renaming()
		new_image1 = pre_processing(true_image1)
		arr1.append(new_image1)	
	print("\n")

for i in range (1,41):
	for j in range(7,11):
		arr4.append(i)
		true_image2 = renaming()
		new_image2 = pre_processing(true_image2)
		new_image2 = new_image2
		arr3.append(new_image2)

mode = int(input("1. ANN 1/2\n2. ANN Vary\n3. ANN PCP\n4. SVM\n5. SVM PK 1-5\n6. SVM RBF\nChoose mode: "))

if (mode == 1):
	mlp = neural_network(1500)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test ANN 1/2: ",score_module*100,"%")
	print("Train ANN 1/2: ",score_module1*100,"%")

elif (mode == 2):
	num = 1500
	while (num < 3100):
		mlp = neural_network(num)
		fit_module = mlp.fit(arr1,arr2)
		score_module = fit_module.score(arr3,arr4)
		score_module1 = fit_module.score(arr1,arr2)
		print("Test ANN ",num," ",score_module*100,"%")
		print("Train ANN ",num," ",score_module1*100,"%")
		num = num + 100

elif (mode == 3):
	pca = PCA(n_components = 10)
	arr1 = pca.fit_transform(arr1)
	arr3 = pca.fit_transform(arr3)
	mlp = neural_network3()
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test ANN PCA",score_module*100,"%")
	print("Train ANN PCA: ",score_module1*100,"%")

elif(mode == 4):
	mlp = support_vector()
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM: ",score_module*100,"%")
	print("Train SVM: ",score_module1*100,"%")

elif(mode == 5):
	for i in range(1,6):
		mlp = support_vector2(i)
		fit_module = mlp.fit(arr1,arr2)
		score_module = fit_module.score(arr3,arr4)
		score_module1 = fit_module.score(arr1,arr2)
		print("Test SVM Kernel ",i," ",score_module*100,"%")
		print("Train SVM Kernel ",i," ",score_module1*100,"%")

elif(mode == 6):
	i = 0.1
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.2
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.3
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.4
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.5
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.6
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.7
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.8
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 0.9
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
	i = 1.0
	mlp = support_vector3(i)
	fit_module = mlp.fit(arr1,arr2)
	score_module = fit_module.score(arr3,arr4)
	score_module1 = fit_module.score(arr1,arr2)
	print("Test SVM Gamma ",i," ",score_module*100,"%")
	print("Train SVM Gamma ",i," ",score_module1*100,"%")
else:
	print("Mode unavailable!")
	exit()

print("Running time : %s seconds" % (time.time() - do_time))