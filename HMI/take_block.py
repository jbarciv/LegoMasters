"""
Title: Take block
Description: Basic function for taking a block
Authors: Micaela Cabrera, Jorge Guijarro
Date: May 21, 2024
"""

import time
import math

from open_gripper import OpenGripper
from close_gripper import CloseGripper

def CogePieza(Pieza,rtde_c,rtde_r):
        Zonas = {
                "Cerca_Constr": {"x":-158.39, "y":-249.82, "z":-270},
                "Cerca_Piez": [130,-90.95,-100.17,-78.88,90.02,194.98]
        }        
        OpenGripper()

        Cerca_Piez_radian = [math.radians(i) for i in Zonas["Cerca_Piez"]]
        Pieza_radian = [math.radians(i) for i in Pieza]
        
        rtde_c.moveJ(Cerca_Piez_radian, 1, 0.6) 
        time.sleep(1)
        rtde_c.moveJ(Pieza_radian, 1, 0.6) 
        time.sleep(1) 

        target = rtde_r.getActualTCPPose()
        target[2] -= 0.07
        rtde_c.moveL(target, 0.05, 0.05, True)
        time.sleep(4)
        CloseGripper()
        time.sleep(1)
        target[2] += 0.07
        rtde_c.moveL(target, 0.05, 0.05, True)
        time.sleep(4)
        rtde_c.moveJ(Cerca_Piez_radian, 1, 0.6) 

