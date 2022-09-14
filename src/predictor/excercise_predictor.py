import cv2
import tensorflow as tf
import numpy as np
import random
import time


class Predictor:

    def __init__(self, model_paths):
        up_path, down_path = model_paths
        self.model_up = self.load_model(up_path)
        self.model_down = self.load_model(down_path)
        self.test_predict()
    
    def load_model(self, path):
        model = tf.lite.Interpreter(path)
        model.allocate_tensors()
        return model
    
    def test_predict(self):
        test_img = np.zeros((224, 224, 3), dtype='uint8')
        self.predict(test_img, ty=1)
        self.predict(test_img, ty=0)

    @staticmethod
    def preprocessing_image(img):
        img = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = (img/127.5) - 1
        img = img.reshape(1, 224, 224, 3)
        img = tf.cast(img,tf.float32)
        return img

    def predict(self, image, ty=1):
        model = self.model_up
        if ty == 0:
            model = self.model_down
        input_details = model.get_input_details()
        output_details = model.get_output_details()
        processed_img = self.preprocessing_image(image)
        model.set_tensor(input_details[0]['index'], processed_img)
        model.invoke()
        output_data = model.get_tensor(output_details[0]['index'])[0]
        # Get class index
        class_idx = tf.argmax(output_data, axis=0)
        return class_idx, output_data[class_idx]


if __name__ == '__main__':
    import time

    predictor = Predictor(
        [
        'src/predictor/pushups/models/mobinet-20220724_up.tflite',
        'src/predictor/pushups/models/mobinet-20220724_down.tflite'
        ]
    )
    test_img = cv2.imread('src/sample_images/img001.png')
    for _ in range(10):
        ty = random.choice([0, 1])
        p_time = time.time()
        predictor.predict(test_img, ty=ty)
        c_time = time.time()
        print(c_time - p_time)

