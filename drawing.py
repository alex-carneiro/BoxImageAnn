# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 18:04:19 2021

@author: Alex Carneiro
"""

import cv2

class BoxDrawing:
    def __init__(self):
        self.ref_pt = []
        self.cropping = False
        self.win_name = 'Image'
        self.box_color = (0, 255, 0)
        self.label = None
        self.label_id = None
        self.points = []
        self.annotations = []
    
    def set_image(self, image):
        self.image = image.copy()
        self.original_image = image.copy()
    
    def set_win_name(self, win_name):
        self.win_name = win_name
    
    def set_box_color(self, box_color):
        self.box_color = box_color
    
    def set_label(self, label, label_id):
        self.label = label
        self.label_id = label_id
        if label is not None:
            print('INFO: Next annotation is a', label)
    
    def get_label(self):
        return self.label, self.label_id
    
    def get_annotations(self):
        return self.annotations
    
    def reset(self):
        self.ref_pt = []
        self.cropping = False
        self.win_name = 'Image'
        self.box_color = (0, 255, 0)
        self.image = self.original_image.copy()
        self.label = None
        self.label_id = None
        self.points = []
        self.annotations = []
        cv2.imshow(self.win_name, self.image)
    
    def make_box(self, event, x, y, flags, param):
        if self.label is not None:
        	if event == cv2.EVENT_LBUTTONDOWN:
        		self.ref_pt = [(x, y)]
        		self.cropping = True
        	elif self.cropping and event == cv2.EVENT_MOUSEMOVE:
        		image_aux = self.image.copy()
        		x0, y0 = self.ref_pt[0]
        		margin = 10
        		cv2.rectangle(image_aux, self.ref_pt[0], (x, y),
                          self.box_color, 2)
        		cv2.putText(image_aux, self.label, (x0, y0 - margin),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        		cv2.imshow(self.win_name, image_aux)
        	elif event == cv2.EVENT_LBUTTONUP:
        		self.ref_pt.append((x, y))
        		self.cropping = False
        		x0, y0 = self.ref_pt[0]
        		margin = 10
        		cv2.rectangle(self.image, self.ref_pt[0], self.ref_pt[1],
                      self.box_color, 2)
        		cv2.putText(self.image, self.label, (x0, y0 - margin),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        		cv2.imshow(self.win_name, self.image)
            
        		h, w = self.image.shape[:2]
        		p = self.ref_pt[0] + self.ref_pt[1]
        		self.points.append(p)
        		ann = (self.label_id, (p[2] + p[0])/(2*w), (p[3] + p[1])/(2*h), (p[2] - p[0])/w, (p[3] - p[1])/h)
        		self.annotations.append(ann)
    