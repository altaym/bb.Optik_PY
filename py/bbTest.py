import cv2 as cv
import numpy as np
import os
import argparse
import datetime
import json
from openpyxl import Workbook,load_workbook
from imutils.perspective import four_point_transform
import pdf2image
from bbOmr import bbOmr
from bbPars import *
# import omr

parser = argparse.ArgumentParser(description='Optik Okuyucu V.1.0')
parser.add_argument('--ogrencioptik', type=str, help='Ogrencilerin optiklerinin bulunduğu klasör...', default="d:/_temp/optik/ogrenciler")
parser.add_argument('--cevapkagidi', type=str, help='Cevap Kağıtlarının olduğu klasör...', default="d:/_temp/optik/cevapkagidi")
parser.add_argument('--sonuckayit',type=str,help='Sonuçların txt olarak kaydedileceği yer...', default="d:/_temp/optik/")
parser.add_argument('--sonucisim',type=str,help='Oluşturulacak excel dosyasının adı...',default= "sonuclar")
parser.add_argument('--grup',type=int,help='Grup varmı yok mu ? ...', default=True)
parser.add_argument('--yanlisdogru',type=int,help='Kaç yanlış bir doğruyu götürsün? ...',default=100)
parser.add_argument('--puanlama',type=int,help='Sınav Kaç Üzerinden Hesaplansın?...',default=100)
args = parser.parse_args()

cevap_kagidi = {}
cevap_kagidi_dict = {}
ogrenci_cevap = {}



bb = bbOmr()
args.ogrencioptik = "d:/_temp/optik/pdfImages"

def test():
        # img = cv.imread("111.png")
        # (h, w) = img.shape[:2]
        # imgMarker = img[0:h , 0:100]
        
        # markers, makImg = bb.getMarkers(imgMarker)
        # print("markers",markers)
        
        # angle = bb.get_angle(markers[-1], markers[0])
        # # print("Açı", angle)

        # img = bb.resimDondur(img, angle, True )

        # x = int((markers[-1][0] + markers[0][0])/2)
        # # y = markers[-1][1]
        # img = img[0:h, x: w]

        # img = cv.resize(img, (600, 800))
        # aGrup = img[380:410, 298:312]
        # aCevaplar = img[307:706, 50:120]
        # cv.imshow("cvp", aCevaplar)
        # cv.waitKey(0)

        # grup = bb.rArea(aGrup, 2, 1)
        # cevaplar = bb.rAreaX(aCevaplar, 23, 4, 17, 17, karakterGrubu= bb.cevaplar, dikeyDuzeltme= True, duzeltmeMiktari=1, olcek= 50)
        # # bb.rSave(name)
        # sonuc = f" {grup} {cevaplar}\n"
        # print(sonuc)
        
        # with open("bbSonuclar.txt", "a", encoding="UTF-8") as f:
        #         f.write(sonuc)
        
        # os.chdir("pdfImagesKontrol")
        # cv.imwrite("1x.png" , img )
        # os.chdir("..")

        test0()
       
def test2():
        
        # img = cv.imread('1.png')
        # img = cv.resize(img, (400, 600))
        # aGrup = img[284:310, 197:209]
        # aCevaplar = img[232:532, 47:95]
        # grup = bb.rArea(aGrup, 2, 1)
        # cevaplar = bb.rAreaX(aCevaplar, 23, 4, 12, 13, karakterGrubu= bb.cevaplar, dikeyDuzeltme= False)


        img = cv.imread('testForm.png')
        #img = bb.resimDondur(img)
        img = cv.resize(img, (600, 800))

        aGrup = img[380:410, 298:312]
        aCevaplar = img[307:706, 76:144]

        grup = bb.rArea(aGrup, 2, 1)
        cevaplar = bb.rAreaX(aCevaplar, 23, 4, 17, 17, karakterGrubu= bb.cevaplar, dikeyDuzeltme= True, duzeltmeMiktari=1, olcek= 50)

        # cevaplar = bb.rAreaX2(232,532, 47,95 , 23, 4, 12, 13, karakterGrubu= bb.cevaplar, dikeyDuzeltme= False)
        #  bb.rSave("1.png")
        cv.rectangle(img, (76,307),(144,706),(255,255,0),1)
        sonuc = f"{grup} {cevaplar}\n"
        print(sonuc)
        cv.imshow("kontrol",img)
        cv.waitKey(0)
        cv.destroyAllWindows()
      

def test1():
        """
        img = cv.imread('test.png')
        img = cv.resize(img,(600,800))

        aAdSoyad = img[121:461,264:532] 
        # aGrup = img[222:238, 130:253]
        aOgrenciNo = img[336:460, 71:192]
        aCevaplar = img[485:710, 83:535] # cevaplar 226,460



        t = bb.rArea(aAdSoyad, 30 , 22 , 12,11, True, karakterGrubu = bb.harfler)
        print(t)

        t = bb.rArea(aOgrenciNo, 10, 10 , 12, 11, False, karakterGrubu = bb.rakamlar)
        print(t)

        t= bb.getCevaplar(aCevaplar, 20, 5, 3, 3)
        print(t)
        # cv.imshow("read",t)
        cv.waitKey(0)
        cv.destroyAllWindows()
        """

def test0():
        #bb.pdfCoz("200dpi-dik.pdf","pdfImages")

        for root, dirs,files in os.walk(args.ogrencioptik, topdown= False):
                for index, name in enumerate(files):
                        img = cv.imread(os.path.join(root, name))
                        (h, w) = img.shape[:2]
                        imgMarker = img[0:h , 0:100]
                        
                        markers, makImg = bb.getMarkers(imgMarker)
                        print("markers",markers)
                        
                        angle = bb.get_angle(markers[-1], markers[0])
                        # print("Açı", angle)
                
                        img = bb.resimDondur(img, angle, True )

                        x = int((markers[-1][0] + markers[0][0])/2)
                        y = markers[-1][1]
                        # img = img[y:h, x: w]
                        img = img[0:h, x: w]
          
                        # img = cv.resize(img, (400, 600))

                        # aGrup = img[284:310, 197:209]
                        # aCevaplar = img[232:532, 47:95]

                        # grup  = bb.rArea( aGrup, 2, 1)
                        # cevaplar = bb.rAreaX(aCevaplar, 23, 4, 12, 13, karakterGrubu= bb.cevaplar, dikeyDuzeltme= False)
                        # img = bb.resimDondur(img)
                        img = cv.resize(img, (600, 800))
                        aGrup = img[380:410, 298:312]
                        # aCevaplar = img[307:706, 76:144]
                        aCevaplar = img[307:706, 50:121]

                        grup = bb.rArea(aGrup, 2, 1)
                        cevaplar = bb.rAreaX(aCevaplar, 23, 4, 17, 17, karakterGrubu= bb.cevaplar, dikeyDuzeltme= True, duzeltmeMiktari=1, olcek= 50)
                        # bb.rSave(name)
                        sonuc = f"{index+1} {grup} {cevaplar}\n"
                        print(sonuc)
                        
                        with open("bbSonuclar.txt", "a", encoding="UTF-8") as f:
                                f.write(sonuc)
                        
                        os.chdir("pdfImagesKontrol")
                        cv.imwrite(name , img )
                        os.chdir("..")

        cv.destroyAllWindows()


test()
