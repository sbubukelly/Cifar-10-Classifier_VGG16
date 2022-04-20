from PyQt5 import QtWidgets, QtGui, QtCore

from UI import Ui_MainWindow

import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

import torch
import torch.nn as nn
from torch import optim
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms


class MainWindow_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.pushButton.clicked.connect(self.showImage)
        self.ui.pushButton_3.clicked.connect(self.net)

    def showImage(self):
        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        batch_size = 9
        trainset = torchvision.datasets.CIFAR10(
            root='./data', train=True, download=False, transform=transform)
        trainloader = torch.utils.data.DataLoader(
            trainset, batch_size=batch_size, shuffle=True, num_workers=2)
        testset = torchvision.datasets.CIFAR10(
            root='./data', train=False, download=False, transform=transform)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                 shuffle=False, num_workers=2)
        classes = ('airplane', 'automobile', 'bird', 'cat',
                   'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
        dataiter = iter(trainloader)
        images, labels = dataiter.next()
        plt.figure(figsize=(8, 8))
        for i in range(9):
            plt.subplot(3, 3, i+1)
            plt.axis('off')
            plt.title(classes[labels[i]])
            images[i] = images[i] / 2 + 0.5     # unnormalize
            npimg = images[i].numpy()
            plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.show()

    def net(self):
        vgg16 = models.vgg16(pretrained=True)
        vgg16.eval()
        print(vgg16)
