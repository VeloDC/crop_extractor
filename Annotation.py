import os
import xml.etree.ElementTree as ET
from Object import Object

from PIL import Image, ImageDraw


class Annotation(object):


    def __init__(self, annotation_file):
        self.annotation_file = annotation_file
        xml_tree = ET.parse(annotation_file)
        root = xml_tree.getroot()
        self.folder = root.findall('folder')[0].text
        self.filename = root.findall('filename')[0].text
        size = root.findall('size')[0]
        self.width = int(size.findall('width')[0].text)
        self.height = int(size.findall('height')[0].text)
        self.objects = self.register_objects(root.findall('object'))



    def register_objects(self, dom_nodes):
        objects = []
        for dom_node in dom_nodes:
            objects.append(Object(dom_node,self))
        return objects


    def scale_bboxes(self, p):
        for obj in self.objects:
            obj.scale_bbox(p)


    def get_obj_with_crop(self, image, scale=False, p=0):
        objects_with_crops = []
        for obj in self.objects:
                obj.generate_crop(image, scale=scale, p=p)
                objects_with_crops.append(obj)
        return objects_with_crops


    def save_crops(self, image, target_folder, ext='JPEG', scale=False, p=0):
        objects_with_crops = self.get_obj_with_crop(image, scale, p)
        crop_count = 0
        for obj_with_crops in objects_with_crops:
            if ((self.folder == obj_with_crops.name)):
                dest_folder = target_folder + self.folder + '/'
                os.system('mkdir -p ' + dest_folder)
            else:
                dest_folder = target_folder + obj_with_crops.name + '/'
                os.system('mkdir -p ' + dest_folder)
            try:
                for crop in obj_with_crops.crops:
                    filename = self.filename + '_crop' + str(crop_count) + '.' + ext
                    crop.save(dest_folder + filename)
                    crop_count += 1
            except SystemError:
                #bad bounding box
                pass
        return len(objects_with_crops)
