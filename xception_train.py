import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import keras

from keras.applications.xception import Xception
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten
from keras.callbacks import Callback, ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop

import os
from tqdm import tqdm
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import cv2


from random import randint
im_size =224
num_samples = 10222
num_class = 120
epochs = 90
batch_size = 32

train_dir = '../data_gen_9/train'
validation_dir = '../data_gen_9/validation'

checkpointpath="/media/airscan/Data/AIRSCAN/EE298F/dogbreed/xception_rlr_weights/xception_samplewise_center-weights-{epoch:02d}.hdf5"

train_datagen = ImageDataGenerator(
    rescale=1./255,
    samplewise_center=True,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    shear_range=0.1,
    zoom_range=0.1
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(im_size, im_size),
        batch_size=batch_size,
        class_mode='categorical')
total_train_image_count = train_generator.samples
class_count = train_generator.num_class

validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(im_size, im_size),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False)
total_val_image_count = train_generator.samples

base_model = Xception(#weights='imagenet',
    weights = 'imagenet', include_top=False, input_shape=(im_size, im_size, 3))

# Append layers
x = base_model.output
x = Flatten()(x)
x = Dropout(0.5)(x)
x = Dense(1024)(x)
x = Dropout(0.5)(x)
predictions = Dense(num_class, activation='softmax')(x)

# whole model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the base model layers except the last 5 layers.
frz=len(base_model.layers)-5
for layer in base_model.layers[:frz]:
    layer.trainable = False

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(lr=0.00005),
              metrics=['accuracy'])

model.summary()

checkpoint = ModelCheckpoint(checkpointpath, verbose=1)

ReduceLROnPlateau(monitor='loss', patience=3, verbose=1, factor=0.5, min_lr=0.00001)

num_batches = num_samples//batch_size

csv_logger = CSVLogger('training_xception_with_samplewisecenter.log')

model.fit_generator(train_generator,
                    steps_per_epoch=num_batches,
                    epochs=epochs, validation_data=validation_generator,validation_steps=num_batches, verbose =1,callbacks=[checkpoint, csv_logger])
#model.fit_generator(train_generator,
#                    steps_per_epoch=5,
#                    epochs=1, validation_data=validation_generator,validation_steps=1, verbose =1)



print("Finished training.")
