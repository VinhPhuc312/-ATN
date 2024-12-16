import cv2
import numpy as np

def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Check if the left mouse button was clicked
        hsv_value = hsv_frame[y, x]
        print(f"HSV Value at ({x}, {y}): {hsv_value}")

# Initialize webcam capture
cap = cv2.VideoCapture(0)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", get_hsv_value)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Display the frame
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # Esc key to break
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
