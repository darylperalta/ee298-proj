This repository contains my submission for the project requirement of EE 298F Deep Learning and Computer Vision.

## Project Details

I decided to join the Kaggle Challenge: *Dog Breed Identification*. The task is to identify the breed of the dog in the image.

The challenge here is that there are 120 classes of dogs but the provided training data is only 10222 images.

> Here's the [link](https://www.kaggle.com/c/dog-breed-identification) for the kaggle challenge.
## Dataset

The dataset is based on the Stanford dataset. It contains 10222 images.  

<p align="center"><img src="img/norfolk_terrier1.jpg" width="40%" /><br><br></p>
Norfolk Terrier

<p align="center"><img src="img/norwich_terrier1.jpg" width="40%" /><br><br></p>
Norwich Terrier  

The *class distribution* of the dataset is shown in the image below.

<p align="center"><img src="img/breed_dist.png" width="50%" /><br><br></p>


## Data Preprocessing and Augmentation

To compensate the lack of enough training images. I used data augmentation. I implemented it using the Keras' ImageDataGenerator.

I used the code dataprep.py to create the necessary directory that will be used for the ImageDataGenerator.

## Architecture

I used transfer learning for this project.

I used an existing architecture used in general classification as base model. I appended fully connected layers that will resize the shape that will be fit for the number of classes. An illustration of the architecture is shown in the figure below.

<p align="center"><img src="img/architecture.png" width="20%" /><br><br></p>

I experimented with different base models. I experimented with xception, inceptionV3 and resnet50.

I used dropout layers to avoid overfitting.

The image data generator also serves as the generator for batch processing of data to fit the memory.


## Experiments

During my initial tests I split the given data into a 9:1 train to validation ratio to have see if the network is overfitting.

I first tested experimented with different models. Tweaked the hyperparameters. The best scores I was able to get are summarized in the table below. The kaggle challenge uses multiclass loss or categorical cross entropy loss as its scoring metric.

I used 135 epochs and used the best checkpoint based on training loss for prediction.

<p align="center"><img src="img/model_results.png" width="50%" /><br><br></p>

## Results

Based on my experiments the resnet50 architecture gives the highest submission score.

I used the resnet50 as the base model for my architecture and continued training the network up to 200 epochs. The best result I was able to get is shown in the image below.

<p align="center"><img src="img/score_resnet200e.png" width="70%" /><br><br></p>

The loss is 1.67119 which is around 55% accuracy based on my training data.

The low score can be attributed to the low number of training image per class as seen in the class distribution plot. Even with data augmentation the network is having a hard time learning to classify between breeds. Include also the fact that some breeds are very much alike as seen in the sample image above. Also the background of the training images are different from each other like the images below of the same breed.

<p align="center"><img src="img/afghan_hound2.jpg" width="50%" /><br><br></p>

<p align="center"><img src="img/afghan_hound.jpg" width="50%" /><br><br></p>

Two training images of aghan hound.
## Usage

Run this script, run:
```
mkdir input
cd input
```
Then download the dataset from the kaggle challenge in this directory. Here's the [link](https://www.kaggle.com/c/dog-breed-identification/data) for the data. Extract train.zip and test.zip here.

Then execute this to clone the repo and format the data for the data generator:
```
cd ..
git clone https://github.com/darylperalta/ee298-proj
cd ee298-proj
python dataprep.py
```


Download the checkpoint of the model [here](https://drive.google.com/open?id=1mnFhXLOiYGoRgwh6TAeEeTtS3zWMKUCC).

For prediction, go to pred.py and edit checkpointpath to the path of the downloaded checkpoint. You can also change the pred_filename for the output submission filename.

Run **pred.py** to create predictions for the test data and output a submission file.

Submit the output csv file to the kaggle website to see the result.

The code used for train are:
  >resnet50_train.py for the architecture with resnet as its base model
  >xception_train.py for the architecture with xception as its base model
  >inceptionV3_train.py for the architecture with inceptionV3 as its base model
