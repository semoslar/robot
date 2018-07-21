from pynput.mouse import  Controller,Button
from PIL import Image
import time
import pyautogui
import pytesseract
import os

from pynput.mouse import Listener
import tkinter as tk
from tkinter import messagebox
from PIL import Image

#HARD CODE
#-------------
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
doviz_noktasi = [51, 14]
al_noktasi =  [1200,655]
sat_noktasi = [1040,655]
stoch_nokta = [397, 577]

stoch_genislik = (60, 22)

pozisyon_noktasi = [670,836]
pozisyon_genislik = [38,17]
tamam_noktasi = [1040,688]
pozisyon_kapama_noktasi = [1040,688]

dir_path = os.getcwd()

temp_image = Image
temp_result = ""


#--------------




def resmiBuyut(image):
    basewidth = 300
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    img = image.resize((basewidth, hsize),Image.ANTIALIAS)
    return img

def pozisyonkapa(mouse,Button):
    mouseGotur(pozisyon_noktasi,mouse)
    ciftTıkla(mouse)
    mouseGotur(pozisyon_kapama_noktasi,mouse)
    tekTık(mouse)
    bekle(5)
    mouseGotur(tamam_noktasi, mouse)
    tekTık(mouse)

def renameResult(result):
    result = result.replace("?", "7")
    result = result.replace("S", "5")
    result = result.replace("U", "9")
    result = result.replace("C","0")
    return result



def stochResmiSayiyaCevir(nokta,genislik):
    im1 = pyautogui.screenshot(region=(nokta[0], nokta[1], genislik[0], genislik[1]))
    im1 = resmiBuyut(im1)




    result = pytesseract.image_to_string(im1)
    bekle(0.1)
    result = renameResult(result)


    try:
        result = int(result[0]+result[1])
    except ValueError:

        try:
            result = int(result[0])
        except ValueError:
            result = "Okunamadı."

    finally:
        # Rapor Temp İşlemleri
        global temp_image
        temp_image = im1
        global temp_result
        temp_result = str(result)

        return result

def raporDöküm():
    temp_image.save("C:\\Users\\Administrator\\PycharmProjects\\robot\\rapor\\" + temp_result + ".jpg")


def bekle(sleep_time = 5):
    time.sleep(sleep_time)

def mouseGotur(tuple,mouse):
    mouse.position = tuple

def tekTık(mouse):
    mouse.click(Button.left,1)

def ciftTıkla(mouse):
    mouse.click(Button.left,2)

def al(mouse):
    mouseGotur(doviz_noktasi, mouse)
    ciftTıkla(mouse)
    mouseGotur(al_noktasi, mouse)
    tekTık(mouse)
    mouseGotur(tamam_noktasi,mouse)
    bekle(3)
    tekTık(mouse)

def sat(mouse):
    mouseGotur(doviz_noktasi, mouse)
    ciftTıkla(mouse)
    mouseGotur(sat_noktasi, mouse)
    tekTık(mouse)
    mouseGotur(tamam_noktasi,mouse)
    bekle(3)
    tekTık(mouse)


def pozisyonTürüBelirle():
    im1 = pyautogui.screenshot(region=(pozisyon_noktasi[0], pozisyon_noktasi[1], pozisyon_genislik[0], pozisyon_genislik[1]))
    result = pytesseract.image_to_string(im1)

    if (result == "buy") | (result == "sell"):

        return result
    else:

        return "Pozisyon yok"





def metatraderbot():



    mouse = Controller()
    mouseGotur(stoch_nokta,mouse)
    sayac = 0

    while True:
        sonuc = stochResmiSayiyaCevir(stoch_nokta,stoch_genislik)

        if sonuc >= 80:
            if pozisyonTürüBelirle()=="buy":
                pozisyonkapa(mouse,Button)
                sat(mouse)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            elif pozisyonTürüBelirle() == "Pozisyon yok":
                sat(mouse)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            else:
                continue

        elif sonuc <=20:
            if pozisyonTürüBelirle() == "sell":
                pozisyonkapa(mouse,Button)
                al(mouse)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            elif pozisyonTürüBelirle() == "Pozisyon yok":
                al(mouse)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            else:
                continue


        bekle(3)




#----------------------Consoleeeeeeeeee----------------------



class MyException(Exception
                  ):
    def __init__(self, x, y):
        self.x = x
        self.y = y




class console(tk.Frame):




    def __init__(self,parent):

        tk.Frame.__init__(self,parent)




        #al Noktasi

        self.alNoktasiButton = tk.Button(self, text ="Al Noktasi Belirle",width = 25)
        self.alNoktasiButton.grid(row = 0, column=0, sticky ='W')
        self.alNoktasiButton.bind("<Button-1>", self.setLabelsAlNoktasi)



        self.entryAlX= tk.Entry(self, text ="")
        self.entryAlX.insert(tk.END, "0")
        self.entryAlX.grid(row = 0, column=1, sticky ='W')


        self.entryAlY = tk.Entry(self, text="")
        self.entryAlY.insert(tk.END, "0")
        self.entryAlY.grid(row = 0, column=2, sticky ='W')


        self.fotoCekButton = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButton.grid(row = 0,column=3,sticky = 'W')
        self.fotoCekButton.bind("<Button-1>", self.fotoCekAlNoktasi)

        # sat Noktasi

        self.satNoktasıButton = tk.Button(self, text="Sat Noktasi Belirle",width = 25)
        self.satNoktasıButton.grid(row=1, column=0, sticky='W')
        self.satNoktasıButton.bind("<Button-1>", self.setLabelsSatNoktasi)

        self.entrySatX = tk.Entry(self, text="")
        self.entrySatX.insert(tk.END, "0")
        self.entrySatX.grid(row=1, column=1, sticky='W')

        self.entrySatY = tk.Entry(self, text="")
        self.entrySatY.insert(tk.END,"0")
        self.entrySatY.grid(row=1, column=2, sticky='W')

        self.fotoCekButtonsat = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButtonsat.grid(row=1, column=3, sticky='W')
        self.fotoCekButtonsat.bind("<Button-1>", self.fotoCekSatNoktasi)

        # usdtry Noktasi

        self.dovizNoktasıButton = tk.Button(self, text="Doviz Noktasi Belirle",width = 25)
        self.dovizNoktasıButton.grid(row=2, column=0, sticky='W')
        self.dovizNoktasıButton.bind("<Button-1>", self.setLabelsDovizNoktasi)

        self.entryDovizX = tk.Entry(self, text="")
        self.entryDovizX.insert(tk.END, "0")
        self.entryDovizX.grid(row=2, column=1, sticky='W')

        self.entryDovizY = tk.Entry(self, text="")
        self.entryDovizY.insert(tk.END,"0")
        self.entryDovizY.grid(row=2, column=2, sticky='W')

        self.fotoCekButton = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButton.grid(row=2, column=3, sticky='W')
        self.fotoCekButton.bind("<Button-1>", self.fotoCekUsdNoktasi)

        # tamam Noktasi

        self.tamamNoktasıButton = tk.Button(self, text="Tamam Noktasi Belirle",width = 25)
        self.tamamNoktasıButton.grid(row=3, column=0, sticky='W')
        self.tamamNoktasıButton.bind("<Button-1>", self.setLabelsTamamNoktasi)

        self.entryTamamX = tk.Entry(self, text="")
        self.entryTamamX.insert(tk.END, "0")
        self.entryTamamX.grid(row=3, column=1, sticky='W')

        self.entryTamamY = tk.Entry(self, text="")
        self.entryTamamY.insert(tk.END,"0")
        self.entryTamamY.grid(row=3, column=2, sticky='W')

        self.fotoCekButton = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButton.grid(row=3, column=3, sticky='W')
        self.fotoCekButton.bind("<Button-1>", self.fotoCekTamamNoktasi)

        # Pozisyonu Belirleme Noktasi

        self.pozisyonBelirlemeNoktasi = tk.Button(self, text="Pozisyon Noktasi Belirle",width = 25)
        self.pozisyonBelirlemeNoktasi.grid(row=4, column=0, sticky='W')
        self.pozisyonBelirlemeNoktasi.bind("<Button-1>", self.setLabelsPozisyonBelirlemeNoktasi)

        self.entryPozisyonBelirlemeX = tk.Entry(self, text="")
        self.entryPozisyonBelirlemeX.insert(tk.END,pozisyon_noktasi[0])
        self.entryPozisyonBelirlemeX.grid(row=4, column=1, sticky='W')

        self.entryPozisyonBelirlemeY = tk.Entry(self, text="")
        self.entryPozisyonBelirlemeY.insert(tk.END,pozisyon_noktasi[1])
        self.entryPozisyonBelirlemeY.grid(row=4, column=2, sticky='W')

        self.fotoCekButton = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButton.grid(row=4 , column=3, sticky='W')
        self.fotoCekButton.bind("<Button-1>", self.fotoCekPozisyonNoktasi)

        # Pozisyon Kapama Noktasi

        self.pozisyonKapamaNoktasi = tk.Button(self, text="Pozisyon Kapama Belirle",width = 25)
        self.pozisyonKapamaNoktasi.grid(row=5, column=0, sticky='W')
        self.pozisyonKapamaNoktasi.bind("<Button-1>", self.setLabelsPozisyonKapamaBelirlemeNoktasi)

        self.entryPozisyonKapamaBelirlemeX = tk.Entry(self, text="")
        self.entryPozisyonKapamaBelirlemeX.insert(tk.END, "0")
        self.entryPozisyonKapamaBelirlemeX.grid(row=5, column=1, sticky='W')

        self.entryPozisyonKapamaBelirlemeY = tk.Entry(self, text="")
        self.entryPozisyonKapamaBelirlemeY.insert(tk.END,"0")
        self.entryPozisyonKapamaBelirlemeY.grid(row=5, column=2, sticky='W')

        self.fotoCekButton = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButton.grid(row=5 , column=3, sticky='W')
        self.fotoCekButton.bind("<Button-1>", self.fotoCekPozisyonKapamaNoktasi)


        # Stoch Belirleme Noktasi

        self.stochBelirlemeNoktasi = tk.Button(self, text="Stoch Noktasi Belirle", width=25)
        self.stochBelirlemeNoktasi.grid(row=6, column=0, sticky='W')
        self.stochBelirlemeNoktasi.bind("<Button-1>", self.setLabelsStochBelirlemeNoktasi)

        self.entryStochX = tk.Entry(self, text="")
        self.entryStochX.insert(tk.END,stoch_nokta[0])
        self.entryStochX.grid(row=6, column=1, sticky='W')

        self.entryStochY = tk.Entry(self)
        self.entryStochY.insert(tk.END,stoch_nokta[1])
        self.entryStochY.grid(row=6, column=2, sticky='W')

        self.fotoCekButton = tk.Button(self, text="Fotografını Cek",width=25)
        self.fotoCekButton.grid(row=6, column=3, sticky='W')
        self.fotoCekButton.bind("<Button-1>", self.fotoCekStochNoktasi)

        # Stoch Okuduğu Değer

        self.stochOkumaNoktasi = tk.Label(self, text="Okunan Değer", width=25)
        self.stochOkumaNoktasi.grid(row=7, column=0, sticky='W')


        self.OkunanDeger = tk.Label(self, text=".......")
        self.OkunanDeger.grid(row=7, column=1, sticky='W')


        # Baslatma Button Noktasi

        self.baslatButton = tk.Button(self, text="Başlat",width=25)
        self.baslatButton.grid(row=8,column = 3,sticky='W')


        self.baslatButton.bind("<Button-1>", self.baslatButtonActivity)



    def setLabelsAlNoktasi(self, event= None):



        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entryAlX.delete(0, "end")
                self.entryAlY.delete(0, "end")
                self.entryAlX.insert(0, e.x)
                self.entryAlY.insert(0, e.y)






    def setLabelsSatNoktasi(self, event=None):

        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entrySatX.delete(0, "end")
                self.entrySatY.delete(0, "end")
                self.entrySatX.insert(0, e.x)
                self.entrySatY.insert(0, e.y)




    def setLabelsDovizNoktasi(self, event=None):

        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entryDovizX.delete(0, "end")
                self.entryDovizY.delete(0, "end")
                self.entryDovizX.insert(0, e.x)
                self.entryDovizY.insert(0, e.y)



    def setLabelsTamamNoktasi(self, event=None):

        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entryTamamX.delete(0, "end")
                self.entryTamamY.delete(0, "end")
                self.entryTamamX.insert(0, e.x)
                self.entryTamamY.insert(0, e.y)




    def setLabelsPozisyonBelirlemeNoktasi(self, event=None):

        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entryPozisyonBelirlemeX.delete(0, "end")
                self.entryPozisyonBelirlemeY.delete(0, "end")
                self.entryPozisyonBelirlemeX.insert(0, e.x)
                self.entryPozisyonBelirlemeY.insert(0, e.y)


    def setLabelsPozisyonKapamaBelirlemeNoktasi(self, event=None):

        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entryPozisyonKapamaBelirlemeX.delete(0, "end")
                self.entryPozisyonKapamaBelirlemeY.delete(0, "end")
                self.entryPozisyonKapamaBelirlemeX.insert(0, e.x)
                self.entryPozisyonKapamaBelirlemeY.insert(0, e.y)


    def setLabelsStochBelirlemeNoktasi(self, event=None):

        with Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except MyException as e:
                self.entryStochX.delete(0, "end")
                self.entryStochY.delete(0, "end")
                self.entryStochX.insert(0, e.x)
                self.entryStochY.insert(0, e.y)


    def baslatButtonActivity(self, event=None):

        flag = True
        if not ((self.entryAlY.get() == "0") | (self.entryAlX.get() =="0") | (self.entrySatY.get() == "0") | (self.entrySatX.get() == "0") | (self.entryDovizY.get() == "0") | (self.entryDovizX.get() =="0") | (self.entryTamamY.get() == "0") | (self.entryTamamX.get() =="0") | (self.entryPozisyonBelirlemeY.get() == "0") | (self.entryPozisyonBelirlemeX.get() =="0") | (self.entryStochY.get() == "0") | (self.entryStochX.get() =="0")):
            flag = False

        if flag:
            messagebox.showinfo("Uyarı!!","Herhangi Kordinatlardan biri 0 olmamalı")
        else:


            doviz_noktasi[0] = int(self.entryDovizX.get())
            doviz_noktasi[1] = int(self.entryDovizY.get())

            al_noktasi[0] = int(self.entryAlX.get())
            al_noktasi[1] = int(self.entryAlY.get())

            sat_noktasi[0]= int(self.entrySatX.get())
            sat_noktasi[1] = int(self.entrySatY.get())

            pozisyon_noktasi[0] = int(self.entryPozisyonBelirlemeX.get())
            pozisyon_noktasi[1] = int(self.entryPozisyonBelirlemeY.get())


            pozisyon_kapama_noktasi[0] = int(self.entryPozisyonKapamaBelirlemeX.get())
            pozisyon_kapama_noktasi[1] = int(self.entryPozisyonKapamaBelirlemeY.get())


            tamam_noktasi[0] = int(self.entryTamamX.get())
            tamam_noktasi[1] = int(self.entryTamamY.get())


            stoch_nokta[0] = int(self.entryStochX.get())
            stoch_nokta[1] = int(self. entryStochY.get())


            metatraderbot()







    def fotoCekAlNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entryAlX.get()) , int(self.entryAlY.get()), stoch_genislik[0], stoch_genislik[1]))
        im1.show()


    def fotoCekSatNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entrySatX.get()) , int(self.entrySatY.get()), stoch_genislik[0], stoch_genislik[1]))
        im1.show()



    def fotoCekUsdNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entryDovizX.get()) , int(self.entryDovizY.get()), stoch_genislik[0], stoch_genislik[1]))
        im1.show()


    def fotoCekTamamNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entryTamamX.get()) , int(self.entryTamamY.get()), stoch_genislik[0], stoch_genislik[1]))
        im1.show()


    def fotoCekPozisyonNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entryPozisyonBelirlemeX.get()) , int(self.entryPozisyonBelirlemeX.get()), pozisyon_genislik[0], pozisyon_genislik[1]))
        im1.show()



    def fotoCekPozisyonKapamaNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entryPozisyonKapamaBelirlemeX.get()) , int(self.entryPozisyonKapamaBelirlemeY.get()), stoch_genislik[0], stoch_genislik[1]))
        im1.show()


    def fotoCekStochNoktasi(self, event=None):
        im1 = pyautogui.screenshot(region=(int(self.entryStochX.get()) , int(self.entryStochY.get()), stoch_genislik[0], stoch_genislik[1]))
        im1.show()
        noktaX = int(self.entryStochX.get())
        noktaY = int(self.entryStochY.get())
        nokta = (noktaX,noktaY)
        result = self.stochResmiSayiyaCevir(nokta,stoch_genislik)
        print(result)
        self.OkunanDeger.config(text = result)








    def on_click(self,x, y, button, pressed):

        if pressed:
            raise MyException(x=x,y=y)

    def stochResmiSayiyaCevir(self,nokta, genislik):

        im1 = pyautogui.screenshot(region=(nokta[0], nokta[1], genislik[0], genislik[1]))

        im1 = self.resmiBuyut(im1)
        im1.show()


        result = pytesseract.image_to_string(im1)
        self.bekle(0.1)
        result = self.renameResult(result)
        try:
            result = int(result[0]+result[1])
        except ValueError:

            try:
                result = int(result[0])
            except ValueError:
                result = "Okunamadı."

        finally:
            return result

    def renameResult(self,result):
        result = result.replace("?", "7")
        result = result.replace("S", "5")
        result = result.replace("U", "9")
        result = result.replace("C", "0")
        return result

    def bekle(self,sleep_time=5):
        time.sleep(sleep_time)

    def resmiBuyut(self,image):
        basewidth = 300
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        img = image.resize((basewidth, hsize), Image.ANTIALIAS)
        return img



#----------------------Consoleeeeeeeeee----------------------
if __name__ == '__main__':


    root = tk.Tk()

    console(root).pack()
    root.mainloop()
