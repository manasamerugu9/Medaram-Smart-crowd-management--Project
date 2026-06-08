import tkinter as tk
import threading
import cv2
from ultralytics import YOLO
import pandas as pd
import datetime

# ---------------- MODEL ---------------- #
model = YOLO("yolov8n.pt")

running = False
data_log = []

# ---------------- CROWD LEVEL ---------------- #
def get_status(count):
    if count <= 100:
        return "LOW CROWD", "green"
    elif count <= 500:
        return "MEDIUM CROWD", "orange"
    elif count <= 1000:
        return "LARGE CROWD", "blue"
    elif count <= 5000:
        return "HIGH ALERT", "red"
    else:
        return "DANGER ZONE", "darkred"

# ---------------- SAVE TO EXCEL ---------------- #
def save_to_excel(count, mode):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status, _ = get_status(count)

    data_log.append([time, mode, count, status])

    df = pd.DataFrame(data_log, columns=["Time", "Mode", "People Count", "Status"])
    df.to_excel("crowd_data.xlsx", index=False)

# ---------------- MANUAL MODE ---------------- #
def manual_check():
    try:
        count = int(entry.get())
        status, color = get_status(count)

        result_label.config(
            text=f"People Count: {count}\n{status}",
            fg=color,
            font=("Arial", 14, "bold")
        )

        save_to_excel(count, "MANUAL")

    except:
        result_label.config(text="Enter valid number!", fg="red")

# ---------------- AI MODE ---------------- #
def start_ai():
    global running
    running = True

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        result_label.config(text="Camera Not Found!", fg="red")
        return

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

        save_to_excel(count, "AI")

        cv2.imshow("YOLO Crowd Monitoring System", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

def run_ai():
    t = threading.Thread(target=start_ai)
    t.start()

def stop_ai():
    global running
    running = False

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Crowd Monitoring System - FINAL PROJECT")
root.geometry("500x450")

title = tk.Label(root, text="CROWD MONITORING SYSTEM",
                 font=("Arial", 14, "bold"))
title.pack(pady=10)

# -------- MANUAL -------- #
tk.Label(root, text="Manual Mode", font=("Arial", 12, "bold")).pack()

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(root, text="CHECK MANUAL",
          bg="green", fg="white",
          command=manual_check).pack(pady=5)

# -------- AI -------- #
tk.Label(root, text="AI Mode (YOLO)", font=("Arial", 12, "bold")).pack(pady=10)

tk.Button(root, text="START AI",
          bg="blue", fg="white",
          command=run_ai).pack(pady=5)

tk.Button(root, text="STOP AI",
          bg="red", fg="white",
          command=stop_ai).pack(pady=5)

# -------- OUTPUT -------- #
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=20)

root.mainloop()