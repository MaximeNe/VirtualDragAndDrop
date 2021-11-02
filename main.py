#!/usr/bin/env python3

"""
This project is about making a little program that allows the user to move objects virtually using the webcam
It is made by Maxime NEMO

module mediapipe version 0.8.7 works, but 0.8.8 crashes...

"""
import cv2
from cvzone.HandTrackingModule import *

video_capture = cv2.VideoCapture(0)

# Set the width and the Height of the video stream
width, height = 1080, 720
video_capture.set(3, width)
video_capture.set(4, height)


# Detector for the hand
hand_detector = HandDetector(detectionCon=0.7)


class Rectangle:
    def __init__(self, cx, cz, w, h, color):
        self.cx = cx
        self.cz = cz
        self.w = w
        self.h = h
        self.color = color
        self.original_color = color

    def update_coord(self, landmarks_list):
        if landmarks_list: # There is a hand detected
            # Check if the box is in the hand
            l = max(landmarks_list[5][0] - landmarks_list[17][0], - landmarks_list[5][0] + landmarks_list[17][0])
            # Find the center of the hand:
            center = []
            center.append((landmarks_list[5][0] + landmarks_list[9][0] + landmarks_list[13][0] + landmarks_list[17][
                0] + 2 * landmarks_list[0][0]) // 6)
            center.append((landmarks_list[5][1] + landmarks_list[9][1] + landmarks_list[13][1] + landmarks_list[17][
                1] + 2 * landmarks_list[0][1]) // 6)

            if self.cx - center[0] <= l//2 and self.cz - center[1] <= l//2: # If the center of the hand is close enough of the center of the box
                # Check if holding or not:
                z_min = min(landmarks_list[5][1], landmarks_list[9][1], landmarks_list[13][1], landmarks_list[17][1], landmarks_list[0][1])  #the higest point of the hand palm in the image
                if landmarks_list[8][1] >= z_min and landmarks_list[12][1] >= z_min and landmarks_list[16][1] >= z_min and landmarks_list[20][1] >= z_min:
                    # Then holding
                    self.color = (0, 255, 0)
                    self.cx = center[0]
                    self.cz = center[1]
                    return
        # Otherwise, set the color as the original one
        self.color = self.original_color


rectangles = [Rectangle(width//4, height//4, 50, 50, (0, 0, 255))]


# Show image
while True:
    _, img = video_capture.read()
    img = cv2.flip(img, 1, img)


    img = hand_detector.findHands(img)
    landmarks_list, _ = hand_detector.findPosition(img, draw=False)
    # https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/
    # For landmarks explanations


    for rect in rectangles:
        rect.update_coord(landmarks_list)
        cv2.rectangle(img, (rect.cx - rect.w // 2, rect.cz - rect.h // 2),
                      (rect.cx + rect.w // 2, rect.cz + rect.h // 2), rect.color, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)  # Approximately 30fps

