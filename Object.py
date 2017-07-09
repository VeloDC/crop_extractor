import xml.etree.ElementTree as ET
import math
import random
import copy

from Bounding_Box import Bounding_Box

class Object(object):

    def __init__(self, dom_node, annotation):
        self.name = dom_node.findall('name')[0].text
        self.original_bounding_box = Bounding_Box(dom_node.findall('bndbox')[0])
        self.bounding_box = None
        self.annotation = annotation
        self.crops = []
        self.reset_bbox()


    def reset_bbox(self):
        self.bounding_box = copy.deepcopy(self.original_bounding_box)


    def generate_crop(self, image, scale=False, p=0.1):
        if scale:
            self.scale_bbox(p)
        self.crops.append(image.crop((self.bounding_box.xmin,self.bounding_box.ymin,self.bounding_box.xmax,self.bounding_box.ymax)))
        self.reset_bbox()


    def scale_bbox(self, p):
        x_abs_disp = int(self.bounding_box.width * p)
        y_abs_disp = int(self.bounding_box.height * p)
        self.bounding_box.reset_wh()
        self.recompute_bbox(self.bounding_box.xmin - x_abs_disp,
                            self.bounding_box.xmax + x_abs_disp,
                            self.bounding_box.ymin - y_abs_disp,
                            self.bounding_box.ymax + y_abs_disp)


    def translate_bbox(self, x_abs_disp, y_abs_disp):
        self.recompute_bbox(self.bounding_box.xmin + x_abs_disp,
                            self.bounding_box.xmax + x_abs_disp,
                            self.bounding_box.ymin + y_abs_disp,
                            self.bounding_box.ymax + y_abs_disp)


    def recompute_bbox(self,xmin,xmax,ymin,ymax):
        self.bounding_box.xmin = xmin
        self.bounding_box.xmax = xmax
        self.bounding_box.ymin = ymin
        self.bounding_box.ymax = ymax
        self.bounding_box.reset_wh()
        if self.bounding_box.xmin < 0:
            self.bounding_box.xmin = 0
        if self.bounding_box.ymin < 0:
            self.bounding_box.ymin = 0
        if self.bounding_box.xmax > self.annotation.width:
            self.bounding_box.xmax = self.annotation.width
        if self.bounding_box.ymax > self.annotation.height:
            self.bounding_box.ymax = self.annotation.height
