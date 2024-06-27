import cv2
import dlib
import numpy as np
from imutils import face_utils
from scipy.spatial import distance as dist

# Load dlib's pre-trained face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')

def get_eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

def detect_head_shake(shape):
    # Get the left and right eye landmarks
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    # Compute the eye aspect ratio for both eyes
    leftEAR = get_eye_aspect_ratio(leftEye)
    rightEAR = get_eye_aspect_ratio(rightEye)

    # Average the eye aspect ratio
    ear = (leftEAR + rightEAR) / 2.0

    return ear

cap = cv2.VideoCapture(0)

# Define the indexes for the left and right eye landmarks
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Variables to keep track of head shake
frame_count = 0
shake_threshold = 15  # Adjust this threshold based on your needs
shake_detected = False
left_right_sequence = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        nose = shape[33]  # Nose tip landmark
        left_cheek = shape[1]  # Left cheek landmark
        right_cheek = shape[15]  # Right cheek landmark

        left_right_movement = nose[0] - (left_cheek[0] + right_cheek[0]) / 2
        left_right_sequence.append(left_right_movement)

        # Keep the sequence list to a fixed length
        if len(left_right_sequence) > 20:
            left_right_sequence.pop(0)

        # Detect head shake by checking the variation in left-right movements
        if len(left_right_sequence) == 20:
            movement_std = np.std(left_right_sequence)
            if movement_std > shake_threshold:
                shake_detected = True
                print("shake head")
            else:
                shake_detected = False

        # Draw facial landmarks
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
