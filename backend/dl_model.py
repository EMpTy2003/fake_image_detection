from keras.models import load_model
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import os

class Prediction:
    
    # model = load_model("./Data/Model/keras_model.h5", compile=False)
    # labels = open("./Data/Model/labels.txt", "r").readlines()
    model = load_model(os.path.join("Data","Model","keras_model.h5"), compile=False)
    labels = open(os.path.join("Data","Model","labels.txt"), "r").readlines()

    def __init__(self) -> None:
        self._test_image_path = ""

    @property
    def test_image_path(self):
        return self._test_image_path

    # To set image path
    @test_image_path.setter
    def test_image_path(self, value):
        self._test_image_path = value

    # Detection Process
    def process(self):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = self.model

        # Load the labels
        labels = self.labels

        # Load an image from file
        image_path = self._test_image_path
        image = cv2.imread(image_path)
        copy_img = image.copy()

        # Aspect Ratio calcuation
        max_width = 500
        height, width, _ = copy_img.shape
        aspect_ratio = width / height
        new_width = min(max_width, width)
        new_height = int(new_width / aspect_ratio)

        copy_img = cv2.resize(
            copy_img, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Resize the image to (224-height, 224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the model's input shape
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predict using the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        label = labels[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", label[2:])
        print("Confidence Score:", str(
            np.round(confidence_score * 100))[:-2], "%")

        # Generate ELA of the image
        ela_image = self.generate_ela(copy_img)

        # Save the ELA image
        ela_image.save("./out/ela_result.jpg")

        return [label[2:], str(np.round(confidence_score * 100))[:-2]]

    # Summary of the model
    def model_summary(self):
        self.model.summary()

    # Error Level Analysis
    @staticmethod
    def generate_ela(image):
        original_image = Image.fromarray(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        original_image.save("./out/original.jpg", "JPEG")

        # Create a blank white image with the same size as the original
        white_image = Image.new("RGB", original_image.size)
        diff = ImageChops.difference(original_image, white_image)

        # Calculate the ELA using a scale factor (e.g., 10)
        scale = 10
        ela_image = ImageEnhance.Brightness(diff).enhance(scale)

        return ela_image
