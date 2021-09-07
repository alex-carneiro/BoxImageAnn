# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 15:48:37 2021

@author: Alex Carneiro
"""

import cv2

from drawing import BoxDrawing
from labels import Interface, save_annotations

import os
import argparse
from glob import glob

WIN_NAME = 'Image'
WIN_AUX = 'Select the name'

if __name__ == '__main__':
    # Set the input command line arguments
    parser = argparse.ArgumentParser(description='Read all images from folder')
    parser.add_argument('--folder', default='.',
                        help='folder to be read')
    
    parser.add_argument('--extensions', default=['jpg', 'jpeg', 'png', 'bmp'],
                        type=list, help='list of accepted extensions')
    
    parser.add_argument('--names', default='names.txt',
                        help='file to be read with the labels')
    
    parser.add_argument('--max_side', default=None,
                        type=int, help='maximum size for image side')
    
    args = parser.parse_args()
    folder_path = args.folder
    
    # Get the paths for all images inside --folder
    images_paths = []
    for ext in args.extensions:
        images_paths += glob(os.path.join(folder_path, '*.' + ext))
    
    # Draw boxes and save the coordinates
    draw = BoxDrawing()
    draw.set_win_name(WIN_NAME)
    
    with open(args.names, 'r') as names_file:
        names = names_file.read().splitlines()
    
    names_interface = Interface(names, WIN_AUX)
    
    for image_path in images_paths:
        image = cv2.imread(image_path)
        
        if args.max_side is not None:
            rate = args.max_side / max(image.shape[:2])
            image = cv2.resize(image, None, fx=rate, fy=rate,
                               interpolation=cv2.INTER_LINEAR)
        
        cv2.namedWindow(WIN_AUX)
        cv2.setMouseCallback(WIN_AUX, names_interface.select_label)
        aux_image = names_interface.get_image()
        selected_label_id = names_interface.get_selected()
        cv2.imshow(WIN_AUX, aux_image)
        
        names_interface.set_support(draw)
        draw.set_image(image)
        draw.reset()
        names_interface.support()
        cv2.namedWindow(WIN_NAME)

        cv2.setMouseCallback(WIN_NAME, draw.make_box)
        cv2.imshow(WIN_NAME, image)
        
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        
        save_annotations(draw.get_annotations(), image_path)
    
    cv2.destroyAllWindows()
