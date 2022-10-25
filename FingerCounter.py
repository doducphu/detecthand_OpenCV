import cv2
import time
import os
import Handtracking as htm
import paho.mqtt.client as mqtt #import the client1
broker_address = "broker.hivemq.com"
import time
wCam, hCam = 2560,1920
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    sub = str(message.payload.decode("utf-8"))
    print("message topic=",message.topic)

    if (sub == "ON"):
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)

        folderPath = "FingerImages"
        myList = os.listdir(folderPath)
        print(myList)
        overlayList = []
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            image = cv2.resize(image, (600, 480))
            # print(f'{folderPath}/{imPath}')
            overlayList.append(image)

        print(len(overlayList))
        pTime = 0

        detector = htm.HandDetector(detectionCon=0.75)

        tipIds = [4, 8, 12, 16, 20]

        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)

        folderPath = "FingerImages"
        myList = os.listdir(folderPath)
        print(myList)
        overlayList = []
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            image = cv2.resize(image, (600, 480))
            # print(f'{folderPath}/{imPath}')
            overlayList.append(image)

        print(len(overlayList))
        pTime = 0

        detector = htm.HandDetector(detectionCon=0.75)

        tipIds = [4, 8, 12, 16, 20]

        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            # print(lmList)

            if len(lmList) != 0:
                fingers = []

                # Thumb
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # print(fingers)
                totalFingers = fingers.count(1)
                print(totalFingers)

                h, w, c = overlayList[totalFingers - 1].shape
                img[0:h, 0:w] = overlayList[totalFingers - 1]

                cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                            10, (255, 0, 0), 25)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 0, 0), 3)

            cv2.imshow("Image", img)
            cv2.waitKey(1)
    elif (sub == "OFF"):
        cv2.VideoCapture(1)
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address,1883) #connect to broker

client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
sub=client.subscribe("house/bulbs/bulb1")
time.sleep(5) # wait
client.loop_stop() #stop the loop