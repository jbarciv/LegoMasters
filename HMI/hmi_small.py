# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np

def show_frames():
    global cap, captured
    ret, frame = cap.read()
    if ret:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label_camera.imgtk = imgtk
        label_camera.configure(image=imgtk)
        label_camera.after(10, show_frames)
    else:
        print("Camera capture failed")
    if captured:
        analyze_image(frame, imgtk)
        captured = False

def toggle_camera():
    global camera_running, cap
    if not camera_running:
        camera_button.config(text='Off')
        camera_running = True
        cap = cv2.VideoCapture(0)  # Reinitialize camera capture
        show_frames()
        print("Camera turned on")
    else:
        camera_button.config(text='On/Off')
        camera_running = False
        cap.release()  # Release camera capture when turning off
        # Show black image when camera is turned off
        black_image = np.zeros((480, 640, 3), dtype=np.uint8)
        black_image = Image.fromarray(black_image)
        black_imgtk = ImageTk.PhotoImage(image=black_image)
        label_camera.imgtk = black_imgtk
        label_camera.configure(image=black_imgtk)
        print("Camera turned off")

def capture_image():
    global captured
    captured = True
    print("Image captured")

def analyze_image(frame, imgtk):
    label_analyze.imgtk = imgtk
    label_analyze.configure(image=imgtk)
    print("Image analyzed")

def build(what_to_build):
    print("Building: ", what_to_build)

def go_home():
    print("Going home")

def close_all():
    global camera_running
    camera_running = False
    cap.release()
    root.quit()

def emergency_stop():
    print("Emergency stop triggered")

camera_running = False
captured = False


root = Tk()

root.title("LegoMasters HMI")
root.geometry("2000x1000")

########## Top: Replicate your own creation ##########
replica_label = Label(root, text="Replicate your own creation", font=('Arial', 20))
replica_label.grid(row=0, column=1, padx=10)

# Generate a black image
black_image = np.zeros((480, 640, 3), dtype=np.uint8)
black_image = Image.fromarray(black_image)
black_imgtk = ImageTk.PhotoImage(image=black_image)

label_camera = Label(root, image=black_imgtk)
label_analyze = Label(root, image=black_imgtk)
label_robot = Label(root, image=black_imgtk)
label_camera.grid(row=1, column=0)
label_analyze.grid(row=1, column=1)
label_robot.grid(row=1, column=2)

camera_frame = Frame(root)
capture_frame = Frame(root)
build_frame = Frame(root)

camera_frame.grid(row=2, column=0, pady=10)
capture_frame.grid(row=2, column=1, pady=10)
build_frame.grid(row=2, column=2, pady=10)

camera_button = Button(camera_frame, text="On/Off", command=toggle_camera)
capture_button = Button(capture_frame, text="Take and Analyze", command=capture_image)
build_button = Button(build_frame, text="Build!", command=lambda: build(0))
camera_button.grid(row=0, column=0, pady=1)  
capture_button.grid(row=0, column=0, pady=1)
build_button.grid(row=0, column=0, pady=1)

replica_label = Label(root, text="Replicates other example constructions", font=('Arial', 20))
replica_label.grid(row=3, column=1)

image_path = "18.png"
loaded_image = Image.open(image_path)
new_size = (200, 200)  # Width, Height
resized_image = loaded_image.resize(new_size, Image.LANCZOS)
loaded_imgtk = ImageTk.PhotoImage(image=resized_image)

camera_frame = Frame(root)
capture_frame = Frame(root)
build_frame = Frame(root)

camera_frame.grid(row=4, column=0, pady=10)
sample_1 = Label(camera_frame, image=loaded_imgtk)
sample_1.grid(row=0, column=0, pady=10)
sample_2 = Label(camera_frame, image=loaded_imgtk)
sample_2.grid(row=0, column=1, pady=10)
sample_3 = Label(camera_frame, image=loaded_imgtk)
sample_3.grid(row=0, column=2, pady=10)

capture_frame.grid(row=4, column=1, pady=10)
sample_4 = Label(capture_frame, image=loaded_imgtk)
sample_4.grid(row=0, column=0, pady=10)
sample_5 = Label(capture_frame, image=loaded_imgtk)
sample_5.grid(row=0, column=1, pady=10)
sample_6 = Label(capture_frame, image=loaded_imgtk)
sample_6.grid(row=0, column=2, pady=10)

build_frame.grid(row=4, column=2, pady=10)
sample_7 = Label(build_frame, image=loaded_imgtk)
sample_7.grid(row=0, column=0, pady=10)
sample_8 = Label(build_frame, image=loaded_imgtk)
sample_8.grid(row=0, column=1, pady=10)
sample_9 = Label(build_frame, image=loaded_imgtk)
sample_9.grid(row=0, column=2, pady=10)

camera_button_1 = Button(camera_frame, text="Build", command=lambda: build(1))
camera_button_2 = Button(camera_frame, text="Build", command=lambda: build(2))
camera_button_3 = Button(camera_frame, text="Build", command=lambda: build(3))
camera_button_1.grid(row=1, column=0, pady=1)  
camera_button_2.grid(row=1, column=1, pady=1)
camera_button_3.grid(row=1, column=2, pady=1)

capture_button_4 = Button(capture_frame, text="Build", command=lambda: build(4))
capture_button_5 = Button(capture_frame, text="Build", command=lambda: build(5))
capture_button_6 = Button(capture_frame, text="Build", command=lambda: build(6))
capture_button_4.grid(row=1, column=0, pady=1)  
capture_button_5.grid(row=1, column=1, pady=1)
capture_button_6.grid(row=1, column=2, pady=1)

build_button_7 = Button(build_frame, text="Build", command=lambda: build(7))
build_button_8 = Button(build_frame, text="Build", command=lambda: build(8))
build_button_9 = Button(build_frame, text="Build", command=lambda: build(9))
build_button_7.grid(row=1, column=0, pady=1)  
build_button_8.grid(row=1, column=1, pady=1)
build_button_9.grid(row=1, column=2, pady=1)

close_button = Button(camera_frame, text="CLOSE ALL", command=close_all, bg='lightgrey', width=15, height=2)
close_button.grid(row=2, column=0, padx=10, pady=30)

home_button = Button(capture_frame, text="GO HOME", command=go_home, bg='lightgreen', width=15, height=2)
home_button.grid(row=2, column=1, padx=10, pady=30)

stop_button = Button(build_frame, text="STOP!", command=emergency_stop, bg='red', width=15, height=2)
stop_button.grid(row=2, column=2, padx=10, pady=30)

root.mainloop()
