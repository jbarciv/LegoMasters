"""
Title: Open Gripper
Description: Basic function for opening gripper
Authors: Micaela Cabrera, Jorge Guijarro
Date: May 21, 2024
"""

import rtde_io
import time

def OpenGripper():
        rtde_io_ = rtde_io.RTDEIOInterface("192.168.56.20")
        rtde_io_.setToolDigitalOut(1, False)
        time.sleep(0.1)
        rtde_io_.setToolDigitalOut(0, True)
        time.sleep(0.1)
        rtde_io_.setToolDigitalOut(0, False)


