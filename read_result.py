import cv2
import sys

def save_result(level,f,value):
    file_name='result//BMP_'+str(level)+'_'+f[0]+".txt"
    # value=float(sys.argv[3])
    with open(file_name) as f:
        result_test = [x.strip().split(',') for x in f.readlines()]

    targetIMG = "img//BMP_"+str(level)+"//"+f[0]+".bmp"   
    # print(targetIMG)
    imgRGB = cv2.imread(targetIMG,1)
    space=30 
    x=int(f[6])
    y=int(f[7])
    r=math.ceil(float(f[3]))
    r2=int(math.ceil(r/2))
    cv2.circle(im,(x,y),r2,(255,0,0),1)
    
    cv2.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)
    for r in result_test:
        if(float(r[2])>value):
            i,j=int(r[0]),int(r[1])
            cv2.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)
    cv2.imwrite('result//BMP_'+str(level)+'_'+f[0]+".bmp",imgRGB)

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