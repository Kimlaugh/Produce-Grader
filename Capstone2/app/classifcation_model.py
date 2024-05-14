from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import warnings
warnings.filterwarnings('ignore')

from keras.models import load_model
model = keras.models.load_model(r"app/pretrained_model.h5") 

class_map = {0: 'carrot', 1: 'pepper', 2: 'tomato'}
image_categories = ['carrot','pepper','tomato']


#######################################################################################################
#          Plotting Funtions
#-----------------------------------------------------------------------------------------------------

# test_gen = ImageDataGenerator() # Normalise the data
# test_image_generator = test_gen.flow_from_directory(
#                                             test_path,
#                                             target_size=(150, 150),
#                                             batch_size=32,
#                                             class_mode='categorical')

# def plot(hist):
#     h = hist.history
#     plt.style.use('ggplot')
#     plt.figure(figsize=(10, 5))
#     plt.plot(h['loss'], c='red', label='Training Loss')
#     plt.plot(h['val_loss'], c='red', linestyle='--', label='Validation Loss')
#     plt.plot(h['accuracy'], c='blue', label='Training Accuracy')
#     plt.plot(h['val_accuracy'], c='blue', linestyle='--', label='Validation Accuracy')
#     plt.xlabel("Number of Epochs")
#     plt.legend(loc='best')
#     plt.show()

# test_gen = ImageDataGenerator() # Normalise the data
# test_image_generator = test_gen.flow_from_directory(
#                                             r"C:\Users\calvin\Downloads\UWI\Year 3\Semester 2\CSTONE\ImageClassifier\test_images",
#                                             target_size=(150, 150),
#                                             batch_size=32,
#                                             class_mode='categorical')


#########################################################################################################
#                                   PREDICTIONS
#--------------------------------------------------------------------------------------------------------  
from keras.metrics import MeanMetricWrapper, Accuracy

## Assuming you have created your model
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[Accuracy()])

## Then in your evaluation function
# test_loss, test_acc = model.evaluate(test_image_generator)

# image_path = r"C:\Users\calvin\Pictures\Screenshots\Screenshot 2024-03-25 090909.png"
def predictor(img_path, loop, crop_width_height):
    from keras.applications.vgg16 import preprocess_input
    from keras.preprocessing import image
    
    try:
        image_path = img_path
        img = image.load_img(image_path, target_size=(150, 150))
      

        img_array = image.img_to_array(img)
        
        # Preprocess the image array
        img_array = preprocess_input(img_array)

        # Expand dimensions to match the expected shape (batch size, height, width, channels)
        img_array = np.expand_dims(img_array, axis=0)
        
        prediction = model.predict(img_array)

        # Set a threshold for prediction confidence
        threshold = 0.75

        if loop == 0:
            return {'status': "error",
                    'content': "Not identified"}
        
        # Check if the maximum confidence is below the threshold
        if np.max(prediction) < threshold:
            return {'status': "error",
                    'content': "Confidence"}
        else:
            # Get the class with the highest confidence
            predicted_class = np.argmax(prediction)
            return {'status': 'success',
                    'content': image_categories[predicted_class],
                    'confidence': prediction[0][predicted_class] }
            # print(f"The image is predicted as class {image_categories[predicted_class]} with confidence {prediction[0][predicted_class]}")

    except Exception as e:
        # print(f"An error occurred: {e}")
        return {'status': "error",
                    'content': e}

# counter = 0
# # while (counter < 5):
# #     image_path = str(input("enter image path: ",))

# #     image_path = image_path.replace("\\",'/')
# #     try:
# #         predictor("Custom_Images\carrot\carrot_side1.jpg",3,700)
# #     except():
# #         image_path = image_path[3:]
# #     counter+= 1
    
# result = predictor("Custom_Images\carrot\carrot_side1.jpg",3,700)
# print (result)



# print(999999)
    