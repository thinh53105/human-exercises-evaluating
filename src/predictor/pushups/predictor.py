import cv2
import tensorflow as tf
import random


class PushupsPredictor:

    def __init__(self, model_paths):
        up_path, down_path = model_paths
        # self.model_up = tf.keras.models.load_model(up_path)
        # self.model_down = tf.keras.models.load_model(down_path)
        self.test_predict()

    def test_predict(self):
        return 1

    @staticmethod
    def preprocessing_image(img):
        img = cv2.resize(img, dsize=(224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape(1, 224, 224, 3)
        # return img

    def predict(self, image, ty=1):
        # img = self.preprocessing_image(image)
        # if ty == 1:
        #     return self.model_up.predict(img)[0][0]
        # else:
        #     return self.model_down.predict(img)[0][0]
        return random.random()
