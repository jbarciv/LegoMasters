import pyrealsense2 as rs
import numpy as np
import cv2
import glob
import os

pipe = rs.pipeline()
cfg  = rs.config()

cfg.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 30)
cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)

pipe.start(cfg)

images_path = "./images"
if not os.path.exists(images_path):
    os.makedirs(images_path)
    print(f"Folder '{images_path}' created.")
else:
    pass
images = glob.glob("images/*.png")
img =[]
for image in images:
    img.append(int(image[7:-4]))
img.sort()
print(img)
num = img[-1] + 1
print(num)

while True:
    frame = pipe.wait_for_frames()
    
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,
                                     alpha = 0.5), cv2.COLORMAP_JET)

    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('rgb', color_image)
    cv2.imshow('depth', depth_cm)

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        image_path = 'images/' + str(num) + '.png'
        cv2.imwrite('images/' + str(num) + '.png', color_image)
        # height, width, channels = color_image.shape
        # print(height, width, channels)
        print(color_image.shape[::-1])
        if cv2.imread(image_path) is None:
            print("error in saving!")
            continue
        print("Image: ", num, "saved!")
        num += 1

    if cv2.waitKey(1) == ord('q'):
        break

pipe.stop()