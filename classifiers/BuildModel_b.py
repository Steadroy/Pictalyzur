from sklearn.linear_model import LogisticRegression
import numpy as np
import cPickle as pickle
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.cross_validation import train_test_split
import csv
import os

# Model variables
n_features = 150

# read in a list of .npy file to use to build the model
np_path = '../bin/npys/categories/'
# np_lst = pd.read_csv('np_lst.txt', header=None)[0].values

stream = os.popen('ls '+np_path)
cat_folders = stream.read().split()

for category in cat_folders:

	stream = os.popen('ls '+np_path+category+'/')
	label_folders = stream.read().split()

	# load the .npy files from the list.
	feat_array = []
	categories = []

	for i, feats in enumerate(label_folders):
	    if '_a' in feats:
		feat_array.append(np.load(np_path+category+'/'+feats))
		categories.append(feats[:-6])
	    else:
		feat_array[-1] = np.vstack([feat_array[-1], np.load(np_path+category+'/'+feats)])

	X = np.vstack(feat_array)

	# Create a list of labels based on the .npy files
	label_lst = []
	for i, feats in enumerate(feat_array):
	    label_lst.append(i*np.ones(len(feats)))

	y = np.hstack(label_lst)

	X_t, y_t, X_rem, y_rem = train_test_split(X, y, train_size=.99)

	# Feature reduction
	X_svd = TruncatedSVD(n_components=n_features)
	X_red = X_svd.fit_transform(X_t)

	# Train logistic regression
	mod_logit = LogisticRegression()
	mod_logit.fit(X_t, y_t)

	# Pickle the model
	with  open(category+'_logit.pkl', 'w') as f:
	    pickle.dump(mod_logit, f)

	with  open(category+'_svd.pkl', 'w') as f:
	    pickle.dump(X_svd, f)

	# Write the category labels to a .csv
	with open(category+'_labels.csv', 'wb') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    wr.writerow(categories)
