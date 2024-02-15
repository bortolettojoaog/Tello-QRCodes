from djitellopy import Tello
from time import sleep
from distance import *
from report import *
from find_path import *
from pyzbar.pyzbar import decode

import datetime
import threading
import cv2
import numpy as np

tello = Tello()

################## PARAMETERS #######################
#fowardSpeed = 117 / 10 #Foward Speed in cm/s (15cm/s)
fowardSpeed = 6

angularSpeed = 360 / 10 #Angular Speed in Degrees/s
angularSpeed = angularSpeed / 2

interval = 0.25

travel = False
################## PARAMETERS #######################

distanceInterval = fowardSpeed * interval
angleInterval = angularSpeed * interval


def connect():
    global tello

    try:
        tello.connect()
        print('[✓] Sucesso ao conectar-se ao drone!')
    except:
        print('[X] Erro ao conectar-se ao drone!')

def takeOff():
    global tello
    global travel

    try:
        tello.takeoff()
        print('[✓] Sucesso ao decolar o drone!')

        sleep(4)

        if travel == False:
            startTravel()
    except:
        print('[X] Erro ao decolar ao drone!')

def getDurationForSomeDir(grid):
    sequencias = []
    quantidade_atual = 1

    for i in range(1, len(grid)):
        if grid[i] == grid[i - 1]:
            quantidade_atual += 1
        else:
            sequencias.append([quantidade_atual, grid[i - 1]])
            quantidade_atual = 1

    sequencias.append([quantidade_atual, grid[-1]])

    print(sequencias)

    return sequencias


def getVelocitys(grid):
    lr, ud = 0, 0
    speed = 50

    results = []

    if grid is None: return None

    durationForSomeDir = getDurationForSomeDir(grid)

    if durationForSomeDir is None: return None

    print('[✓] Sucesso ao capturar as direcoes!')

    for res in durationForSomeDir:
        qnt = res[0]
        dir = res[1] 

        lr = 0
        ud = 0
        
        if dir == 'esquerda':
            lr = -speed
        elif dir == 'direita':
            lr = speed

        if dir == 'cima':
            ud = speed
        elif dir == 'baixo':
            ud = -speed

        results.append([qnt, [lr, ud]])
    
    return results

def getTrajectory(grid):
    global tello

    velocitys = getVelocitys(grid)

    print('entrando no trajeto')

    for velocity in velocitys:
        for _ in range(velocity[0]):
            print('#'*100)
            print('Medida: ', _)
            tello.send_rc_control(velocity[1][0], 0, velocity[1][1], 0)
            print(datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3])
            sleep(distanceInterval / 2)
            tello.send_rc_control(0, 0, 0, 0)
            print(datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3])
            sleep(distanceInterval)
            print('#'*100)

def startTravel():
    global travel

    print('Iniciando Trajetória')

    sample = final_dirs
    getTrajectory(sample)

    travel = True

def startStreaming():
    global tello

    frame_read = tello.get_frame_read()

    print("Bateria: ", tello.get_battery(), "%")

    cv2.namedWindow("Tello Streaming")

    while frame_read.frame is not None:
        frame = frame_read.frame

        frame = cv2.resize(frame, (640, 480))

        ######################### GETTING DISTANCE ##########################
        marker = find_marker(frame, KNOWN_WIDTH, KNOWN_HEIGHT)
    
        if marker is not None:
            milimeters = distance_to_camera(KNOWN_WIDTH, focal_length, marker[1][0])
            box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
            box = np.intp(box)
            cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
            cv2.putText(frame, "%.2fcm" % ((milimeters / 10) - 30),
                        (frame.shape[1] - 400, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)

        frame = frame[:, :, ::-1]

        ########### GETTING QRCODES INFORMATION ###########
        try:
            codigos_qr = decode(frame)
            createReport(codigos_qr)
        except:
            print('Erro ao Decodificar Imagem')

        ########### GETTING QRCODES INFORMATION ###########

        cv2.imshow("Tello Streaming", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'): 
            try:
                tello.land()
                print('[✓] Sucesso ao pousar o drone!')
            except:
                print('[X] Erro ao pousar o drone!')

            break
    
    #cv2.destroyAllWindows()

    try:
        tello.streamoff()
        print('[✓] Sucesso ao parar o streaming!')
    except:
        print('[X] Erro ao parar o streaming!')

    tello.end()

connect()

tello.streamon()

sleep(3)

thread1 = threading.Thread(target=takeOff)
thread2 = threading.Thread(target=startStreaming)

thread1.start()
thread2.start()

thread1.join()
thread2.join()