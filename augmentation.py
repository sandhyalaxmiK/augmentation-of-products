import argparse
import os,os.path
import cv2
from pylab import array, plot, show, axis, arange, figure, uint8
import sys
import numpy as np
from matplotlib import pyplot as plt
import json
def cropping(image,f,x1,x2,y1,y2):
	if (xmin <= x1 and xmax >= x2 and ymin <= y1 and ymax >= y2):
		cropped = img[y1:y2,x1:x2]
		cv2.imwrite(imageDir+"/img/"+f.split('.')[0]+"crop"+str(x1)+'_'+str(x2)+'_'+str(y1)+'_'+str(y2)+".jpg",cropped)
		with open(imageDir+'/ann/'+f.split('.')[0]+"crop"+str(x1)+'_'+str(x2)+'_'+str(y1)+'_'+str(y2)+'.json','w') as data_file:
			data['annotation']['object']['bndbox']['xmin'] = str(0)
			data['annotation']['object']['bndbox']['ymin'] = str(0)
			data['annotation']['object']['bndbox']['xmax'] = str(x2-x1)
			data['annotation']['object']['bndbox']['ymax'] = str(y2-y1)
			json.dump(data,data_file,indent = 4 ,separators=(',',':'))

def rotating(img,f,rows,cols):
	for degree in range(0,360,30):
			M = cv2.getRotationMatrix2D((cols/2,rows/2),degree,1)
			rotated_img = cv2.warpAffine(img, M,(cols,rows))
			mask1 = np.zeros((img.shape[0], img.shape[1]),dtype = "uint8")
			cv2.circle(mask1,(xmin,ymin),3,(255,255,255),10)
			cv2.circle(mask1,(xmax,ymin),3,(255,255,255),10)
			cv2.circle(mask1,(xmin,ymax),3,(255,255,255),10)
			cv2.circle(mask1,(xmax,ymax),3,(255,255,255),10)
			rows,cols = mask1.shape
			rotated_mask = cv2.warpAffine(mask1,M,(cols,rows))
			im2, contours, hierarchy = cv2.findContours(rotated_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			cnt = contours
			p=[]	
			for i in range (len(cnt)):
				M =cv2.moments(cnt[i])
				#print (M)
				if M['m00'] == 0:
					break		
				else:		
					cx = int(M['m10']/M['m00'])
					cy = int(M['m01']/M['m00'])
					p.append((cx,cy))
				w,h = rotated_mask.shape[:2]	
	
			if len(p)==4:	
				p5 = (min(p[0][0],p[1][0],p[2][0],p[3][0]),min(p[0][1],p[1][1],p[2][1],p[3][1]))
				p6 = (max(p[0][0],p[1][0],p[2][0],p[3][0]),max(p[0][1],p[1][1],p[2][1],p[3][1]))	
				w,h = rotated_mask.shape[:2]			
			#cv2.rectangle(rotated_img,p5,p6,(255,255,255),3)
	
				cv2.imwrite(imageDir+"/img/"+f.split('.')[0]+str(degree)+".jpg",rotated_img)
				with open(imageDir+'/ann/'+f.split('.')[0]+str(degree)+'.json','w') as data_file:
					data['annotation']['object']['bndbox']['xmin'] = str(p5[0])
					data['annotation']['object']['bndbox']['ymin'] = str(p5[1])
					data['annotation']['object']['bndbox']['xmax'] = str(p6[0])
					data['annotation']['object']['bndbox']['ymax'] = str(p6[1])
					json.dump(data,data_file,indent = 4 ,separators=(',',':'))

def flipping(img,f,j):
	flipped_img = cv2.flip(img,j)
	mask1 = np.zeros((img.shape[0], img.shape[1]),dtype = "uint8")
	cv2.circle(mask1,(xmin,ymin),3,(255,255,255),10)
	cv2.circle(mask1,(xmax,ymin),3,(255,255,255),10)
	cv2.circle(mask1,(xmin,ymax),3,(255,255,255),10)
	cv2.circle(mask1,(xmax,ymax),3,(255,255,255),10)
	rows,cols = mask1.shape
	flipped_mask = cv2.flip(mask1,j)
	im2, contours, hierarchy = cv2.findContours(flipped_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnt = contours
	p=[]	
	for i in range (len(cnt)):
		M =cv2.moments(cnt[i])
		if M['m00'] == 0:
			break		
		else:		
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			p.append((cx,cy))
			w,h = flipped_mask.shape[:2]	
		if len(p)==4:	
			p5 = (min(p[0][0],p[1][0],p[2][0],p[3][0]),min(p[0][1],p[1][1],p[2][1],p[3][1]))
			p6 = (max(p[0][0],p[1][0],p[2][0],p[3][0]),max(p[0][1],p[1][1],p[2][1],p[3][1]))	
			#cv2.rectangle(rotated_img,p5,p6,(255,255,255),3)
			cv2.imwrite(imageDir+"/img/"+f.split('.')[0]+'flip'+str(j)+".jpg",flipped_img)
			with open(imageDir+'/ann/'+f.split('.')[0]+'flip'+str(j)+'.json','w') as data_file:
				data['annotation']['object']['bndbox']['xmin'] = str(p5[0])
				data['annotation']['object']['bndbox']['ymin'] = str(p5[1])
				data['annotation']['object']['bndbox']['xmax'] = str(p6[0])
				data['annotation']['object']['bndbox']['ymax'] = str(p6[1])
				json.dump(data,data_file,indent = 4 ,separators=(',',':'))

				
parser = argparse.ArgumentParser()
parser.add_argument("--Crop", help = "Displays cropped images",action = 'store_true')
parser.add_argument("--Flip", help = "Displays horizontal or vertical or both flipped images",action = 'store_true' )
parser.add_argument("--Rotate", help = "Displays rotated images",action = 'store_true')
parser.add_argument("--Resize", help = "Enter 2 values to resize an image",nargs = 2, type = int)
parser.add_argument("--LTranslation", help="displays linearly translated image",action = 'store_true')
#parser.add_argument("--directory_name",help="enter the images directry name: ",nargs=1)
args = parser.parse_args()
		
if args.Crop:
	imageDir = "./atta"
	j = 1
	for f in os.listdir(imageDir+"/img"):
		if os.path.splitext(f)[1] != '.jpg':
			continue
		with open(imageDir+'/ann/'+f.split('.')[0]+'.json') as data_file:
			data=json.load(data_file)
		xmin =int(data['annotation']['object']['bndbox']['xmin'])
		ymin=int(data['annotation']['object']['bndbox']['ymin'])
		xmax=int(data['annotation']['object']['bndbox']['xmax'])
		ymax=int(data['annotation']['object']['bndbox']['ymax'])
		imagepath = os.path.join(imageDir,'img',f)	
		img =cv2.imread(imagepath)
		#print (img)
		rows, cols =img.shape[:2]
		i =1		
		cropping(img,f,100,200,100,200)		
		cropping(img,f,160,250,150,240)
		cropping(img,f,250,220,200,330)
		cropping(img,f,150,170,180,210)
		cropping(img,f,200,280,300,350)		
		
		
		
if args.Rotate:
	imageDir =  "./atta"
	import pdb
	pdb.set_trace()
	for f in os.listdir(imageDir+"/img"):
		if os.path.splitext(f)[1] != '.jpg':
			continue
		with open(imageDir+'/ann/'+f.split('.')[0]+'.json') as data_file:
			data=json.load(data_file)
		print('data',data)
		xmin =int(data['annotation']['object']['bndbox']['xmin'])
		ymin=int(data['annotation']['object']['bndbox']['ymin'])
		xmax=int(data['annotation']['object']['bndbox']['xmax'])
		ymax=int(data['annotation']['object']['bndbox']['ymax'])
		imagepath = os.path.join(imageDir,'img',f)		
		img =cv2.imread(imagepath)		
		rows, cols =img.shape[:2]
		rotating(img,f,rows,cols)
		
     		
if args.Flip:
	imageDir =  "./atta"
	for f in os.listdir(imageDir+"/img"):
		if os.path.splitext(f)[1] != '.jpg':
			continue
		with open(imageDir+'/ann/'+f.split('.')[0]+'.json') as data_file:
			data=json.load(data_file)
		xmin =int(data['annotation']['object']['bndbox']['xmin'])
		
		ymin=int(data['annotation']['object']['bndbox']['ymin'])
		xmax=int(data['annotation']['object']['bndbox']['xmax'])
		ymax=int(data['annotation']['object']['bndbox']['ymax'])
		imagepath = os.path.join(imageDir,'img',f)		
		img =cv2.imread(imagepath)
		cv2.imshow('',img)
		cv2.waitKey(1)		
		rows, cols =img.shape[:2]
		flipping(img,f,0)
		flipping(img,f,1)
		flipping(img,f,-1)
	
		
if args.Resize:
	imageDir =  "./atta"
	for f in os.listdir(imageDir+"/img"):
		if os.path.splitext(f)[1] != '.jpg':
			continue
		with open(imageDir+'/ann/'+f.split('.')[0]+'.json') as data_file:
			data=json.load(data_file)
		xmin =int(data['annotation']['object']['bndbox']['xmin'])
		ymin=int(data['annotation']['object']['bndbox']['ymin'])
		xmax=int(data['annotation']['object']['bndbox']['xmax'])
		ymax=int(data['annotation']['object']['bndbox']['ymax'])
		imagepath = os.path.join(imageDir,'img',f)		
		img =cv2.imread(imagepath)		
		rows, cols =img.shape[:2]
		h,w,c = img.shape
		xmin = float(xmin)/w
		xmax = float(xmax)/w
		ymin = float(ymin)/h
		ymax = float(ymax)/h
		cv2.imshow("image",img)
		resized_img = cv2.resize(img,(args.Resize[0],args.Resize[1]))
		h1, w1,c1 = resized_img.shape
		xmin = int(xmin*w1)
		xmax = int(xmax*w1)
		ymin = int(ymin*h1)
		ymax = int(ymax*h1)
		cv2.imwrite(imageDir+"/img/"+f.split('.')[0]+'Resize'+str(args.Resize[0])+'_'+str(args.Resize[1])+".jpg",resized_img)
		with open(imagedir+'/ann/'+f.split('.')[0]+'Resize'+str(args.Resize[0])+'_'+str(args.Resize[1])+'.json','w') as data_file:
				
			data['annotation']['object']['bndbox']['xmin'] = str(xmin)
			data['annotation']['object']['bndbox']['ymin'] = str(ymin)
			data['annotation']['object']['bndbox']['xmax'] = str(xmax)
			data['annotation']['object']['bndbox']['ymax'] = str(ymax)
			json.dump(data,data_file,indent = 4 ,separators=(',',':'))		

  		

if args.LTranslation:
	imageDir = "./atta"
	for f in os.listdir(imageDir+"/img"):
		if os.path.splitext(f)[1] != '.jpg':
			continue
		with open(imageDir+'/ann/'+f.split('.')[0]+'.json') as data_file:
			data=json.load(data_file)
		xmin =int(data['annotation']['object']['bndbox']['xmin'])
		ymin=int(data['annotation']['object']['bndbox']['ymin'])
		xmax=int(data['annotation']['object']['bndbox']['xmax'])
		ymax=int(data['annotation']['object']['bndbox']['ymax'])
		imagepath = os.path.join(imageDir,'img',f)		
		img =cv2.imread(imagepath)		
		rows, cols =img.shape[:2]
		h,w,c = img.shape
		d=[(0,0),(1,1),(10,20),(30,30),(100,100),(200,250),(300,350),(2,5),(3,4),(5,4),(7,8),(2,2),(3,3)]		
		for i in range(len(d)):		
			M = np.float32([[1,0,d[i][0]],[0,1,d[i][1]]])
			ltrans_img = cv2.warpAffine(img, M, (cols,rows))
			h1,w1 = ltrans_img.shape[:2]
			if (((xmin+d[i][0]) > w1) or ((ymin+d[i][1]) >h1) or ((xmax+d[i][0]) > w1) or ((ymax+d[i][1]) > h1)):
				continue		
			cv2.imwrite(imageDir+"/img/"+f.split('.')[0]+'LTranslated'+str(d[i][0])+'_'+str(d[i][1])+".jpg",ltrans_img)
			with open(imageDir+'/ann/'+f.split('.')[0]+'LTranslated'+str(d[i][0])+'_'+str(d[i][1])+'.json','w') as data_file:
				
				data['annotation']['object']['bndbox']['xmin'] = str(xmin+d[i][0])
				data['annotation']['object']['bndbox']['ymin'] = str(ymin+d[i][1])
				data['annotation']['object']['bndbox']['xmax'] = str(xmax+d[i][0])
				data['annotation']['object']['bndbox']['ymax'] = str(ymax+d[i][1])
				json.dump(data,data_file,indent = 4 ,separators=(',',':'))
		

				







