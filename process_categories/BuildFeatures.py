import numpy as np
import pandas as pd
import csv
import os

image_path = '../bin/jpgs/categories/'
npy_path = '../bin/npys/categorb/'
caffe_classify_path = '../../caffe/python/classify.py'

stream = os.popen('ls '+image_path)
cat_folders = stream.read().split()

stream = os.popen('ls '+npy_path)
curr_npys = stream.read().split()

for folder in cat_folders:
	if folder not in curr_npys:
		os.system(' '.join(['python ', 
				    caffe_classify_path, 
				    '--gpu', 
                                    image_path+folder, 
                                    npy_path+folder]))