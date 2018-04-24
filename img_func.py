import numpy as np
import cv2
import math 

def show_im(name,image):
    n=1
    image = cv2.resize(image, (0,0), fx=n, fy=n)
    cv2.imshow(name,image)
    cv2.waitKey(0)
def water_edges(scr,ch):

    kernel = np.ones((3,3),np.uint8)
    test_img = cv2.morphologyEx(scr, cv2.MORPH_OPEN, kernel)
    test_img = cv2.morphologyEx(test_img, cv2.MORPH_CLOSE, kernel)

    test_img[test_img < np.mean(test_img)] = 0

    out= cv2.equalizeHist(test_img) 
    out= cv2.GaussianBlur(out,(7,7),0)
    # fil=151
    fil=151
    if(ch=='M'):
        thresh = cv2.adaptiveThreshold(out,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,fil,1)
    else:
        thresh = cv2.adaptiveThreshold(out,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,fil,1)    
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((9,9),np.uint8))
    
    scr=cv2.cvtColor(scr.copy(),cv2.COLOR_GRAY2BGR)

    # sure background area
    
    erode = cv2.erode(thresh,np.ones((5,5),np.uint8),iterations=2)        
    sure_bg = cv2.dilate(erode,np.ones((5,5),np.uint8),iterations=3)
    # test = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # show_im('thresh',erode)
    dist_transform = cv2.distanceTransform(erode,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0
    markers = cv2.watershed(scr,markers)
    zeros_n=Draw_contour = water = np.zeros([scr.shape[0],scr.shape[1],3],dtype=np.uint8)
    Draw_contour[markers == -1] = [255,255,255]
    
    ##find area that have most white
    max_n=np.max(markers)
    max_avg_color=0
    zeros_n=np.zeros([scr.shape[0],scr.shape[1],3],dtype=np.uint8)
    # show_im('out',out)
    for i in range(1,max_n+1):
        tmp=zeros_n.copy()
        tmp[markers==i]=[255,255,255]
        avg_color=np.sum(out[markers==i])/(scr.shape[0]*scr.shape[1])
        # print(avg_color)
        if(avg_color>max_avg_color):
            max_avg_color=avg_color
            water=tmp.copy()
    
    ## find contour 
    water = cv2.cvtColor(water,cv2.COLOR_BGR2GRAY)
    # water = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    contourmask = bwmasktemp,contours,hierarchy = cv2.findContours(water,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # Draw_contour=scr.copy()
    # cv2.drawContours(Draw_contour,contours, -1, (0,255,0), 1)
 
   
    target = []
    bigest = 0
    for cnt in contours:
        size=cv2.contourArea(cnt)
        if size > bigest :
            bigest = size
            target = cnt

    # cv2.drawContours(Draw_contour,[target], -1, (0,255,0), 1)
    return water,Draw_contour,target
def adaptiveThreshold_img(img,ch):
    out= cv2.equalizeHist(img) 
    # out= cv2.GaussianBlur(out,(3,3),0)
    out= cv2.medianBlur(out,ksize=7) 
    filter_n=59
    # show_im('out',out)
    out = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    if(ch=='G'):
        thresh = cv2.adaptiveThreshold(out,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY,filter_n,1)
    else:
        thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C  ,cv2.THRESH_BINARY,filter_n,1)  

    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    return thresh
def canny_edges(img):
    sum_n=np.sum(img)
    avg_n=sum_n/(img.shape[0]*img.shape[1])
    edges = cv2.Canny(img,avg_n*0.3,avg_n*0.6)
    # kernel = np.ones((3,3),np.uint8)
    # edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    return edges
def canny_2_for_wavelet(scr,ch):
    kernel = np.ones((3,3),np.uint8)
    test_img = cv2.morphologyEx(scr, cv2.MORPH_OPEN, kernel)
    test_img = cv2.morphologyEx(test_img, cv2.MORPH_CLOSE, kernel)

    test_img[test_img < np.mean(test_img)*0.7] = 0
    # show_im('test',test_img)
    im2= cv2.equalizeHist(test_img) 
    im2= cv2.GaussianBlur(im2,(7,7),0)
    fil=151
    if(ch=='G'):
        thresh = cv2.adaptiveThreshold(im2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY,fil,1)
    elif(ch=='M'):
        thresh = cv2.adaptiveThreshold(im2,255,cv2.ADAPTIVE_THRESH_MEAN_C  ,cv2.THRESH_BINARY,fil,1)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((9,9),np.uint8))
    erode = cv2.dilate(thresh,np.ones((5,5),np.uint8),iterations=1)

    im2=np.int64(im2)
    im2[erode==255]=im2[erode==255]+30
    im2[im2>255]=255
    im2=np.uint8(im2)
    im2 = cv2.medianBlur(im2,ksize=3) 
    sum_n=np.sum(im2)
    avg_n=sum_n/(im2.shape[0]*im2.shape[1])
    e= cv2.Canny(im2,avg_n*0.6,avg_n*0.8)
    # e = cv2.morphologyEx(e, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
  
    return e
def contour_test(scr,ch):
    im2= cv2.equalizeHist(scr) 
    im2= cv2.GaussianBlur(im2,(7,7),0)
    if(ch=='G'):
        thresh = cv2.adaptiveThreshold(im2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY,155,1)
    elif(ch=='M'):
        thresh = cv2.adaptiveThreshold(im2,255,cv2.ADAPTIVE_THRESH_MEAN_C  ,cv2.THRESH_BINARY,155,1)
    kernel = np.ones((3,3),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((9,9),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((5,5),np.uint8)
    erode = cv2.erode(thresh,kernel,iterations=2)
    # print(erode)
    im2=np.int64(im2)
    im2[erode==255]=im2[erode==255]+20
    im2[im2>255]=255
    im2=np.uint8(im2)

    contourmask = bwmasktemp,contours,hierarchy = cv2.findContours(im2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    test=cv2.cvtColor(im2,cv2.COLOR_GRAY2BGR)
    cv2.drawContours(test,contours, -1, (0,255,0), 1)
    return test
def multiple_water(scr,ch):
    kernel = np.ones((3,3),np.uint8)
    test_img = cv2.morphologyEx(scr, cv2.MORPH_OPEN, kernel)
    test_img = cv2.morphologyEx(test_img, cv2.MORPH_CLOSE, kernel)

    test_img[test_img < np.mean(test_img)] = 0

    out= cv2.equalizeHist(test_img) 
    out= cv2.GaussianBlur(out,(7,7),0)
    # fil=151
    fil=151
    if(ch=='M'):
        thresh = cv2.adaptiveThreshold(out,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,fil,1)
    else:
        thresh = cv2.adaptiveThreshold(out,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,fil,1)    
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((9,9),np.uint8))
    
    scr=cv2.cvtColor(scr.copy(),cv2.COLOR_GRAY2BGR)

    # sure background area
    
    erode = cv2.erode(thresh,np.ones((5,5),np.uint8),iterations=2)        
    sure_bg = cv2.dilate(erode,np.ones((5,5),np.uint8),iterations=3)
    # test = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # show_im('thresh',erode)
    dist_transform = cv2.distanceTransform(erode,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers+1
    markers[unknown==255] = 0
    markers = cv2.watershed(scr,markers)
    zeros_n=Draw_contour = np.zeros([scr.shape[0],scr.shape[1],3],dtype=np.uint8)
    Draw_contour[markers == -1] = [255,255,255]

    # show_im('d',Draw_contour)
    ##find area that have most white
    max_n=np.max(markers)
    
    zeros_n=np.zeros([scr.shape[0],scr.shape[1],3],dtype=np.uint8)
    # show_im('out',out)
    water=[]
    target = []
    for i in range(1,max_n+1):
        tmp=zeros_n.copy()
        tmp[markers==i]=[255,255,255]
        avg_color=np.sum(out[markers==i])/(scr.shape[0]*scr.shape[1])
        
        tmp = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
        
    
        ## find contour 
        
        # water = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
        contourmask = bwmasktemp,contours,hierarchy = cv2.findContours(tmp,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        # Draw_contour=scr.copy()
        # cv2.drawContours(Draw_contour,contours, -1, (0,255,0), 1)
    
        bigest = 0
        for cnt in contours:
            size=cv2.contourArea(cnt)
            if size > bigest :
                bigest = size
                target.append(cnt)
                water.append(tmp.copy())
    print('len :',len(water),len(target))
    # cv2.drawContours(Draw_contour,[target], -1, (0,255,0), 1)
    return water,Draw_contour,target,len(water)