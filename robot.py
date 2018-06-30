from pynput.mouse import Button, Controller
from PIL import Image
import time
import pyautogui
import pytesseract
import os


#HARD CODE
#-------------
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
usdtry = (51,145)
al_noktasi =  (1200,655)
sat_noktasi = (1040,655)
stoch_nokta = (394, 535)
stoch_genislik = (20.5, 13)
pozisyon_noktasi = (670,836)
pozisyon_genislik = (38,17)
tamam_noktasi = (1040,688)
pozisyon_kapama_noktasi = (1040,688)

dir_path = os.getcwd()

temp_image = Image
temp_result = ""

#--------------


def resmiBuyut(image):
    basewidth = 300
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    img = image.resize((basewidth, hsize), Image.ANTIALIAS)
    return img

def pozisyonkapa(mouse,Button):
    mouseGotur(pozisyon_noktasi,mouse)
    ciftTıkla(mouse,Button)
    mouseGotur(pozisyon_kapama_noktasi,mouse)
    tekTık(mouse,Button)
    bekle(5)
    mouseGotur(tamam_noktasi, mouse)
    tekTık(mouse,Button)

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
    while 1:

        try:
            result = int(result)
        except ValueError:

            im1 = pyautogui.screenshot(region=(nokta[0]+3, nokta[1], genislik[0], genislik[1]))
            im1 = resmiBuyut(im1)


            result = pytesseract.image_to_string(im1)
            bekle(0.1)
            result = renameResult(result)
            result = float(result)

            break
        finally:

            # Rapor Temp İşlemleri
            global temp_image
            temp_image = im1
            global temp_result
            temp_result = str(result)

            return int(result)
def raporDöküm():
    temp_image.save(dir_path + "\\rapor\\" + temp_result + ".jpg")


def bekle(sleep_time = 5):
    time.sleep(sleep_time)

def mouseGotur(tuple,mouse):
    mouse.position = tuple

def tekTık(mouse, Button):
    mouse.press(Button.left)
    mouse.release(Button.left)

def ciftTıkla(mouse, Button):
    tekTık(mouse, Button)
    tekTık(mouse, Button)

def al(mouse,Button):
    mouseGotur(usdtry, mouse)
    ciftTıkla(mouse, Button)
    mouseGotur(al_noktasi, mouse)
    tekTık(mouse, Button)
    mouseGotur(tamam_noktasi,mouse)
    bekle(3)
    tekTık(mouse,Button)

def sat(mouse,Button):
    mouseGotur(usdtry, mouse)
    ciftTıkla(mouse, Button)
    mouseGotur(sat_noktasi, mouse)
    tekTık(mouse, Button)
    mouseGotur(tamam_noktasi,mouse)
    bekle(3)
    tekTık(mouse,Button)


def pozisyonTürüBelirle():
    im1 = pyautogui.screenshot(region=(pozisyon_noktasi[0], pozisyon_noktasi[1], pozisyon_genislik[0], pozisyon_genislik[1]))
    result = pytesseract.image_to_string(im1)

    if (result == "buy") | (result == "sell"):

        return result
    else:

        return "Pozisyon yok"




if __name__ == '__main__':

    mouse = Controller()
    sayac = 0

    while True:
        sonuc = stochResmiSayiyaCevir(stoch_nokta,stoch_genislik)

        if sonuc >= 80:
            if pozisyonTürüBelirle()=="buy":
                pozisyonkapa(mouse,Button)
                sat(mouse,Button)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            elif pozisyonTürüBelirle() == "Pozisyon yok":
                sat(mouse, Button)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            else:
                continue

        elif sonuc <=20:
            if pozisyonTürüBelirle() == "sell":
                pozisyonkapa(mouse,Button)
                al(mouse,Button)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            elif pozisyonTürüBelirle() == "Pozisyon yok":
                al(mouse, Button)
                sayac += 1
                raporDöküm()
                print(sayac)
                bekle(2)
            else:
                continue


        bekle(3)
        






