import cv2
import simpleaudio as sa
from cvzone.HandTrackingModule import HandDetector
from time import sleep
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1280)
detector = HandDetector(detectionCon=0.8)

def drawAll(img,buttonlist):
    for button in buttonlist:
        x,y = button.pos
        w,h = button.size
        cv2.rectangle(img,button.pos,(x+w , y+h),(0,0,0),cv2.FILLED)
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img
class button():
    def __init__(self,pos,text,size=(85,85)):
        self.pos = pos
        self.text = text
        self.size = size
        
        #x,y = self.pos
        #w,h = self.size
        #cv2.rectangle(img,self.pos,(x+w , y+h),(0,0,0),cv2.FILLED)
        #cv2.putText(img,self.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)

buttonlist = []

keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"],
        ["DL","SP"]]
finaltext = ""
for i in range(len(keys)):
    #img = my_button.draw(img)
    for j, key in enumerate( keys[i]):
        buttonlist.append(button([100*j + 50,100 * i + 50],key))
while True:

    success, img = cap.read()
    # Find the hand and its landmarks
    img = cv2.resize(img,(1920,1080))
    hands, img = detector.findHands(img)
    
    img = drawAll(img,buttonlist)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        #print(lmList1[8][:2])
        for button in buttonlist:
            x,y = button.pos
            w,h = button.size

            if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                cv2.rectangle(img,button.pos,(x+w , y+h),(0,255,0),cv2.FILLED)
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                length, info, img = detector.findDistance(lmList1[8][:2],lmList1[12][:2],img)
                print(length)
                if length<+30:
                    cv2.rectangle(img,button.pos,(x+w , y+h),(255,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    if button.text == "DL":
                        finaltext = finaltext[:-1]
                    if button.text == "SP":
                        finaltext += " "
                    
                    if button.text != "DL" and button.text !="SP":
                        finaltext += button.text
                    
                    filename = 'mixkit-arcade-game-jump-coin-216.wav'
                    wave_obj = sa.WaveObject.from_wave_file(filename)
                    play_obj = wave_obj.play()
                    play_obj.wait_done()
                    sleep(0.1)

    cv2.rectangle(img,(300,500),(950, 600),(178, 190, 181),cv2.FILLED)
    cv2.putText(img,finaltext,(295,590),cv2.FONT_HERSHEY_TRIPLEX,4,(0,0,0),4)



    cv2.imshow('Image',img)

    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()
cap.release()