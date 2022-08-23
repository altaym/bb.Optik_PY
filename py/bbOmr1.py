import cv2
import numpy as np
import os
import argparse
import datetime
import json
from openpyxl import Workbook,load_workbook
from imutils.perspective import four_point_transform
import pdf2image 
import bbOmr

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

gruplar =['A','B','C','D','E'] #['Q','X','Y','Z','T']


""" alan tanımlamaları
isim_img = image[119:464,265:532]
no_image = image[335:460, 71:192]
grup = thresh[216:238, 130:253]
"""
soruSayisi = 60
secenekSayisi = 4

imgSonuc = cv2.imread('testForm.png',0)
imgSonuc = cv2.resize(imgSonuc ,(600,800))

def test():
    img = cv2.imread('testForm.png',0)
    img = cv2.resize(img,(600,800))
    
    #ret,thresh = cv2.threshold(img,127,255,0)
    aAdSoyad = img[119:464,265:532]    
    aGrup = img[380:412, 300:312]
    # aOgrenciNo = img[335:460, 71:192]
    aCevaplar = img[310:706, 74:146]
    
    # cv2.imshow("sec",aGrup)
    # cv2.waitKey(0)
    
    
    # isim = getAdSoyad(aAdSoyad)
    # no = getOgrenciTCNo(aOgrenciNo,10)
    #grup = getGrup(aGrup, 2, 1 )
    
    artis = 2
    for i in range(0,2):
        harf = aGrup[artis:artis + 11, 0:11]
        artis += 11
        if i%4 ==0:
            artis +=1
        bps = np.sum(harf == 255)
        if bps>50:
            grup = i
        elif i==29 and bps<50:
            grup =  "-1"

    # def getAdSoyad(aAdSoyad , basamakSayisi = 22 ):
    # image = cv2.cvtColor(aAdSoyad, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(aAdSoyad2, (7,7), 0)
    thresh = cv2.threshold(aAdSoyad, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    artis = 1
    isim = ""
    basamakSayisi = 2
    for i in range(0, basamakSayisi ):
        cevap = thresh[0:342,artis:artis+11]
        harf = harf_cikar(cevap)
        isim +=harf
        artis += 12    
    return isim.strip()

    # ogrenci_cevap = getCevaplar(aCevaplar, 1 )
    # print("form 1 >> ",  grup , ogrenci_cevap )


def test2():
    # paper = four_point_transform(os.path.join(root, name), docCnt.reshape(4, 2))
    # cv2.drawContours(paper, [cnts[k]], -1, "red", 3)
    
    # mask = np.zeros(thresh.shape, dtype="uint8")
    # cv2.drawContours(mask,-1,"red",3)
    
    # rect = cv2.minAreaRect(cnt)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(img,[box],0,(0,0,255),2)

    # im = cv2.imread('test.png')
    # imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # cnt = contours[4]
    # # cv2.drawContours (img, [ cnt ], 0, (0,255,0), 3)
    # cv2.drawContours (im2, contours , 0, (0,255,0), 3)
    # cv2.imshow("kontur",im)
    # cv2.waitKey(0)


    # Let's load a simple image with 3 black squares
    image = cv2.imread('test.png')
    image = cv2.resize(image,(600,800))
    #cv2.waitKey(0)

    img = image
    cv2.circle(img,(447,63), 5 , (0,0,255), 1 )
    cv2.imshow("daire",img)

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)
    #cv2.waitKey(0)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.imshow('Canny Edges After Contouring', edged)
    #cv2.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    cv2.imshow('Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test0():
    img = cv2.imread('test.png',0)
    img = cv2.resize(img,(600,800))
    
    img2 = cv2.imread('bbtest.png',0)
    img2 = cv2.resize(img2,(600,800))
    #ret,thresh = cv2.threshold(img,127,255,0)
    aAdSoyad = img[119:464,265:532]
    aAdSoyad2 = img2[118:453,304:574] 
    
    aGrup = img[222:238, 130:253]
    aGrup2 = img2[500:512, 400:450]
    aOgrenciNo = img[335:460, 71:192]
    aOgrenciNo2 = img2[292:408, 38:172]
    aCevaplar = img[484:710, 74:534] # cevaplar 226,460
    
    # cv2.imshow("sec",aCevaplar)
    # cv2.waitKey(0)
    
    isim = getAdSoyad(aAdSoyad)
    no = getOgrenciTCNo(aOgrenciNo,10)
    grup = getGrup(aGrup, 4, 1 )
    ogrenci_cevap = getCevaplar(aCevaplar, 3 )
    print("form 1 >> ", no, isim, grup , ogrenci_cevap )


    cv2.imshow("sonuc", imgSonuc)
    cv2.waitKey(0)
    # no2 = getOgrenciTCNo(aOgrenciNo2,11)
    # isim2 = getAdSoyad(aAdSoyad2)
    # grup2 = getGrup(aGrup2, 4 )
    # print ("form 2 >> ", no2, isim2 , grup2)

    # 10, 100,190,280,370
    # 10, 105,200

    # lmargin = 105 
    # rm = 64
    # thresh = cv2.threshold(aCevaplar, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cevap = thresh[0:250, lmargin : lmargin + rm] 
    # cv2.imshow("cevap",cevap)
    # cv2.waitKey(0)


def pdfCoz():
    pages = pdf2image.pdf2image.convert_from_path("d:/_temp/optik/test.pdf", 200, args.ogrencioptik)
    testCounter = 1
    for page in pages:
        filename = args.ogrencioptik +"/" + str(testCounter)+".png"
        page.save(filename, 'png') 
        testCounter +=  1


def getCevaplar(aCevaplar, sutunSayisi = 1  ):
    lmargin = 10
    rm = 64
    rowTop = 0
    rowBottom = 12

    thresh = cv2.threshold(aCevaplar, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    for s in range(0, sutunSayisi ): 
        print(lmargin)
        if not np.sum(thresh == 255) > 4000:
            for i in range(20):
                ogrenci_cevap.setdefault(s * 20 + i, cevaplar[6])
        else:
            for row in range(0,20):
                cevap = thresh[rowTop:rowBottom, lmargin : lmargin + rm] 
                ret = kontrolCevap(cevap)
                ogrenci_cevap.setdefault(s * 20 + row +1  ,ret)
                rowBottom += 11
                rowTop += 11
                if row % 4 == 0:
                    rowTop += 1
                    rowBottom += 1
        lmargin += 95
        rowTop = 0
        rowBottom = 12

    return ogrenci_cevap

def kontrolCevapCiz( koord ): # koordinat bilgisi düzenlenecek
    # image = cv2.imread("test.png")
    cv2.circle(imgSonuc , koord  , 5, (0,0,255), 1)
    #cv2.circle(image ,(447,63), 5 , (0,0,255), 1 )

def kontrolCevap(image):
    artis = 0
    array = []
    for j in range(0,5):
        siklar = image[0:12,artis:artis+12]
        # cv2.imshow("ter",siklar)
        # cv2.waitKey(0)
        artis +=12
        bps = np.sum(siklar == 255)
        if bps >= 30:
            array.append(cevaplar[j])
    if len(array) == 0:
        return cevaplar[6]
    elif len(array) == 1:
        return array[0]
    else:
        return cevaplar[5]

def getGrup(aGrup, grupSayisi = 4, bosluk = 0 ):
    bosluk += 1 
    if args.grup == 1:
        artis = 0
        secenek = -1
        thresh = cv2.threshold(aGrup, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        for i in range(0, grupSayisi ):
            grup = thresh[1:21, artis : artis + (12 * bosluk) ]
            bps = np.sum(grup==255)
            artis += (12 * bosluk)
            if bps>=60 and bps<=95:
                secenek = i
                break
        return gruplar[secenek]
    else:
        return 0

def getOgrenciTCNo(aOgrenciNo, basamakSayisi = 11 ):
    # gray = cv2.cvtColor(aOgrenciNo, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(aOgrenciNo, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    numara = ""
    artis = 1
    for i in range(0, basamakSayisi):
        kolon = thresh[0:124,artis:artis+11]
        artis +=12
        sayi = sayi_cikar(kolon)
        numara += sayi
    return numara

def getAdSoyad(aAdSoyad , basamakSayisi = 22 ):
    # image = cv2.cvtColor(aAdSoyad, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(aAdSoyad2, (7,7), 0)
    thresh = cv2.threshold(aAdSoyad, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    artis = 1
    isim = ""
    for i in range(0, basamakSayisi ):
        cevap = thresh[0:342,artis:artis+11]
        harf = harf_cikar(cevap)
        isim +=harf
        artis += 12    
    return isim.strip()



# yardımcı 
def sayi_cikar(img):
    artis = 0
    for i in range(0, 11):
        sayi = img[artis:artis + 11, 0:11]
        if i % 4 == 0:
            artis += 1
        artis += 11
        bps = np.sum(sayi == 255)
        if bps > 40 and i == 10:
            return '-'
        elif bps >40 and i<10:
            return str(i)

def harf_cikar(image):
    artis = 2
    for i in range(0,30):
        harf = image[artis:artis + 11,0:11]
        artis += 11
        if i%4 ==0:
            artis +=1
        bps = np.sum(harf == 255)
        if bps>50:
            return harfler[i]
        elif i==29 and bps<50:
            return harfler[-1]


def main():
    for root, dirs, files in os.walk(args.ogrencioptik, topdown=False):
        for index,name in enumerate( files):
            answers,no,name, grup  = alan_crop(os.path.join(root, name))
            sonuc = f"{index+1} {no} {name} {grup} {answers}\n"
            print( sonuc )
            with open("okuyucu.txt","a",encoding="UTF-8") as f:
                f.write(sonuc)


test()