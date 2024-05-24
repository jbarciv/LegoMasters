
import math
import time

Zonas_2 = {
        "Home": [91.22,-88.11,-3.37,-89.40,0.8,67.6],
        "Cerca_Captura2_1": [94.45,-88.09,-86.42,-94.83,-3.84,68.35],
        "Cerca_Captura2_2": [134.43,-127.43,-76.26,-156.79,42.43,159.78],
        "Cerca_Captura2_3": [128.67,-148.04,-55.45,-149.1,38.07,150.58]
} 

Zonas_1 = {
        "Home": [91.22,-88.11,-3.37,-89.40,0.8,67.6],
        "Cerca_Captura1_1": [92.14,-83.2,-96.57,-176.93,2.04,154.74],
        "Cerca_Captura1_2": [63.17,-81.53,-125.42,-157.03,-115.52,153.45],
        "Cerca_Captura1_3": [54.94,-106.38,-143.05,-113.76,-125.2,154.2]
}

def go_zone_2(rtde_c):
        Cerca_Captura2_1 = [math.radians(i) for i in Zonas_2["Cerca_Captura2_1"]]
        Cerca_Captura2_2 = [math.radians(i) for i in Zonas_2["Cerca_Captura2_2"]]
        Cerca_Captura2_3 = [math.radians(i) for i in Zonas_2["Cerca_Captura2_3"]]
        rtde_c.moveJ(Cerca_Captura2_1, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura2_2, 0.5, 0.2) 
        time.sleep(1) 
        rtde_c.moveJ(Cerca_Captura2_3, 0.5, 0.2) 

def come_from_zone_2(rtde_c):
        Cerca_Captura2_1 = [math.radians(i) for i in Zonas_2["Cerca_Captura2_1"]]
        Cerca_Captura2_2 = [math.radians(i) for i in Zonas_2["Cerca_Captura2_2"]]

        Home = [math.radians(i) for i in Zonas_2["Home"]]
        rtde_c.moveJ(Cerca_Captura2_2, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura2_1, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Home, 0.5, 0.2)
        time.sleep(1)

def go_zone_1(rtde_c):
        Cerca_Captura1_1 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_1"]]
        Cerca_Captura1_2 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_2"]]
        Cerca_Captura1_3 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_3"]]
        rtde_c.moveJ(Cerca_Captura1_1, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura1_2, 0.5, 0.2) 
        time.sleep(1) 
        rtde_c.moveJ(Cerca_Captura1_3, 0.5, 0.2) 

def come_from_zone_1(rtde_c):
        Cerca_Captura1_1 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_1"]]
        Cerca_Captura1_2 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_2"]]
        Home = [math.radians(i) for i in Zonas_1["Home"]]
        rtde_c.moveJ(Cerca_Captura1_2, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura1_1, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Home, 0.5, 0.2)
        time.sleep(1)

def Captura_1(rtde_c):
        Cerca_Captura1_1 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_1"]]
        Cerca_Captura1_2 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_2"]]
        Cerca_Captura1_3 = [math.radians(i) for i in Zonas_1["Cerca_Captura1_3"]]
        # Home = [math.radians(i) for i in Zonas_2["Home"]]
        rtde_c.moveJ(Cerca_Captura1_1, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura1_2, 0.5, 0.2) 
        time.sleep(1) 
        rtde_c.moveJ(Cerca_Captura1_3, 0.5, 0.2) 
        time.sleep(5) 
        rtde_c.moveJ(Cerca_Captura1_2, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura1_1, 0.5, 0.2) 
        time.sleep(1) 
        # rtde_c.moveJ(Home, 0.5, 0.2) 
        # time.sleep(1)

def Captura_2(rtde_c):
        Cerca_Captura2_1 = [math.radians(i) for i in Zonas_1["Cerca_Captura2_1"]]
        Cerca_Captura2_2 = [math.radians(i) for i in Zonas_1["Cerca_Captura2_2"]]
        Cerca_Captura2_3 = [math.radians(i) for i in Zonas_1["Cerca_Captura2_3"]]
        rtde_c.moveJ(Cerca_Captura2_1, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura2_2, 0.5, 0.2) 
        time.sleep(1) 
        rtde_c.moveJ(Cerca_Captura2_3, 0.5, 0.2) 
        time.sleep(5) 
        rtde_c.moveJ(Cerca_Captura2_2, 0.5, 0.2) 
        time.sleep(1)
        rtde_c.moveJ(Cerca_Captura2_1, 0.5, 0.2) 
        time.sleep(1)