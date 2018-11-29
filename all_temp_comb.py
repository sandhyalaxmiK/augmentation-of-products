#################################################
###                                           ###
### This program places the 11 object          ###
### permutations in order with width          ###
###											  ###
#################################################


import os
import random
import itertools
import json
import itertools
import sys

import numpy as np
import cv2


os.environ["CUDA_VISIBLE_DEVICES"]="1"
import save
'''
# read json and get the objects
def readJson(sngl_prod,img):
	class_list = []
	obj = []
	class_name ={}
	data  = json.load(open('./dataset/json/'+sngl_prod.split('.')[0]+'.json'))
	for ann in data['annotation']['object']:
		if ann['name'] != "726165651054":
			class_list.append(ann['name'])
			xmin = int(ann['bndbox']['xmin'])
			ymin = int(ann['bndbox']['ymin'])
			xmax = int(ann['bndbox']['xmax'])
			ymax = int(ann['bndbox']['ymax'])
			obj.append(img[ymin:ymax,xmin:xmax])
	class_list.append("726165651054")
	return obj,class_list
'''

#blur the boarders
def blurring(mask,xmin,ymin,xmax,ymax):
	for i in range(50):
		mask[ymin-2:ymin+2,xmin-2:xmax+2] = cv2.blur(mask[ymin-2:ymin+2,xmin-2:xmax+2],(5,5))  #upper side
		mask[ymin-2:ymax+2,xmin-2:xmin+2] = cv2.blur(mask[ymin-2:ymax+2,xmin-2:xmin+2],(5,5))  #left side
		mask[ymax-2:ymax+2,xmin-2:xmax+2] = cv2.blur(mask[ymax-2:ymax+2,xmin-2:xmax+2],(5,5))  #lower side
		mask[ymin-2:ymax+2,xmax-2:xmax+2] = cv2.blur(mask[ymin-2:ymax+2,xmax-2:xmax+2],(5,5))  #right side

		mask[ymin-2:ymin+2,xmin-2:xmax+2] = cv2.medianBlur(mask[ymin-2:ymin+2,xmin-2:xmax+2],5)  #upper side
		mask[ymin-2:ymax+2,xmin-2:xmin+2] = cv2.medianBlur(mask[ymin-2:ymax+2,xmin-2:xmin+2],5)  #left side
		mask[ymax-2:ymax+2,xmin-2:xmax+2] = cv2.medianBlur(mask[ymax-2:ymax+2,xmin-2:xmax+2],5)  #lower side
		mask[ymin-2:ymax+2,xmax-2:xmax+2] = cv2.medianBlur(mask[ymin-2:ymax+2,xmax-2:xmax+2],5)
	return mask


#placing the products in a background image
def placing(comb_obj,class_names):
	mask = cv2.imread('./background2.jpg')
	ann = {}
	new_xmin , new_ymin , new_xmax , new_ymax , new_class = [] , [] , [] , [] , []
	for index,prod in enumerate(comb_obj):
		if index == 0:
			# for placing the first product in the image
			new_xmin.append(250)
			new_xmax.append(prod.shape[1]+ new_xmin[index])
			new_ymin.append(random.randint(150,300))#-prod.shape[0]))
			new_ymax.append(prod.shape[0] + new_ymin[index])
			mask[new_ymin[index]:new_ymax[index] , new_xmin[index]:new_xmax[index]] = prod
			new_class.append(class_names[index])
		else:
			if new_xmax[index-1]+10+prod.shape[1] >= 1030:
				break
			new_xmin.append(new_xmax[index-1]+10)
			new_xmax.append(new_xmin[index]+prod.shape[1])
			new_ymin.append(random.randint(150,300))#-prod.shape[0]))
			new_ymax.append(prod.shape[0] + new_ymin[index])
			mask[new_ymin[index]:new_ymax[index] , new_xmin[index]:new_xmax[index]] = prod
			new_class.append(class_names[index])
		#blur the boarders
		#mask = blurring(mask,new_xmin[index],new_ymin[index],new_xmax[index],new_ymax[index])
	ann['xmin'],ann['ymin'],ann['xmax'],ann['ymax'] = new_xmin , new_ymin , new_xmax , new_ymax
	ann['class'] = new_class
	#save both image and annotations
	#cv2.namedWindow('img',cv2.WINDOW_NORMAL)
	#cv2.imshow('img',mask)
	#cv2.waitKey(0)
	global number
	save.save_both(mask,ann,str(number)) #filename.split('.')[0]+'_'
	number  += 1
	print(number)
	#save_img(mask,index)
	#save_ann(ann,index)	
	return #mask,ann



#reading apollo templates
def get_prod_roi(foldername):
	dir_list = os.listdir(foldername+'/img/')
	#print(dir_list)
	prod_set = []
	for temp in dir_list:
		template = cv2.imread(foldername+'/img/'+temp)
		#print(temp)
		temp_ann = json.load(open(foldername+'/ann/'+temp.split('.')[0]+'.json'))
		temp_ann_box = temp_ann['annotation']['object']['bndbox']
		temp_xmin,temp_ymin = int(temp_ann_box['xmin']),int(temp_ann_box['ymin'])
		temp_xmax,temp_ymax = int(temp_ann_box['xmax']),int(temp_ann_box['ymax'])
		cropped = template[temp_ymin:temp_ymax , temp_xmin:temp_xmax]
		prod_set.append(cropped)
	temp_ann = json.load(open(foldername+'/ann/'+temp.split('.')[0]+'.json'))
	prod_set_class = temp_ann['annotation']['object']['name']
	return prod_set,prod_set_class
		


'''	
#Read the image directory
if __name__ == '__main__':
	products = [f for f in os.listdir('./dataset/img/') if f.endswith('.jpg')]
	number = 1
	newset  = apollo_roi()
	for apollo in newset:
		for sngl_prod in products:
			img = cv2.imread('./dataset/img/'+sngl_prod)
			obj,class_list = readJson(sngl_prod,img)
			obj.append(apollo)
			img_combo = list(itertools.permutations(obj,7))
			class_combo = list(itertools.permutations(class_list,7))
			choices = random.sample(range(0,len(img_combo)),50)
			for i in choices:
				placing(img_combo[i],class_combo[i],sngl_prod)
			#for obj_list,class_names in zip(img_combo,class_combo):
			#	placing(obj_list,class_names,sngl_prod)
		del obj[-1]

'''		
if __name__ == '__main__':
	all_prod_roi = []
	all_prod_class = []
	number = 1
	for folder in [f for f in os.listdir('./sk_1/') if os.path.isdir('./sk_1/'+f)]:
		print(folder)
		prod_set , prod_set_class = get_prod_roi('./sk_1/'+folder)
		all_prod_roi.append(prod_set)
		all_prod_class.append(prod_set_class)
		
	for first_prod_temp in all_prod_roi[0]:
		#print(all_prod_class[0])
		#sys.exit(0)
		for i in range(max([len(sub_array) for sub_array in all_prod_roi])):
			obj = []
			obj.append(first_prod_temp)
			for sub_array in all_prod_roi[1:]:
				obj.append(random.choice(sub_array))
			
			img_combo = list(itertools.permutations(obj,11))
			class_combo = list(itertools.permutations(all_prod_class,11))
			
			choices = random.sample(range(0,len(img_combo)),100)
			for i in choices:
				placing(img_combo[i],class_combo[i])
		
	
	
	
	
	
