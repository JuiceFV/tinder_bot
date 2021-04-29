"""The current module contains the function which extracts face from a photo.
The complete description of performance of the function described in notebook.
"""

import cv2
import numpy as np
from skimage.transform import resize
from path import Path


def extract_faces(im, img_size):
    """Extracts face from an image.
    :param img: an image passed as np-array.
    :return: resized image of a face
    """
    faces_in_image_limit = 1
    model_file = Path(__file__).parent.parent / "utils/opencv_face_detector_uint8.pb"
    config_file = Path(__file__).parent.parent / "utils/opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(model_file, config_file)

    image_data_result = []

    img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            print("The probability it is a human face is: {:.2f}%".format(confidence * 100))
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            roi_color = img[y:y1, x:x1]
            im = resize(roi_color, (img_size, img_size))
            image_data_result.append(im)

    if len(image_data_result) > faces_in_image_limit:
        return []
    else:
        return image_data_result
