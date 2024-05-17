import rtde_control
import rtde_receive
import time
import math


from N1 import CogePieza
from N2 import ConstruyePieza
from N2 import ConstruyePiezaCentro

rtde_receive_ = rtde_receive.RTDEReceiveInterface("192.168.56.20")
rtde_c = rtde_control.RTDEControlInterface("192.168.56.20")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.20")

Piezas = {
        "P1": {
        "Joints": [166,-109.71,-87.73,-72.22,88.69,232.80],
        "Color": "yellow" }, 
        "P2": {
        "Joints": [162.94,-96.7,-104.34,-68.56,88.67,229.74],
        "Color": "yellow"},
        "P3": {
        "Joints": [158.6,-84.55,-116.66,-68.29,88.68,225.43],
        "Color": "white"},
        "P4": {
        "Joints": [151.67,-72.66,-125.74,-70.96,88.68,218.52],
        "Color": "white"},
        "P5": {
         "Joints": [140.94,-63.69,-130.81,-74.66,88.78,207.81],
        "Color": "green"},
        "P6": {
        "Joints": [155.25,-121.61,-69.88,-77.94,88.79,222.06],
        "Color": "orange"},
        "P7": {
        "Joints": [150.94,-110.24,-87.12,-71.99,88.8,217.74],
        "Color": "yellow"},
        "P8": {
        "Joints": [145.01,-100.37,-100.17,-68.7,88.84,211.8],
        "Color": "white"},
        "P9": {
        "Joints": [137.38,-92.68,-108.96,-67.45,88.92,204.19],
        "Color": "white"},
        "P10": {
        "Joints": [127.43,-87.52,-114.19,-67.23,89.06,194.24],
        "Color": "green"},
        "P11": {
        "Joints": [146.61,-138.02,-41.53,-89.72,88.91,213.44],
        "Color": "blue" },
        "P12": {
        "Joints": [141.74,-125.37,-63.82,-79.99,88.94,208.55],
        "Color": "red" },
        "P13": {
        "Joints": [135.67,-116.49,-78.05,-74.53,89.01,202.46],
        "Color": "red" },
        "P14": {
        "Joints": [128.49,-110.31,-87.18,-71.47,89.11,195.28],
        "Color": "red" },
        "P15": {
        "Joints": [119.72,-116.35,-103.33,-49.17,89.33,186.5],
        "Color": "green" },
        "P16": {
        "Joints": [128.55,-137.1,-43.33,-88.52,89.18,195.37],
        "Color": "none" },
        "P17": {
        "Joints": [122.03,-130.17,-55.77,-82.94,89.28,188.83],
        "Color": "none" },
        "P18": {
        "Joints": [114.45,-126.29,-62.44,-80.06,89.42,181.25],
        "Color": "blue"},
        
        "P19": [121.86,-67.94,-128.75,-72.18,89.11,188.71],
        "P20": [111.79,-96.26,-105.19,-67.31,89.39,178.59],
        "P21": [107.06,-120.3,-72.26,-76.17,89.55,173.85]
}

Zonas = {
        
        "Z1": [252.42,-91.07,-110.05,-68.63,89.88,227.38],
        "Z2": [258.87, -85.58, -115.84, -67.83, 89.84, 233.85],
        "Z3": [265.90,-80.54,-119.61,-69.60,89.81,240.88],
        "Z4": [273.91,-75.74,-123.22,-70.82,89.78,248.89],
        "Z5": [273.45,-84.41,-116.36,-68.98,89.80,338.42],
        "Z6": [273.13,-91.36,-110.04,-68.35,89.82,338.09],
        "Z7": [272.83,-98.82,-101.78,-69.14,89.84,337.79],
        "Z8": [254.23,-97.38,-103.19,-69.18,89.89,319.18],
        "Z9": [255.69,-103.64,-95.84,-70.27,89.90,320.63],
        "Z10": [272.78,-100.13,-99.93,-69.7,89.85,337.73],
        "Z12": [266.9,-102.43,-97.34,-70.05,89.91,241.83],
        "Z11": [261.68, -106.26, -92.37, -71.20, 89.93,236.61],
        "Z13": [260.48, -93.02, -107.93, -69.64, 89.73,325.56],
        "Z14": [266.43,-88.34, -112.75,-68.67,89.83,331.39],
        "Z15": [266.79,-94.90,-105.97,-68.88,89.95,331.74],
        "Z16": [261.15,-98.6,-101.76,-69.40,89.88,326.10]            
}


#Selección tamaño construcción
numero_piezas = int(input("Selecciona el número de piezas de la construcción: "))

#Lista para almacenar piezas/zonas
piezas_seleccionadas = []
zonas_seleccionadas = []

#Solicitar piezas/zonas
for i in range(numero_piezas):
    nombre_pieza = input("Selecciona la pieza que deseas coger (P1, P2, P3...): ")
    nombre_zona = input("Selecciona la zona donde se desea construir (Z1, Z2, Z3...): ")
    
    piezas_seleccionadas.append(nombre_pieza)
    zonas_seleccionadas.append(nombre_zona)

#Verificación de piezas/zonas válidas
for nombre_pieza, nombre_zona in zip(piezas_seleccionadas, zonas_seleccionadas):
    if nombre_pieza in Piezas:
        pieza = Piezas[nombre_pieza]["Joints"]
        
    else:
        print("La pieza seleccionada no está en la lista.")

    if nombre_zona in Zonas:
        zona = Zonas[nombre_zona]
    else:
        print("La zona seleccionada no está en la lista.")

#Ejecución del movimiento
    if nombre_pieza in Piezas and nombre_zona in Zonas:
        CogePieza(pieza, rtde_c, rtde_r)
        if nombre_zona in ["Z13", "Z14", "Z15", "Z16"]:
                ConstruyePiezaCentro(zona, rtde_c, rtde_r)
        else:
                ConstruyePieza(zona, rtde_c, rtde_r)
     
rtde_c.moveJ([1.59, -1.538, -0.06,-1.56,0.014,1.18], 0.15, 0.1)
        
#Revisar Z6,Z7, Z9 (oRDEN MAL?), Z10, Z11 (REPETIDA), Z12
 

