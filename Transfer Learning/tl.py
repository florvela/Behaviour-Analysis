# example of loading the vgg16 model
from tensorflow.keras.applications.vgg16 import VGG16
# load model
model = VGG16()
# summarize the model
model.summary()