

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import os
from tqdm import tqdm
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import cv2
from keras.models import Model, load_model

im_size =224


x_test = []

#checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/resnet50_nosplit/resnet50-weights-improvement-89.hdf5"
#checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/resnet50_dropout/resnet50-weights-improvement-139.hdf5"
#checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/xception_rlr_weights/xception-weights-improvement-89.hdf5"
#checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/inception_weights/inception_weights_lr-89.hdf5"
##checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/inception_weights/inception_weights_lr-131.hdf5"
#checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/inception_comp_weights/inception_weights_comp-88.hdf5"
#checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/resnet_comp_weights/resnet50_weights_comp-88.hdf5"
checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/resnet_comp_weights/resnet50_weights_comp-198.hdf5"


pred_filename = "resnet50_complete_data_300e.csv"

#load model
model = load_model(checkpointpath)

df_test = pd.read_csv('../input/sample_submission.csv')
df_train = pd.read_csv('../input/labels.csv')

targets_series = pd.Series(df_train['breed'])
one_hot = pd.get_dummies(targets_series, sparse = True)
col_names = one_hot.columns.values

del one_hot
del targets_series
del df_train

for f in tqdm(df_test['id'].values):
    img = cv2.imread('../input/test/{}.jpg'.format(f))
    x_test.append(cv2.resize(img, (im_size, im_size)))

x_test  = np.array(x_test, np.float32) / 255.


preds = model.predict(x_test, verbose=1)



sub = pd.DataFrame(preds)
# Set column names to those generated by the one-hot encoding earlier

sub.columns = col_names
# Insert the column id from the sample_submission at the start of the data frame
sub.insert(0, 'id', df_test['id'])
#sub.head(10358)
sub.to_csv(pred_filename, index=None)
