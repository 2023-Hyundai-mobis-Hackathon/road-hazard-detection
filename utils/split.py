# for splitting raw data into train / val / test

import shutil, random, os
import random

dirpath = "dataset/new_dataset/images/" # image data path
destDirectory = "dataset/new_dataset/test/images/" # destination image data path
labelpath = "dataset/new_dataset/labels/" # label data path
labeldestDirectory = "dataset/new_dataset/test/labels/" # destination label data path

filenames = random.sample(os.listdir(dirpath), 1123) # Randomly sample images into new path
for fname in filenames:
    srcpath = os.path.join(dirpath, fname)
    destPath = os.path.join(destDirectory, fname)
    #print(srcpath, destPath)
    shutil.move(srcpath, destPath)

    fname = fname.replace(".png", ".txt")
    srcpath = os.path.join(labelpath, fname)
    destPath = os.path.join(labeldestDirectory, fname)
    #print(srcpath, destPath)
    shutil.move(srcpath, destPath)
