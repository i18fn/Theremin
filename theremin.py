#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pygame
import sys
import os

"""GPIOピン番号"""
trig = 21 
echo = 20

"""各センサーの準備"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, GPIO.LOW)

class Sound():
    """Soundクラス
    mp3ファイル情報と、再生メソッドを持つ"""
    def __init__(self, foldername, filename):
        filename = filename + ".mp3"
        self.file = os.path.join(foldername, filename)
    def play(self):
        try:
            pygame.mixer.music.load(self.file)
        except pygame.error: #ファイルが存在しなかったときの処理
            print("Cannot load {}".format(self.file))
            sys.exit()
        pygame.mixer.music.play()

def readDistance():
    """距離を計測するメソッド"""
    time.sleep(0.01)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(echo) == 0:
        sigoff = time.time()

    while GPIO.input(echo) == 1:
        sigon = time.time()
    
    timepassed = sigon - sigoff
    distance = round(timepassed * 17000, 2) #四捨五入

    return distance

def soundsLoad(folder):
    """Soundオブジェクトを作成し、リストに格納して返すメソッド"""
    soundlist = []
    soundlist.append(Sound(folder, "C4")) #ド
    soundlist.append(Sound(folder, "D4")) #レ
    soundlist.append(Sound(folder, "E4")) #ミ
    soundlist.append(Sound(folder, "F4")) #ファ
    soundlist.append(Sound(folder, "G4")) #ソ
    soundlist.append(Sound(folder, "A4")) #ラ
    soundlist.append(Sound(folder, "B4")) #シ
    soundlist.append(Sound(folder, "C5")) #ド(1オクターブ高い)
    return soundlist

def main():
    pygame.init() #pygameモジュールの初期化
    #音源のロード
    try: #コマンドライン引数に何もセットしない時の処理
        sound = soundsLoad(sys.argv[1]) 
    except IndexError:
        sound = soundsLoad("organ")
    onebefore = 0

    while True:
        #ここら辺の詳しい説明はREADME.mdに載せます
        distance = int(readDistance()) // 5
        #例外処理
        try:
            if distance != onebefore:
                sound[distance].play()
                onebefore = distance
        except IndexError:
            pygame.mixer.music.stop()
        
    
    #GPIOピンの初期化
    GPIO.output(trig,False)
    GPIO.cleanup()

if __name__ == "__main__":
    main()
