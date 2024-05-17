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
        speed = [0, 0, -0.010, 0, 0, 0]
        rtde_c.moveUntilContact(speed)
        target_2 = rtde_r.getActualTCPPose()
        target_2[2] -= 0.0045
        rtde_c.moveL(target_2, 0.01, 0.01, True)       
        time.sleep(2)
        OpenGripper()
        time.sleep(2)
        rtde_c.moveL(target, 0.01, 0.01, True)
        time.sleep(2)
        rtde_c.moveJ(Cerca_Constr_radian, 0.5, 0.2) #Posición Cerca_Constr
        time.sleep(2)
        rtde_c.moveJ(Cerca_Piez_radian, 0.5, 0.2) #Posición Cerca_Constr
        

