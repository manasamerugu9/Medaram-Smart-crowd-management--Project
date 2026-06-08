import tkinter as tk
import threading
import cv2
from ultralytics import YOLO

# ---------------- YOLO MODEL ---------------- #
model = YOLO("yolov8n.pt")

running = False

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
    except:
        result_label.config(text="Enter valid number!", fg="red")

# ---------------- AI MODE ---------------- #
def start_ai():
    global running
    running = True

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        result_label.config(text="Camera not found!", fg="red")
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
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("AI Crowd Detection", frame)

        if cv2.waitKey(1) == 27:
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
root.title("Crowd Monitoring System (Manual + AI)")
root.geometry("450x400")

title = tk.Label(root, text="CROWD MONITORING SYSTEM",
                 font=("Arial", 14, "bold"))
title.pack(pady=15)

# ---------------- MANUAL SECTION ---------------- #
tk.Label(root, text="Manual Mode", font=("Arial", 12, "bold")).pack()

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(root, text="CHECK MANUAL",
          bg="green", fg="white",
          command=manual_check).pack(pady=5)

# ---------------- AI SECTION ---------------- #
tk.Label(root, text="AI Mode (YOLO)", font=("Arial", 12, "bold")).pack(pady=10)

tk.Button(root, text="START AI CAMERA",
          bg="blue", fg="white",
          command=run_ai).pack(pady=5)

tk.Button(root, text="STOP AI CAMERA",
          bg="red", fg="white",
          command=stop_ai).pack(pady=5)

# ---------------- OUTPUT ---------------- #
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=20)

root.mainloop()