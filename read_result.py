import cv2
import sys
import math
def show_result(value,space):
    for level in range(4,6):
        with open("img//BMP_"+str(level)+"//list.txt") as f:
            fileimage = [x.strip().split('\t') for x in f.readlines()] 
        for f in fileimage:
            print('************')
            print(f[0])
            targetIMG = "img//BMP_"+str(level)+"//"+f[0]+".bmp"           
            print(targetIMG)
    
            imgRGB = cv2.imread(targetIMG,1) 
                
            file_result='result//BMP_'+str(level)+'_'+f[0]+".txt"
            with open(file_result) as fr:
                result_test = [x.strip().split(',') for x in fr.readlines()]

            for r in result_test:
                if(float(r[2])>value):
                    i,j=int(r[0]),int(r[1])
                    cv2.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)

            
            ### draw ground truth result###################################################                
            x=int(f[6])
            y=int(f[7])
            d=math.ceil(float(f[3]))
            r=int(math.ceil(d/2))
            winWb = r+10
            cv2.rectangle(imgRGB, (x-winWb,y-winWb), (x+winWb,y+winWb), (255,0,0), 2)

            ### save result ###################################################
            image_name='result//BMP_'+str(level)+'_'+f[0]+'.bmp'
            print(image_name)       
            cv2.imwrite(image_name,imgRGB)
            # cv2.circle(imgRGB,(x,y),r2,(255,0,0),1)

#####################################################################################################

# file_name='result//BMP_'+sys.argv[1]+'_'+sys.argv[2]+".txt"
# value=float(sys.argv[3])
# with open(file_name) as f:
#     result_test = [x.strip().split(',') for x in f.readlines()]

# targetIMG = 'img//BMP_'+sys.argv[1]+'//JPCLN'+sys.argv[2]+'.bmp'
# print(targetIMG)
# imgRGB = cv2.imread(targetIMG,1)
# space=30 
 
# for r in result_test:
#     if(float(r[2])>0):
#         i,j=int(r[0]),int(r[1])
#         cv2.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)
# cv2.imwrite('result//BMP_'+sys.argv[1]+'_'+sys.argv[2]+".bmp",imgRGB)