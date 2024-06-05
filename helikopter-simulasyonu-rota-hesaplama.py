import random
import math
import matplotlib.pyplot as plt

# İki nokta arasındaki Euclidean mesafesini hesapla
def mesafe_hesapla(nokta1, nokta2):
    return math.sqrt((nokta1[0] - nokta2[0])**2 + (nokta1[1] - nokta2[1])**2)

# Dosyaları oku
def oku_varis_noktalari(dosya_adı):
    try:
        with open(dosya_adı, 'r') as dosya:
            varis_noktalari = [tuple(map(float, line.strip().split(','))) for line in dosya]
        return varis_noktalari
    except FileNotFoundError:
        print(f"{dosya_adı} dosyası bulunamadı.")
        return None
    except Exception as e:
        print("Bir hata oluştu:", e)
        return None

def oku_koordinatlar(dosya_adı):
    try:
        with open(dosya_adı, 'r') as dosya:
            koordinatlar = [tuple(map(float, line.strip().split(','))) for line in dosya]
        return koordinatlar
    except FileNotFoundError:
        print(f"{dosya_adı} dosyası bulunamadı.")
        return None
    except Exception as e:
        print("Bir hata oluştu:", e)
        return None
    

def simülasyon_yap(koordinatlar, varis_noktalari):
    plt.figure(figsize=(10, 6))
    
    if not varis_noktalari:
        print("Varış noktaları bulunamadı.")
        return
    
    while varis_noktalari:  # Tüm varış noktaları ziyaret edilene kadar devam et
        for helikopter_koordinat in koordinatlar:
            if not varis_noktalari:  # Tüm varış noktaları ziyaret edildiyse döngüyü sonlandır
                break
            
            # Helikopterin en yakın noktayı bulma
            en_yakin_nokta = min(varis_noktalari, key=lambda nokta: mesafe_hesapla(helikopter_koordinat, nokta))
            
            # Helikopteri en yakın noktaya gitmeye gönder
            varis_x, varis_y = en_yakin_nokta
            plt.plot(varis_x, varis_y, 'rx')
            plt.plot([helikopter_koordinat[0], varis_x], [helikopter_koordinat[1], varis_y], 'g--')
            
            # Helikopterin yeni konumunu güncelle
            helikopter_koordinat = en_yakin_nokta
            
            # Varış noktasını listeden kaldır
            varis_noktalari.remove(en_yakin_nokta)
        
        # Tüm helikopterlerin başlangıç noktasına geri dönmesi
        for helikopter_koordinat in koordinatlar:
            plt.plot(helikopter_koordinat[0], helikopter_koordinat[1], 'bo')  # Helikopterin son konumu
        
    plt.xlabel("Boylam")
    plt.ylabel("Enlem")
    plt.title("Helikopter Simülasyonu")
    plt.grid(True)
    plt.show()

# Dosyaları oku
varis_noktalari = oku_varis_noktalari("selected-coordinate-numbers.txt")
if varis_noktalari:
    koordinatlar = oku_koordinatlar("yıldız-hava-numara.txt")
    if koordinatlar:
        simülasyon_yap(koordinatlar, varis_noktalari)
