import rtde_control
import rtde_receive
import time
import math
import rtde_io



from Abrirpinza import OpenGripper
from Cerrarpinza import CloseGripper




def CogePieza(Pieza,rtde_c,rtde_r):
        Zonas = {
        "Cerca_Constr": {"x":-158.39, "y":-249.82, "z":-270},
        "Cerca_Piez": [130,-90.95,-100.17,-78.88,90.02,194.98]
}        
        OpenGripper()
        #Coordenadas a radian
        Cerca_Piez_radian = [math.radians(i) for i in Zonas["Cerca_Piez"]]
        Pieza_radian = [math.radians(i) for i in Pieza]
        
        rtde_c.moveJ(Cerca_Piez_radian, 0.5, 0.2) #Posición Cerca_Constr
        time.sleep(1)
        rtde_c.moveJ(Pieza_radian, 0.5, 0.2) #Posición Pieza Escogida
        time.sleep(1) #Pausa y configuramos movimiento vertical
        
        target = rtde_r.getActualTCPPose()
        target[2] -= 0.07
        rtde_c.moveL(target, 0.05, 0.05, True)
        time.sleep(4)
        CloseGripper()
        time.sleep(1)
        target[2] += 0.07
        rtde_c.moveL(target, 0.05, 0.05, True)
        time.sleep(4)
        rtde_c.moveJ(Cerca_Piez_radian, 0.5, 0.2) #Posición Cerca_Constr
#7,11, 13, 17se da. 16 está mal puesta4

