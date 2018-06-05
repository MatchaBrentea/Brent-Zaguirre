import sys
import os
import re
import email
import nltk
import string
import csv
import nltk
import numpy as np
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier

def pre_process():
	limit = 75420
	words = set(nltk.corpus.words.words())
	for i in range(1,limit):
		print(i)
		mail = "data\inmail."+str(i)
		new_mail = "dataset\inmail."+str(i)
		file = open(mail,"r",errors = "ignore")
		file_2 = open(new_mail,"w")
		strings = file.read()
		emails = re.sub(r'<.*?>',r'',strings)
		emails = re.sub(r'\d',r'',emails)
		emails = re.sub(r'<.*?\n.*?>',r'',emails)
		emails = re.sub(r'-{1,50}'+r'={1,50}',r'',emails)
		b = email.message_from_string(emails)
		if b.is_multipart():
			for payload in b.get_payload():
				if payload.is_multipart():
					for temp in payload.get_payload():
						item = temp.get_payload()
						item = re.sub(re.compile('[%s]' % re.escape(string.punctuation)),'',item)
						item = re.sub(r'http//.*?|http.',r'',item)
						item = " ".join(w for w in nltk.wordpunct_tokenize(item) \
							if w.lower() in words or not w.isalpha())
						item = ' '.join( [w for w in item.split() if len(w)>2] )
						file_2.write(item)
				else:
					item = payload.get_payload()
					item = re.sub(re.compile('[%s]' % re.escape(string.punctuation)),'',item)
					item = re.sub(r'http//.*',r'',item)
					item = " ".join(w for w in nltk.wordpunct_tokenize(item) \
						if w.lower() in words or not w.isalpha())
					item = ' '.join( [w for w in item.split() if len(w)>2] )
					file_2.write(item)

		else:	
			item = b.get_payload()
			item = re.sub(re.compile('[%s]' % re.escape(string.punctuation)),'',item)
			item = re.sub(r'http//.*?',r'',item)
			item = " ".join(w for w in nltk.wordpunct_tokenize(item) \
				if w.lower() in words or not w.isalpha())
			item = ' '.join( [w for w in item.split() if len(w)>2] )
			file_2.write(item)

		file.close()
		file_2.close()

#=================================================================================================================#

def normal_dictionary():
	for i in range(1,limit):
		print(i)
		mail = "dataset\inmail."+str(i)
		new_mail = "dictionary\dictionary.txt"
		file = open(mail,"r")
		file2 = open(new_mail,"a+")
		strings = file.read()
		strings2 = '\n'.join([w for w in strings.split() if len(w)>2] )
		file2.write(strings2)
		file.close()
		file2.close()

def stop_dictionary():
	for i in range(limit):
		print(i)
		mail = "dataset\inmail."+str(i)
		new_mail = "dictionary\dictionary.txt"
		file = open(mail,"r")
		file2 = open(new_mail,"a+")
		strings = file.read()
		filtered_words = [word for word in strings if word not in stopwords.words('english')]
		strings2 = '\n'.join([w for w in strings.split() if len(w)>2] )
		file2.write(strings2)
		file.close()
		file2.close()

def stem_dictionary():
	for i in range(limit):
		print(i)
		mail = "dataset\inmail."+str(i)
		new_mail = "dictionary\dictionary.txt"
		file = open(mail,"r")
		file2 = open(new_mail,"a+")
		ps = PorterStemmer()
		strings = file.read().split()
		strings2 = '\n'.join([w for w in strings.split() if len(w)>2] )
		for word in strings2:
			file2.write(ps.stem(word))
		file.close()
		file2.close()		
#=================================================================================================================#

def train():
	temp = "dictionary\dictionary.txt"
	file2 = open(temp,"r")
	string2 = file2.read().split()
	string3 = Counter(string2)
	csv_file = r'vector\train.csv'
	file3 = open(csv_file,'w')	
	for i in range(1,45253):
		train_matrix = []
		print (i)
		mail = 'dataset\inmail.'+str(i)
		file1 = open(mail,"r")
		string1 = file1.read()
		string1 = word_tokenize(string1)
		for x in string3:
			train_matrix.append((string1.count(x)))
		write_me = csv.writer(file3,delimiter =',')
		write_me.writerow(train_matrix)
	#------------------------------------------------------#

def test():
	temp = "dictionary\dictionary.txt"
	file2 = open(temp,"r")
	string2 = file2.read().split()
	string3 = Counter(string2)
	csv_file = r'vector\test.csv'
	file3 = open(csv_file,'w')	
	for i in range(45253,75420):
		test_matrix = []
		print (i)
		mail = 'dataset\inmail.'+str(i)
		file1 = open(mail,"r")
		string1 = file1.read()
		string1 = word_tokenize(string1)
		for x in string3:
			test_matrix.append((string1.count(x)))
		write_me = csv.writer(file3,delimiter =',')
		write_me.writerow(test_matrix)
	#------------------------------------------------------#
#=================================================================================================================#

def model_do():
	ex = []
	spam =[]
	ham = []
	ex_mail = r"full\index"
	file3 = open(ex_mail,"r")
	for i in range(1,75420):
		print (i)
		string3 = file3.readlines() 
		for x in string3:
		    ex.append(x.split(None, 1))
	for a in range(1,75420):
		if arr[a] == 'spam':
			spam.append(a)
		elif arr[a] == 'ham':
			ham.append(a)

	mail = r"vector\train.csv"
	new_mail = r"vector\test.csv"
	file1 = csv.reader(open(mail,"rb"),delimiter=",")
	file = csv.reader(open(new_mail,"rb"),delimiter=",")
	train_lab = np.zeros(45252)
	test_lab = np.zeros(30168)
	for q in spam:
		train_lab[q] = 1
	for v in ham:
		test_lab[v] = 1
	temp1 = list(file1)
	temp2 = list(file2)

	result1 = np.array(temp1).astype("float")
	result2 = np.array(temp2).astype("float")
	print("1.) Bernoulli Naive Bayes\n2.) Multinomial Naive Bayes\n")
	model_type = input("Type of Model: ")
	if model_type == '1':
		model = BernoulliNB()
		mod_type = 'BernoulliNB '
	elif model_type == '2':
		model = MultinomialNB()
		mod_type = 'MultinomialNB '
	else:
		print("error\n")

	# model.fit(result1,train_lab)
	# result = mode.predict(result2)
	# print confussion_matrix(test_lab,result1)
	
	print("\nAccuracy of E-mail Spam Filteration on "+str(mod_type)+": (missing.no)%\n\n|ERROR ENCOUNTERED|\n\nNot able to run the program until Naive Bayes\n")

#=================================================================================================================#

print("| E-MAIL SPAM FILTERING |\n")
print("1.) Pre-processing\n2.) Dictionary Building\n3.) Feature Vector\n4.) Model\n")
step = input ("Choose the step: ") 

if (step == '1'):
	pre_process()

elif(step == '2'):
	print("1.) Normal dictionary\n2.) Stop Word Dictionary\n3.) Stem Dictionry\n")
	dict_type = input("Type of dictionary: ")
	if (dict_type == '1'):
		normal_dictionary()
	elif (dict_type == '2'):
		stop_dictionary()
	elif (dict_type == '3'):
		stem_dictionary()
	else:
		print("error\n")

elif(step == '3'):
	train()
	test()

elif(step == '4'):
	model_do()

else:
	print("error\n")



