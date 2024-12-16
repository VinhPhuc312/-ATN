import cv2
import numpy as np
import threading
from blynk_function import *
import serial
import time
try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)

greenlow = (30, 70, 90)
greenup = (55, 140, 255)
stop_event = threading.Event()
position = '0'
positions = {
    "1": (0, 1),#LEFT3
    "2": (1, 2),#Left2
    "3": (2, 3),#Left1
    "4": (3, 4),#Forward
    "5": (4, 5),#RIGHT1
    "6": (5, 6),#RIGHT2
    "7": (6, 7)#RIGHT3
}
# Hàm để trích xuất vùng màu xanh từ frame
def extract_green(frame, greenlow, greenup):
    blur = cv2.GaussianBlur(frame, (21, 21), 0)# Làm mờ frame để giảm nhiễu
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # Chuyển đổi sang không gian màu HSV
    mask = cv2.inRange(hsv, greenlow, greenup)# Tạo mask dựa trên khoảng màu xanh
    mask = cv2.dilate(mask, None, iterations=4)# Mở rộng mask để loại bỏ nhiễu
    return mask
# Hàm để xác định vị trí của quả bóng trên frame
def contour_ext(mask, img):
    conts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Tìm contour trong mask
    center = None
    position = None
    if len(conts) > 0:
        c = max(conts, key=cv2.contourArea)# Tìm contour lớn nhất  
        perimeter = cv2.arcLength(c, True)#tính chu vi contour
        approx = cv2.approxPolyDP(c, .03 * cv2.arcLength(c, True), True)
        area = cv2.contourArea(c)# tính diện tích contour
        cv2.imshow('Disp Frame', mask) 
        #print(len(approx))
        if len(approx)>1 and area / (perimeter * perimeter) > 0.05:
            cv2.drawContours(img, [c], 0, (220, 152, 91), -1)
            ((x, y), radius) = cv2.minEnclosingCircle(c)# Tìm tâm và bán kính của vòng tròn bao quanh contour  
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) # Tính toán tọa độ tâm 
            if radius > 20: 
                cv2.circle(img, (int(x), int(y)), int(radius), (126, 255, 60), 2)  # Vẽ vòng tròn và tâm trên frame
                cv2.circle(img, center, 2, (75, 54, 255), 2)  # Vẽ vòng tròn và tâm trên frame
                position = get_position(center, img.shape[1])  # Xác định vị trí dựa trên tọa độ tâm
    return img, position
# Hàm để xác định vị trí của quả bóng dựa trên tọa độ tâm của vòng tròn
def get_position(center, img_width):
    x_center = center[0]
    segment_width = img_width / 7
    segment_id = int(x_center // segment_width) + 1
    position = '0'
    for key, value in positions.items():
        if segment_id in value:
            position = key
            break
    return position

# Hàm chạy trong thread 1 để xử lý video và xác định vị trí của quả bóng
def thread_function_1():
    global position, controlMode
    while True:
        _, frame = cap.read()# Đọc frame từ video
        frame=cv2.resize(frame,(640,480))
        frame_height, frame_width, _ = frame.shape
        
        for i in range(1, 7):# Vẽ các đường thẳng chia thành các vùng
        x_coordinate = frame_width // 7 * i
        cv2.line(frame, (x_coordinate, 0), (x_coordinate, frame_height), (255, 255, 255), 1, lineType=cv2.LINE_AA)
        disp = extract_green(frame, greenlow, greenup)   # Trích xuất vùng màu xanh
        frame, position = contour_ext(disp, frame)  # Xác định vị trí của quả bóng
        cv2.putText(frame, f'Ball Position: {position}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Original Frame', frame)   # Hiển thị frame
        if cv2.waitKey(20) & 0xFF == ord('q')# Kiểm tra nút nhấn để dừng lại
            break
    cap.release() # Giải phóng camera
    cv2.destroyAllWindows() # Đóng cửa sổ OpenCV

def send_data(position1):
    global controlMode
    if position1 == None:
        position1 = '0'
    if not controlMode:#chế độ
        ser.write(position1.encode())
        time.sleep(0.5)
# Hàm chạy trong thread 2 để in ra vị trí của quả bóng         
def thread_function_2():
    while True: #not stop_event.is_set() and
        send_data(position)
        
        print(f"Ball Position: {position}")

if __name__ == "__main__":
    thread1 = threading.Thread(target=thread_function_1)
    thread2 = threading.Thread(target=thread_function_2)
    thread3 = threading.Thread(target=blynk_activate)
    thread1.start()
    thread2.start()
    thread3.start()
        
    
    
