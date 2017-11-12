from __future__ import print_function
import yaml
import argparse
import sys
import os
from PIL import Image
import xml.etree.ElementTree as ET
import shutil
import progressbar
from time import sleep
import pickle


dict = {}


class Image_Object():
    name = ""
    pose = ""
    bndbox_x_min = 0.0
    bndbox_y_min = 0.0
    bndbox_x_max = 0.0
    bndbox_y_max = 0.0
    
    def __init__(self, name, pose, x_min, y_min, x_max, y_max):
        self.name = name
        self.pose = pose
        self.bndbox_x_min = x_min
        self.bndbox_y_min = y_min
        self.bndbox_x_max = x_max
        self.bndbox_y_max = y_max

    def __str__(self):
        return "From str method of Test: Name is %s, Pose is %s" % (self.name, self.pose)


def read_config(path):
    global dict
    files = os.listdir(path)
    print("Parsing the XML Files ...")
    for file in files:
        fullname = os.path.join(path, file)
        tree = ET.parse(fullname)
        root = tree.getroot()
        list_obj = []
        file_name = root.find("filename").text.replace('.jpg', '')
        # print(file_name)
        for child in root:
            # print(child.tag)
            if child.tag == "object":
                for step_child in child:
                    # print("***")
                    if step_child.tag == "name":
                        name = step_child.text
                    if step_child.tag == "pose":
                        pose = step_child.text
                    if step_child.tag == "bndbox":
                        for step_step_child in step_child:
                            if step_step_child.tag == "xmin":
                                x_min = float(step_step_child.text)
                            if step_step_child.tag == "ymin":
                                y_min = float(step_step_child.text)
                            if step_step_child.tag == "xmax":
                                x_max = float(step_step_child.text)
                            if step_step_child.tag == "ymax":
                                y_max = float(step_step_child.text)
                        img_obj = Image_Object(name, pose, x_min, y_min, x_max, y_max)
                        if file_name not in dict:
                            dict[file_name] = {}
                            dict[file_name][name] = []
                            dict[file_name][name].append(img_obj)
                        else:
                            if name not in dict[file_name]:
                                dict[file_name][name] = []
                                dict[file_name][name].append(img_obj)
                            else:
                                dict[file_name][name].append(img_obj)
                        # list_obj.append(img_obj)
                    # if step_child.tag == "part":
                        # for step_step_child in step_child:
                            # if step_step_child.tag == "name":
                                # name = step_step_child.text
                            # if step_step_child.tag == "bndbox":
                                # for s_child in step_step_child:
                                    # if s_child.tag == "xmin":
                                        # p_x_min = float(s_child.text)
                                    # if s_child.tag == "ymin":
                                        # y_min = float(s_child.text)
                                    # if s_child.tag == "xmax":
                                        # x_max = float(s_child.text)
                                    # if s_child.tag == "ymax":
                                        # y_max = float(s_child.text)
                                # p_img_obj = Image_Object(name, "", p_x_min, y_min, x_max, y_max)
                                # list_obj.append(p_img_obj)
            # dict[file_name] = list_obj
    print("Completed parsing the XML Files ...")
    # exit(0)


def get_class_labels(path):
    set_dir = path
    all_files = os.listdir(path)
    # print(all_files)
    image_sets = sorted(list(set([filename.replace('.txt', '').strip().split('_')[0] for filename in all_files])))
    image_sets.remove("trainval")
    image_sets.remove("val")
    # print(image_sets)
    # initialize_dict(image_sets)
    # print(dict)
    # exit()
    
def initialize_dict(image_sets):
    global dict
    for x in image_sets:
        dict[x] = {}


def compress_file(path_to_output_images):
    # content = b"Lots of content here"
    print("Compressing images on the Hard Drive ...")
    binary_path = "./Binary_Output/"
    if not os.path.exists(binary_path):
        os.makedirs(binary_path)
    full_path = os.path.join(binary_path, "Assignment_1")
    shutil.make_archive(full_path, 'zip', path_to_output_images)
    print("Done!")


def compress_in_memory(data):
    print("Compressing images in memory ...")
    binary_path = "./Binary_Output/"
    if not os.path.exists(binary_path):
        os.makedirs(binary_path)
    full_path = os.path.join(binary_path, "Assignment_2.bin")
    output_file = open(full_path, "wb")
    for x in data:
        pickle.dump(x, output_file)
    output_file.close()
    print("Done!")


def parse_images(path, type):
    global dict
    print("Parsing Images ...")
    maxsize = 244, 244
    i = 0
    bar = progressbar.ProgressBar(maxval = len(dict), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    j = 0
    list_images = []
    for key, value in dict.items():
        im = Image.open(path + key + ".jpg")
        # print(im.format, im.size, im.mode)
        list = value
        j = j + 1
        bar.update(j)
        sleep(0.1)
        for key1, value1 in value.items():
            list = value1
            for x in list:
                i = i + 1
                x_min = x.bndbox_x_min
                y_min = x.bndbox_y_min
                x_max = x.bndbox_x_max
                y_max = x.bndbox_y_max
                box = (x_min, y_min, x_max, y_max)
                region = im.crop(box)
                # region.thumbnail(maxsize, Image.ANTIALIAS)
                region = region.resize(maxsize, Image.ANTIALIAS)
                if type == "HD":
                    file_name = "".join([x.name, "_", str(i), ".JPEG"])
                    output_path = "./Output_Final/" + key1
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    o_path = os.path.join(output_path, file_name)
                    region.save(o_path, quality = 95)
                    list_images.append(region)
                elif type == "RAM":
                    list_images.append(region)
                    # compress_in_memory(list_images)
    compress_in_memory(list_images)
            # exit()
    bar.finish()


def main():
    global dict
    parser = argparse.ArgumentParser()
    parser.add_argument("type", nargs = "?", choices = ["HD", "RAM"], default = "HD", help = "Type 'HD': To parse images and objects and save it on a Hard Drive \n 'RAM': To parse images and objects in memory and save it as a binary file.")
    args = parser.parse_args()
    if not os.path.exists("./Output"):
        os.makedirs("./Output")
    img_classes_path = "./VOCdevkit/VOC2012/ImageSets/Main/"
    xml_files_path = "./VOCdevkit/VOC2012/Annotations/"
    img_files_path = "./VOCdevkit/VOC2012/JPEGImages/"
    get_class_labels(img_classes_path)
    read_config(xml_files_path)
    if args.type == "HD":
        # exit()
        parse_images(img_files_path, args.type)
        compress_file("./Output")
    elif args.type == "RAM":
        parse_images(img_files_path, args.type)


if __name__ == "__main__":
    sys.exit(main())
