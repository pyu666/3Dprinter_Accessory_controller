#coding:utf-8

#インポート関連
import sys
import serial
from serial.tools import list_ports
import os
import io
import tkinter
from tkinter import messagebox

#ウィンドウ生成
top=tkinter.Tk()
top.title("USB Light and Power Changer")
top.geometry("300x150")
port_Name = tkinter.StringVar()
port_Swich = tkinter.StringVar()
port_Power = tkinter.StringVar()
#シリアル通信オブジェクトの生成
ser= serial.Serial()
ser.bsudrate=9600
ser.timeout=1
ser.setDTR(False) # 一部環境のArduino UNOの再起動防止
lb_port = tkinter.Label(textvariabl = port_Name)
lb_port.place(x = 0,y = 130)
lb_switch = tkinter.Label(textvariabl = port_Swich)
lb_switch.place(x = 100,y = 130)
lb_Power = tkinter.Label(textvariabl = port_Power)
lb_Power.place(x = 200,y = 130)
#アプリケーションクラスの作成
class Application(tkinter.Frame):

    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.config()
        port_Name.set("No connect")
        port_Swich.set("LED:？")
        port_Power.set("POWER:?")
    #ボタンの作成
    def create_widgets(self):

        #検索ボタンの生成
        #ここで繋がってるポートを探すボタンを作る
        self.hi_there=tkinter.Button(self)
        self.hi_there["text"]="serch and connection"
        self.hi_there["command"]=self.serch_device
        self.hi_there.pack(side="top")

        #LED点灯用ボタン
        self.hi_there=tkinter.Button(self)
        self.hi_there["text"]="LED ON"
        self.hi_there["command"]=self.tx_on
        self.hi_there.pack(side="top")

        #LED消灯用ボタン
        self.hi_there=tkinter.Button(self)
        self.hi_there["text"]="LED OFF"
        self.hi_there["command"]=self.tx_off
        self.hi_there.pack(side="top")

        # 電源OFF用ボタン
        self.hi_there=tkinter.Button(self)
        self.hi_there["text"]="3DPrinter Power OFF"
        self.hi_there["command"]=self.ask_power_off
        self.hi_there.pack(side="top")

        #シリアル通信終了用ボタン
        self.hi_there=tkinter.Button(self)
        self.hi_there["text"]="close connection"
        self.hi_there["command"]=self.close
        self.hi_there.pack(side="top")


        #アプリケーション終了ボタン
        self.quit=tkinter.Button(self,text="Exit",command=self.master.destroy)
        self.quit.pack(side="bottom")

    #検索を行う
    def serch_device(self):

        devices = serial.tools.list_ports.comports()
        for device in devices:
            # Arduino Unoを見つけたとき，ポートセット及びダイアログを作成
            # 使う種類によって適宜変更を(特にUno互換を使う場合)
            if device.usb_description()=='Arduino Uno':
                ser.port=device[0]
                port_Name.set("connect")
                port_Power.set("POWER:ON")
          #usbデバイスが見つからなかった時の処理
        else:
              #繋がらなかったことを示すダイアログボックスを作成
              not_found()
    #点灯用ボタンの動作の定義
    def tx_on(self):
        port_Swich.set("LED:ON")
        ser.write(bytes("n",'utf-8'))

    #消灯用ボタンの動作の定義
    def tx_off(self):
        port_Swich.set("LED:OFF")
        ser.write(bytes("f",'utf-8'))
    #シリアル通信終了用ボタンの動作の定義
    def close(self):
        ser.close()
        port_Name.set("disconnect")

    def ask_power_off(self):
        if ask_power_info():
            port_Power.set("POWER:OFF")
            ser.write(bytes("m",'utf-8'))
            print("true")
#見つからなかった時のメッセージボックス
def not_found():
    messagebox.showerror("デバイスが見つかりませんでした","デバイスが見つかりませんでした")
#3Dプリンタの電源を切る時に確認するダイアログ
def ask_power_info():
    pw = messagebox.askyesno('確認','主電源をOFFにしますか')
    return pw
app=Application(master=top)

#ウィンドウの生成
app.mainloop()
