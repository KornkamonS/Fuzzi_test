import math

import cv2
import numpy as np


def show_result(value,space,window_size):
	resultOfPic=[[],[],[],[],[],[]]
	acc_test=[[0,0],[0,0]]
	winsize=130
	test_file=["img//Train//nodule//","img//Train//none//"]
	nodule=['nodule','none']
    #################################################################################
	for ni in range(2):
		with open(test_file[ni]+'list.txt') as f:
			fileimage = [x.strip().split('\t') for x in f.readlines()] 
			
		for f in fileimage:
				
			print('************')
			# print(f[0])
			targetIMG = test_file[ni]+f[0]+".bmp"    
			print(targetIMG)

			imgRGB = cv2.imread(targetIMG,1) 

			### Get ground truth result ###################################################
			if(ni==0):
				x=int(f[6])
				y=int(f[7])
				d=math.ceil(float(f[3]))
				r=int(math.ceil(d/2))			
				winWb = r+10  
				if(r<(winsize*2)):
					winWb=int(math.ceil(winsize/2))    
				else:
					winWb =int(math.ceil(r/2))+10 
				nodule_position=[x-winWb,y-winWb,x+winWb,y+winWb]
				
			file_result='result//'+nodule[ni]+'//'+f[0]+".txt" 
			with open(file_result) as fr:
				result_test = [x.strip().split(',') for x in fr.readlines()]

			## non max suppression #################################################
			_boxes=[]
			for r in result_test:
				if(float(r[2])>value):
					i,j=int(r[0]),int(r[1])
					x1=j*space
					y1=i*space
					x2=(j*space)+window_size
					y2=(i*space)+window_size
					_boxes.append((x1,y1,x2,y2))
					
			boxes=non_max_suppression_fast(np.array(_boxes),0.3)
			if(boxes!=[]):
				_boxes=boxes.tolist()

			## count accuracy ############################################
			count_TP=0
			count_FP=0
			
			if(ni==0):
				for b in _boxes:
					_b=[b,nodule_position] 
					_r=non_max_suppression_fast(np.array(_b),0.3) 
					if(len(_r)==1):
						cv2.rectangle(imgRGB, (b[0],b[1]),(b[2],b[3]), (0,255,0), 3)
						count_TP+=1
					else:
						cv2.rectangle(imgRGB, (b[0],b[1]),(b[2],b[3]), (0,0,255), 2)
						count_FP+=1

					if(count_TP==0 ):
						# count_FN+=1
						cv2.rectangle(imgRGB, (x-winWb,y-winWb), (x+winWb,y+winWb), (255,0,0), 2)
			elif(len(_boxes)>0):
				count_FP+=len(_boxes)
				for b in _boxes:
					cv2.rectangle(imgRGB, (b[0],b[1]),(b[2],b[3]), (0,0,255), 2)

			print('==',count_TP,count_FP)
			resultOfPic[ni].append([f[0],count_TP,count_FP])
			acc_test[ni][0]+=count_TP
			acc_test[ni][1]+=count_FP
			### draw image result ###################################################
				
			image_name='result//'+nodule[ni]+'//'+f[0]+'.bmp'
			print(image_name)   
			cv2.imwrite(image_name,imgRGB)

	file_name='result//accurancy.txt'
	file = open(file_name,'w')
		
	write_file='nodule\ttrue_positive\tfalse_positive'+'\n'
	sum_TP=0
	num_of_pic=0
	sum_FP=0
	file.write(write_file)

	for i in range(2):
		# print(acc_test[i])
		write_file=nodule[i]+'\t'+str(acc_test[i][0])+'\t'+str(acc_test[i][1])+'\n'
		file.write(write_file)
		sum_TP+=acc_test[i][0]
		sum_FP+=acc_test[i][1]
		num_of_pic+=len(resultOfPic[i])

	write_file='Total \nTrue_Positive: '+str(sum_TP)+'\n'+'Total_pictures: '+str(num_of_pic)+' \n'+'accuracy: '+str(sum_TP/num_of_pic)+'\n'
	file.write(write_file)		

	for i in range(2):
		# print(resultOfPic[i])
		write_file=nodule[i]+'\n'
		file.write(write_file)
		for j in resultOfPic[i]:
			write_file=str(j[0])+'\t'+str(j[1])+'\t'+str(j[2])+'\n'
			file.write(write_file)
	file.close()
	print(sum_TP,sum_FP/num_of_pic)
	return sum_TP,sum_FP/num_of_pic
def non_max_suppression_fast(boxes, overlapThresh):
	if len(boxes) == 0:
		return []

	pick = []
 
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
 
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
 
	while len(idxs) > 0:
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
 
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
 
		overlap = (w * h) / area[idxs[:last]]
 
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
 
	return boxes[pick].astype("int")


#####################################################################################################

# file_name='result//BMP_'+sys.argv[1]+'_'+sys.argv[2]+".txt"
# value=float(sys.argv[3])
# with open(file_name) as f:
# result_test = [x.strip().split(',') for x in f.readlines()]

# targetIMG = 'img//BMP_'+sys.argv[1]+'//JPCLN'+sys.argv[2]+'.bmp'
# print(targetIMG)
# imgRGB = cv2.imread(targetIMG,1)
# space=30 
 
# for r in result_test:
# if(float(r[2])>0):
# i,j=int(r[0]),int(r[1])
# cv2.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)
# cv2.imwrite('result//BMP_'+sys.argv[1]+'_'+sys.argv[2]+".bmp",imgRGB)
