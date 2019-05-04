## 接続

```text
VCC  一一一一一一一一一一一一一　5VO
Trig 一一一一一一一一一一一一一　GPIO21
Echo 一一一一一一一一一一一一一　GPIO20
GND  一一一一一一一一一一一一一　GND
```

## コード解説

解説が必要そうな所だけ解説します

```python
import RPi.GPIO as GPIO
import time
import pygame
import sys
import os
```

距離センサーを使うので、RPi.GPIO、timeモジュールは必ずインポートします  
pygameは音の出力に使いました(他にも音を鳴らすことができるモジュールはありますが、自分が使い慣れているということもあって、今回はこのモジュールを使いました)  
osモジュールはファイルのパスの取得に使いました(別にRaspbian以外のOSで使うことはないので必要はなかったのかも)  
sysモジュールはコマンドライン引数に鳴らす楽器を指定するという処理をするために使用

```python
class Sound():
    def __init__(self, foldername, filename):
        filename = filename + ".mp3"
        self.file = os.path.join(foldername, filename)
    def play(self):
        try:
            pygame.mixer.music.load(self.file)
        except pygame.error:
            print("Cannot load {}".format(self.file))
            sys.exit()
        pygame.mixer.music.play()

def soundsLoad(folder):
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
```

このプログラムではドから1オクターブ上のドまでの音源を作って、それらを再生しています。  
Soundクラスは、その音のファイル名をデータとして持ち、play()メソッドを呼び出すことでそのファイルを再生します。  
SoundクラスのインスタンスはsoundLoad()でそれぞれの音程ごとに生成し、それらをsoundlistに格納します。  
soundLoad()の返り値のリストの中身は  
[ドの音, レの音, ミの音, ファの音, ソの音, ラの音, シの音, ドの音]  
というように順に格納されています。例えば、soundlist［0］.play()で、ドの音が再生されます。  

```python
def main():
    pygame.init()
    try:
        sound = soundsLoad(sys.argv[1])
    except IndexError:
        sound = soundsLoad("organ")
    onebefore = 0
```

mainメソッドではまず、コマンドラインから楽器を指定して、soundLoad()に実引数として渡し、返り値のリストをsoundに格納します

```
$ python3 theremin.py organ
```

例えば、上記のようなコマンドで実行すると、楽器がorganになります。  
もしコマンドライン引数に何も指定されていないと、sound = soundsLoad(sys.argv[1])の所でIndexErrorになってしまうので、例外処理をしています。

```python
    while True:
        distance = int(readDistance()) // 5
        try:
            if distance != onebefore:
                sound[distance].play()
                onebefore = distance
        except IndexError:
            pygame.mixer.music.stop()
```

while文の中で、音の再生処理を行っています。  
readDistance()で距離を取得し、それをint型に変換して5で割った値をsound[]の添字に入れて、play()を呼び出しています。  
分かりにくいので例を挙げると、  
readDistance()で取得した値が23.41の場合、int型に変換して23。
その値を5で割ると4(小数点以下切り捨て)。なのでsound［4］.play()が呼び出されます。(ソの音が出力される)  
もし距離が遠すぎる場合、int(readDistance()) // 5で得られる値がsoundの要素数を超えてしまうので、例外処理で音を鳴らさないように調整しています。

## 問題点

### 1.音が安定しない

これはしょうがないことなのかもしれませんが、ずっと同じ音程で鳴らすことが難しいです。センサーの調子とかもあるでしょうし...

### 2.出せる音が少ない

ドの音、レの音...と別々に音源を作り、距離に応じて使う音源を変えたりしているだけのチープな設計なので、どうしても出せる音が少なくなります。音源も、DominoというMIDIシーケンサーを使って作成したものなので、色々な音程の音源を作るのは少し大変です。pythonのモジュールに再生しているmp3音源のピッチ変更ができるやつとかないですかね...

### 3.そもそもテルミンと仕組みが全然違う

本気で作ろうと思ったら、周波数がどうこうだとか静電容量がどうこうだとか考える必要があります。  
今回のは遊びの一環として作ったものなので、テルミンっぽいサンプリング楽器だと思ってください。

### その他改善点等あればコメントに書いてもらえると助かります

## 参考文献

・「Raspberry Pi 電気工作レシピ」 ----　河野悦昌　　翔泳社  
・「みんなのPython 第四版」　----　柴田淳　　SB Creative