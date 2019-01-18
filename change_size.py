# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 08:52:20 2018
-----savename is dirname[-4:]+filename-----
@author: zxb
"""
import os
import cv2
import xml.etree.ElementTree as ET
from lxml import etree

#savexml
class GEN_Annotations:
    def __init__(self, filename):
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = "VOC2007"

        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename

        child3 = etree.SubElement(self.root, "source")
        # child2.set("database", "The VOC2007 Database")
        child4 = etree.SubElement(child3, "annotation")
        child4.text = "PASCAL VOC2007"
        child5 = etree.SubElement(child3, "database")

        child6 = etree.SubElement(child3, "image")
        child6.text = "flickr"
        child7 = etree.SubElement(child3, "flickrid")
        child7.text = "35435"

        # root.append( etree.Element("child1") )
        # root.append( etree.Element("child1", interesting="totally"))
        # child2 = etree.SubElement(root, "child2")

        # child3 = etree.SubElement(root, "child3")
        # root.insert(0, etree.Element("child0"))

    def set_size(self,witdh,height,channel):
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(witdh)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "channel")
        channeln.text = str(channel)
    def savefile(self,filename):
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')
    def add_pic_attr(self,label,x,y,w,h,diffi_=0):
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        diffi = etree.SubElement(object, "difficult")
        diffi.text = str(diffi_)

        truncated_ = etree.SubElement(object, "truncated")
        truncated_.text = str(0)

        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(x)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(y)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(x+w)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(y+h)

#change_size
#TARGET_PIC_SIZE = (720,1280)  #(1080,1920)
scale = 720/1080
def multi_scale(pic_path, xml_path, counter, path_limage = None):
    global scale
    path_list = pic_path.split('\\')
    dir_path = os.path.dirname(os.path.dirname(pic_path))
    print(dir_path)
    #print(path_list)
    im = cv2.imread(pic_path)
    if im is None:
        return
    if im.shape[1]<1 or im.shape[0]<1:
        return
    tree = ET.parse(xml_path)
    file_objs = tree.findall('filename')

    filetext = file_objs[0].text
    objs = tree.findall('object')

    objs_diffi = tree.findall('object/difficult')
    if len(objs_diffi)==0:
        print(xml_path, objs_diffi, len(objs_diffi))

    bbox_list = []
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        x1 = int(bbox.find('xmin').text)
        y1 = int(bbox.find('ymin').text)
        x2 = int(bbox.find('xmax').text)
        y2 = int(bbox.find('ymax').text)
        bbox_list.append((x1,y1,(x2-x1),(y2-y1),name))

    if bbox_list:
        bbox_list1 = []
        im = cv2.imread(pic_path)
        im = cv2.resize(im, (1280, 720),interpolation=cv2.INTER_CUBIC)
        for (x,y,w,h,name) in bbox_list:
            x_ = int(x * scale)
            y_ = int(y * scale)
            w_ = int(w * scale)
            h_ = int(h * scale)
            name = name
            bbox_list1.append((x_,y_,w_,h_,name))

        save_file_name = '%s' % (path_list[-1][0:-4])
        dir_name = '%s' % (dir_path.split('\\')[-1][-4:])
        anno = GEN_Annotations(save_file_name + '.jpg')
        anno.set_size(1280, 720, 3)
        for (x, y, w, h,name) in bbox_list1:
            anno.add_pic_attr(name, x, y, w, h)
            anno.savefile(save_xml_path + dir_name + save_file_name + '.xml')
            cv2.imwrite(save_pic_path + dir_name +  save_file_name + '.jpg', im)

if __name__ == '__main__':
    # save file path
    save_xml_path = r'\\192.168.55.73\Team-CV\1227_mod_new1\Annotations/'
    save_pic_path = r'\\192.168.55.73\Team-CV\1227_mod_new1\JPEGImages/'

    os.makedirs(save_xml_path, exist_ok=True)
    os.makedirs(save_pic_path, exist_ok=True)
    # file path
    path = r'\\192.168.55.73\Team-CV\1227_mod_old'
    pic_files = [os.path.join(rootdir, file) for rootdir, _, files in os.walk(path) for file in files if
             (file.endswith('.jpg'))]
    for i,pic_file in enumerate(pic_files):
        xml_file = pic_file.replace('JPEGImages','Annotations').replace('.jpg','.xml')
        multi_scale(pic_file, xml_file, i)

