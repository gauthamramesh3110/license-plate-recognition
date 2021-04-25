"""
COMMAND SYNTAX:
> python get_images_from_mnist.py <save_path> <mnist_binary_path>
"""


import os
import sys
import cv2
import numpy as np
from mnist import MNIST
from tqdm import tqdm


def get_mnist(mnist_path):
    mnist_path = os.path.join(mnist_path)
    mnist = MNIST(mnist_path)
    x_train, y_train = mnist.load_training()
    return x_train, y_train


def get_images(X):
    images = []
    for x in tqdm(X):
        img = np.reshape(x, (28, 28))
        img = np.flip(img, axis=0)
        img = np.rot90(img, axes=(1, 0))
        images.append(img)
    return images


def save_images(images, y, savepath):
    number_count = dict()

    for i in tqdm(range(len(images))):
        img = images[i]
        label = str(y[i])

        if label not in number_count.keys():
            number_count[label] = 0
            os.mkdir(os.path.join(savepath, label))

        filename = 'IMG_' + str(number_count[label]) + '.jpg'
        filepath = os.path.join(savepath, label, filename)
        cv2.imwrite(filepath, img)
        number_count[label] += 1


def main(savepath, mnist_path):
    x_train, y_train = get_mnist(mnist_path)
    images = get_images(x_train)
    save_images(images, y_train, savepath)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])