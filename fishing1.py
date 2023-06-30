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
        self.model = YOLO("fishing1.pt")  # load a pretrained YOLOv8n model
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
        self.target_fps = 59
        self.bot = telega.Telega(self.USER1_ID,self.USER2_ID, self.TOKEN)
        self.SleepMode=False
        self.stop = False
        self.lkmpressed = False
        self.pkmpressed = False
        self.hwnd = win32gui.FindWindow(None, 'Mortal Online 2  ')
        # hwnd = win32gui.FinwdWindow("UnrealWindow", None) # Fortnite
        self.rect = win32gui.GetWindowRect(self.hwnd)
        #region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
        print (self.rect[0],self.rect[1],self.rect[2],self.rect[3])

        self.img = None
        self.fullimg = None
        self.fpstimer= time()

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
        self.img = img[150:(640-266),224:(640-192)]

    def _debug(self, text):
        if self.debug:
            print(f"DEBUG: {text}")

    # Посылает сообщение в телегу
    def send_message_telega(self, text):
        self.bot.send_message(f"{text} \n when {self.spiritCounter} spirits were fluxed and {self.nospiritCounter} summon fails,\n overall AFKtime = {self.AFKtime} seconds \n sultrasaves: {self.ultrasavecounter}")


    def lkmpress(self):
        if not self.lkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            self.lkmpressed = True
            return True
        return False
    def pkmpress(self):
        if not self.pkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            self.pkmpressed = True
            return True
        return False
    def pkmrelease(self):
        if self.pkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            self.pkmpressed = False
            return True
        return False

    def lkmrelease(self):
        if self.lkmpressed:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        self.lkmpressed = False

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

        # Read the images from the file
        img = self.fullimg[80:280, 0:200]
        mxLoc = self.imgfind(img, "hook.png", "hookmask.png",loc=True)
        if  mxLoc is not None:
            self.mousemove(mxLoc[0]-320 +10,mxLoc[1]-320+80 +10)
            sleep(0.5)
            self.pkmpress()
            sleep(0.1)
            self.pkmrelease()
            return True
        else:
            mxLoc = self.imgfind(img, "hook1.png", "hook1mask.png", loc=True)
            if mxLoc is not None:
                self.mousemove(mxLoc[0] - 320 + 10, mxLoc[1] - 320 + 80 + 10)
                sleep(0.5)
                self.pkmpress()
                sleep(0.1)
                self.pkmrelease()
                return True
            else:
                return False

    def equipline(self):

        # Read the images from the file
        img = self.fullimg[80:280, 0:200]
        mxLoc = self.imgfind(img, "line.png", "linemask.png",loc=True)
        if  mxLoc is not None:
            self.mousemove(mxLoc[0]-320 +10,mxLoc[1]-320+80 +10)
            sleep(0.5)
            self.pkmpress()
            sleep(0.1)
            self.pkmrelease()
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
        result = cv.matchTemplate(large_image, small_image, method, None, mask)
        # We want the minimum squared difference
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

    def blackScreenDetect(self):

        # Read the images from the file

        img = self.img[0:66, 0:66]
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
        self.press('z')
        sleep(0.1)
        self.equiprod()
        sleep(0.3)
        self.press('z')
        sleep(2.5)
        self.press('x')
        sleep(1)
        self.equiphook()
        sleep(0.6)
        self.press('z')
        sleep(0.6)
        self.press('z')
        sleep(0.5)
        self.equipline()
        sleep(0.6)
        self.press('z')
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
    def custom(self):

        self.getNextFrame()
        sleep(1)
        Prediction = self.model.predict(source=self.img, device=0, conf=0.2, imgsz=640, batch=8)
        losted = False
        #self.camera.start(region=(8+self.rect[0], 31+self.rect[1], 640+self.rect[0]-8, 640+self.rect[1]-31), target_fps=self.target_fps)
        while True:

            while not losted:

                self.lkmpress()
                sleep(0.4)
                self.lkmrelease()
                sleep(3.5)
                while not losted:
                    self.getNextFrame()



                    if self.checklost():
                        print("LOST YOUR BAIT")
                        losted=True
                        break
                        ###
                    Prediction = self.model.predict(source=self.img, device=0, conf=0.01, imgsz=224,batch=2,show = True)
                    print(Prediction[0].probs.top1,Prediction[0].probs.top1conf)
                    if Prediction[0].probs.top1 == 2 or (Prediction[0].probs.top1 == 1 and Prediction[0].probs.top5[1] == 2 and Prediction[0].probs.top5conf[1] > 0.15):
                        print("PULL")
                        self.lkmpress()
                        break
                if self.checklost():
                    print("LOST YOUR BAIT")
                    losted = True
                    break
                sleep(3)
                counter =0
                pkmtimer = time()
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
                    Prediction = self.model.predict(source=self.img, device=0, conf=0.01, imgsz=224, batch=2)
                    print(Prediction[0].probs.top1, Prediction[0].probs.top1conf)
                    if Prediction[0].probs.top1 == 0  or (Prediction[0].probs.top1 == 1 and Prediction[0].probs.top5[1] == 0):
                        counter+=1

                    else:
                        counter =0
                    if counter>5:
                        print("GOT IT")
                        self.lkmrelease()
                        break
                if self.checklost():
                    print("LOST YOUR BAIT")
                    losted = True
                    break
                sleep(1)
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
