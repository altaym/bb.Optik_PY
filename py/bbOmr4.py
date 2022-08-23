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

    aCevaplar = img[228:530, 46:96]
cv.rectangle(img,(46,228),(96,530), (0,255,0), 1)
"""

boble = 12
topMargin = 0
leftMargin = 0

def controlArea(img,  satirSayisi:int = 20, colonSayisi:int = 4 , xUzunluk:int = 12, yUzunluk:int = 12 , dikeyDuzeltme : bool = False , duzeltmeMiktari :int = 1 , sutunSayisi = 1 , sutunSolBosluk = 0):
    kx = xUzunluk
    ky = yUzunluk
    rky = 0 
    for sutun in range(0, sutunSayisi):
        rky = 0 
        x = ( colonSayisi + sutunSolBosluk ) * kx * sutun
        if sutun % 2 == 0:
            x += 3

        for r in range(0,satirSayisi):
            for s in range(0, colonSayisi ):
                skx = s * kx
                start_point = ( x + skx      ,  rky      ) 
                end_point =   ( x + skx + kx ,  rky + ky )
                color = (255, 0, 0)
                thickness = 1
                cv.rectangle(img, start_point, end_point, color, thickness)

            rky += ky  # r * ky
            if dikeyDuzeltme and r % 4 == 0 :
                rky += duzeltmeMiktari
          
    cv.imshow("kontrol", img)
    cv.waitKey(0) 




def test():
    # img = cv.imread('test.png')
    # img = cv.resize(img,(600,800))
    # row , col = int( 800/12 ), int(600/12)

    img = cv.imread("testForm.png")
    img = cv.resize(img, (400,600))
    row , col = int( 600/12 ), int(400/12)
    
    print(row, col)

    x = 0
    y = 11
    for r in range(0, row ):
        for c in range(0, col ):
            start_point = ( x + c * 12     ,  y+ r * 12     ) 
            end_point =   ( x + c * 12 + 12 , y+ r * 12 + 12 )
            color = (255, 0, 0)
            thickness = 1
            cv.rectangle(img, start_point, end_point, color, thickness)
     
        # if r % 4 == 0 :
        #     y +=1

    cv.imshow("bb",img)
    cv.waitKey(0)
   


def controlArea0(img,  satirSayisi:int = 20, sutunSayisi:int = 4 , xUzunluk:int = 12, yUzunluk:int = 12 , dikeyDuzeltme : bool = False , duzeltmeMiktari :int = 1 ):
    kx = xUzunluk
    ky = yUzunluk
    rky = 0 
    for r in range(0,satirSayisi):
        for s in range(0, sutunSayisi):
            skx = s * kx
            start_point = ( skx      , rky      ) 
            end_point =   ( skx + kx , rky + ky )
            color = (255, 0, 0)
            thickness = 1
            cv.rectangle(img, start_point, end_point, color, thickness)

        rky += ky  # r * ky
        if dikeyDuzeltme and r % 4 == 0 :
            rky += duzeltmeMiktari
          
    cv.imshow("kontrol", img)
    cv.waitKey(0) 

  
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