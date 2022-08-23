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
import math

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


class OkumaYonu(Enum):
    DIKEY = 0
    YATAY = 1

class bbOmr():
    cevaplar=['A','B','C','D','E','-1','0']
    harfler =['A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö', 'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z', ' ']
    gruplar =['A','B','C','D','E'] 
    rakamlar =['0','1','2','3','4','5','6','7','8','9','-']

    bobleX = 12
    bobleY = 12
    ogrenci_cevap = {}
   
    def get_angle(self,p1, p2):
        x_diff = p2[0] - p1[0]
        y_diff = p2[1] - p1[1]
        return math.degrees(math.atan2(y_diff, x_diff))
        
    def getMarkers(self, img):
             # img=cv.imread('111.png') 
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
        blur = cv.GaussianBlur(gray,(3,3),0) 
        edges = cv.Canny(blur,50,100) 

        contours, hierarchy = cv.findContours(edges,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) 

        # ret, thresh = cv.threshold(gray, 127 , 255, 1)

        # contours, hierarchy = cv.findContours(thresh.copy() , cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        
        i = 1
        markers = []
        for cnt in contours:
                if cv.contourArea(cnt) < 500:
                        arclen = cv.arcLength(cnt, True)
                        approx = cv.approxPolyDP(cnt, 0.05 * arclen ,True)
                        if len(approx) == 4 :
                                
                                x,y,w,h = cv.boundingRect(cnt)
                                # if abs(w-h) <= 3 kare
                                # M = cv.moments(cnt)             
                                # cx = int(M['m10']/M['m00'])
                                # cy = int(M['m01']/M['m00'])
                                
                                # 4 kenari olan sekil bir kare mi yoksa dikdortgen mi
                                # bunun kontrolunu yapmak icin kenar uzunluklarini bakiliyor
                                if w >= 25 and 16 > h >= 11 :
                                        ar = w / float(h)
                                        sekil_adi = "kare" if ar >= 0.95 and ar <= 1.05 else "diktörgen"
                                        text = sekil_adi #f"{i}"
                                        cv.drawContours(img, [cnt] ,-1 ,(0,0,255),-1)
                                        markers.append((x,y))
                                        # cv.putText(img, text , (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0),1)
                                        # print(i,w,h)
                                        i+=1
                        elif len(approx) != [3,4,5] :
                                pass  
       


        # cv.drawContours(img,contours,-1,(0,255,0),2) 
        
        # cv.namedWindow("im", cv.WINDOW_FREERATIO)
        # cv.imshow('im',img) 
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        return markers, img


    def rAreaX(self,  img,  satirSayisi:int = 20, colonSayisi:int = 4 , xUzunluk:int = 12, yUzunluk:int = 12 , 
      dikeyDuzeltme : bool = False , duzeltmeMiktari :int = 1 , sutunSayisi = 1 , sutunSolBosluk = 0, 
      karakterGrubu = harfler, olcek = 30 ):

        kx = xUzunluk # boble kutu x 
        ky = yUzunluk # boble kutu y
        row_ky = 0 

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.bitwise_not(gray)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        num_rows = np.shape(thresh)[0]   

        sonuc = {}

        x1 , x2 = 0, kx
        #for col in range(0, colonSayisi):
        for row in range(0, satirSayisi):
            y1 = row_ky
            y2 = row_ky + ky

            for col in range(0, colonSayisi):
                col_kx = col * kx
                x1 = col_kx
                x2 = col_kx + kx
                # işlem ===                    
                #cv.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 1)
                hucre = thresh[y1+2:y2-2, x1+2 :x2-2]
                # hucre = thresh[y1+1:y2-1, x1+1 :x2-1]
                bps = np.sum(hucre == 255)
                if bps >= olcek :
                    sonuc.setdefault( row + 1, karakterGrubu[col])
                    cv.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 1)
                elif bps > 0:
                     cv.rectangle(img, (x1,y1), (x2,y2), (0,0,255), 1)
                        
                # === işlem 
            row_ky += ky  # r * ky

            if dikeyDuzeltme and row % 4 == 0 :
                row_ky += duzeltmeMiktari 
        # cv.imshow("rAreaX kontrol",img)
        # cv.waitKey(0)  
        return sonuc

    def rArea(self,  img,  satirSayisi:int = 20, colonSayisi:int = 4 , xUzunluk:int = 12, yUzunluk:int = 12 , dikeyDuzeltme : bool = False , duzeltmeMiktari :int = 1 , sutunSayisi = 1 , sutunSolBosluk = 0, karakterGrubu = harfler):
        kx = xUzunluk # boble kutu x 
        ky = yUzunluk # boble kutu y
        row_ky = 0 

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.bitwise_not(gray)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        num_rows = np.shape(thresh)[0]   

        sonuc = ""

        x1 , x2 = 0, kx
        for col in range(0, colonSayisi):
                col_kx = col * kx
                row_ky = 0

                x1 = col_kx
                x2 = col_kx + kx

                sutun = thresh[0:num_rows , x1 :x2]                 
                if np.sum(sutun == 255 ) < 10 :
                        sonuc += " "                
                else :
                        for row in range(0, satirSayisi ):
                                y1 = row_ky
                                y2 = row_ky + ky
                                # işlem ===                    
                                
                                hucre = thresh[y1+1:y2-1, x1+1 :x2-1]
                                bps = np.sum(hucre == 255)
                                if bps > 50 :
                                    sonuc += karakterGrubu[row]
                                    cv.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 1)
                                else :
                                    cv.rectangle(img, (x1,y1), (x2,y2), (0,0,255), 1)
                                # elif row == satirSayisi -1   and bps < 50  :
                                #   sonuc += "_"
                                        
                                # === işlem 
                                row_ky += ky  # r * ky

                                if dikeyDuzeltme and row % 4 == 0 :
                                        row_ky += duzeltmeMiktari   

        # cv.imshow("rArea kontrol",img)                                
        return sonuc.strip()


    def cArea(self,  img,  satirSayisi:int = 20, colonSayisi:int = 4 , xUzunluk:int = 12, yUzunluk:int = 12 , dikeyDuzeltme : bool = False , duzeltmeMiktari :int = 1 , sutunSayisi = 1 , sutunSolBosluk = 0):
        kx = xUzunluk # boble kutu x 
        ky = yUzunluk # boble kutu y
        row_ky = 0 

        for blok in range(0, sutunSayisi):
            row_ky = 0 
            lMargin = ( colonSayisi + sutunSolBosluk ) * kx * blok #birden fazla blok var ise bloklar arası boşluk
            if blok % 2 == 0:
                lMargin += 3

            for row in range(0,satirSayisi):
                for col in range(0, colonSayisi ):
                    col_kx = col * kx
                    x1 = lMargin + col_kx
                    x2 = lMargin + col_kx + kx
                    y1 = row_ky
                    y2 = row_ky + ky
                    
                    cv.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 1)                

                row_ky += ky  # r * ky
                if dikeyDuzeltme and row % 4 == 0 :
                    row_ky += duzeltmeMiktari   

        return img 


    def pdfCoz(self, pdfDosya , pngKlasor ):
        pages = pdf2image.pdf2image.convert_from_path(pdfDosya , 200, pngKlasor )
        testCounter = 1
        for page in pages:
            filename = pngKlasor +"/" + str(testCounter)+".png"
            page.save(filename, 'png') 
            testCounter +=  1
        return  testCounter

    def izgaraCiz(self,  img ):
        height, width , channel = img.shape
        row , col = int( height / self.bobleY ), int(width / self.bobleX)
        # print(row, col)
        x = 0
        y = 11
        for r in range(0, row ):
            for c in range(0, col ):
                start_point = ( x + c * self.bobleX     ,  y+ r * self.bobleY     ) 
                end_point =   ( x + c * self.bobleX + self.bobleX , y+ r * self.bobleY + self.bobleY )
                color = (255, 0, 0)
                thickness = 1
                cv.rectangle(img , start_point, end_point, color, thickness)
        
            # if r % 4 == 0 :
            #     y +=1
        return img

    def resimDondur(self, img, angle, info: bool = False):
        if angle > 0  and angle<45 :
                angle = -angle
        elif angle > 45:
                angle = -(90-angle)
        else :
                angle = 90 + angle

        # angle = 90 - angle
        
        # eğriliği gidermek için resmi döndürün
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv.warpAffine(img, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)

        # Doğrulayabilmemiz için resmin üzerine düzeltme açısını çizin
        if info:
            cv.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return rotated

    def resimDondur0(self, image):
        # image = cv2.imread(args["image"])
        #image = cv2.imread("1.png")

        # görüntüyü gri tonlamaya dönüştürün ve ön planı çevirin ve ön planın artık "beyaz" olmasını sağlamak için arka plan ve arka plan "siyah"
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.bitwise_not(gray)

        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

        # tüm piksel değerlerinin (x, y) koordinatlarını sıfırdan büyükse, bu koordinatları kullanarak
        # tümünü içeren döndürülmüş bir sınırlayıcı kutu hesaplayın koordinat
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv.minAreaRect(coords)[-1]

        print(angle)
        # "cv2.minAreaRect" işlevi, aralık [-90, 0); dikdörtgen saat yönünde dönerken
        # açı trendlerini 0'a döndürdü - bu özel durumda açıya 90 derece eklemeniz gerekiyor
        
        # if angle < -45:
        #     angle = -(90 + angle)

        # # # aksi takdirde, yapmak için sadece açının tersini alın olumlu
        # else:
        #     angle = float(90-angle)

        if angle > 0  and angle<45 :
            angle = -angle
        elif angle > 45:
            angle = -(90-angle)
        else :
            angle = 90 + angle

        # angle = 90 - angle
        
        # eğriliği gidermek için resmi döndürün
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv.warpAffine(image, M, (w, h),
            flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)

        # Doğrulayabilmemiz için resmin üzerine düzeltme açısını çizin
        cv.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        # print("[INFO] angle: {:.3f}".format(angle))
        # image = cv2.resize( image, (400,600))
        # rotated = cv2.resize( rotated, (400, 600 ))
        # cv2.imshow("Input", image )
        # cv2.imshow("Rotated", rotated )
        # cv2.waitKey(0)
        return rotated



    def controlArea(self, img,  satirSayisi:int = 20, colonSayisi:int = 4 , xUzunluk:int = 12, yUzunluk:int = 12 , dikeyDuzeltme : bool = False , duzeltmeMiktari :int = 1 , sutunSayisi = 1 , sutunSolBosluk = 0):
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
        return img 

    def getArea(self, img , karakterGrubu  ,  satir =1 , sutun = 1, bosluk = 0 , yon : OkumaYonu  = 0 ):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold( img  , 0, 255 , cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        num_rows = np.shape(thresh)[0]
        sonuc = ""
        for i in range(0, sutun ):
            hucre = thresh[0:num_rows , self.bobleY * i  : self.bobleY * (i + 1)  ]
            karakter = self.karakterCikar(hucre, karakterGrubu)
            sonuc += karakter
        return sonuc

    def getCevaplar(self, img , soruSayisi = 20, secenekSayisi = 4, sutunSayisi = 1 , sutunSolBosluk = 0):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(img , 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        for sutun in range(0, sutunSayisi ): 
            rowTop = 0
            rowBottom = self.bobleY
            x = ( secenekSayisi + sutunSolBosluk ) * self.bobleX * sutun
            y = x + ( secenekSayisi  * self.bobleY )

            if not np.sum(thresh == 255) > 4000:
                for i in range(soruSayisi):
                    self.ogrenci_cevap.setdefault(sutun * 20 + i, self.cevaplar[6])
            else:
                for row in range(0, soruSayisi ):
                    # cevap = thresh[rowTop:rowBottom, sutunSolBosluk * sutun : sutunSolBosluk * sutun + boble * secenekSayisi ] 
                    cevap = thresh[rowTop:rowBottom, x : y ] 
                    ret = self.kontrolCevap(cevap, secenekSayisi )
                    self.ogrenci_cevap.setdefault(sutun * 20 + row + 1  , ret)
                    
                    if row % 4 == 0:
                        rowTop += self.bobleY + 1
                        rowBottom += self.bobleY + 1
                    else :
                        rowTop += self.bobleY
                        rowBottom += self.bobleY
                        
        return self.ogrenci_cevap

    def kontrolCevap(self, img, secenekSayisi):
        array = []
        num_rows = np.shape(img)[0]
        for j in range(0, secenekSayisi ):
            secim = img[0:num_rows , self.bobleX * j : self.bobleX * (j + 1) ]
            bps = np.sum(secim == 255)
            if bps >= 30:
                array.append(self.cevaplar[j])
                st = self.cevaplar[j]
                print("<<", st )
        if len(array) == 0:
            return self.cevaplar[6]
        elif len(array) == 1:
            return array[0]
        else:
            return self.cevaplar[5]

    def karakterCikar(self, img,karakterGrubu ):
        for i in range(0, 30):
            karakter = img[ self.bobleY * i  : self.bobleY * ( i + 1)  , 0: self.bobleX]
            bps = np.sum(karakter == 255)
            # print(i, bps )
            if bps>50:
                return karakterGrubu[i]
            elif i==29 and bps<50:
                return karakterGrubu[-1]

    def kontrolCevapCiz(self, img, koord ): # koordinat bilgisi düzenlenecek
        # image = cv2.imread("test.png")
        cv.circle(img , koord  , 5, (0,0,255), 1)
        #cv2.circle(image ,(447,63), 5 , (0,0,255), 1 )