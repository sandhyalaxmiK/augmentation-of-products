import numpy as np
import os
import xml.etree.ElementTree as ET
import pickle
import sys
import cv2
tree = ET.parse('frame_000001_9915.xml')
root=tree.getroot()
for elem in root.findall(".//object/.."):
	for attr in elem.findall("./object"):
		for sub_attr in attr:
			elem.append(sub_attr)
		elem.remove(attr)
	for attr in elem.findall("./item"):
		attr.tag='object'
tree.write("ggg.xml")



		
