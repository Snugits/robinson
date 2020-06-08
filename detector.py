import io
import picamera
import numpy as np

from PIL import Image
from tflite_runtime.interpreter import Interpreter

class Detector(object):
    def __init__(self, path_to_model, threshold):
        self.threshold = threshold
        self.__camera = picamera.PiCamera(resolution=(640, 480), framerate=30)
        self.__camera.start_preview()

        self.__is_cat_detected = False

        self.__stream = io.BytesIO()

        self.__interpreter = Interpreter(path_to_model)
        self.__interpreter.allocate_tensors()
        self.__img_input_size = self.__interpreter.get_input_details()[0]['shape'][1:3]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__camera.close()

    def check(self):
        result = True
        try:
            self.__stream.seek(0)
            self.__camera.capture(self.__stream, 'jpeg')
            image = Image.open(self.__stream).convert('RGB').resize(self.__img_input_size, Image.ANTIALIAS)

            self.__is_cat_detected = self.__is_cat(image)

            self.__stream.seek(0)
            self.__stream.truncate()
        except BaseException as err:
            print(err)
            result = False
        finally:
            self.__camera.stop_preview()
        return result

    def is_detect(self):
        return self.__is_cat_detected

    def __is_cat(self, image):
        tensor_index = self.__interpreter.get_input_details()[0]['index']
        self.__interpreter.tensor(tensor_index)()[0][:, :] = image

        self.__interpreter.invoke()
        output_details = self.__interpreter.get_output_details()[0]
        output = np.squeeze(self.__interpreter.get_tensor(output_details['index']))

        return output < self.threshold if self.threshold < 0 else output > self.threshold

