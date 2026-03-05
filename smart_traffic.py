from ultralytics import YOLO
import cv2
import tkinter as tk
from PIL import Image, ImageTk

# -----------------------------
# MODEL LOAD
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# IMAGE PATHS
# -----------------------------
image_paths = {
    "North": "junction1.jpg",
    "East": "junction2.jpg",
    "South": "Junction3.png",
    "West": "junction4.png"
}

# -----------------------------
# SIGNAL TIMES
# -----------------------------
GREEN_TIME = 30
YELLOW_TIME = 5
RED_TIME = 45

vehicle_classes = ["car","motorbike","bus","truck"]

vehicle_counts = {}
images_data = {}

# -----------------------------
# VEHICLE DETECTION
# -----------------------------
for direction,path in image_paths.items():

    img = cv2.imread(path)

    if img is None:
        vehicle_counts[direction] = 0
        images_data[direction] = None
        continue

    img = cv2.resize(img,(350,200))

    results = model(img,verbose=False)[0]

    count = 0

    for r in results.boxes.data:

        class_id = int(r[5])
        label = model.names[class_id]

        if label in vehicle_classes:

            count += 1

            x1,y1,x2,y2,conf,_ = r

            cv2.rectangle(
                img,
                (int(x1),int(y1)),
                (int(x2),int(y2)),
                (0,255,0),
                2
            )

            cv2.putText(
                img,
                label,
                (int(x1),int(y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )

    vehicle_counts[direction] = count
    images_data[direction] = img


# -----------------------------
# SIGNAL PRIORITY
# -----------------------------
sorted_lanes = sorted(
    vehicle_counts.items(),
    key=lambda x: x[1],
    reverse=True
)

lanes = [lane for lane,_ in sorted_lanes]

signal_info = {
    lanes[0]:["GREEN",GREEN_TIME],
    lanes[1]:["YELLOW",YELLOW_TIME],
    lanes[2]:["RED",RED_TIME],
    lanes[3]:["RED",RED_TIME]
}

# -----------------------------
# TKINTER GUI
# -----------------------------
root = tk.Tk()
root.title("AI Smart Traffic Dashboard")

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

root.geometry(f"{screen_w}x{screen_h}")
root.configure(bg="black")

frames = {}
signal_labels = {}
timer_labels = {}

positions = {
    "North":(0,0),
    "East":(0,1),
    "South":(1,0),
    "West":(1,1)
}

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)

# -----------------------------
# CREATE PANELS
# -----------------------------
for direction,(r,c) in positions.items():

    frame = tk.Frame(root,bg="#111111",bd=3,relief="ridge")
    frame.grid(row=r,column=c,padx=10,pady=10,sticky="nsew")

    title = tk.Label(
        frame,
        text=direction+" Junction",
        font=("Arial",18,"bold"),
        fg="white",
        bg="#111111"
    )
    title.pack(pady=5)

    img = images_data[direction]

    if img is not None:

        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((400,220))

        img_tk = ImageTk.PhotoImage(img_pil)

        label = tk.Label(frame,image=img_tk)
        label.image = img_tk
        label.pack()

    count_label = tk.Label(
        frame,
        text=f"Vehicles: {vehicle_counts[direction]}",
        font=("Arial",14),
        fg="white",
        bg="#111111"
    )
    count_label.pack()

    signal_label = tk.Label(
        frame,
        text=f"Signal: {signal_info[direction][0]}",
        font=("Arial",16,"bold"),
        fg="yellow",
        bg="#111111"
    )
    signal_label.pack()

    timer_label = tk.Label(
        frame,
        text=f"Time: {signal_info[direction][1]}",
        font=("Arial",16),
        fg="cyan",
        bg="#111111"
    )
    timer_label.pack()

    signal_labels[direction] = signal_label
    timer_labels[direction] = timer_label


# -----------------------------
# TIMER UPDATE FUNCTION
# -----------------------------
def update_timers():

    for lane in signal_info:

        signal,time_left = signal_info[lane]

        if time_left > 0:

            time_left -= 1

        else:

            # RESET TIMER
            if signal == "GREEN":
                time_left = GREEN_TIME

            elif signal == "YELLOW":
                time_left = YELLOW_TIME

            else:
                time_left = RED_TIME

        signal_info[lane][1] = time_left

        timer_labels[lane].config(text=f"Time: {time_left}")

    root.after(1000,update_timers)


update_timers()

root.mainloop()