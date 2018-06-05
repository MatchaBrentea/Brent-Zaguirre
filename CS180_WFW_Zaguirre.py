import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

def kmeans(bac_t,train1,train2,inp,num,centroid_type,color_scheme):
	#read 3 images and form 3rd image's row and column
	img = cv2.imread(train1)
	img2 = cv2.imread(train2)
	on_img = cv2.imread(inp)
	in_img = on_img.copy()
	#HSV
	if color_scheme == 'hsv' or color_scheme == 'Hsv' or color_scheme == 'HSV':
		img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
		in_img = cv2.cvtColor(in_img,cv2.COLOR_BGR2HSV)
	#CIELa*b*
	elif color_scheme == 'cielab' or color_scheme == 'Cielab' or color_scheme == 'CIELAB':
		img = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
		img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2LAB)
		in_img = cv2.cvtColor(in_img,cv2.COLOR_BGR2LAB)
	img_row = in_img.shape[0]
	img_column = in_img.shape[1]
	#reshape array into 2D
	re_img = img.reshape((-1,3))
	re_img2 = img2.reshape((-1,3))
	com_img = np.concatenate((re_img,re_img2),axis = 0)
	#convert into float32 for k-means
	com_img = np.float32(com_img)
	#analyze the number of clusters
	if (bac_t) == 'filaria' or bac_t == 'Filaria' or bac_t=='FILARIA':
		temp_clus = 3
		bac_num = 1
		parasite = in_img[230][425]
		bg = in_img[300][450]
		centroids = np.array([parasite, bg,[0,0,0]])
	elif (bac_t) == 'plasmodium' or bac_t == 'Plasmodium' or bac_t == 'PLASMODIUM':
		temp_clus = 2
		bac_num = 2
		parasite = in_img[530][520]
		bg = in_img[270][900]
		centroids = np.array([parasite, bg])
	elif (bac_t) == 'schistosoma' or bac_t == 'Schistosoma' or bac_t == 'SCHISTOSOMA':
		temp_clus = 3
		bac_num = 3
		parasite = in_img[390][350]
		bg = in_img[300][500]
		centroids = np.array([parasite, bg,[0,0,0]])
	#initialize the kmeans	
	if centroid_type == 'assign' or centroid_type == 'Assign' or centroid_type == 'ASSIGN':
		kmeans = KMeans(n_clusters = temp_clus, init = centroids)
	else:
		#if more than 2 cluster
		if cluster_type == 'morethan2' or cluster_type == 'Morethan2' or cluster_type == 'MORETHAN2':
			temp_clus = 5
		kmeans = KMeans(n_clusters = temp_clus, random_state=0)

	#fit kmeans to usable input
	kmeans = kmeans.fit(com_img)
	#predict clusters
	new_img = np.reshape(in_img,(img_row*img_column,3))
	predict = kmeans.predict(new_img)
	#cluster centers
	centroids = kmeans.cluster_centers_
	#print (centroids)
	# reshape predict array for image
	predict = predict.reshape((img_row, -1))
	#loop for changing the color of the image 
	for x in range(img_row):
		for y in range(img_column):
			if predict[x][y] == 0:
				in_img[x][y] = [0,0,0]
			elif predict[x][y] == 1:
				in_img[x][y] = [128,0,0]
			elif predict[x][y] == 2:
				in_img[x][y] = [255,255,0]
	if bac_num == 1:
		if centroid_type == 'assign' or centroid_type == 'Assign' or centroid_type == 'ASSIGN':
			bacteria = 'new_filaria_assigned'+str(num)+'.jpg'
		else:
			if temp_clus == 5:
				bacteria = 'new_filaria_newcluster'+str(num)+'.jpg'
			else:
				if color_scheme == 'hsv' or color_scheme == 'Hsv' or color_scheme == 'HSV':
					bacteria = 'new_filaria_HSV'+str(num)+'.jpg'
				elif color_scheme == 'cielab' or color_scheme == 'Cielab' or color_scheme == 'CIELAB':
					bacteria = 'new_filaria_CIELAB'+str(num)+'.jpg'
				else:
					bacteria = 'new_filaria'+str(num)+'.jpg'
	elif bac_num == 2:
		if centroid_type == 'assign' or centroid_type == 'Assign' or centroid_type == 'ASSIGN':
			bacteria = 'new_plasmodium_assigned'+str(num)+'.jpg'
		else:
			if temp_clus == 5:
				bacteria = 'new_plasmodium_newcluster'+str(num)+'.jpg'
			else:
				if color_scheme == 'hsv' or color_scheme == 'Hsv' or color_scheme == 'HSV':
					bacteria = 'new_plasmodium_HSV'+str(num)+'.jpg'
				elif color_scheme == 'cielab' or color_scheme == 'Cielab' or color_scheme == 'CIELAB':
					bacteria = 'new_plasmodium_CIELAB'+str(num)+'.jpg'
				else:
					bacteria = 'new_plasmodium'+str(num)+'.jpg'
	elif bac_num == 3:
		if centroid_type == 'assign' or centroid_type == 'Assign' or centroid_type == 'ASSIGN':
			bacteria = 'new_schistosoma_assigned'+str(num)+'.jpg'
		else:
			if temp_clus == 5:
				bacteria = 'new_schistosoma_newcluster'+str(num)+'.jpg'
			else:
				if color_scheme == 'hsv' or color_scheme == 'Hsv' or color_scheme == 'HSV':
					bacteria = 'new_schistosoma_HSV'+str(num)+'.jpg'
				elif color_scheme == 'cielab' or color_scheme == 'Cielab' or color_scheme == 'CIELAB':
					bacteria = 'new_schistosoma_CIELAB'+str(num)+'.jpg'
				else:
					bacteria = 'new_schistosoma'+str(num)+'.jpg'
	cv2.imwrite(bacteria,in_img)

 
#MAIN#
bac_type = input("Input type of bacteria: ")		#filaria,
centroid_type = input("Input type of centroid: ")	#random or assign
cluster_type = input("Input type of clustering: ")	#normal or morethan2
color_scheme = input("Input type of color scheme: ") #RGB or HSV or CIELAB
train_1 = input("1st bacteria to train: ")			#1st .jpg image to train
train_2 = input("2nd bacteria to train: ")			#2nd .jpg image to train
num = 1
#FILARIA
if bac_type == 'filaria' or bac_type == 'Filaria' or bac_type == 'FILARIA':
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria2.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria3.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria4.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria5.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria6.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria7.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria8.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria9.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'filaria10.jpg',num,centroid_type,color_scheme)

elif bac_type == 'plasmodium' or bac_type == 'Plasmodium' or bac_type == 'PLASMODIUM':
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'1c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'3c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'6c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'7c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'11c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'19c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'55c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'79c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'94c.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'105c.jpg',num,centroid_type,color_scheme)	

elif bac_type == 'schistosoma' or bac_type == 'Schistosoma' or bac_type == 'SCHISTOSOMA':
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma2.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma3.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma4.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma5.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma6.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma7.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma8.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma9.jpg',num,centroid_type,color_scheme)
	num += 1
	print ("Outputting ",bac_type," # ", num)
	kmeans(bac_type,train_1,train_2,'schistosoma10.jpg',num,centroid_type,color_scheme)	

else:
	print("Invalid Input.")

print ("=================================================\nProgram terminated")