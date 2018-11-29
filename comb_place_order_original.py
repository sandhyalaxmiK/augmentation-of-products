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
import os
import itertools
import sys

import numpy as np
import cv2



import save

# read json and get the objects
def readJson(sngl_prod,img):
	class_list = []
	obj = []
	class_name ={}
	data  = json.load(open('./dataset/json/'+sngl_prod.split('.')[0]+'.json'))
	for ann in data['annotation']['object']:
		xmin = int(ann['bndbox']['xmin'])
		ymin = int(ann['bndbox']['ymin'])
		xmax = int(ann['bndbox']['xmax'])
		ymax = int(ann['bndbox']['ymax'])
		class_list.append(ann['name'])
		obj.append(img[ymin:ymax,xmin:xmax])
		'''print('the class_list is',class_list)
		print('the obj is',obj)'''              
	return obj,class_list


#blur the boarders
def blurring(mask,xmin,ymin,xmax,ymax):
	for i in range(50):
		mask[ymin-10:ymin+10,xmin-10:xmax+10] = cv2.blur(mask[ymin-10:ymin+10,xmin-10:xmax+10],(5,5))  #upper side
		mask[ymin-10:ymax+10,xmin-10:xmin+10] = cv2.blur(mask[ymin-10:ymax+10,xmin-10:xmin+10],(5,5))  #left side
		mask[ymax-10:ymax+10,xmin-10:xmax+10] = cv2.blur(mask[ymax-10:ymax+10,xmin-10:xmax+10],(5,5))  #lower side
		mask[ymin-10:ymax+10,xmax-10:xmax+10] = cv2.blur(mask[ymin-10:ymax+10,xmax-10:xmax+10],(5,5))  #right side

		mask[ymin-10:ymin+10,xmin-10:xmax+10] = cv2.medianBlur(mask[ymin-10:ymin+10,xmin-10:xmax+10],5)  #upper side
		mask[ymin-10:ymax+10,xmin-10:xmin+10] = cv2.medianBlur(mask[ymin-10:ymax+10,xmin-10:xmin+10],5)  #left side
		mask[ymax-10:ymax+10,xmin-10:xmax+10] = cv2.medianBlur(mask[ymax-10:ymax+10,xmin-10:xmax+10],5)  #lower side
		mask[ymin-10:ymax+10,xmax-10:xmax+10] = cv2.medianBlur(mask[ymin-10:ymax+10,xmax-10:xmax+10],5)
	return mask


#placing the products in a background image
def placing(comb_obj,class_names,filename):
	mask = cv2.imread('./background2.jpg')
	ann = {}
	a_list = []
        
	new_xmin , new_ymin , new_xmax , new_ymax , new_class = [] , [] , [] , [] , []
	for index,prod in enumerate(comb_obj):
		if index == 0:
			#product_shapes = []
			#products_s=products_shapes.append(prod.shape)
			a_list.append(tuple((prod.shape)))
			print('the product shape is',a_list)
			# for placing the first product in the image
			new_xmin.append(250)
			new_xmax.append(prod.shape[1]+ new_xmin[index])
			new_ymin.append(random.randint(150,320))#-prod.shape[0]))
			new_ymax.append(prod.shape[0] + new_ymin[index])
			mask[new_ymin[index]:new_ymax[index] , new_xmin[index]:new_xmax[index]] = prod
			new_class.append(class_names[index])
		else:
			new_xmin.append(new_xmax[index-1]+10)
			new_xmax.append(new_xmin[index]+prod.shape[1])
			new_ymin.append(random.randint(150,320))#-prod.shape[0]))
			new_ymax.append(prod.shape[0] + new_ymin[index])
			mask[new_ymin[index]:new_ymax[index] , new_xmin[index]:new_xmax[index]] = prod
			new_class.append(class_names[index])
		#blur the boarders
		#mask = blurring(mask,new_xmin[index],new_ymin[index],new_xmax[index],new_ymax[index])
	ann['xmin'],ann['ymin'],ann['xmax'],ann['ymax'] = new_xmin , new_ymin , new_xmax , new_ymax
	'''print('the new ann[xmin] is',new_xmin)
	print('the new ann[ymin] is',new_ymin)
	print('the new ann[xmax] is',new_xmax)
	print('the new ann[ymax] is',new_ymax)'''
	ann['class'] = new_class
	#print(ann['class'])
	#save both image and annotations
	cv2.namedWindow('img',cv2.WINDOW_NORMAL)
	cv2.imshow('img',mask)
	cv2.waitKey(0)
	#global number
	#save.save_both(mask,ann,filename.split('.')[0]+'_'+str(number))
	#number  += 1
	#save_img(mask,index)
	#save_ann(ann,index)	
	return #mask,ann
	
#Read the image directory
if __name__ == '__main__':
	products = [f for f in os.listdir('./dataset/img/') if f.endswith('.jpg')]
	number = 1
	for sngl_prod in products:
                #print('the sngl_prod',sngl_prod)
		img = cv2.imread('./dataset/img/'+sngl_prod)
		#print('./dataset/img/'+sngl_prod)
		obj,class_list = readJson(sngl_prod,img)
    
		print ('the obj and class_list',obj,class_list)
		img_combo = list(itertools.permutations(obj,11))
		class_combo = list(itertools.permutations(class_list,11))
		choices = random.sample(range(0,len(img_combo)),50000)    # Number of samples to be chosen
		for i in choices:
			placing(img_combo[i],class_combo[i],sngl_prod)
		
		'''
		for i in range(10):
		
			new_img = placing(obj,img.shape)
			print('---------------------------------------')
			cv2.namedWindow('img',cv2.WINDOW_NORMAL)
			cv2.imshow('img',new_img)
			cv2.waitKey(0)
			#sys.exit(0)
		'''
	
	
	
	
	
