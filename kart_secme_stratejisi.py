from abc import ABC, abstractmethod
import random


class KartSecmeStratejisi(ABC):
    """Kart seçme stratejisi için abstract temel sınıf (Strategy Pattern)"""
    
    @abstractmethod
    def kart_sec(self, kartlar, brans=None):
        """Verilen kartlar arasından bir kart seç
        
        Args:
            kartlar (list): Seçim yapılacak kart listesi
            brans (str, optional): Seçilecek branş filtresi
            
        Returns:
            dict: Seçilen kart
        """
        pass
    
    @abstractmethod
    def strateji_adi(self):
        """Stratejinin adını döndür
        
        Returns:
            str: Stratejinin adı
        """
        pass
    
    def _bransta_filtrele(self, kartlar, brans):
        """Kartları branşa göre filtrele
        
        Args:
            kartlar (list): Kart listesi
            brans (str): Branş adı
            
        Returns:
            list: Filtrelenmiş kart listesi
        """
        if brans:
            return [k for k in kartlar if k['brans'] == brans and not k.get('oyundan_cikarildi', False)]
        return [k for k in kartlar if not k.get('oyundan_cikarildi', False)]


class KolayStrateji(KartSecmeStratejisi):
    """Kolay zorluk seviyesi stratejisi
    
    Uygun branştan rastgele kart seçer.
    """
    
    def kart_sec(self, kartlar, brans=None):
        """Uygun branştan rastgele bir kart seç
        
        Args:
            kartlar (list): Seçim yapılacak kart listesi
            brans (str, optional): Seçilecek branş filtresi
            
        Returns:
            dict: Seçilen kart veya None
        """
        # Branşa göre filtrele
        uygun_kartlar = self._bransta_filtrele(kartlar, brans)
        
        if not uygun_kartlar:
            return None
        
        # Rastgele kart seç
        return random.choice(uygun_kartlar)
    
    def strateji_adi(self):
        """Stratejinin adını döndür"""
        return "Kolay"


class OrtaStrateji(KartSecmeStratejisi):
    """Orta zorluk seviyesi stratejisi
    
    Uygun branştaki kartlar içinde güncel ortalama performansı en yüksek kartı seçer.
    """
    
    def kart_sec(self, kartlar, brans=None):
        """Güncel ortalama performansı en yüksek kartı seç
        
        Args:
            kartlar (list): Seçim yapılacak kart listesi
            brans (str, optional): Seçilecek branş filtresi
            
        Returns:
            dict: Seçilen kart veya None
        """
        # Branşa göre filtrele
        uygun_kartlar = self._bransta_filtrele(kartlar, brans)
        
        if not uygun_kartlar:
            return None
        
        # Her kart için güncel ortalama performans hesapla
        en_iyi_kart = None
        en_yuksek_ortalama = -1
        
        # Branşa göre özellikler
        brans_ozellikleri = {
            "Futbol": ["penalti", "serbestturus", "kaleci_karsikarsiya"],
            "Basketbol": ["ucluk", "ikilik", "serbest_atis"],
            "Voleybol": ["servis", "blok", "smac"]
        }
        
        for kart in uygun_kartlar:
            sporcu = kart.get('sporcu_ref')
            if not sporcu:
                continue
            
            kart_brans = kart.get('brans')
            ozellikler = brans_ozellikleri.get(kart_brans, [])
            
            # Temel puanları topla
            toplam_puan = 0
            ozellik_sayisi = 0
            
            for ozellik in ozellikler:
                if hasattr(sporcu, ozellik):
                    temel_puan = getattr(sporcu, ozellik)
                    toplam_puan += temel_puan
                    ozellik_sayisi += 1
            
            if ozellik_sayisi == 0:
                continue
            
            # Ortalama temel puan
            ortalama_temel = toplam_puan / ozellik_sayisi
            
            # Güncel performans için bonusları ekle
            enerji = kart.get('enerji', 100)
            seviye = kart.get('seviye', 1)
            
            # Enerji cezası hesapla (düşük enerjide ceza)
            enerji_cezasi = 0
            if enerji < 50:
                enerji_cezasi = (50 - enerji) * 0.2  # Her 1 eksik enerji için 0.2 ceza
            
            # Seviye bonusu hesapla
            seviye_bonusu = (seviye - 1) * 3
            
            # Güncel ortalama performans
            guncel_ortalama = ortalama_temel - enerji_cezasi + seviye_bonusu
            
            if guncel_ortalama > en_yuksek_ortalama:
                en_yuksek_ortalama = guncel_ortalama
                en_iyi_kart = kart
        
        return en_iyi_kart if en_iyi_kart else uygun_kartlar[0]
    
    def strateji_adi(self):
        """Stratejinin adını döndür"""
        return "Orta"


class ZorStrateji(KartSecmeStratejisi):
    """Zor zorluk seviyesi stratejisi
    
    En yüksek seviyeli ve enerjili kartı seçer.
    """
    
    def kart_sec(self, kartlar, brans=None):
        """En iyi kartı seç (seviye ve enerji bazında)
        
        Args:
            kartlar (list): Seçim yapılacak kart listesi
            brans (str, optional): Seçilecek branş filtresi
            
        Returns:
            dict: Seçilen kart veya None
        """
        # Branşa göre filtrele
        uygun_kartlar = self._bransta_filtrele(kartlar, brans)
        
        if not uygun_kartlar:
            return None
        
        # Seviye ve enerjiye göre en iyisini seç
        return max(uygun_kartlar, key=lambda x: (x.get('seviye', 0), x.get('enerji', 100)))
    
    def strateji_adi(self):
        """Stratejinin adını döndür"""
        return "Zor"
