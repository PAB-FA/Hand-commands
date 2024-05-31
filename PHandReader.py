#V0.1.265
sensitivity = 0
VideoIn = 1

import cv2 as CV
import time as T
from cvzone.HandTrackingModule import HandDetector
from DVal import P0 , Handdistanceinvolume

cap = CV.VideoCapture(VideoIn)
HD = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
lmlistR = None
lmlistL = None

def distancefraction(IN = 100 ,Base = 100):
    if IN == Base :
        return 0
    elif IN > Base:
        return -(IN - Base)
    else :
        return -(IN-Base)




V = {
    'LP84':False,
    'LGP84':False,
    'RP84':False,
    'RGP84':False,
    'LTIMEVOL':0,
    'RTIMEVOL':0,
    'LP812' : False,
    'RP812' : False,
    'LPR8L8': False,
}

def HandCommand(hand,lmlist,HT,frame,Hands,center,bbox):
    global lmlistR,lmlistL
    global V
    if len(Hands) == 1 :
        lmlistL = None
        lmlistR = None
    if HT == 'Right':
        lmlistR = lmlist
    if HT == 'Left' :
        lmlistL = lmlist
    P84,S84,frame = HD.findDistance(lmlist[8][0:2], lmlist[4][0:2], frame, color=(255, 250, 255),scale=3)
    P82,S82,frame = HD.findDistance(lmlist[8][0:2], lmlist[2][0:2], frame, color=(255, 250, 255),scale=3)
    P812,S812,frame = HD.findDistance(lmlist[8][0:2], lmlist[12][0:2], frame, color=(255, 220, 255),scale=3)
    P412,S412,frame = HD.findDistance(lmlist[4][0:2], lmlist[12][0:2], frame, color=(255, 220, 255),scale=3)
    P416,S416,frame = HD.findDistance(lmlist[4][0:2], lmlist[16][0:2], frame, color=(255, 220, 255),scale=3)
    P420,S420,frame = HD.findDistance(lmlist[4][0:2], lmlist[20][0:2], frame, color=(255, 220, 255),scale=3)
    if lmlistL != None and lmlistR != None:
        PR8L8,SR8L8,frame = HD.findDistance(lmlistR[8][0:2], lmlistL[8][0:2], frame, color=(0, 0, 255),scale=5)
        PR1L1,SR1L1,frame = HD.findDistance(lmlistR[1][0:2], lmlistL[1][0:2], frame, color=(0, 0, 255),scale=5)
    finger = HD.fingersUp(hand)
    fingers = finger.count(1)
    if HT == 'Left':
        LP84 = P84 + (distancefraction(bbox[3],P0) / 7)
        LP812 = P812 + (distancefraction(bbox[3],P0) / 7)
        LPR8L8 = 10100
        if lmlistL != None and lmlistR != None:
            LPR8L8 = PR8L8 + (distancefraction(bbox[3],P0) / 7)
        if LPR8L8 < 30 : LPR8L8 = 10010
        else : LPR8L8 = 10100
        if LP812 < 25 : LP812 = 10010
        else: LP812 =10100
        if LP84  < 30: LP84 = 10010
        else : LP84 = 10100
        if LPR8L8 == 10010 :
            V['LPR8L8'] = True
        if LPR8L8 == 10100 and V['LPR8L8'] == True:
            V['LPR8L8'] = False
            return 'POWER'
        if LP812 == 10010:
            if fingers == 2:
                V['LP812'] = True
        if V['LP812'] == True and LP812 == 10100:
            if fingers < 4:
                V['LP812'] = False
                return 'Cut'
            else :
                V['LP812'] = False
                return 'Snipping'
        if LP84 == 10010:
            if fingers == 2 and V['LGP84'] == False:
                V['LGP84'] = True
                return 'grab'
            V['LP84'] = True
            if fingers > 4:
                V['LTIMEVOL'] += 1
        elif LP84 == 10100 :
            if V['LGP84'] == True:
                if fingers == 2 :
                    V['LGP84'] = False
                    return 'forsake'
        if V['LTIMEVOL'] > 10 :
            V['LP84'] = False
            LP82 = P82 + (distancefraction(bbox[3],P0) / 3) + Handdistanceinvolume
            LP82 = LP82 - 43
            LP82 = LP82 * 100 / 30
            if LP82 > 100 : LP82 = 100
            if LP82 < 0:LP82 = 0
            if fingers < 3:
                V['LTIMEVOL'] = 0
                return 'SETV',int(LP82)
            return 'STRV',int(LP82)
        if  V['LP84'] == True:
            if LP84 == 10100 :
                V['LP84'] = False
                if fingers == 5:
                    return 'clic'
                elif fingers == 3:
                    return 'dot'
    if HT == 'Right':
        RP84 = P84 + (distancefraction(bbox[3],P0) / 7)
        RP812 = P812 + (distancefraction(bbox[3],P0) / 7)
        if RP812 < 25 : RP812 = 10010
        else: RP812 =10100
        if RP84  < 30: RP84 = 10010
        else : RP84 = 10100
        if RP812 == 10010:
            if fingers == 2:
                V['RP812'] = True
        if V['RP812'] == True and RP812 == 10100:
            if fingers < 4:
                V['RP812'] = False
                return 'Cut'
            else :
                V['RP812'] = False
                return 'Snipping'
        if RP84 == 10010:
            if fingers == 2 and V['RGP84'] == False:
                V['RGP84'] = True
                return 'grab'
            V['RP84'] = True
            if fingers > 4:
                V['RTIMEVOL'] += 1
        elif RP84 == 10100 :
            if V['RGP84'] == True:
                if fingers == 2 :
                    V['RGP84'] = False
                    return 'forsake'
        if V['RTIMEVOL'] > 10 :
            V['RP84'] = False
            RP82 = P82 + (distancefraction(bbox[3],P0) / 3) + Handdistanceinvolume
            RP82 = RP82 - 43
            RP82 = RP82 * 100 / 30
            if RP82 > 100 : RP82 = 100
            if RP82 < 0:RP82 = 0
            if fingers < 5:
                V['RTIMEVOL'] = 0
                return 'SETV',int(RP82) - 2
            return 'STRV',int(RP82)
        if  V['RP84'] == True:
            if RP84 == 10100 :
                V['RP84'] = False
                if fingers == 5:
                    return 'clic'
                elif fingers == 3:
                    return 'dot'
OUT1 = []
def Handone(Hands,frame,Mode):
    if Hands :
        global OUT1
        # Information for the first hand detected
        hand1 = Hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")
        if Mode == 'GD' : return hand1,lmList1,handType1,frame,Hands,center1,bbox1
        else :
            OUT1.clear()
            OUT1.append(hand1["type"])
            OUT1.append(HandCommand(hand1,lmList1,handType1,frame,Hands,center1,bbox1))
            OUT1.append(center1)
            OUT1.append(lmList1[8][0:2])
            OUT1.append(HD.fingersUp(hand1))
            return OUT1
OUT2 = []
def Handtow(Hands,frame,Mode):
    if len(Hands) == 2 :
        global OUT2
        hand2 = Hands[1]
        lmList2 = hand2["lmList"]
        bbox2 = hand2["bbox"]
        center2 = hand2['center']
        handType2 = hand2["type"]
        if Mode == 'GD' : return hand2,lmList2,handType2,frame,Hands,center2,bbox2
        else :
            OUT2.clear()
            OUT2.append(hand2["type"])
            OUT2.append(HandCommand(hand2,lmList2,handType2,frame,Hands,center2,bbox2))
            OUT2.append(center2)
            OUT2.append(lmList2[8][0:2])
            OUT2.append(HD.fingersUp(hand2))
            return OUT2
def PHR(Mode = 'GD'):
    rec, frame = cap.read()
    Hands, frame = HD.findHands(frame,draw=True,flipType=True)
    OUT = []
    OUT.append(Handone(Hands,frame,Mode))
    OUT.append(Handtow(Hands,frame,Mode))
    if Mode[2:3] == 'F':
        CV.imshow("Hand Reader-Pabfa", frame)
        CV.waitKey(1)
    return OUT

