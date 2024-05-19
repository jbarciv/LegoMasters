import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

def toggle_camera():
    global camera_running
    if not camera_running:
        camera_button.config(text='Off')
        camera_running = True
        update_camera_feed()
        print("Camera turned on")
    else:
        camera_button.config(text='On/Off')
        camera_running = False
        image_display.config(image='')  # Clear the display
        cap.release()
        print("Camera turned off")

def update_camera_feed():
    if camera_running:
        ret, frame = cap.read()
        if ret:
            display_image(frame, image_display)
        root.after(20, update_camera_feed)  # Update the camera feed every 20ms

def capture_image():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured")
        display_image(frame, image_display)
    else:
        print("Failed to capture image")

def analyze_image():
    frame = cv2.imread("captured_image.jpg")
    if frame is not None:
        display_image(frame, analyzed_display)
        print("Image analyzed")
    else:
        print("No image to analyze")

def construct():
    print("Construction started")

def go_home():
    print("Going home")

def close_all():
    global camera_running
    camera_running = False
    cap.release()
    root.quit()

def emergency_stop():
    print("Emergency stop triggered")

def display_image(frame, display_label):
    frame = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    image_display.imgtk = imgtk
    image_display.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    image_display.after(20, display_image)

# Initialize the camera
cap = cv2.VideoCapture(0)
camera_running = False

# Main window setup
root = tk.Tk()
root.title("LegoMasters HMI")
root.geometry("1100x900")

# Top frames for modes
mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)

# Labels for modes
replica_label = tk.Label(mode_frame, text="Replica tu propia creacion", font=('Arial', 14))
replica_label.grid(row=0, column=0, padx=10)

stored_label = tk.Label(mode_frame, text="Otras construcciones guardadas", font=('Arial', 14))
stored_label.grid(row=0, column=1, padx=100)

# Main frames for camera and analysis
camera_frame = tk.Frame(root)
camera_frame.pack(pady=10)

image_display = tk.Label(root)
image_display.grid(row=0, column=0, padx=10)

analyzed_display = tk.Label(camera_frame, text="Analyzed Image Here", width=40, height=10, bg='grey')
analyzed_display.grid(row=0, column=1, padx=10)

robot_view_label = tk.Label(camera_frame, text="Robot Camera", width=40, height=10, bg='lightgrey')
robot_view_label.grid(row=0, column=2, padx=10)

# Buttons for camera actions
camera_button = tk.Button(camera_frame, text="On/Off", command=toggle_camera)
camera_button.grid(row=1, column=0, pady=5)

capture_button = tk.Button(camera_frame, text="Capturar y Analizar", command=capture_image)
capture_button.grid(row=1, column=1, pady=5)

analyze_button = tk.Button(camera_frame, text="Analizar", command=analyze_image)
analyze_button.grid(row=1, column=2, pady=5)

construct_button = tk.Button(camera_frame, text="Construir!", command=construct)
construct_button.grid(row=1, column=3, pady=5)

# Frame for saved constructions
saved_frame = tk.Frame(root)
saved_frame.pack(pady=10)

# Labels and buttons for saved constructions
for i in range(5):
    tk.Label(saved_frame, text="Construction {}".format(i+1), width=20, height=10, bg='grey').grid(row=0, column=i, padx=5)
    tk.Button(saved_frame, text="Construir!", command=construct).grid(row=1, column=i, pady=5)

# Control buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=20)

close_button = tk.Button(control_frame, text="CLOSE ALL", command=close_all, bg='lightgrey', width=15, height=2)
close_button.grid(row=0, column=0, padx=10)

home_button = tk.Button(control_frame, text="GO HOME", command=go_home, bg='lightgreen', width=15, height=2)
home_button.grid(row=0, column=1, padx=10)

stop_button = tk.Button(control_frame, text="STOP!", command=emergency_stop, bg='red', width=15, height=2)
stop_button.grid(row=0, column=2, padx=10)

# Run the main loop
root.mainloop()
