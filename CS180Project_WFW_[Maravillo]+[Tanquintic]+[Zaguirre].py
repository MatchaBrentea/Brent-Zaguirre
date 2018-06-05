# Reference
# Title: Bill Detection
# Author: Maytas Somsmai, Pinpong Kurkcharoen
# Availability: http://assassinsdz.wixsite.com/comvisproject

import numpy as np
import cv2
import common
import time
import _thread
import sys, getopt
import wave
import pyaudio
import os

##################################################################################################
# FLANN parameters
MIN_POINT = 30
chunk = 1024
FLANN_INDEX_KDTREE = 5
do_time = time.time()
def init_feature():
    # Scale Invariant Feature Transform Algorithm for extracting keypoints and computing descriptors 
    detector = cv2.xfeatures2d.SIFT_create()
    norm = cv2.NORM_L1
    # http://www.chioka.in/differences-between-l1-and-l2-as-loss-function-and-regularization/
    
    matcher = cv2.BFMatcher(norm) # Brute Force Matcher object

    # FLANN parameters (used for larger dataset)
    # flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = MIN_POINT)

    return detector, matcher


# plays the audio after finding match
def play_Sound(cash):
    if cash == '20':
        stream = p.open(format = p.get_format_from_width(sound20.getsampwidth()),  
                        channels = sound20.getnchannels(),  
                        rate = sound20.getframerate(),  
                        output = True)
        playnow = sound20
    elif cash == '50':
        stream = p.open(format = p.get_format_from_width(sound50.getsampwidth()),  
                        channels = sound50.getnchannels(),  
                        rate = sound50.getframerate(),  
                        output = True)
        playnow = sound50
    elif cash == '100':
        stream = p.open(format = p.get_format_from_width(sound100.getsampwidth()),  
                        channels = sound100.getnchannels(),  
                        rate = sound100.getframerate(),  
                        output = True)
        playnow = sound100
    elif cash == '200':
        stream = p.open(format = p.get_format_from_width(sound200.getsampwidth()),  
                        channels = sound200.getnchannels(),  
                        rate = sound200.getframerate(),  
                        output = True)
        playnow = sound200
    elif cash == '500':
        stream = p.open(format = p.get_format_from_width(sound500.getsampwidth()),  
                        channels = sound500.getnchannels(),  
                        rate = sound500.getframerate(),  
                        output = True)
        playnow = sound500
    elif cash == '1000':
        stream = p.open(format = p.get_format_from_width(sound1000.getsampwidth()),  
                        channels = sound1000.getnchannels(),  
                        rate = sound1000.getframerate(),  
                        output = True)
        playnow = sound1000


    data = playnow.readframes(chunk)

    #play stream  
    while data != b'':
        stream.write(data)  
        data = playnow.readframes(chunk)

    playnow.rewind()
    #stop stream  
    stream.stop_stream()  
    stream.close()
    print("Running time : %s seconds" % (time.time() - do_time))
    #close PyAudio  
    p.terminate()
   
    

def filter_matches(kp1, kp2, matches, ratio = 0.75):
    # ratio test as per Dr. Lowe's paper
    # This test rejects poor matches by computing the ratio between the best and second-best match
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            # store good matches
            m = m[0]
            mkp1.append(kp1[m.queryIdx])
            mkp2.append(kp2[m.trainIdx])
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    # save the coordinates of the matches in img1 and img2 in one list
    kp_pairs = zip(mkp1, mkp2)

    return p1, p2, kp_pairs

def explore_match(win, img1, img2, kp_pairs, status = None, H = None):
    # initialize visualization (vis) display 
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if H is not None :
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32(cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0)) # get the corners depending on its position/perspective
        corners2 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners2 = np.int32(cv2.perspectiveTransform(corners2.reshape(1, -1, 2), H).reshape(-1, 2) + (0, 0)) # get the corners depending on its position/perspective
        
        # bound the bills on both the vis and frame displays
        cv2.polylines(vis, [corners], True, (0, 255, 0))
        cv2.polylines(frame, [corners2], True, (0, 255, 0))
        
        # put the value of the bill on the corner 
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(vis, showText, (corners[0][0],corners[0][1]), font, 1,(0,0,255),2)
        cv2.putText(frame, showText, (corners2[0][0],corners2[0][1]), font, 1,(0,0,255),2)
    
    p2 = np.int32([kpp[1].pt for kpp in kp_pairs]) + (w1, 0)
    if status is None:
        status = np.ones(len(kp_pairs), np.bool_)
    p1 = np.int32([kpp[0].pt for kpp in kp_pairs])
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            # draw circles on the matching keypoints
            col = (0, 255, 0)
            cv2.circle(vis, (x1, y1), 2, col, 1)
            cv2.circle(vis, (x2, y2), 2, col, 1)
    return vis

def match_and_draw(win, checksound, found , count):
    if(len(kp2) > 0):
    # matching feature
        raw_matches = matcher.knnMatch(desc1, desc2, k = 2)
        p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches) # gets the best matches
        print("Number of frames matched: "+str(len(p1)))
        if len(p1) >= MIN_POINT: # if p1 contains/matches at least 30 points
            if not found:
                checksound = True
            found = True
            count += 1
            # If enough matches are found, we extract the locations of matched keypoints in both the images
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0) # gets the H matrix for the match extraction (position of the matches in img1 and img2)
            vis = explore_match(win, img1, img2, kp_pairs, status, H) # returns the resulting frame where the bill is already bounded and recognized
            
        else: # insufficient matches found (not enough for homography estimation)
            # reset variables
            found = False
            checksound = False
            H, status = None, None
            count = 0
            # normal frame display
            vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
            vis[:h1, :w1] = img1
            vis[:h2, w1:w1+w2] = img2
        
        cv2.imshow('detect', frame)
        cv2.imshow('BFMatcher', vis)
        # check if it matched more than once
        if(count > 1):
            if checksound:
                # reset variables
                checksound = False
                play_Sound(showText) # to play the audio
                count = 0
                found = False

    return found, checksound ,count 

        
################################################################################################################
cv2.useOptimized()

cap = cv2.VideoCapture(0)
detector, matcher = init_feature()

# initialize variables
checksound = True # indicates whether we will play the audio or not
found = False # indicates if there is a match found
searchIndex = 1 # for match searching
count = 0 # counts how many times has matched an image in the dataset

# preload dataset images
img_source1 = cv2.imread( os.path.join('img', '20a.jpg') , 0 )
temp_kp1, temp_desc1 = detector.detectAndCompute(img_source1, None)

img_source2 = cv2.imread( os.path.join('img', '20b.jpg') , 0 )
temp_kp2, temp_desc2 = detector.detectAndCompute(img_source2, None)

img_source3 = cv2.imread( os.path.join('img', '50a.jpg') , 0 )
temp_kp3, temp_desc3 = detector.detectAndCompute(img_source3, None)

img_source4 = cv2.imread( os.path.join('img', '50b.jpg') , 0 )
temp_kp4, temp_desc4 = detector.detectAndCompute(img_source4, None)

img_source5 = cv2.imread( os.path.join('img', '100a.jpg') , 0 )
temp_kp5, temp_desc5 = detector.detectAndCompute(img_source5, None)

img_source6 = cv2.imread( os.path.join('img', '100b.jpg') , 0 )
temp_kp6, temp_desc6 = detector.detectAndCompute(img_source6, None)

img_source7 = cv2.imread( os.path.join('img', '200a.jpg') , 0 )
temp_kp7, temp_desc7 = detector.detectAndCompute(img_source7, None)

img_source8 = cv2.imread( os.path.join('img', '200b.jpg') , 0 )
temp_kp8, temp_desc8 = detector.detectAndCompute(img_source8, None)

img_source9 = cv2.imread( os.path.join('img', '500a.jpg') , 0 )
temp_kp9, temp_desc9 = detector.detectAndCompute(img_source9, None)

img_source10 = cv2.imread( os.path.join('img', '500b.jpg') , 0 )
temp_kp10, temp_desc10 = detector.detectAndCompute(img_source10, None)

img_source11 = cv2.imread( os.path.join('img', '1000a.jpg') , 0 )
temp_kp11, temp_desc11 = detector.detectAndCompute(img_source11, None)

img_source12 = cv2.imread( os.path.join('img', '1000b.jpg') , 0 )
temp_kp12, temp_desc12 = detector.detectAndCompute(img_source12, None)


print("\nChoose language:\n[1] English\n[2] Tagalog\n-> ", end = '')
flag = True
#preload audio
while(flag):
    mode = input()
    if mode == '1':
        sound20 = wave.open(os.path.join("Audio", "English", "20.wav"),"rb")
        sound50 = wave.open(os.path.join("Audio", "English", "50.wav"),"rb")
        sound100 = wave.open(os.path.join("Audio", "English", "100.wav"),"rb")
        sound200 = wave.open(os.path.join("Audio", "English", "200.wav"),"rb")
        sound500 = wave.open(os.path.join("Audio", "English", "500.wav"),"rb")
        sound1000 = wave.open(os.path.join("Audio", "English", "1000.wav"),"rb")
        flag = False
    elif mode == '2':
        sound20 = wave.open(os.path.join("Audio", "Tagalog", "20.wav"),"rb")
        sound50 = wave.open(os.path.join("Audio", "Tagalog", "50.wav"),"rb")
        sound100 = wave.open(os.path.join("Audio", "Tagalog", "100.wav"),"rb")
        sound200 = wave.open(os.path.join("Audio", "Tagalog", "200.wav"),"rb")
        sound500 = wave.open(os.path.join("Audio", "Tagalog", "500.wav"),"rb")
        sound1000 = wave.open(os.path.join("Audio", "Tagalog", "1000.wav"),"rb")
        flag = False
    else:
        print("Choose 1 or 2 only.\n-> ", end = '')

print("Starting program...")
print("\nPress:\n1 - change language\n2 - exit program")

while(True):
    # create pyAudio object
    p = pyaudio.PyAudio() 
    
    #switch template (try each image in dataset to get match)
    if not found:
        if searchIndex <= 12:
            if searchIndex == 1:
                img1 = img_source1
                kp1 = temp_kp1
                desc1 = temp_desc1
                showText = '20'
            elif searchIndex == 2:
                img1 = img_source2
                kp1 = temp_kp2
                desc1 = temp_desc2
                showText = '20'
            elif searchIndex == 3:
                img1 = img_source3
                kp1 = temp_kp3
                desc1 = temp_desc3
                showText = '50'
            elif searchIndex == 4:
                img1 = img_source4
                kp1 = temp_kp4
                desc1 = temp_desc4
                showText = '50'
            elif searchIndex == 5:
                img1 = img_source5
                kp1 = temp_kp5
                desc1 = temp_desc5
                showText = '100'
            elif searchIndex == 6:
                img1 = img_source6
                kp1 = temp_kp6
                desc1 = temp_desc6
                showText = '100'
            elif searchIndex == 7:
                img1 = img_source7
                kp1 = temp_kp7
                desc1 = temp_desc7
                showText = '200'
            elif searchIndex == 8:
                img1 = img_source8
                kp1 = temp_kp8
                desc1 = temp_desc8
                showText = '200'
            elif searchIndex == 9:
                img1 = img_source9
                kp1 = temp_kp9
                desc1 = temp_desc9
                showText = '500'
            elif searchIndex == 10:
                img1 = img_source10
                kp1 = temp_kp10
                desc1 = temp_desc10
                showText = '500'
            elif searchIndex == 11:
                img1 = img_source11
                kp1 = temp_kp11
                desc1 = temp_desc11
                showText = '1000'
            elif searchIndex == 12:
                img1 = img_source12
                kp1 = temp_kp12
                desc1 = temp_desc12
                showText = '1000'
                
            searchIndex = searchIndex+1
        else:
            searchIndex = 1
            img1 = img_source1
            
                    
    # Capture frame-by-frame
    ret, frame = cap.read()
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # get height and width
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # calculate features
    # find the keypoints and descriptors with SIFT (detector)
    kp2, desc2 = detector.detectAndCompute(img2, None)

    # find best match from the dataset
    found, checksound, count = match_and_draw('find_obj',checksound,found,count)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('1'):
        print("\nChoose language:\n[1] English\n[2] Tagalog\n-> ", end = '')
        flag = True
        # preload audio
        while(flag):
            mode = input()
            if mode == '1':
                sound20 = wave.open(os.path.join("Audio", "English", "20.wav"),"rb")
                sound50 = wave.open(os.path.join("Audio", "English", "50.wav"),"rb")
                sound100 = wave.open(os.path.join("Audio", "English", "100.wav"),"rb")
                sound200 = wave.open(os.path.join("Audio", "English", "200.wav"),"rb")
                sound500 = wave.open(os.path.join("Audio", "English", "500.wav"),"rb")
                sound1000 = wave.open(os.path.join("Audio", "English", "1000.wav"),"rb")
                flag = False
            elif mode == '2':
                sound20 = wave.open(os.path.join("Audio", "Tagalog", "20.wav"),"rb")
                sound50 = wave.open(os.path.join("Audio", "Tagalog", "50.wav"),"rb")
                sound100 = wave.open(os.path.join("Audio", "Tagalog", "100.wav"),"rb")
                sound200 = wave.open(os.path.join("Audio", "Tagalog", "200.wav"),"rb")
                sound500 = wave.open(os.path.join("Audio", "Tagalog", "500.wav"),"rb")
                sound1000 = wave.open(os.path.join("Audio", "Tagalog", "1000.wav"),"rb")
                flag = False
            else:
                print("Choose 1 or 2 only.\n-> ", end = '')
        print("Done.")
        print("\nPress:\n1 - change language\n2 - end program")
    elif key & 0xFF == ord('2'):
        break
    
#close PyAudio  
p.terminate()
 
# When everything's done, release the capture
cap.release()
cv2.destroyAllWindows()
