
import numpy as np
import features
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import metrics
import sys
import joblib
import pandas as pd








def main(url):
	print(url)
	print (len(url))
	

	training_data = np.genfromtxt('dataset.csv', delimiter=',', dtype=np.int32)
	training_data = training_data[:,[0,1,2,3,4,5,6,8,9,11,12,13,14,15,16,17,22,23,24,29,30]]
	print (training_data.shape)
    #training_data = training_data[:,[0,1,2,3,4,30]]



    #print (training_data.shape)
	#print(training_data[0:1])

	# Extract the inputs from the training data array (all columns but the last one)
	inputs = training_data[:,:-1]
	# Extract the outputs from the training data arra (last column)
	outputs = training_data[:, -1]
	#training_inputs = inputs[:11000]
	#training_outputs = outputs[:11000]
	training_inputs = inputs
	training_outputs = outputs
	#print (training_outputs.shape)
    
	#testing_inputs = inputs[11000:]
	#testing_outputs = outputs[11000:]
	#print (training_inputs.shape)
	#print (testing_outputs.shape)
	#print("\n\n ""Random Forest Algorithm Results"" ")
	clf4 = RandomForestClassifier( random_state = 42)
	clf4.fit(training_inputs, training_outputs)
	'''

	predictions = clf4.predict(testing_inputs)
	accuracy = 100.0 * accuracy_score(testing_outputs, predictions)
	print ("The accuracy of your decision tree on testing data is: " + str(accuracy))

	'''

	#url="https://www.youtube.com/"

	#url="https://v1.notification-time.com/notifications/push/cpm/1/black/index.html?p1=https%253A%252F%252Fzme8o3l1c4.com%252Fbbuksw2n%253Fkey%253D4495b037ca8e6d310b124eb8262de409&subid_short=6ccd1a938d617db3d7d9f08244994a8f"
	s=features.main(url)
	print (s)
	#s=[ 1 ,  1,  1,  1,  1, -1,  0, -1,  1, -1,  1,  0, -1, -1,  1,  1,  1, -1, -1,  1]

	y=clf4.predict([s])
	print (y)
	if y[0]==-1:

		print("Phishing ")
	else :
		print ("Not Phishing")




	print(clf4.feature_importances_)
	return y[0]


    



















if __name__ == "__main__":
    main()