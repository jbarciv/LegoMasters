"""
Title: Build block
Description: Basic function for building a block
Authors: Micaela Cabrera, Jorge Guijarro
Date: May 21, 2024
"""

import rtde_control
import rtde_receive
import time
import math
import rtde_io

from open_gripper import OpenGripper
from close_gripper import CloseGripper

def ConstruyePieza(Pieza,rtde_c,rtde_r):
        Zonas = {
                "Cerca_Piez": [130,-90.95,-100.17,-78.88,90.02,194.98],
                "Cerca_Constr": [264.17, -81.89, -103.30,-84.55,89.78,329.17]
        }        
        
        Cerca_Piez_radian = [math.radians(i) for i in Zonas["Cerca_Piez"]]
        Cerca_Constr_radian = [math.radians(i) for i in Zonas["Cerca_Constr"]]
        Pieza_radian = [math.radians(i) for i in Pieza]
        
        rtde_c.moveJ(Cerca_Constr_radian, 1, 0.6) 
        time.sleep(1)
        rtde_c.moveJ(Pieza_radian, 1, 0.6) 
        time.sleep(1)
        
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
        rtde_c.moveJ(Cerca_Constr_radian, 1, 0.6) 
        time.sleep(2)
        rtde_c.moveJ(Cerca_Piez_radian, 1, 0.6)
        

