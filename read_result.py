import math

import cv2
import numpy as np


def show_result(value,space):
	resultOfPic=[[],[],[],[],[],[]]
	acc_test=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

	for level in range(4,6):
		with open("img//BMP_"+str(level)+"//list.txt") as f:
			fileimage = [x.strip().split('\t') for x in f.readlines()] 
		
		for f in fileimage:
			
			print('************')
			print(f[0])
			targetIMG = "img//BMP_"+str(level)+"//"+f[0]+".bmp"   
			print(targetIMG)

			imgRGB = cv2.imread(targetIMG,1) 

			### Get ground truth result ###################################################
			x=int(f[6])
			y=int(f[7])
			d=math.ceil(float(f[3]))
			r=int(math.ceil(d/2))
			winWb = r+10
			nodule_position=[x-winWb,y-winWb,x+winWb,y+winWb]
			
			file_result='result//BMP_'+str(level)+'_'+f[0]+".txt"
			with open(file_result) as fr:
				result_test = [x.strip().split(',') for x in fr.readlines()]

			## non max suppression #################################################
			_boxes=[]
			for r in result_test:
				if(float(r[2])>value):
					i,j=int(r[0]),int(r[1])
					x1=j*space
					y1=i*space
					x2=(j*space)+130
					y2=(i*space)+130
					_boxes.append((x1,y1,x2,y2))
				
			boxes=non_max_suppression_fast(np.array(_boxes),0.3)
			if(boxes!=[]):
				_boxes=boxes.tolist()

			## count accuracy ############################################
			count_TP=0
			count_FP=0

			for b in _boxes:
				_b=[b,nodule_position] 
				_r=non_max_suppression_fast(np.array(_b),0.3)
				if(len(_r)==1):
					cv2.rectangle(imgRGB, (b[0],b[1]),(b[2],b[3]), (255,0,255), 2)
					count_TP+=1
				else:
					cv2.rectangle(imgRGB, (b[0],b[1]),(b[2],b[3]), (0,0,255), 2)
					count_FP+=1

			if(count_TP==0):
				# count_FN+=1
				cv2.rectangle(imgRGB, (x-winWb,y-winWb), (x+winWb,y+winWb), (255,0,0), 2)

			print('==',count_TP,count_FP)
			resultOfPic[level].append([f[0],count_TP,count_FP])
			acc_test[level][0]+=count_TP
			acc_test[level][1]+=count_FP
			### draw image result ###################################################
			
			image_name='result//BMP_'+str(level)+'_'+f[0]+'.bmp'
			print(image_name)   
			cv2.imwrite(image_name,imgRGB)
		
			# print(resultOfPic[level])

		# print(true_positive[i])
		# print(false_negative[i])
	# print(true_positive,false_positive,false_negative)
		# cv2.circle(imgRGB,(x,y),r2,(255,0,0),1)

	file_name='result//accurancy.txt'
	file = open(file_name,'w')
	
	# print(np.sum(resultOfPic))
	
	result_print='level\ttrue positive\tfalse positive'+'\n'
	file.write(result_print)
	for i in range(4,6):
		print(acc_test[i])
		result_print='level_'+str(i)+'\t'+str(acc_test[i][0])+'\t'+str(acc_test[i][1])+'\n'
		file.write(result_print)

	for i in range(4,6):
		print(resultOfPic[i])
		result_print='level_'+str(i)+'\n'
		file.write(result_print)
		for j in resultOfPic[i]:
			result_print=str(j[0])+'\t'+str(j[1])+'\t'+str(j[2])+'\n'
			file.write(result_print)
	file.close()
def non_max_suppression_fast(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
 
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	# if boxes.dtype.kind == "i":
	# 	boxes = boxes.astype("float")
 
	# initialize the list of picked indexes	
	pick = []
 
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
 
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
 
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
 
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
 
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
 
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
 
	# return only the bounding boxes that were picked using the
	# integer data type
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
