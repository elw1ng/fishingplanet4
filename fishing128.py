from scripts.base import BaseScript  # обязательный импорт для наследования
from ultralytics import YOLO
import cv2 as cv
import numpy as np
import os
import random
from time import sleep
from time import time
from PIL import Image, ImageGrab
import dxcam
import win32api, win32con, win32gui
import math
from tools import telega
from matplotlib import pyplot as plt
class ClassName(BaseScript):  # Название класса (должен отличаться от других названий скриптов)

    def __init__(self):
        super().__init__()  # инициализация класса после наследования

        """                   Ключи - Обязательное                   """

        self.name = "fluxing"  # имя в базе ключей
        self.keys = self.keys_data[self.name]  # загрузка настройки всех ключей данного скрипта
        self.keyActivate = self.keys["activate_key"]  # кнопка активации скрипта
        # обязательно скопировать ключ-значение "base", и переименовать согласно значению в self.name
        """ Полезное, но имеющее значение по дефолту, удалить при ненадобности """

        self.loop = True  # True активирует бесконечный цикл метода custom()
        self.debug = True  # Логи на стандартные функции

        """ Кастомные атрибуты писать здесь """
        self.debug = True
        self.mousereturn = [0, 0]
        self.model = YOLO("fishingcrop128.pt")  # load a pretrained YOLOv8n model
        #self.model = YOLO("bestOUTDOORnew.pt")  # load a pretrained YOLOv8n model

        # Get rect of Window
        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FindWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        self.region = self.rect[0], self.rect[1], self.rect[2] - self.rect[0], self.rect[3] - self.rect[1]
        # initialize the WindowCapture class
        self.camera = dxcam.create()
        self.restart = False
        self.USER1_ID = self.keys['key17']['value']
        self.USER2_ID = self.keys['key18']['value']
        self.TOKEN = self.keys['key19']['value']
        self.yPos = int(self.keys['key1']['value'])
        self.depth = (self.keys['key2']['value'])
        self.target_fps = 59
        self.bot = telega.Telega(self.USER1_ID,self.USER2_ID, self.TOKEN)
        self.SleepMode=False
        self.stop = False
        self.lkmpressed = False
        self.pkmpressed = False
        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        win32gui.SetForegroundWindow(self.hwnd)
        # hwnd = win32gui.FinwdWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        #region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
        print (self.rect[0],self.rect[1],self.rect[2],self.rect[3])

        self.img = None
        self.fullimg = None
        self.fpstimer= time()

        self.pulls = 0
        self.fakepulls = 0
        self.afkrestarts = 0

    def getNextFrame(self):

        while time() - self.fpstimer < (1 / self.target_fps):
            sleep(0.001)
        img = self.camera.grab(
            region=(8 + self.rect[0], 31 + self.rect[1], 640 + self.rect[0] + 8, 640 + self.rect[1] + 31))
        while img is None:
            img = self.camera.grab(
                region=(8 + self.rect[0], 31 + self.rect[1], 640 + self.rect[0] + 8, 640 + self.rect[1] + 31))
        '''
        frameloop = time()
        img = self.camera.get_latest_frame()
        print(time()-frameloop)
        if time()-frameloop < 0.01:
            img = self.camera.get_latest_frame()
        '''
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        self.fullimg = img
        self.img = img[192:(192+128),275:(275+128)]

    def _debug(self, text):
        if self.debug:
            print(f"DEBUG: {text}")

    # Посылает сообщение в телегу
    def send_message_telega(self, text):
        if self.fakepulls+self.pulls>0:
            self.bot.send_message(f"{text}, pulls: {self.pulls}, fake pulls: {self.fakepulls}, fakepull percentage: {round(100*self.fakepulls/(self.fakepulls+self.pulls),2)}% \n AFKrestarts:{self.afkrestarts}")
        else:
            self.bot.send_message(f"{text}, pulls: {self.pulls}, fake pulls: {self.fakepulls}\n AFKrestarts:{self.afkrestarts}")


    def lkmpress(self):
        print("lkmpressed")
        win32gui.SetForegroundWindow(self.hwnd)
        if not self.lkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            self.lkmpressed = True
            return True
        return False
    def pkmpress(self):
        win32gui.SetForegroundWindow(self.hwnd)
        if not self.pkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            self.pkmpressed = True
            return True
        return False
    def pkmrelease(self):
        win32gui.SetForegroundWindow(self.hwnd)
        if self.pkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            self.pkmpressed = False
            return True
        return False

    def lkmrelease(self):
        win32gui.SetForegroundWindow(self.hwnd)
        if self.lkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        self.lkmpressed = False
        print("lkmreleased")

    def spiritdetect(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[328:346, 290:350]
        if self.imgfind(img, self.SpiritFile, "mask.png"):
            self.NoAnsweredThecalltime = time()
            return True
        else:
            return False
    def checknospirit(self):

        # Read the images from the file
        self.getNextFrame()
        img = self.img[358:372,223:244]
        if self.imgfind(img, "nospirit.png", "nospiritmask.png"):
            self.getNextFrame()
            if self.imgfind(img, "nospirit.png", "nospiritmask.png"):
                return True
            else:
                return False
        else:
            return False
    def checklost(self):

        # Read the images from the file
        img = self.fullimg[348:382, 300:353]
        if self.imgfind(img, "lost1.png", "lost1mask.png"):
            return True
        else:
            return False
    def equiprod(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[80:280, 0:200]
        mxLoc = self.imgfind(img, "rod.png", "rodmask.png",loc=True)
        if  mxLoc is not None:
            self.mousemove(mxLoc[0]-320 +10,mxLoc[1]-320+80 +10)
            sleep(0.5)
            self.pkmpress()
            sleep(0.1)
            self.pkmrelease()
            return True
        else:
            mxLoc = self.imgfind(img, "rod1.png", "rod1mask.png", loc=True)
            if mxLoc is not None:
                self.mousemove(mxLoc[0] - 320 + 10, mxLoc[1] - 320 + 80 + 10)
                sleep(0.5)
                self.pkmpress()
                sleep(0.1)
                self.pkmrelease()
                return True
            else:
                return False
    def equiphook(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "hook.png", "hookmask.png",loc=True,conf=0.6)
        if  mxLoc is not None:
            self.equipLoc(mxLoc)
            return True
        else:
            mxLoc = self.imgfind(img, "hook1.png", "hook1mask.png", loc=True,conf=0.6)
            if mxLoc is not None:
                self.equipLoc(mxLoc)
                return True
            else:
                return False

    def equipline(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "line.png", "linemask.png",loc=True,conf=0.6)
        if  mxLoc is not None:
            self.equipLoc(mxLoc)
            return True
        else:
            return False

    def pressLoc(self,mxLoc):
        win32gui.SetForegroundWindow(self.hwnd)
        self.mousemoveABS(mxLoc[0], mxLoc[1])
        sleep(0.5)
        self.lkmpress()
        sleep(0.5)
        self.lkmrelease()
        sleep(0.5)
    def equipLoc(self,mxLoc):
        win32gui.SetForegroundWindow(self.hwnd)
        self.mousemoveABS(mxLoc[0], mxLoc[1])
        sleep(0.5)
        self.pkmpress()
        sleep(0.5)
        self.pkmrelease()
        sleep(0.5)
    def deleteLoc(self,mxLoc):
        win32gui.SetForegroundWindow(self.hwnd)
        self.hold('alt')
        self.mousemoveABS(mxLoc[0],mxLoc[1])
        sleep(0.4)
        self.pkmpress()
        sleep(0.3)
        self.pkmrelease()
        sleep(0.5)
        win32gui.SetForegroundWindow(self.hwnd)
        self.release('alt')
        sleep(0.5)
        self.mousemoveABS(278,  356)
        sleep(0.2)
        self.lkmpress()
        sleep(0.1)
        self.lkmrelease()
        sleep(0.4)
    def delete_t1t1(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "t1t1.png", "t1t1mask.png",loc=True,conf=0.85)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return self.delete_t1t1filter()
    def delete_t1t1filter(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "t1t1filter.png", "t1t1filtermask.png",loc=True,conf=0.85)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return False
    def delete_at2t1(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "at2t1.png", "at2t1mask.png",loc=True,conf=0.77)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return False
    def delete_t2t1(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "t2t1.png", "t2t1mask.png",loc=True,conf=0.86)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return False
    def delete_t2t2(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "t2t2.png", "t2t2mask.png",loc=True,conf=0.85)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return False
    def delete_at1t1(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "at1t1.png", "at1t1mask.png",loc=True,conf=0.75)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return False
    def delete_at1t1filter(self):
        self.getNextFrame()
        # Read the images from the file
        img = self.fullimg[0:300, 0:300]
        mxLoc = self.imgfind(img, "at1t1filter.png", "at1t1filtermask.png",loc=True,conf=0.75)
        if  mxLoc is not None:
            self.deleteLoc(mxLoc)
            return True
        else:
            return False
    def checklowmana(self , percentage = None , ignoresafemode = False ):
        result = True
        if not self.safeMode and not ignoresafemode:
            return False
        if percentage is None:
            percentage = self.lowmana_percentage
        # Read the images from the file
        bgrA=self.img[33:38, int(182 * percentage)]
        for i in range(5):
            bgr = bgrA[i]
            #print(bgr)
            if bgr[0]>=bgr[1]-1 and bgr[2]+1<bgr[0] and bgr[0]>4:
                result = False
        return result

    def imgfind(self, large_image, small_img, mask, conf=0.8, loc = False ):

        # Read the images from the file
        small_image = cv.imread(small_img)
        mask = cv.imread(mask)
        method = cv.TM_CCOEFF_NORMED
        result = cv.matchTemplate(large_image, small_image, method, None,mask=mask)
        # We want the minimum squared diff`erence
        _, mx, _, mxLoc = cv.minMaxLoc(result)
        print(mx)
        if mx > conf and mx < 1.1:
            self.NoAnsweredThecalltime = time()
            if loc:
                return mxLoc
            return True
        else:
            if loc:
                return None
            return False

    def imgfindccorr(self, large_image, small_img, mask, conf=0.99, loc = False ):

        # Read the images from the file
        small_image = cv.imread(small_img)
        mask = cv.imread(mask)
        method = cv.TM_SQDIFF
        result = cv.matchTemplate(large_image, small_image, method, None, mask)
        # We want the minimum squared difference
        mn, mx, mnLoc, mxLoc = cv.minMaxLoc(result)
        print(mn,mx)
        if 1-mn > conf and mn > 0:
            self.NoAnsweredThecalltime = time()
            if loc:
                return mnLoc
            return True
        else:
            if loc:
                return None
            return False
    def menuDetect(self):

        # Read the images from the file

        img = self.fullimg[0:66, 300:630]
        small_image = cv.imread("white.png")
       # cv.imshow("asdasd",small_image)


        small_image = small_image#[43:57, 60:88]
        large_image = img
        #cv.imshow("asdasd", large_image)
       # cv.waitKey(0)
        method = cv.TM_CCORR_NORMED
        result = cv.matchTemplate( large_image , small_image , method,None)
        # We want the minimum squared difference
        _, mx, _, _ = cv.minMaxLoc(result)
        if mx == 0:
            return True
        else:
            return False
    def reequip(self):
        sleep(1)
        self.hold_and_release_sleep('x',0.2)
        sleep(2)
        self.hold_and_release_sleep('i',0.2)
        sleep(1)
        self.equiphook()
        sleep(0.5)
        self.mousemoveABS(320,320)
        sleep(0.5)
        self.equipline()
        sleep(1)
        self.hold_and_release_sleep('z',0.2)

    def mousemoveABS(self, x, y):
        pos = (x + 8 + self.rect[0], y + 31 + self.rect[1])
        win32api.SetCursorPos(pos)
        win32gui.SetForegroundWindow(self.hwnd)
    def mousemove(self, x, y, timer=0.01):

        n = int(max(abs(x) / 70, abs(y) / 70))

        if abs(x) > 0 or abs(y) > 0:
            if n > 0:
                xstep = int(x / n)
                ystep = int(y / n)
                xlast = x - xstep * n
                ylast = y - ystep * n
                timestep = timer / n
                for _ in range(n):
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xstep, ystep, 0, 0)
                    sleep(timestep)

                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, xlast, ylast, 0, 0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
                sleep(timer)
        win32gui.SetForegroundWindow(self.hwnd)

    def delete(self):
        self.hold_and_release_sleep('z',0.2)
        sleep(1)
        self.delete_t1t1()
        self.delete_at1t1()
        self.delete_t2t1()
        self.delete_at2t1()
        sleep(1)
        self.hold_and_release_sleep('z',0.2)

    def changeDepth(self):
        self.hold_and_release_sleep('z', 0.2)
        sleep(1)
        self.mousemoveABS(317,590)
        sleep(0.5)
        self.lkmpress()
        sleep(0.3)
        self.lkmrelease()
        sleep(1)
        for i in range(3):
            self.hold_and_release_sleep('del', 0.3)
            sleep(0.5)
        sleep(1)
        for i in self.depth:
            self.hold_and_release_sleep(i, 0.1)
            sleep(0.6)
        sleep(1)
        self.mousemoveABS(320,320)
        sleep(0.5)
        self.lkmpress()
        sleep(0.3)
        self.lkmrelease()
        sleep(1)
        self.hold_and_release_sleep('z', 0.2)
        sleep(1)
    def restorefarming(self):
        self.lkmrelease()
        for i in range(5):
            self.press('enter')
            sleep(5)
        self.mousemoveABS(125,356)
        sleep(0.5)
        self.lkmpress()
        sleep(0.1)
        self.lkmrelease()
        sleep(20)
        self.mousemoveABS(125, 275)
        sleep(0.5)
        self.lkmpress()
        sleep(0.1)
        self.lkmrelease()
        sleep(45)
        self.hold_and_release_sleep('r',0.3)
        sleep(2)
        self.mousemove(0,self.yPos)
        sleep(1)
        self.reequip()
        sleep(1)
        self.changeDepth()
    def custom(self):
        self.getNextFrame()
        #self.restorefarming()
        #self.reequip()
        sleep(1)
        Prediction = self.model.predict(source=self.img, device=0, conf=0.2, imgsz=128,show=False)
        losted = False
        #self.camera.start(region=(8+self.rect[0], 31+self.rect[1], 640+self.rect[0]-8, 640+self.rect[1]-31), target_fps=self.target_fps)
        cyclecounter = 0
        mainmenu = False
        while True:
            fakepullpercentage = 0
            while not losted:
                cyclecounter +=1
                if self.fakepulls+self.pulls>0:
                    fakepullpercentage = round(100*self.fakepulls/(self.fakepulls+self.pulls),2)
                print(f"Cast № {cyclecounter}, pulls: {self.pulls}, fake pulls: {self.fakepulls}, fakepull percentage: {fakepullpercentage}% \n AFKrestarts:{self.afkrestarts}\n")
                while self.menuDetect():
                    if not mainmenu:
                        self.send_message_telega("MAIN MENU")
                    else:
                        sleep(900)
                    mainmenu = True
                    self.restorefarming()

                    sleep(2)
                if mainmenu:
                    self.send_message_telega("restored from main menu")
                    mainmenu = False
                self.lkmpress()
                sleep(0.001)
                self.lkmrelease()
                sleep(3.5)
                AFKtimer = time()
                afkrestart = False
                pulled = False
                pulledtimer = time()
                pullconfirmcounter = 0
                while not losted:
                    self.getNextFrame()



                    Prediction = self.model.predict(source=self.img, device=0, conf=0.01, imgsz=128,show = False)
                    #print(Prediction[0].probs.top1,Prediction[0].probs.top1conf)
                    if Prediction[0].probs.top1 >= 3 and ((Prediction[0].probs.top1conf> 0.95) or (Prediction[0].probs.top1conf + Prediction[0].probs.top5conf[1]> 0.97 and Prediction[0].probs.top5[1]>=3)):
                        if not pulled:
                            pulled = True
                            print("PULL")
                            self.lkmpress()
                            pulledtimer = time()
                            pullconfirmcounter = 0
                        if pulled and time() -pulledtimer > 0.7:
                            pullconfirmcounter+=1
                    if pulled and pullconfirmcounter>=10:
                        self.pulls+=1
                        break
                    if pulled and pullconfirmcounter<10 and time() -pulledtimer>1.8:
                        print("fake pull reset")
                        self.fakepulls += 1
                        self.lkmrelease()
                        pulled = False

                    if time()-AFKtimer > 300:
                        self.lkmpress()
                        sleep(4)
                        self.lkmrelease()
                        sleep(0.3)
                        self.send_message_telega("nema poklyovki 5 min")
                        afkrestart = True
                        self.afkrestarts+=1
                        break
                if afkrestart:
                    continue
                sleep(1.5)
                counter =0
                PULLtimer = time()
                while not losted:
                    self.getNextFrame()
                    '''
                    while time()-pkmtimer > 6:
                        self.getNextFrame()
                        if self.checklost():
                            print("LOST YOUR BAIT")
                            losted = True
                            break
                        self.pkmpress()
                        if time()-pkmtimer > 7:
                            self.pkmrelease()
                            pkmtimer= time()
                            break
                    '''
                    ###
                    if self.checklost():
                        print("LOST YOUR BAIT")
                        losted = True
                        break
                    Prediction = self.model.predict(source=self.img, device=0, conf=0.01, imgsz=128,show=False)
                    #print(Prediction[0].probs.top1, Prediction[0].probs.top1conf)
                    if Prediction[0].probs.top1 < 2:
                        counter+=1

                    else:
                        counter =0
                    if counter>15:
                        print("GOT IT")
                        self.lkmrelease()
                        sleep(0.5)
                        self.delete()
                        sleep(2)
                        break
                    if time() - PULLtimer > 30:
                        print("TOO LONG TIME PULL")
                        self.lkmrelease()
                        sleep(0.5)
                        break
                if self.checklost():
                    print("LOST YOUR BAIT")
                    losted = True
                    break

                #sleep(1)
            sleep(5)
            self.reequip()
            sleep(2)
            losted = False
        ###

        self.camera.stop()
        print('Done.')
        pass


def run():
    script_class = ClassName()  # инициализация класса (сменить название на актуальное)
    script_class.custom()


if __name__ == "__main__":
    run()
