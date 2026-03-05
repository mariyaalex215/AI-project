from ultralytics import YOLO
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import random
import time

# -----------------------------
# MODEL LOAD
# -----------------------------
model = YOLO("Cars Detection/best.pt")

# -----------------------------
# IMAGE PATHS
# -----------------------------
image_paths = {
    "North": "junction1.jpg",
    "East": "junction2.jpg",
    "South": "junction3.png",
    "West": "junction4.png"
}

vehicle_classes = ["car","motorbike","bus","truck","ambulance"]

GREEN_TIME = 45

# -----------------------------
# DASHBOARD CLASS
# -----------------------------
class TrafficDashboard:

    def __init__(self,root):

        self.root = root
        self.root.title("AI SMART TRAFFIC CONTROL CENTER")

        # AUTO SCREEN SIZE
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()

        root.geometry(f"{screen_w}x{screen_h}")
        root.configure(bg="black")

        title = tk.Label(
            root,
            text="BATCH 10 TRAFFIC CONTROL CENTER",
            font=("Arial",22,"bold"),
            fg="cyan",
            bg="black"
        )
        title.pack(pady=10)

        # GRID FRAME
        grid = tk.Frame(root,bg="black")
        grid.pack(expand=True)

        self.labels = {}
        self.vehicle_text = {}
        self.timer_text = {}

        directions = list(image_paths.keys())

        for i,d in enumerate(directions):

            panel = tk.Frame(
                grid,
                bg="#202020",
                bd=2,
                relief="ridge"
            )

            panel.grid(row=i//2,column=i%2,padx=20,pady=20)

            title = tk.Label(
                panel,
                text=d+" Junction",
                font=("Arial",16,"bold"),
                fg="yellow",
                bg="#202020"
            )
            title.pack()

            img_label = tk.Label(panel)
            img_label.pack()

            vehicle_label = tk.Label(
                panel,
                text="Vehicles: 0",
                font=("Arial",12),
                fg="white",
                bg="#202020"
            )
            vehicle_label.pack()

            timer_label = tk.Label(
                panel,
                text="Timer: --",
                font=("Arial",12),
                fg="cyan",
                bg="#202020"
            )
            timer_label.pack()

            self.labels[d] = img_label
            self.vehicle_text[d] = vehicle_label
            self.timer_text[d] = timer_label

        threading.Thread(target=self.run_system,daemon=True).start()


    # -----------------------------
    # MAIN SYSTEM
    # -----------------------------
    def run_system(self):

        while True:

            vehicle_counts = {}
            images = {}
            ambulance = {}

            # DETECTION
            for direction,path in image_paths.items():

                img = cv2.imread(path)

                results = model(img,verbose=False)[0]

                count = 0
                ambulance[direction] = False

                for r in results.boxes.data:

                    x1,y1,x2,y2,conf,class_id = r
                    label = model.names[int(class_id)]

                    if label.lower() in vehicle_classes:
                        count += 1

                    if label.lower()=="ambulance":
                        ambulance[direction] = True

                    cv2.rectangle(
                        img,
                        (int(x1),int(y1)),
                        (int(x2),int(y2)),
                        (255,0,0),
                        2
                    )

                    cv2.putText(
                        img,
                        label,
                        (int(x1),int(y1)-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255,0,0),
                        2
                    )

                vehicle_counts[direction] = count
                images[direction] = img

            # PRIORITY
            green_lane = None

            for d,v in ambulance.items():
                if v:
                    green_lane = d
                    break

            if green_lane is None:
                green_lane = max(vehicle_counts,key=vehicle_counts.get)

            # COUNTDOWN
            for t in range(GREEN_TIME,-1,-1):

                for d,img in images.items():

                    frame = img.copy()

                    if d == green_lane:

                        cv2.circle(frame,(40,40),18,(0,255,0),-1)

                        cv2.putText(
                            frame,
                            "SIREN DETECTED",
                            (200,40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,0,255),
                            3
                        )

                        self.timer_text[d].config(text=f"Timer: {t}")

                    else:

                        cv2.circle(frame,(40,40),18,(0,0,255),-1)
                        self.timer_text[d].config(text="Timer: --")

                    # RESIZE IMAGE TO FIT PANEL
                    frame = cv2.resize(frame,(420,240))

                    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(rgb)
                    imgtk = ImageTk.PhotoImage(im)

                    self.labels[d].imgtk = imgtk
                    self.labels[d].config(image=imgtk)

                    self.vehicle_text[d].config(
                        text=f"Vehicles: {vehicle_counts[d]}"
                    )

                self.root.update()
                time.sleep(1)


# -----------------------------
# RUN DASHBOARD
# -----------------------------
root = tk.Tk()
app = TrafficDashboard(root)
root.mainloop()