import cv2 as cv
import numpy as np
import os
import argparse
import datetime
import json
from openpyxl import Workbook,load_workbook
from imutils.perspective import four_point_transform
import pdf2image 
from enum import Enum

class OkumaYonu(Enum):
    DIKEY = 0
    YATAY = 1

parser = argparse.ArgumentParser(description='Optik Okuyucu V.1.0')
parser.add_argument('--ogrencioptik', type=str, help='Ogrencilerin optiklerinin bulunduğu klasör...', default="d:/_temp/optik/ogrenciler")
parser.add_argument('--cevapkagidi', type=str, help='Cevap Kağıtlarının olduğu klasör...', default="d:/_temp/optik/cevapkagidi")
parser.add_argument('--sonuckayit',type=str,help='Sonuçların txt olarak kaydedileceği yer...', default="d:/_temp/optik/")
parser.add_argument('--sonucisim',type=str,help='Oluşturulacak excel dosyasının adı...',default= "sonuclar")
parser.add_argument('--grup',type=int,help='Grup varmı yok mu ? ...', default=True)
parser.add_argument('--yanlisdogru',type=int,help='Kaç yanlış bir doğruyu götürsün? ...',default=100)
parser.add_argument('--puanlama',type=int,help='Sınav Kaç Üzerinden Hesaplansın?...',default=100)
args = parser.parse_args()


cevaplar=['A','B','C','D','E','-1','0']
harfler =['A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö', 'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z', ' ']
cevap_kagidi = {}
cevap_kagidi_dict = {}
ogrenci_cevap = {}

gruplar =['A','B','C','D','E'] 
# gruplar =['Q','X','Y','Z','T']
rakamlar =['0','1','2','3','4','5','6','7','8','9','-']

""" alan tanımlamaları
isim_img = image[119:464,265:532]
no_image = image[335:460, 71:192]
grup = thresh[216:238, 130:253]

    # for i in range(0,secenekSayisi):
    #     #siklar = aCevaplar[0:num_rows , boble * i  : boble * i + boble]
    #     siklar = aCevaplar[ boble * i  : boble * i + boble , 0: num_columns]
    #     cv.imshow("test",siklar)
    #     cv.waitKey(0)

"""

boble = 12
topMargin = 0
leftMargin = 0

def test():
    img = cv.imread('testForm.png',0)
    img = cv.resize(img,(600,800))
    

    aGrup = img[380:412, 300:312]
    aCevaplar = img[310:706, 73:141]

    sonuc = getArea(aGrup, gruplar )
    sonuc1  = getCevaplar(aCevaplar,  23 )
    print(sonuc, sonuc1)

    # img = cv.imread('test.png',0)
    # img = cv.resize(img,(600,800))
    
    # img2 = cv.imread('bbtest.png',0)
    # img2 = cv.resize(img2,(600,800))
    # aAdSoyad = img[121:461,265:532]
    # aAdSoyad2 = img2[118:453,304:574] 
    
    # aGrup = img[222:238, 130:253]
    # aGrup2 = img2[500:512, 400:450]
    # aOgrenciNo = img[335:460, 71:192]
    # aOgrenciNo2 = img2[292:408, 38:172]
    # aCevaplar = img[484:710, 84:532] # cevaplar 226,460
    

    # isim = getArea(aAdSoyad , harfler , 31, 22 )
    # print(isim)
    # no = getArea(aOgrenciNo, rakamlar, 10)
    # grup = "X" # getGrup(aGrup, 4, 1 )
    # ogrenci_cevap = getCevaplar(aCevaplar, 20, 5, 3, 3 )
    # print("form 1 >> ", no, isim, grup , ogrenci_cevap )

  
def getArea(aImage, karakterGrubu  ,  satir =1 , sutun = 1, bosluk = 0 , yon : OkumaYonu  = 0 ):
    thresh = cv.threshold(aImage , 0, 255 , cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    num_rows = np.shape(thresh)[0]
    sonuc = ""
    for i in range(0, sutun ):
        hucre = thresh[0:num_rows , boble * i  : boble * (i + 1)  ]
        karakter = karakterCikar(hucre, karakterGrubu)
        sonuc += karakter
    return sonuc


def getCevaplar(aCevaplar, soruSayisi = 20, secenekSayisi = 4, sutunSayisi = 1 , sutunSolBosluk = 0):
    thresh = cv.threshold(aCevaplar, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    for sutun in range(0, sutunSayisi ): 
        rowTop = 0
        rowBottom = boble
        x = ( secenekSayisi + sutunSolBosluk ) * boble * sutun
        y = x + ( secenekSayisi  * boble )

        if not np.sum(thresh == 255) > 4000:
            for i in range(soruSayisi):
                ogrenci_cevap.setdefault(sutun * 20 + i, cevaplar[6])
        else:
            for row in range(0, soruSayisi ):
                # cevap = thresh[rowTop:rowBottom, sutunSolBosluk * sutun : sutunSolBosluk * sutun + boble * secenekSayisi ] 
                cevap = thresh[rowTop:rowBottom, x : y ] 
                ret = kontrolCevap(cevap, secenekSayisi )
                ogrenci_cevap.setdefault(sutun * 20 + row + 1  , ret)
                
                if row % 4 == 0:
                    rowTop += boble + 1
                    rowBottom += boble + 1
                else :
                    rowTop += boble
                    rowBottom += boble
                    
    return ogrenci_cevap

def kontrolCevap(image, secenekSayisi):
    array = []
    num_rows = np.shape(image)[0]
    for j in range(0, secenekSayisi ):
        secim = image[0:num_rows , boble * j : boble * (j + 1) ]
        bps = np.sum(secim == 255)
        if bps >= 30:
            array.append(cevaplar[j])
            st = cevaplar[j]
            print("<<", st )
    if len(array) == 0:
        return cevaplar[6]
    elif len(array) == 1:
        return array[0]
    else:
        return cevaplar[5]

def karakterCikar(img,karakterGrubu ):
    for i in range(0, 30):
        karakter = img[ boble * i  : boble * ( i + 1)  , 0: boble]
        bps = np.sum(karakter == 255)
        print(i, bps )
        if bps>50:
            return karakterGrubu[i]
        elif i==29 and bps<50:
            return karakterGrubu[-1]

def karakterCikar0(img,karakterGrubu ):
    artis =0
    for i in range(0, 30):
        karakter = img[artis:artis + 11, 0:11]
        if i % 4 == 0:
            artis += 1
        artis += 11
        bps = np.sum(karakter == 255)
        if bps>50:
            return karakterGrubu[i]
        elif i==29 and bps<50:
            return karakterGrubu[-1]



test()