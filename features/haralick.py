# from https://gogul09.github.io/software/texture-recognition
import cv2
import numpy as np
import os
import glob
import mahotas as mt
from sklearn.svm import LinearSVC
from typing import List
import matplotlib.pyplot as plt
import pickle

# load the training dataset
train_path = "../inputs/for_texture_model/train"
train_names = os.listdir(train_path)

# empty list to hold feature vectors and train labels
train_features = []
train_labels = []


def extract_features(image):
    # calculate haralick texture features for 4 types of adjacency
    textures = mt.features.haralick(image)

    # take the mean of it and return it
    ht_mean = textures.mean(axis=0)
    return ht_mean


def train_feature_model():
        # loop over the training dataset
        print("[STATUS] Started extracting haralick textures..")
        for train_name in train_names:
                current_path = train_path + "/" + train_name
                current_label = train_name
                index = 1
                for file in glob.glob(current_path + "/*.jpg"):
                        print("Processing Image - {} in {}".format(
                                index, current_label))
                        # read the training image
                        image = cv2.imread(file)

                        # convert the image to grayscale
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                        # extract haralick texture from the image
                        features = extract_features(gray)

                        # append the feature vector and label
                        train_features.append(features)
                        train_labels.append(current_label)

                        # show loop update
                        index += 1

        # have a look at the size of our feature vector and labels
        print("Training features: {}".format(np.array(train_features).shape))
        print("Training labels: {}".format(np.array(train_labels).shape))

        # create the classifier
        print("[STATUS] Creating the classifier..")
        clf_svm = LinearSVC(random_state=9)

        # fit the training data and labels
        print("[STATUS] Fitting data/label to model..")
        clf_svm.fit(train_features, train_labels)

        # save the model to disk
        filename = 'outputs/finalized_model.sav'
        pickle.dump(clf_svm, open(filename, 'wb'))

        # loop over the test images
        test_path = "../inputs/for_texture_model/test"
        fig = plt.figure(figsize=(5, 5))
        for i, file in enumerate(glob.glob(test_path + "/*.jpg")):
                # read the input image
                image = cv2.imread(file)

                # convert to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # extract haralick texture from the image
                features = extract_features(gray)

                # evaluate the model and predict label
                prediction = clf_svm.predict(features.reshape(1, -1))[0]

                # show the label
                ax = fig.add_subplot(1, 4, i + 1)
                ax.imshow(image, interpolation="nearest", cmap=plt.cm.gray)
                ax.set_title(prediction, fontsize=10)
                ax.set_xticks([])
                ax.set_yticks([])
        # display the output image
        fig.tight_layout()
        plt.show()
