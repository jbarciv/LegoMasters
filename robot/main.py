#!/usr/bin/env python
# coding: utf-8

import time
import math
import rtde_control
import rtde_receive
from N1 import CogePieza
from N2 import ConstruyePieza
# Imports for Vision
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pyrealsense2 as rs
from copy import deepcopy


# Constants for robot connection
ROBOT_IP = "192.168.56.20"

# Initialize robot interfaces
rtde_receive_ = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

# Data for pieces and zones
PIEZAS_TOTAL = {
    "P1": {"Joints": [166, -109.71, -87.73, -72.22, 88.69, 232.80], "Color": "yellow"},
    "P2": {"Joints": [162.94, -96.7, -104.34, -68.56, 88.67, 229.74], "Color": "yellow"},
    "P3": {"Joints": [158.6, -84.55, -116.66, -68.29, 88.68, 225.43], "Color": "white"},
    "P4": {"Joints": [151.67, -72.66, -125.74, -70.96, 88.68, 218.52], "Color": "white"},
    "P5": {"Joints": [140.94, -63.69, -130.81, -74.66, 88.78, 207.81], "Color": "green"},
    "P6": {"Joints": [155.25, -121.61, -69.88, -77.94, 88.79, 222.06], "Color": "orange"},
    "P7": {"Joints": [150.94, -110.24, -87.12, -71.99, 88.8, 217.74], "Color": "yellow"},
    "P8": {"Joints": [145.01, -100.37, -100.17, -68.7, 88.84, 211.8], "Color": "white"},
    "P9": {"Joints": [137.38, -92.68, -108.96, -67.45, 88.92, 204.19], "Color": "white"},
    "P10": {"Joints": [127.43, -87.52, -114.19, -67.23, 89.06, 194.24], "Color": "green"},
    "P11": {"Joints": [146.61, -138.02, -41.53, -89.72, 88.91, 213.44], "Color": "blue"},
    "P12": {"Joints": [141.74, -125.37, -63.82, -79.99, 88.94, 208.55], "Color": "red"},
    "P13": {"Joints": [135.67, -116.49, -78.05, -74.53, 89.01, 202.46], "Color": "red"},
    "P14": {"Joints": [128.49, -110.31, -87.18, -71.47, 89.11, 195.28], "Color": "red"},
    "P15": {"Joints": [119.72, -116.35, -103.33, -49.17, 89.33, 186.5], "Color": "green"},
    "P16": {"Joints": [128.55, -137.1, -43.33, -88.52, 89.18, 195.37], "Color": "none"},
    "P17": {"Joints": [122.03, -130.17, -55.77, -82.94, 89.28, 188.83], "Color": "none"},
    "P18": {"Joints": [114.45, -126.29, -62.44, -80.06, 89.42, 181.25], "Color": "blue"},
    "P19": [121.86, -67.94, -128.75, -72.18, 89.11, 188.71],
    "P20": [111.79, -96.26, -105.19, -67.31, 89.39, 178.59],
    "P21": [107.06, -120.3, -72.26, -76.17, 89.55, 173.85]
}

ZONAS_TOTAL = {
    1: [252.42, -91.07, -110.05, -68.63, 89.88, 227.38],
    2: [258.87, -85.58, -115.84, -67.83, 89.84, 233.85],
    3: [265.90, -80.54, -119.61, -69.60, 89.81, 240.88],
    4: [273.91, -75.74, -123.22, -70.82, 89.78, 248.89],
    5: [273.45, -84.41, -116.36, -68.98, 89.80, 338.42],
    6: [273.13, -91.36, -110.04, -68.35, 89.82, 338.09],
    7: [272.83, -98.82, -101.78, -69.14, 89.84, 337.79],
    8: [254.23, -97.38, -103.19, -69.18, 89.89, 319.18],
    9: [255.69, -103.64, -95.84, -70.27, 89.90, 320.63],
    10: [272.78, -100.13, -99.93, -69.7, 89.85, 337.73],
    11: [261.68, -106.26, -92.37, -71.20, 89.93, 236.61],
    12: [266.9, -102.43, -97.34, -70.05, 89.91, 241.83],
    13: [260.48, -93.02, -107.93, -69.64, 89.73, 325.56],
    14: [266.43, -88.34, -112.75, -68.67, 89.83, 331.39],
    15: [266.79, -94.90, -105.97, -68.88, 89.95, 331.74],
    16: [261.15, -98.6, -101.76, -69.40, 89.88, 326.10]
}

def planificador(columnas, filas, profundidad,color):
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
        for j in range(len(seleccion_piezas)-1):
            if piezas_del_color[0] in seleccion_piezas:
                piezas_del_color.remove(piezas_del_color[0])
        seleccion_piezas.append(piezas_del_color[0])
    return seleccion_piezas
    
def get_photo():
    pipe = rs.pipeline()
    cfg  = rs.config()
    cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
    cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)
    pipe.start(cfg)
    while True:
        frame = pipe.wait_for_frames()
        color_frame = frame.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        img = color_image
        edges_r = cv2.Canny(img, 100, 200)
        blurred = cv2.GaussianBlur(edges_r, (17, 17), 2)
        edges_r = cv2.Canny(blurred, 90, 150)
        thresh = cv2.adaptiveThreshold(edges_r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 1)
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
        cv2.imshow('rgb', image_cpy)
        k = cv2.waitKey(5)
        if k == ord('s'):
            break
    pipe.stop()
    cv2.destroyAllWindows()
    return color_image

def get_bounding_boxes(img):
    edges_r = cv2.Canny(img, 100, 200)
    blurred = cv2.GaussianBlur(edges_r, (17, 17), 2)
    edges_r = cv2.Canny(blurred, 90, 150)
    thresh = cv2.adaptiveThreshold(edges_r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 1)
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
    legos = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > area_min and area < area_treshold :
            x,y,w,h = cv2.boundingRect(c)
            legos.append([x, y, w, h])
    return legos

def get_legos_matrix(img):
    lego = get_bounding_boxes(img)
    xlegos = lego.copy()
    xlegos.sort(key=lambda x: x[0])
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
    colors = {
        'blue': {
            'rgb': [[13, 177, 200], [69, 187, 212],[39,175,200], [58, 188, 213], [78, 199, 234], [5, 157, 189], [37, 237, 253], [37, 229, 253], [45, 200, 237], [45, 192, 222], [56, 213, 253], [14, 215, 251], [18, 209, 250], [32, 205, 248], [24, 196, 234], [13, 197, 235], [2, 204, 251]],
            'hsv': [[193.3, 77.6, 98.04], [193.398, 58.19, 69.41]]},
        # 'light_blue': {
        #     'rgb': [191, 228, 231], 
        #     'hsv': [92, 44, 231]},
        'white': {
            'rgb': [[206, 209, 208], [218, 215, 210], [243, 237, 231], [245, 244, 250], [192, 198, 200], [252, 255, 250]],
            'hsv': [[65.4545, 4.3137, 100.0000],[37.5000, 3.6866, 85.0980]]},
        'red': {
            'rgb': [[191, 62, 59], [169, 26, 26], [244, 50, 43], [190, 38, 33], [180, 28, 17], [168, 38, 33], [209, 55, 49], [194, 45, 47], [241, 37, 24], [200, 22, 19], [217, 47, 27], [207, 34, 15], [224, 45, 44], [223, 28, 27], [212, 18, 14]],
            'hsv': [[2.0690, 84.2324, 94.5098], [1.7021, 85.4545, 64.7059]]},
        # 'light_red': {
        #     'rgb': [253, 132, 126], 
        #     'hsv': [1, 128, 253]},
        'orange': {
            'rgb': [[252, 129, 21], [246, 116, 16], [230, 112, 23], [254, 172, 21], [252, 123, 2], [254, 161, 8], [252, 142, 4], [252, 145, 20], [252, 148, 31]],
            'hsv': [[26.2722, 66.2745, 100.0000], [24.6729, 91.0638, 92.1569]]},
        'green': {
            'rgb': [[158, 181, 57], [152, 168, 48], [162, 184, 79], [205, 233, 78], [197, 224, 81], [190, 207, 66], [176, 191, 46], [187, 202, 60], [202, 216, 51], [189, 204, 44], [172, 200, 64], [169, 198, 59]],
            'hsv': [[63.8961, 38.6935, 78.0392], [69.8824, 68.0000, 49.0196]]},
        # 'light_green': {
        #     'rgb': [213, 232, 163], 
        #     'hsv': [38, 76, 232]},
        'yellow': {
            'rgb': [[251, 202, 73], [251, 191, 43], [252, 189, 59], [253,192,70], [250,187,32], [252, 201, 32], [254, 255, 83], [253, 244, 45], [252, 230, 55], [252, 215, 41], [252, 204, 17], [253, 212, 52], [252, 228, 66]],
            'hsv': [[39.5455, 70.4000, 98.0392], [45.0829, 79.7357, 89.0196]]},
        # 'light_yellow': {
        #     'rgb': [251, 230, 143], 
        #     'hsv': [24, 110, 251]}
    }
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
        for key, value in colors.items():
            for space, value in value.items():
                if space == 'hsv':
                    continue
                add = 10
                for in_value in value:
                    plus = [x + add for x in in_value]
                    minus = [x - add for x in in_value]
                    if ( (r <= plus[0] and r >= minus[0]) and (g <= plus[1] and g >= minus[1]) and (b <= plus[2] and b >= minus[2]) ):
                        print(key, space, (r, g, b), minus, plus, value)
                        m_legos[i].append(in_value)
                        m_legos[i].append(key)
                        break
    my_legos = m_legos.copy()
    my_legos_ord = []
    for j in range(1,lego_rows+1):
        for i in range(1,lego_columns+1):
            for my_lego in my_legos:
                if ( (my_lego[4][0] == i) and (my_lego[4][1] == j)):
                    print(my_lego)
                    my_legos_ord.append(my_lego)
    return my_legos_ord

def main():
    photo = get_photo()
    legos = get_legos_matrix(photo)
    columnas=[]
    filas=[]
    color=[]
    profundidad=[]           
    for i in range(0, len(legos)):
        my_lego=legos[i]
        columnas.append(my_lego[4][0])
        filas.append(my_lego[4][1])
        # profundidad.append(my_lego[4][2])
        color.append(my_lego[6])
    zonas, colores = planificador(columnas, filas, profundidad, color)
    print(zonas)
    piezas = planificador_carga(colores)
    print(piezas)
    for pieza_seleccionada, zona_seleccionada in zip(piezas, zonas):
        pieza = PIEZAS_TOTAL[pieza_seleccionada]["Joints"]
        zona = ZONAS_TOTAL[zona_seleccionada]
        CogePieza(pieza, rtde_c, rtde_r)
        ConstruyePieza(zona, rtde_c, rtde_r)
    # Go home
    rtde_c.moveJ([1.59, -1.538, -0.06, -1.56, 0.014, 1.18], 0.15, 0.1)


if __name__ == "__main__":
    main()
     


