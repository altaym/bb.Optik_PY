import numpy as np
import argparse
import cv2


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to input image file")
# args = vars(ap.parse_args())

def test():
    img = cv2.imread("testForm.png")
    #img = cv2.resize(img, (400,600))
    resimDondur(img)

def resimDondur(image):
    # image = cv2.imread(args["image"])
    #image = cv2.imread("1.png")

    # görüntüyü gri tonlamaya dönüştürün ve ön planı çevirin ve ön planın artık "beyaz" olmasını sağlamak için arka plan ve arka plan "siyah"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # tüm piksel değerlerinin (x, y) koordinatlarını sıfırdan büyükse, bu koordinatları kullanarak
    # tümünü içeren döndürülmüş bir sınırlayıcı kutu hesaplayın koordinat
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    print(angle)
    # "cv2.minAreaRect" işlevi, aralık [-90, 0); dikdörtgen saat yönünde dönerken
    # açı trendlerini 0'a döndürdü - bu özel durumda açıya 90 derece eklemeniz gerekiyor
    
    # if angle < -45:
    #     angle = -(90 + angle)

    # # aksi takdirde, yapmak için sadece açının tersini alın olumlu
    # else:
    #     angle = -angle

    if angle > 0  and angle<45 :
        angle = -angle
    elif angle > 45:
        angle = -(90-angle)

    # eğriliği gidermek için resmi döndürün
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Doğrulayabilmemiz için resmin üzerine düzeltme açısını çizin
    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    print("[INFO] angle: {:.3f}".format(angle))
    image = cv2.resize( image, (400,600))
    rotated = cv2.resize( rotated, (400, 600 ))
    cv2.imshow("Input", image )
    cv2.imshow("Rotated", rotated )
    cv2.waitKey(0)

test()