"""
VeriOkuyucu Sınıfı
Dosyadan kartları okur ve nesnelere dönüştürür
"""

from dosya_yoneticisi import DosyaYoneticisi
from futbolcu import Futbolcu
from basketbolcu import Basketbolcu
from voleybolcu import Voleybolcu


class VeriOkuyucu:
    """Dosyadan veri okuma ve nesneye dönüştürme işlemleri için sınıf"""
    
    def __init__(self, dosya_adi="sporcular.txt"):
        """VeriOkuyucu sınıfını başlat
        
        Args:
            dosya_adi (str): Okunacak sporcu verilerinin bulunduğu dosya
        """
        self.dosya_adi = dosya_adi
        self.futbolcular = []
        self.basketbolcular = []
        self.voleybolcular = []
        self.yuklendi = False
    
    def kartlari_oku(self):
        """Dosyadan kartları/sporcuları oku
        
        Returns:
            tuple: (futbolcular, basketbolcular, voleybolcular) dictionary listeleri
            
        Raises:
            FileNotFoundError: Dosya bulunamadığında
            ValueError: Dosya formatı hatalı olduğunda
        """
        futbol_data, basket_data, voley_data = DosyaYoneticisi.sporcular_oku(self.dosya_adi)
        self.yuklendi = True
        return futbol_data, basket_data, voley_data
    
    def nesnelere_donustur(self):
        """Okunan verileri Sporcu nesnelerine dönüştür
        
        Returns:
            tuple: (Futbolcu listesi, Basketbolcu listesi, Voleybolcu listesi)
            
        Raises:
            RuntimeError: Veriler henüz yüklenmemişse
        """
        if not self.yuklendi:
            # Önce verileri oku
            self.kartlari_oku()
        
        # Verileri al
        futbol_data, basket_data, voley_data = DosyaYoneticisi.sporcular_oku(self.dosya_adi)
        
        # Futbolcuları dönüştür
        futbolcular = []
        for data in futbol_data:
            futbolcu = Futbolcu()
            futbolcu.sporcu_id = data.get('sporcu_id')
            futbolcu.sporcu_adi = data.get('sporcu_adi')
            futbolcu.takim_adi = data.get('takim_adi')
            futbolcu.brans = "Futbol"
            
            # Futbol özellikleri - dosyadan gelen veriler
            futbolcu.penalti = data.get('ozellikler', 70)
            futbolcu.serbestturus = data.get('dayaniklilik', 70)
            futbolcu.kaleci_karsikarsiya = data.get('enerji', 70)
            futbolcu.ozel_yetenek_katsayisi = data.get('ozel_yetenek', 1.0)
            
            # Dayanıklılık hesapla (ortalama olarak)
            futbolcu.dayaniklilik = int((futbolcu.penalti + futbolcu.serbestturus + futbolcu.kaleci_karsikarsiya) / 3)
            
            futbolcular.append(futbolcu)
        
        # Basketbolcuları dönüştür
        basketbolcular = []
        for data in basket_data:
            basketbolcu = Basketbolcu()
            basketbolcu.sporcu_id = data.get('sporcu_id')
            basketbolcu.sporcu_adi = data.get('sporcu_adi')
            basketbolcu.takim_adi = data.get('takim_adi')
            basketbolcu.brans = "Basketbol"
            
            # Basketbol özellikleri
            basketbolcu.ucluk = data.get('ozellikler', 70)
            basketbolcu.ikilik = data.get('dayaniklilik', 70)
            basketbolcu.serbest_atis = data.get('enerji', 70)
            basketbolcu.ozel_yetenek_katsayisi = data.get('ozel_yetenek', 1.0)
            
            basketbolcu.dayaniklilik = int((basketbolcu.ucluk + basketbolcu.ikilik + basketbolcu.serbest_atis) / 3)
            
            basketbolcular.append(basketbolcu)
        
        # Voleybolcuları dönüştür
        voleybolcular = []
        for data in voley_data:
            voleybolcu = Voleybolcu()
            voleybolcu.sporcu_id = data.get('sporcu_id')
            voleybolcu.sporcu_adi = data.get('sporcu_adi')
            voleybolcu.takim_adi = data.get('takim_adi')
            voleybolcu.brans = "Voleybol"
            
            # Voleybol özellikleri
            voleybolcu.servis = data.get('ozellikler', 70)
            voleybolcu.blok = data.get('dayaniklilik', 70)
            voleybolcu.smac = data.get('enerji', 70)
            voleybolcu.ozel_yetenek_katsayisi = data.get('ozel_yetenek', 1.0)
            
            voleybolcu.dayaniklilik = int((voleybolcu.servis + voleybolcu.blok + voleybolcu.smac) / 3)
            
            voleybolcular.append(voleybolcu)
        
        # Nesneleri sakla
        self.futbolcular = futbolcular
        self.basketbolcular = basketbolcular
        self.voleybolcular = voleybolcular
        
        return futbolcular, basketbolcular, voleybolcular
    
    def tum_sporculari_al(self):
        """Tüm sporcuları tek liste olarak döndür
        
        Returns:
            list: Tüm sporcu nesnelerinin listesi
        """
        if not self.futbolcular and not self.basketbolcular and not self.voleybolcular:
            self.nesnelere_donustur()
        
        return self.futbolcular + self.basketbolcular + self.voleybolcular
    
    def brans_bazinda_al(self, brans):
        """Belirli bir branştaki sporcuları döndür
        
        Args:
            brans (str): "Futbol", "Basketbol" veya "Voleybol"
            
        Returns:
            list: İlgili branştaki sporcu nesneleri
        """
        if not self.futbolcular and not self.basketbolcular and not self.voleybolcular:
            self.nesnelere_donustur()
        
        if brans == "Futbol":
            return self.futbolcular
        elif brans == "Basketbol":
            return self.basketbolcular
        elif brans == "Voleybol":
            return self.voleybolcular
        else:
            return []
    
    def sporcu_sayisi(self):
        """Toplam sporcu sayısını döndür
        
        Returns:
            dict: Branş bazlı ve toplam sporcu sayıları
        """
        if not self.futbolcular and not self.basketbolcular and not self.voleybolcular:
            self.nesnelere_donustur()
        
        return {
            'futbol': len(self.futbolcular),
            'basketbol': len(self.basketbolcular),
            'voleybol': len(self.voleybolcular),
            'toplam': len(self.futbolcular) + len(self.basketbolcular) + len(self.voleybolcular)
        }
    
    def dosya_degistir(self, yeni_dosya_adi):
        """Okunacak dosyayı değiştir
        
        Args:
            yeni_dosya_adi (str): Yeni dosya adı
        """
        self.dosya_adi = yeni_dosya_adi
        self.yuklendi = False
        self.futbolcular = []
        self.basketbolcular = []
        self.voleybolcular = []
    
    def __str__(self):
        """String gösterimi"""
        sayilar = self.sporcu_sayisi()
        return f"VeriOkuyucu(dosya='{self.dosya_adi}', toplam={sayilar['toplam']} sporcu)"


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("    VeriOkuyucu SINIFI TESTİ")
    print("=" * 70)
    
    # VeriOkuyucu oluştur
    okuyucu = VeriOkuyucu("sporcular.txt")
    
    print(f"\n📂 Dosya: {okuyucu.dosya_adi}")
    
    # Kartları oku (dictionary olarak)
    print("\n1️⃣ Kartları oku (dictionary):")
    try:
        futbol_data, basket_data, voley_data = okuyucu.kartlari_oku()
        print(f"   ✅ Futbol: {len(futbol_data)}, Basketbol: {len(basket_data)}, Voleybol: {len(voley_data)}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")
    
    # Nesnelere dönüştür
    print("\n2️⃣ Nesnelere dönüştür:")
    try:
        futbolcular, basketbolcular, voleybolcular = okuyucu.nesnelere_donustur()
        print(f"   ✅ Futbolcu: {len(futbolcular)}, Basketbolcu: {len(basketbolcular)}, Voleybolcu: {len(voleybolcular)}")
        
        # İlk futbolcuyu göster
        if futbolcular:
            f = futbolcular[0]
            print(f"\n   📋 İlk Futbolcu:")
            print(f"      Ad: {f.sporcu_adi}")
            print(f"      Takım: {f.takim_adi}")
            print(f"      Penaltı: {f.penalti}")
            print(f"      Serbest Vuruş: {f.serbestturus}")
            print(f"      Kaleci Karşı Karşıya: {f.kaleci_karsikarsiya}")
            print(f"      Tip: {type(f).__name__}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")
    
    # Sporcu sayısı
    print("\n3️⃣ Sporcu sayıları:")
    sayilar = okuyucu.sporcu_sayisi()
    for brans, sayi in sayilar.items():
        print(f"   {brans.capitalize()}: {sayi}")
    
    # String gösterimi
    print(f"\n4️⃣ String gösterimi: {okuyucu}")
    
    print("\n" + "=" * 70)
    print("✅ VeriOkuyucu sınıfı dosyadan kartları okur ve nesnelere dönüştürür!")
    print("=" * 70)
