import keras
import numpy as np
from keras.applications import vgg19, inception_v3, resnet50, mobilenet
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
from PIL import Image
from keras import Input
import os


#filename = 'thumbnails\\A9YcrloL3oE.png'
filename = 'thumbnails\\_0ovuLsnU1A.png'

counter = 0
for filename in os.listdir('thumbnails'):
    if filename.endswith(".png"):
        print(os.path.join('.', filename))
        counter += 1
    if counter > 5:
        break



# load an image in PIL format
#original = load_img(filename, interpolation='bicubic')
image = Image.open('thumbnails\\3LNeBf7bOTU.png')
image = image.crop((0,11,120,79))
image = image.resize((224,224), resample=Image.ANTIALIAS)

print(np.mean(image))
print('PIL image size', image.size)

plt.imshow(image)
plt.show()

# convert the PIL image to a numpy array
# IN PIL - image is in (width, height, channel)
# In Numpy - image is in (height, width, channel)
image = img_to_array(image)
print(image.shape)

# Convert the image / images into batch format
# expand_dims will add an extra dimension to the data at a particular axis
# We want the input matrix to the network to be of the form (batchsize, height, width, channels)
# Thus we add the extra dimension to the axis 0.
image_batch = np.expand_dims(image, axis=0)
print('image batch size', image_batch.shape)


vgg_model = vgg19.VGG19(weights='imagenet')
inception_model = inception_v3.InceptionV3(weights='imagenet')
resnet_model = resnet50.ResNet50(weights='imagenet')
mobilenet_model = mobilenet.MobileNet(weights='imagenet')


processed_image = vgg19.preprocess_input(image_batch.copy())
predictions = vgg_model.predict(processed_image)
label = decode_predictions(predictions)
print("vgg19")
print(label)

processed_image = resnet50.preprocess_input(image_batch.copy())
predictions = resnet_model.predict(processed_image)
label = decode_predictions(predictions)
print("resnet50")
print(label)

processed_image = inception_v3.preprocess_input(image_batch.copy())
predictions = inception_model.predict(processed_image)
label = decode_predictions(predictions)
print("inception_v3")
print(label)

processed_image = mobilenet.preprocess_input(image_batch.copy())
predictions = mobilenet_model.predict(processed_image)
label = decode_predictions(predictions)
print("mobilenet")
print(label)