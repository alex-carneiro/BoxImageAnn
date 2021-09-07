# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 19:35:51 2021

@author: Alex Carneiro
"""

import cv2

import numpy as np
import pandas as pd

class Interface:
    GROUND_COLOR = 120
    def __init__(self, names, win_name):
        self.names = names
        self.win_name = win_name
        self.last_selected = -1
        self.image = self.create()
    
    def get_image(self):
        return self.image
    
    def get_selected(self):
        return self.last_selected
    
    def set_support(self, obj):
        self.obj = obj
    
    def support(self):
        if 0 <= self.last_selected < len(self.names):
            selected_name = self.names[self.last_selected]
            self.obj.set_label(selected_name, self.last_selected)
        elif self.last_selected == len(self.names):
            self.obj.reset()
            self.obj.set_label(None, None)
        else:
            self.obj.set_label(None, None)
    
    def create_piece(self, name, shape=(50, 400, 3), margin=10, ground=None, text_color=(255, 255, 255)):
        image = np.ones(shape, dtype=np.uint8)
        
        if ground is None:
            image[:] = self.GROUND_COLOR
        else:
            image[:,:] = ground
        h, w = shape[:2]
        h -= margin
        cv2.putText(image, name, (margin, h),
                    cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 2, cv2.LINE_AA)
        
        return image
    
    def create(self, selected=-1, mouse_on=-1):
        self.last_selected = selected
        self.pieces = []
        for i, name in enumerate(self.names):
            if i == self.last_selected and i == mouse_on:
                self.pieces.append(self.create_piece(name.lower(),
                                   ground=(150, 50, 50),
                                   text_color=(0, 255, 255)))
            elif i == self.last_selected:
                self.pieces.append(self.create_piece(name.lower(),
                                   ground=(150, 50, 50)))
            elif i == mouse_on:
                self.pieces.append(self.create_piece(name.lower(),
                                   text_color=(0, 255, 255)))
            else:
                self.pieces.append(self.create_piece(name.lower()))
        
        if mouse_on == len(self.names):
            self.pieces.append(self.create_piece("CLEAR ANNOTATIONS",
                                                 text_color=(0, 255, 255)))
        else:
            self.pieces.append(self.create_piece("CLEAR ANNOTATIONS"))
        
        self.ranges = []
        h_total = 0
        for p in self.pieces:
            h = p.shape[0]
            self.ranges.append((h_total, h_total + h - 1))
            h_total += h
        
        return np.vstack(self.pieces)
    
    def select_label(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, r in enumerate(self.ranges):
                v_min, v_max = r
                if v_min <= y <= v_max:
                    break
            
            self.image = self.create(selected=i)
            self.support()
            
            cv2.imshow(self.win_name, self.image)
        elif event == cv2.EVENT_MOUSEMOVE:
            for i, r in enumerate(self.ranges):
                v_min, v_max = r
                if v_min <= y <= v_max:
                    break
            
            self.image = self.create(selected=self.last_selected, mouse_on=i)
            
            cv2.imshow(self.win_name, self.image)
    		

def save_annotations(annotations, image_filename):
    ann_filename = '.'.join(image_filename.split('.')[:-1]) + '.txt'
    df = pd.DataFrame({0: [ann[0] for ann in annotations],
                       1: [ann[1] for ann in annotations],
                       2: [ann[2] for ann in annotations],
                       3: [ann[3] for ann in annotations],
                       4: [ann[4] for ann in annotations]})
    
    df.to_csv(ann_filename, sep=' ', header=None, index=None)
    
    
    
