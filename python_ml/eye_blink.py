import cv2
import time
import numpy as np
from typing import Tuple
import f_detector


def process_blinks(vs: cv2.VideoCapture, c: int) -> Tuple[int, int]:
    # Instancio detector
    detector = f_detector.eye_blink_detector()

    # Iniciar variables para el detector de parpadeo
    COUNTER = c
    TOTAL = 0

    start_time = time.time()
    ret, im = vs.read()
    if not ret:
        return

    im = cv2.flip(im, 1)  # Flip horizontally

    # Resize the image to width=720 (maintaining aspect ratio)
    width = 720
    height = int(im.shape[0] * (width / im.shape[1]))
    im = cv2.resize(im, (width, height))

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detectar rostro
    rectangles = detector.detector_faces(gray, 0)
    boxes_face = f_detector.convert_rectangles2array(rectangles, im)

    if len(boxes_face) != 0:
        # Seleccionar el rostro con más área
        areas = f_detector.get_areas(boxes_face)
        index = np.argmax(areas)
        rectangles = rectangles[index]
        boxes_face = np.expand_dims(boxes_face[index], axis=0)

        # Blinks_detector
        COUNTER, TOTAL = detector.eye_blink(gray, rectangles, COUNTER, TOTAL)

        # Agregar bounding box
        img_post = f_detector.bounding_box(im, boxes_face, ["blinks: {}".format(TOTAL)])
    else:
        img_post = im

    # Visualización
    end_time = time.time() - start_time
    FPS = 1 / end_time
    cv2.putText(
        img_post,
        f"FPS: {round(FPS, 3)}",
        (10, 50),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 0, 255),
        2,
    )
    cv2.imshow("blink_detection", img_post)
    return COUNTER, TOTAL
