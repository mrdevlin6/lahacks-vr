import cv2
import mediapipe as mp
import numpy as np
import csv
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For static images:
# hands = mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=2,
#     min_detection_confidence=0.5)
# for idx, file in enumerate(file_list):
#   # Read an image, flip it around y-axis for correct handedness output (see
#   # above).
#   image = cv2.flip(cv2.imread(file), 1)
#   # Convert the BGR image to RGB before processing.
#   results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
#   # Print handedness and draw hand landmarks on the image.
#   print('Handedness:', results.multi_handedness)
#   if not results.multi_hand_landmarks:
#     continue
#   image_hight, image_width, _ = image.shape
#   annotated_image = image.copy()
#   for hand_landmarks in results.multi_hand_landmarks:
#     print('hand_landmarks:', hand_landmarks)
#     print(
#         f'Index finger tip coordinates: (',
#         f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#         f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
#     )
#     mp_drawing.draw_landmarks(
#         annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#   cv2.imwrite(
#       '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
# hands.close()

# For webcam input:
coords = np.array([0.0, 0.0, 0.0, 0.0])
out = coords
cap = cv2.VideoCapture(0)
hands =  mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands = 1
    )
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
#


    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
  # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            coords[0] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * image_width
            coords[1] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height
            coords[2] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z * image_height
            print(coords)
            out = np.vstack((out,coords))
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
hands.close()
cap.release()
with open("C:/Users/mrdev/Documents/Python//HandData.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(["X", "Y", "Z", "GRASP"])
    writer.writerows(out)
