import cv2
import threading
import tkinter as tk
from ultralytics import YOLO
import winsound
import time

# ---------------- YOLO MODEL ---------------- #
model = YOLO("yolov8n.pt")

running = False

# ---------------- ALARM ---------------- #
def play_alarm():
    winsound.Beep(1500, 700)

# ---------------- CROWD STATUS ---------------- #
def get_status(count):
    if count <= 3:
        return "GREEN - SAFE", (0, 255, 0)
    elif count <= 6:
        return "YELLOW - WARNING", (0, 255, 255)
    else:
        return "RED - DANGER", (0, 0, 255)

# ---------------- CAMERA FUNCTION ---------------- #
def start_camera():
    global running
    running = True

    cap = cv2.VideoCapture("http://192.168.1.5:8080/video")
    cap = cv2.VideoCapture("rtsp://username:password@ip:554/stream")

    if not cap.isOpened():
        print("Camera not found")
        return

    last_alarm_time = 0

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)

        count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if label == "person":
                    count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        status, color = get_status(count)

        cv2.putText(frame, f"People: {count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, status, (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # ---------------- ALARM LOGIC ---------------- #
        current_time = time.time()

        if count > 6:
            if current_time - last_alarm_time > 2:
                play_alarm()
                last_alarm_time = current_time

        cv2.imshow("YOLO Crowd Monitoring System", frame)

        if cv2.waitKey(1) == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- THREAD CONTROL ---------------- #
def run_camera():
    t = threading.Thread(target=start_camera)
    t.start()

def stop_camera():
    global running
    running = False

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Crowd Monitoring System - YOLO")
root.geometry("400x300")

label = tk.Label(root, text="YOLO CROWD MONITORING", font=("Arial", 14, "bold"))
label.pack(pady=20)

start_btn = tk.Button(root, text="START CAMERA", bg="green", fg="white",
                       command=run_camera, width=20)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="STOP CAMERA", bg="red", fg="white",
                      command=stop_camera, width=20)
stop_btn.pack(pady=10)

info = tk.Label(root, text="Press ESC to close video window")
info.pack(pady=10)

root.mainloop()