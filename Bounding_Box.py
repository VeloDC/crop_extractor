import xml.etree.ElementTree as ET

class Bounding_Box(object):

    def __init__(self, dom_node):
        self.xmin = int(dom_node.findall('xmin')[0].text)
        self.ymin = int(dom_node.findall('ymin')[0].text)
        self.xmax = int(dom_node.findall('xmax')[0].text)
        self.ymax = int(dom_node.findall('ymax')[0].text)
        self.width = self.xmax - self.xmin
        self.height = self.ymax - self.ymin


    def reset_wh(self):
        self.width = self.xmax - self.xmin
        self.height = self.ymax - self.ymin
