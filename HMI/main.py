"""
Title: Human-Machine Interface to control the building
Description: This script launches a HMI where to decide whether to replicate an own construction or to build some backup constructions.
Authors: Josep Maria Barbera, Ivonne Quishpe
Date: May 21, 2024
"""

from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pyrealsense2 as rs
from copy import deepcopy
import os
import glob
from skimage import io
import json
import os
import time
import math
import rtde_control
import rtde_receive
import shutil
from take_block import CogePieza
from build_block import ConstruyePieza


ROBOT_IP = "192.168.56.20"

PIEZAS_TOTAL = {
    "P1": {"Joints": [166,-109.71,-87.73,-72.22,88.69,232.80],"Color": "yellow" }, 
    "P2": {"Joints": [162.94,-96.7,-104.34,-68.56,88.67,229.74],"Color": "yellow"},
    "P3": {"Joints": [158.6,-84.55,-116.66,-68.29,88.68,225.43],"Color": "white"},
    "P4": {"Joints": [151.67,-72.66,-125.74,-70.96,88.68,218.52],"Color": "white"},
    "P5": { "Joints": [140.94,-63.69,-130.81,-74.66,88.78,207.81],"Color": "green"},
    "P6": {"Joints": [155.25,-121.61,-69.88,-77.94,88.79,222.06],"Color": "orange"},
    "P7": {"Joints": [150.94,-110.24,-87.12,-71.99,88.8,217.74],"Color": "yellow"},
    "P8": {"Joints": [145.01,-100.37,-100.17,-68.7,88.84,211.8],"Color": "white"},
    "P9": {"Joints": [137.38,-92.68,-108.96,-67.45,88.92,204.19],"Color": "white"},
    "P10": {"Joints": [127.43,-87.52,-114.19,-67.23,89.06,194.24],"Color": "green"},
    "P11": {"Joints": [146.61,-138.02,-41.53,-89.72,88.91,213.44],"Color": "blue" },
    "P12": {"Joints": [141.74,-125.37,-63.82,-79.99,88.94,208.55],"Color": "red" },
    "P13": {"Joints": [135.67,-116.49,-78.05,-74.53,89.01,202.46],"Color": "red" },
    "P14": {"Joints": [128.49,-110.31,-87.18,-71.47,89.11,195.28],"Color": "red" },
    "P15": {"Joints": [119.72,-106.68,-92.32,-69.64,89.26,186.52],"Color": "green" },
    "P16": {"Joints": [128.55,-137.1,-43.33,-88.52,89.18,195.37],"Color": "none" },
    "P17": {"Joints": [122.03,-130.17,-55.77,-82.94,89.28,188.83],"Color": "none" },
    "P18": {"Joints": [114.45,-126.29,-62.44,-80.06,89.42,181.25],"Color": "blue"},
    "P19": {"Joints": [121.86,-67.94,-128.75,-72.18,89.11,188.71],"Color": "none" },
    "P20": {"Joints": [111.79,-96.26,-105.19,-67.31,89.39,178.59],"Color": "none" },
    "P21": {"Joints": [107.06,-120.3,-72.26,-76.17,89.55,173.85],"Color": "none" }
}

ZONAS_TOTAL = {        
    1: [252.42,-89.36,-105.45,-74.94,89.86,227.39],
    2: [259.15, -83.5, -111.08, -74.67, 89.82, 234.15],
    3: [266.22,-78.62,-114.85,-76.29,89.78,241.21],
    4: [273.92,-74.08,-118.11,-77.59,89.76,248.91],
    5: [273.45,-84.41,-116.36,-68.98,89.80,338.42],
    6: [273.13,-91.36,-110.04,-68.35,89.82,338.09],
    7: [272.83,-98.82,-101.78,-69.14,89.84,337.79],
    8: [254.23,-97.38,-103.19,-69.18,89.89,319.18],
    9: [255.69,-103.64,-95.84,-70.27,89.90,320.63],
    10: [272.78,-100.13,-99.93,-69.7,89.85,337.73],
    12: [266.9,-102.43,-97.34,-70.05,89.91,241.83],
    11: [261.68, -106.26, -92.37, -71.20, 89.93,236.61],
    13: [260.48, -93.02, -107.93, -69.64, 89.73,325.56],
    14: [266.43,-88.34, -112.75,-68.67,89.83,331.39],
    15: [266.79,-94.90,-105.97,-68.88,89.95,331.74],
    16: [261.15,-98.6,-101.76,-69.40,89.88,326.10]            
}

COLORS = {
    'blue': {
        'rgb': [[13, 177, 200], [69, 187, 212],[39,175,200], [58, 188, 213], [78, 199, 234], [5, 157, 189], [37, 237, 253], [37, 229, 253], [45, 200, 237], [45, 192, 222], [56, 213, 253], [14, 215, 251], [18, 209, 250], [32, 205, 248], [24, 196, 234], [13, 197, 235], [2, 204, 251], [31, 189, 221], [68, 236, 251], [80, 231, 251], [16, 187, 219]],
        'hsv': [[193.3, 77.6, 98.04], [193.398, 58.19, 69.41]]},
    'white': {
        'rgb': [[206, 209, 208], [218, 215, 210], [243, 237, 231], [245, 244, 250], [192, 198, 200], [252, 255, 250], [228, 224, 226], [226, 224, 222], [252, 249, 238]],
        'hsv': [[65.4545, 4.3137, 100.0000],[37.5000, 3.6866, 85.0980]]},
    'red': {
        'rgb': [[191, 62, 59], [169, 26, 26], [244, 50, 43], [190, 38, 33], [180, 28, 17], [168, 38, 33], [209, 55, 49], [194, 45, 47], [241, 37, 24], [200, 22, 19], [217, 47, 27], [207, 34, 15], [224, 45, 44], [223, 28, 27], [212, 18, 14], [202, 35, 34], [236, 14, 14]],
        'hsv': [[2.0690, 84.2324, 94.5098], [1.7021, 85.4545, 64.7059]]},
    'orange': {
        'rgb': [[252, 129, 21], [246, 116, 16], [230, 112, 23], [254, 172, 21], [252, 123, 2], [254, 161, 8], [252, 142, 4], [252, 145, 20], [252, 148, 31], [252, 172, 6]],
        'hsv': [[26.2722, 66.2745, 100.0000], [24.6729, 91.0638, 92.1569]]},
    'green': {
        'rgb': [[158, 181, 57], [152, 168, 48], [162, 184, 79], [205, 233, 78], [197, 224, 81], [190, 207, 66], [176, 191, 46], [187, 202, 60], [202, 216, 51], [189, 204, 44], [172, 200, 64], [169, 198, 59], [145, 167, 35], [163, 184, 32], [203, 216, 40], [208, 227, 59]],
        'hsv': [[63.8961, 38.6935, 78.0392], [69.8824, 68.0000, 49.0196]]},
    'yellow': {
        'rgb': [[251, 202, 73], [251, 191, 43], [252, 189, 59], [253,192,70], [250,187,32], [252, 201, 32], [254, 255, 83], [253, 244, 45], [252, 230, 55], [252, 215, 41], [252, 204, 17], [253, 212, 52], [252, 228, 66], [230, 180, 28], [252, 191, 19], [252, 242, 32], [253, 214, 30]],
        'hsv': [[39.5455, 70.4000, 98.0392], [45.0829, 79.7357, 89.0196]]},
}

def planificador(columnas, filas, color):
    tam=len(columnas)
    zonas=[]
    columnas_copy = columnas[:]
    colores=[]
    for j in range(len(filas)-1):
        if filas[j] <= filas[j+1]:
            zona = columnas_copy[j]
            zonas.append(zona)
            colores.append(color[j])
    zona = columnas[tam-1]
    colores.append(color[tam-1])
    zonas.append(zona)
    return zonas,colores

def planificador_carga(colores):
    seleccion_piezas=[]
    for i in range(len(colores)):
        color_deseado = colores[i]
        piezas_del_color = []
        for pieza_clave, atributos in PIEZAS_TOTAL.items():
            if isinstance(atributos, dict) and "Color" in atributos and atributos["Color"] == color_deseado:
                piezas_del_color.append(pieza_clave)
        for _ in range(len(seleccion_piezas)):
            if piezas_del_color and piezas_del_color[0] in seleccion_piezas:
                piezas_del_color.remove(piezas_del_color[0])
        if piezas_del_color:
            seleccion_piezas.append(piezas_del_color[0])
    return seleccion_piezas

def show_frames():
    global pipe, captured
    try:
        frame = pipe.wait_for_frames()
        color_frame = frame.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        edges_r = cv2.Canny(img, 100, 250)
        blurred = cv2.GaussianBlur(edges_r, (17, 17), 2)
        edges_r = cv2.Canny(blurred, 90, 150)
        thresh = cv2.adaptiveThreshold(edges_r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
        thresh_cpy = thresh.copy()
        cnts = cv2.findContours(thresh_cpy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(thresh_cpy, [c], -1, (0,0,0), 4)
        thresh_cpy_2 = thresh_cpy.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        opening = cv2.morphologyEx(thresh_cpy_2, cv2.MORPH_OPEN, kernel, iterations=1)    
        image_cpy = img.copy()
        cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        area_treshold = 2000
        area_min = 1000
        for c in cnts:
            area = cv2.contourArea(c)
            if area > area_min and area < area_treshold :
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(image_cpy, (x, y), (x + w, y + h), (36,255,12), 3)
        _img = Image.fromarray(image_cpy)
        imgtk = ImageTk.PhotoImage(image=_img)
        label_camera.imgtk = imgtk
        label_camera.configure(image=imgtk)
        label_camera.after(10, show_frames)
    except: 
        pass

    if captured:
        analyze_image(color_image)
        captured = False

def get_bounding_boxes(img):
    edges_r = cv2.Canny(img, 100, 250)
    blurred = cv2.GaussianBlur(edges_r, (17, 17), 2)
    edges_r = cv2.Canny(blurred, 90, 150)
    thresh = cv2.adaptiveThreshold(edges_r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
    thresh_cpy = thresh.copy()
    cnts = cv2.findContours(thresh_cpy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh_cpy, [c], -1, (0,0,0), 4)
    thresh_cpy_2 = thresh_cpy.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    opening = cv2.morphologyEx(thresh_cpy_2, cv2.MORPH_OPEN, kernel, iterations=1)    
    cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    area_treshold = 2000
    area_min = 1000
    legos = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > area_min and area < area_treshold :
            x,y,w,h = cv2.boundingRect(c)
            legos.append([x, y, w, h])
    return legos

def toggle_camera():
    global camera_running, pipe
    if not camera_running:
        camera_button.config(text='Off')
        camera_running = True
        pipe = rs.pipeline()
        cfg  = rs.config()
        cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
        cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)
        pipe.start(cfg)
        show_frames()
        print("Camera turned on")
    else:
        camera_button.config(text='On/Off')
        camera_running = False
        # Release camera capture when turning off
        pipe.stop()  
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

def analyze_image(frame):
    global num
    images_path = "./tmp"
    if not os.path.exists(images_path):
        os.makedirs(images_path)
        print(f"Folder '{images_path}' created.")
    else:
        pass
    images = glob.glob("./tmp/*.png")
    img_num =[]
    for image in images:
        img_num.append(int(image[6:-4]))
    img_num.sort()
    if img_num == []:
        num = 1
    else:
        num = img_num[-1] + 1
    image_path = './tmp/' + str(num) + '.png'
    cv2.imwrite(image_path, frame)
    img = io.imread(image_path)

    lego = get_bounding_boxes(img)

    xlegos = lego.copy()
    xlegos.sort(key=lambda x: x[0], reverse=True)
    legos_x = [] 
    while (len(xlegos)>0):
        compare_x = []
        lego = xlegos.pop(0)
        compare_x.append(lego)
        x_ref, _, _, _ = lego
        ilego = []
        for i in range(len(xlegos)):
            x, _, _, _ = xlegos[i]
            if (abs(x - x_ref) <= 35):
                ilego.append(i)
        for i in ilego:      
            lego = xlegos[i]
            compare_x.append(lego)
        legos_x.append(compare_x)
        xlegos = [xlegos[i] for i in range(len(xlegos)) if i not in ilego]
    for i in range(len(legos_x)):
        sum = []
        for j in range(len(legos_x[i])):
            x, _, _, _ = legos_x[i][j]
            sum.append(x)
        the_mean = np.mean(sum)
        for j in range(len(legos_x[i])):
            legos_x[i][j][0] = round(the_mean)
    lego_columns = len(legos_x)
    xlegos = []
    for i in range(len(legos_x)):
        for j in range(len(legos_x[i])):
            legos_x[i][j].append([i+1])
            xlegos.append(legos_x[i][j])
    ylegos = xlegos.copy()
    ylegos.sort(key=lambda x: x[1])
    legos_y = []
    while (len(ylegos)>0):
        compare_y = []
        lego = ylegos.pop(0)
        compare_y.append(lego)
        _, y_ref, _, _, _ = lego
        ilego = []
        for i in range(len(ylegos)):
            _, y, _, _, _ = ylegos[i]
            if (abs(y - y_ref) <= 25):
                ilego.append(i)
        for i in ilego:      
            lego = ylegos[i]
            compare_y.append(lego)
        legos_y.append(compare_y)
        ylegos = [ylegos[i] for i in range(len(ylegos)) if i not in ilego]
    for i in range(len(legos_y)):
        sum = []
        for j in range(len(legos_y[i])):
            _, y, _, _, _ = legos_y[i][j]
            sum.append(y)
        the_mean = np.mean(sum)
        for j in range(len(legos_y[i])):
            legos_y[i][j][1] = round(the_mean)
    lego_rows = len(legos_y)
    legos = []
    for i in range(len(legos_y)):
        for j in range(len(legos_y[i])):
            legos_y[i][j][4].append(len(legos_y)-i)
            legos.append(legos_y[i][j])
    img_copy = img.copy()
    img_copy = cv2.GaussianBlur(img_copy, (17, 17), 5)
    m_legos = deepcopy(legos)
    plt.figure(figsize=(20, 8)) 
    for i in range(len((m_legos))):
        x, y, w, h, _ = m_legos[i]
        roi = img_copy[y:y+h, x:x+w]
        plt.subplot(1, len(m_legos), i+1)
        plt.imshow(roi)
        r = roi[:,:,0]
        g = roi[:,:,1]
        b = roi[:,:,2]
        r = round(np.mean(r))
        g = round(np.mean(g))
        b = round(np.mean(b))
        print(r,g,b)
        for key, value in COLORS.items():
            for space, value in value.items():
                if space == 'hsv':
                    continue
                add = 11
                for in_value in value:
                    plus = [x + add for x in in_value]
                    minus = [x - add for x in in_value]
                    if ( (r <= plus[0] and r >= minus[0]) and (g <= plus[1] and g >= minus[1]) and (b <= plus[2] and b >= minus[2]) ):
                        # print(key, space, (r, g, b), minus, plus, value)
                        m_legos[i].append(in_value)
                        m_legos[i].append(key)
                        break
    # print(m_legos)
    my_legos = m_legos.copy()
    my_legos_ord = []
    for j in range(1,lego_rows+1):
        for i in range(1,lego_columns+1):
            for my_lego in my_legos:
                if ( (my_lego[4][0] == i) and (my_lego[4][1] == j)):
                    print(my_lego)
                    my_legos_ord.append(my_lego)
    try:
        legos_to_json = []
        for (x,y,w,h, pos, _, label) in my_legos_ord:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
            legos_to_json.append([pos[0], pos[1], label])
        _img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=_img)
        label_analyze.imgtk = imgtk
        label_analyze.configure(image=imgtk)
        file_name = str(num) + ".json"
        with open("./tmp/"+file_name, 'w') as f:
            json.dump(legos_to_json, f)
    except:
        print("Recalibrate! Error while analyzing...")
        _img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=_img)
        label_analyze.imgtk = imgtk
        label_analyze.configure(image=imgtk)
        root.clipboard_clear()
  
def build(build_num, json_path):
    global num, building, backup_folder, folder_path
    building = True

    if build_num == 0:
        tmp_json = glob.glob(os.path.join(folder_path, "*.json"))
        tmp_png = glob.glob(os.path.join(folder_path, "*.png"))
        tmp_json.sort()
        tmp_png.sort()
        print(tmp_json)
        json_path = tmp_json[-1]
        print(json_path)
        png_path = tmp_png[-1]
        shutil.copy(json_path, backup_folder)
        shutil.copy(png_path, backup_folder)
    else:
        json_path = json_path[:-3]+"json"
    with open(json_path, 'r') as file:
        legos = json.load(file)
    print(legos)
    columnas=[]
    filas=[]
    color=[]          
    for lego in legos:
        print(lego)
        columnas.append(lego[0])
        filas.append(lego[1])
        color.append(lego[2])
    zonas, colores = planificador(columnas, filas, color)
    print(zonas)
    piezas = planificador_carga(colores)
    print(piezas)
    for pieza_seleccionada, zona_seleccionada in zip(piezas, zonas):
        pieza = PIEZAS_TOTAL[pieza_seleccionada]["Joints"]
        zona = ZONAS_TOTAL[zona_seleccionada]
        CogePieza(pieza, rtde_c, rtde_r)
        ConstruyePieza(zona, rtde_c, rtde_r)
    building = False

def go_home():
    print("Going home")
    if not building:
        rtde_c.moveJ([1.59, -1.538, -0.06, -1.56, 0.014, 1.18], 1, 0.6)
    else:
        print("Wait the building process to finish")

def close_all():
    global camera_running
    camera_running = False
    try:
        pipe.stop()
    except:
        pass
    root.quit()

def emergency_stop():
    print("Emergency stop triggered")

camera_running = False
captured = False
building = False
num = 0

# We remove the tmp folder
try:
    folder_path = './tmp'
    shutil.rmtree(folder_path)
except:
    pass

root = Tk()

root.title("LegoMasters HMI")
root.geometry("2000x1000")

########## Top: Replicate your own creation ##########
replica_label = Label(root, text="Replicate your own creation", font=('Arial', 20))
replica_label.grid(row=0, column=1, padx=10)

# Generate a black image
black_image = np.zeros((480, 640, 3), dtype=np.uint8)
black_image = Image.fromarray(black_image)
black_imgtk = ImageTk.PhotoImage(image  =black_image)

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
build_button = Button(build_frame, text="Build!", command=lambda: build(0, None))
camera_button.grid(row=0, column=0, pady=1)  
capture_button.grid(row=0, column=0, pady=1)
build_button.grid(row=0, column=0, pady=1)

replica_label = Label(root, text="Replicates other example constructions", font=('Arial', 20))
replica_label.grid(row=3, column=1)

backup_folder = "./backup"
demos_folder = "./demos"
png_files = glob.glob(os.path.join(backup_folder, "*.png"))
demos_files = glob.glob(os.path.join(demos_folder, "*.png"))
load_images = []
num_png_files = len(png_files)
if num_png_files >= 9:
    load_images = png_files[-9:]
elif num_png_files < 9:
    load_images = png_files
    the_rest = 9 - num_png_files
    load_images = load_images + demos_files[-the_rest:]
load_images.sort()

image2load = []
for image_path in load_images:
    loaded_image = Image.open(image_path)
    new_size = (200, 200)
    resized_image = loaded_image.resize(new_size, Image.LANCZOS)
    loaded_imgtk = ImageTk.PhotoImage(image=resized_image)
    image2load.append(loaded_imgtk)

camera_frame = Frame(root)
capture_frame = Frame(root)
build_frame = Frame(root)

camera_frame.grid(row=4, column=0, pady=10)
sample_1 = Label(camera_frame, image=image2load[0])
sample_1.grid(row=0, column=0, pady=10)
sample_2 = Label(camera_frame, image=image2load[1])
sample_2.grid(row=0, column=1, pady=10)
sample_3 = Label(camera_frame, image=image2load[2])
sample_3.grid(row=0, column=2, pady=10)

capture_frame.grid(row=4, column=1, pady=10)
sample_4 = Label(capture_frame, image=image2load[3])
sample_4.grid(row=0, column=0, pady=10)
sample_5 = Label(capture_frame, image=image2load[4])
sample_5.grid(row=0, column=1, pady=10)
sample_6 = Label(capture_frame, image=image2load[5])
sample_6.grid(row=0, column=2, pady=10)

build_frame.grid(row=4, column=2, pady=10)
sample_7 = Label(build_frame, image=image2load[6])
sample_7.grid(row=0, column=0, pady=10)
sample_8 = Label(build_frame, image=image2load[7])
sample_8.grid(row=0, column=1, pady=10)
sample_9 = Label(build_frame, image=image2load[8])
sample_9.grid(row=0, column=2, pady=10)

camera_button_1 = Button(camera_frame, text="Build", command=lambda: build(1, load_images[0]))
camera_button_2 = Button(camera_frame, text="Build", command=lambda: build(2, load_images[1]))
camera_button_3 = Button(camera_frame, text="Build", command=lambda: build(3, load_images[2]))
camera_button_1.grid(row=1, column=0, pady=1)  
camera_button_2.grid(row=1, column=1, pady=1)
camera_button_3.grid(row=1, column=2, pady=1)

capture_button_4 = Button(capture_frame, text="Build", command=lambda: build(4, load_images[3]))
capture_button_5 = Button(capture_frame, text="Build", command=lambda: build(5, load_images[4]))
capture_button_6 = Button(capture_frame, text="Build", command=lambda: build(6, load_images[5]))
capture_button_4.grid(row=1, column=0, pady=1)  
capture_button_5.grid(row=1, column=1, pady=1)
capture_button_6.grid(row=1, column=2, pady=1)

build_button_7 = Button(build_frame, text="Build", command=lambda: build(7, load_images[6]))
build_button_8 = Button(build_frame, text="Build", command=lambda: build(8, load_images[7]))
build_button_9 = Button(build_frame, text="Build", command=lambda: build(9, load_images[8]))
build_button_7.grid(row=1, column=0, pady=1)  
build_button_8.grid(row=1, column=1, pady=1)
build_button_9.grid(row=1, column=2, pady=1)

close_button = Button(camera_frame, text="CLOSE ALL", command=close_all, bg='lightgrey', width=15, height=2)
close_button.grid(row=2, column=0, padx=10, pady=30)

home_button = Button(capture_frame, text="GO HOME", command=go_home, bg='lightgreen', width=15, height=2)
home_button.grid(row=2, column=1, padx=10, pady=30)

stop_button = Button(build_frame, text="STOP!", command=emergency_stop, bg='red', width=15, height=2)
stop_button.grid(row=2, column=2, padx=10, pady=30)

# Connect with UR3
rtde_receive_ = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

root.mainloop()
