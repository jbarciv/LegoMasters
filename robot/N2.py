import rtde_control
import rtde_receive
import time
import math
import rtde_io

from Abrirpinza import OpenGripper
from Cerrarpinza import CloseGripper





    
def ConstruyePieza(Pieza,rtde_c,rtde_r):
        Zonas = {
        "Cerca_Piez": [130,-90.95,-100.17,-78.88,90.02,194.98],
        "Cerca_Constr": [264.17, -82.56, -108.08,-79.10,89.79,329.16]
}        
        
        #Coordenadas a radian
        Cerca_Piez_radian = [math.radians(i) for i in Zonas["Cerca_Piez"]]
        Cerca_Constr_radian = [math.radians(i) for i in Zonas["Cerca_Constr"]]
        Pieza_radian = [math.radians(i) for i in Pieza]
        
        rtde_c.moveJ(Cerca_Constr_radian, 0.5, 0.2) #Posición Cerca_Constr
        time.sleep(1)
        rtde_c.moveJ(Pieza_radian, 0.5, 0.2) #Posición Pieza Escogida
        time.sleep(1) #Pausa y configuramos movimiento vertical
        
        target = rtde_r.getActualTCPPose()
        time.sleep(1)
        speed = [0, 0, -0.050, 0, 0, 0]
        rtde_c.moveUntilContact(speed)
        target_2 = rtde_r.getActualTCPPose()
        target_2[2] -= 0.005
        rtde_c.moveL(target_2, 0.05, 0.05, True)       
        time.sleep(4)
        OpenGripper()
        time.sleep(1)
        rtde_c.moveL(target, 0.05, 0.05, True)
        time.sleep(4)
        rtde_c.moveJ(Cerca_Constr_radian, 0.5, 0.2) #Posición Cerca_Constr
        time.sleep(1)
        rtde_c.moveJ(Cerca_Piez_radian, 0.5, 0.2) #Posición Cerca_Constr
        
def ConstruyePiezaCentro(Pieza,rtde_c,rtde_r):
        Zonas = {
        "Cerca_Piez": [130,-90.95,-100.17,-78.88,90.02,194.98],
        "Cerca_Constr": [264.17, -82.56, -108.08,-79.10,89.79,329.16]
}        
        
        #Coordenadas a radian
        Cerca_Piez_radian = [math.radians(i) for i in Zonas["Cerca_Piez"]]
        Cerca_Constr_radian = [math.radians(i) for i in Zonas["Cerca_Constr"]]
        Pieza_radian = [math.radians(i) for i in Pieza]
        
        rtde_c.moveJ(Cerca_Constr_radian, 0.25, 0.1) #Posición Cerca_Constr
        time.sleep(1)
        rtde_c.moveJ(Pieza_radian, 0.15, 0.1) #Posición Pieza Escogida
        time.sleep(1) #Pausa y configuramos movimiento vertical
        target_1 = rtde_r.getActualTCPPose()
        time.sleep(1)
        target_1[2]-=0.06
        rtde_c.moveL(target_1, 0.15, 0.1, True)      
        time.sleep(4)
        OpenGripper() #La pieza se baja a una zona aproximada
        time.sleep(1)
        target_1[2]+=0.06
        rtde_c.moveL(target_1, 0.15, 0.1, True)
        time.sleep(4)
        CloseGripper() #Se sube un poco y se vuelve a bajar cerrada para ajustar
        time.sleep(4)
        speed = [0, 0, -0.050, 0, 0, 0]
        rtde_c.moveUntilContact(speed)
        target_2 = rtde_r.getActualTCPPose()
        target_2[2] -= 0.005
        rtde_c.moveL(target_2, 0.25, 0.5, True)       
        time.sleep(4)
        rtde_c.moveL(target_2, 0.25, 0.05, True)
        time.sleep(4)
        rtde_c.moveJ(Cerca_Constr_radian, 0.15, 0.1) #Posición Cerca_Constr
        rtde_c.moveJ(Cerca_Piez_radian, 0.15, 0.1) #Posición Cerca_Constr
        
       
