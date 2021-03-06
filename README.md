This repository contains my submission for the project requirement of EE 298F Deep Learning and Computer Vision.

## Project Details

I decided to join the Kaggle Challenge: *Dog Breed Identification*. The task is to identify the breed of the dog in the image.

The challenge here is that there are 120 classes of dogs but the provided training data is only 10222 images.

> Here's the [link](https://www.kaggle.com/c/dog-breed-identification) for the kaggle challenge.

## Usage
Download the dataset here: https://drive.google.com/open?id=139Vyav-E0so1UoAi5ERNUNs8H-_ZVwEP

Extract train.zip and test.zip.

Then execute this:
```
git clone https://github.com/darylperalta/ee298-proj
cd ee298-proj
```

Update the *original_train_dir* and *original_test_dir* variables in dataprep.py to the path of the extracted train and test directory.

Run:
```
python dataprep.py
```

This will make new directory containing the training and validation data. (By default the code won't create vaildation data)

To train, update the *checkpointpath* variable in resnet50_train.py to the directory where you want to save the checkpoint.

After this, run:

```
python resnet50_train.py
```

For prediction, download the checkpoint of the model [here](https://drive.google.com/open?id=1mnFhXLOiYGoRgwh6TAeEeTtS3zWMKUCC).

To run the *pred.py* please change the checkpointpath to the path of the downloaded model checkpoint. https://drive.google.com/file/d/1mnFhXLOiYGoRgwh6TAeEeTtS3zWMKUCC/view. Also, please change the *testDir_path* to the path of the extracted test.zip folder contating the test images.

The code *pred.py* shall output a formatted file containing the predictions that can be submitted to the competition and will be scored.

## Dataset

The dataset is based on the Stanford Dog dataset. It contains 10222 images.  

<p align="center"><img src="img/norfolk_terrier1.jpg" width="40%" /><br><br></p>
Norfolk Terrier

<p align="center"><img src="img/norwich_terrier1.jpg" width="40%" /><br><br></p>
Norwich Terrier  

The *class distribution* of the dataset is shown in the image below.

<p align="center"><img src="img/breed_dist.png" width="50%" /><br><br></p>


## Data Preprocessing and Augmentation

To compensate the lack of enough training images, I implemented data augmentation using the Keras' ImageDataGenerator.

The necessary directory that will be used for the ImageDataGenerator was created using *dataprep.py*.

## Architecture

Since this is a classification task, I used transfer learning for this project. In transfer learning a known architecture that does well in a certain dataset is fine tuned to do classification task in another dataset.

I experimented with three different base models namely xception, inceptionV3 and resnet50. Fully connected layers were appended to the base model to resize the shape that will be fit for the number of classes. An illustration of the architecture is shown in the figure below.

<p align="center"><img src="img/architecture.png" width="20%" /><br><br></p>

Because of the low number of training image, the architecture was very prone to overfitting. To avoid this dropout layers were added.

The image data generator also serves as the generator for batch processing of training data to fit in the limited gpu memory.


## Experiments

During my initial tests I split the given data into a 9:1 train to validation ratio to have see if the network is overfitting.

I first tested experimented with different models. Tweaked the hyperparameters. The best scores I was able to get are summarized in the table below. The kaggle challenge uses multiclass loss or categorical cross entropy loss as its scoring metric.

The architecture were trained for 135 epochs. The best model based on the training loss was used for prediction.

<p align="center"><img src="img/model_results.png" width="50%" /><br><br></p>

## Results

Based on my experiments the resnet50 architecture gives the highest submission score.

I used the resnet50 as the base model for my architecture and continued training the network up to 200 epochs. I also removed the validation and used the entire dataset for training. The best result I was able to get is shown in the image below. The submission file is included in this repo as resnet50_complete_data_198e.csv

<p align="center"><img src="img/score_resnet200e.png" width="70%" /><br><br></p>

The loss is 1.67119 which is around 55% accuracy based on my training data.

The low score can be attributed to the low number of training image per class as seen in the class distribution plot. Even with data augmentation the network is having a hard time learning to classify between breeds. Another factor is that some breeds are very much similar in appearance as seen in the sample image above. Also the background of the training images are different from each other like the images below of the same breed.

<p align="center"><img src="img/afghan_hound2.jpg" width="50%" /><br><br></p>

<p align="center"><img src="img/afghan_hound.jpg" width="50%" /><br><br></p>

Two training images of aghan hound.
