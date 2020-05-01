# coding=utf-8
import numpy as np
import cv2
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

'''
import serial
'''
'''
# Descomentar caso seja utilizado uma webcam'
 cap = cv2.VideoCapture(0) 
 cap.set(3,320) 
 cap.set(4, 240)
'''
r = (232, 174)

camera = PiCamera()
camera.resolution = r
camera.framerate = 120
rawCapture = PiRGBArray(camera, size=r)

time.sleep(0.5)

LcolorLine = np.array([0, 0, 0])  # VALOR BGR MINIMO DO PRETO
UcolorLine = np.array([22, 20, 21])  # VALOR BGR MAXIMO DO PRETO

LcolorBall = np.array([60, 20, 30])  # VALOR BGR MINIMO DO AZUL
UcolorBall = np.array([232, 193, 204])  # VALOR BGR MAXIMO DO AZUL


ser = serial.Serial("/dev/ttyACM0", 9600)
#tempo = 1


AreaLim = 5000
qtdCnts = 0
direction = 0

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    #    if tempo <= 100:

    frame1 = frame.array

    print("aguardando")
    resp = ser.readline()
    print("Resposta eh: ", resp)
    
    # frame = rawCam.array
    # ret, frame = cap.read()
    '''
    w = np.size(frame, 0)
    h = np.size(frame, 1)
    '''
    if frame1 is not None:
        frame1 = frame1.copy()
        w, h = frame1.shape[:2]
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.bilateralFilter(frame1, 10, 75, 75)

        mask = cv2.inRange(frame1, LcolorLine, UcolorLine)
        mask = cv2.dilate(mask, None, iterations=16)

        mask2 = cv2.inRange(frame, LcolorBall, UcolorBall)
        mask2 = cv2.dilate(mask2, None, iterations=16)

        _, cnts1, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, cnts1, -1, (0, 255, 255), 2)  # CONTORNO AMARELO EM VOLTA LINHA

        _, cnts2, _ = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame1, cnts2, -1, (153, 255, 51), 2)  # CONTORNO TURQUESA EM VOLTA LINHA
        '''
        template = cv2.imread('90.jpg',0)
        template = imutils.resize(template, height=360)
        template1 = imutils.rotate_bound(template, 180)
        '''

        for c in (cnts1 or cnts2):
            if cv2.contourArea(c) < AreaLim:
                continue
            qtdCnts = qtdCnts + 1
            # print("Qtd eh: ", qtdCnts)
            if mask.all() > 0:
                (xl, yl, wl, hl) = cv2.boundingRect(c)
                cv2.rectangle(frame1, (int(xl), int(yl)), (int(xl) + int(wl), int(yl) + int(hl)), (0, 255, 0),
                              2)  # RETANGULO EM VOLTA DA LINHA
                CordXLin = int((xl + xl + wl) / 2)
                CordYLin = int((yl + yl + hl) / 2)
                PCLin = (int(CordXLin), int(CordYLin))
                # cv2.circle(frame, int(PC), 1, (0,0,0), 5)
                direction = CordXLin - (int(w / 1.5))

                # cv2.circle(frame, (int(CordX + 50), int(CordY)),2,(255,150,0),4)

                '''
                print("Width eh:",int(w/1.5))
                print("Heigth eh:",int(h))
                '''

                cv2.line(frame1, (int(w / 1.5), 0), (int(w / 1.5), int(h)), (255, 0, 255), 2)  # LINHA ROSA - REF.

                # res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
                # thresh = 0.8
                # loc = np.where(res >= thresh)
                # for pt in zip(*loc[::-1]):
                #    cv2.rectangle(frame, pt, (pt[0]+w, pt[1]+h), (255,255,0), 2)
                if qtdCnts == 0:
                    print('Nenhuma linha encontrada')
                    
                    ser.write(b'404 - Not Found')
                    tempo = tempo + 1
                    time.sleep(0.5)
                    
                    continue

                if qtdCnts > 0:
                    cv2.line(frame1, (int(CordXLin), int(CordYLin - 120)), (int(w / 1.5), int(CordYLin - 120)), (255, 255, 255),
                             2)  # LINHA BRANCA - DISTANCIA
                if direction > 10:
                    print('Distancia eh: ' + str(abs(direction)) + ' pixels à direita')

                    
                    ser.write(b'Distancia da lnha eh: '+str(abs(direction))+b'à direita')
                    #tempo = tempo + 1
                    time.sleep(0.05)
                    

                    continue

                if direction < -10:
                    print('Distancia eh: ' + str(abs(direction)) + ' pixels à esquerda')

                    
                    ser.write(b'Distancia da lnha eh: '+str(abs(direction))+b'à esquerda')
                    #tempo = tempo + 1
                    time.sleep(0.05)
                    

                    continue

                if (direction >= -15) & (direction <= 15):
                    print("Só vai")

                    
                    ser.write(b'Na linha')
                    #tempo = tempo + 1
                    time.sleep(0.05)
                    

                    continue
            if mask2.all() > 0:
                (xb, yb, wb, hb) = cv2.boundingRect(c)
                cv2.rectangle(frame1, (int(xb), int(yb)), (int(xb) + int(wb), int(yb) + int(hb)), (0, 255, 0),
                              2)  # RETANGULO EM VOLTA DA BOLA
                CordXB = int((xb + xb + wb) / 2)
                CordYB = int((yb + yb + hb) / 2)
                PCB = (int(CordXB), int(CordYB))
                # cv2.circle(frame, int(PC), 1, (0,0,0), 5)
                direction = CordXB - (int(w / 1.5))

                # cv2.circle(frame, (int(CordX + 50), int(CordY)),2,(255,150,0),4)

                '''
                print("Width eh:",int(w/1.5))
                print("Heigth eh:",int(h))
                '''

                cv2.line(frame1, (int(w / 1.5), 0), (int(w / 1.5), int(h)), (255, 0, 255), 2)  # LINHA ROSA - REF.

                # res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
                # thresh = 0.8
                # loc = np.where(res >= thresh)
                # for pt in zip(*loc[::-1]):
                #    cv2.rectangle(frame, pt, (pt[0]+w, pt[1]+h), (255,255,0), 2)
                if qtdCnts == 0:
                    print('Nenhuma linha encontrada')
                    
                    ser.write(b'404 - Not Found')
                    #tempo = tempo + 1
                    time.sleep(0.05)
                    
                    continue

                if qtdCnts > 0:
                    cv2.line(frame1, (int(CordXB), int(CordYB - 120)), (int(w / 1.5), int(CordYB - 120)), (255, 255, 255),
                             2)  # LINHA BRANCA - DISTANCIA
                if direction > 10:
                    print('Distancia eh: ' + str(abs(direction)) + ' pixels à direita')

                    
                    ser.write(b'Distancia da lnha eh: '+str(abs(direction))+b'à direita')
                    #tempo = tempo + 1
                    time.sleep(0.05)
                    

                    continue

                if direction < -10:
                    print('Distancia eh: ' + str(abs(direction)) + ' pixels à esquerda')

                    
                    ser.write(b'Distancia da lnha eh: '+str(abs(direction))+b'à esquerda')
                    #tempo = tempo + 1
                    time.sleep(0.05)
                    

                    continue

                if (direction >= -15) & (direction <= 15):
                    print("Só vai")

                    
                    ser.write(b'Na linha')
                    #tempo = tempo + 1
                    time.sleep(0.5)
                    

                    continue

        # cv2.imshow('test1', mask)
        cv2.imshow('test0', frame1)
        # cv2.imshow('test3', template1)
        # cv2.imshow('test2', template)

        rawCapture.truncate(0)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

# cv2.waitKey(0)
# cap.release()
cv2.destroyAllWindows()
