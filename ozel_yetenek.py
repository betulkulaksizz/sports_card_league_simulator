from abc import ABC, abstractmethod


class OzelYetenek(ABC):
    """Özel yetenekler için abstract base class - Polymorphism ile modellendi"""
    
    @abstractmethod
    def ac_kla(self) -> str:
        """Yeteneğin açıklamasını döndür
        
        Returns:
            str: Yetenek açıklaması
        """
        pass
    
    @abstractmethod
    def pasif_mi(self) -> bool:
        """Pasif yetenek mi kontrol et
        
        Returns:
            bool: True ise pasif, False ise aktif
        """
        pass
    
    @abstractmethod
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        """Yeteneğin puan üzerindeki etkisini hesapla
        
        Args:
            temel_puan (float): Temel puan değeri
            kart_durumu (dict): Kart durumu (enerji, seviye, vb.)
            
        Returns:
            float: Ek bonus puan
        """
        pass
    
    @abstractmethod
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        """Yeteneğin enerji kaybı üzerindeki etkisini hesapla
        
        Args:
            enerji_kaybi (int): Temel enerji kaybı
            
        Returns:
            int: Düzeltilmiş enerji kaybı
        """
        pass


class ClutchPlayer(OzelYetenek):
    """Son 3 turda +10 bonus yetenegi - Pasif"""
    
    def ac_kla(self) -> str:
        return "🎯 Clutch Player: Son 3 turda +10 bonus"
    
    def pasif_mi(self) -> bool:
        return True  # Pasif yetenek
    
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        """Son 3 turda oynanmışsa +10 bonus ver"""
        # Not: Tur takibi oyun_arayuzu'nda yapılacak
        if kart_durumu and kart_durumu.get('son_3_turda_oynanmis', False):
            return 10.0
        return 0.0
    
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        return enerji_kaybi  # Enerji etkisi yok


class Captain(OzelYetenek):
    """Aynı branştaki takım kartlarına +5 moral etkisi - Pasif"""
    
    def ac_kla(self) -> str:
        return "👑 Captain: Aynı branştaki takım kartlarına +5 moral etkisi"
    
    def pasif_mi(self) -> bool:
        return True  # Pasif yetenek
    
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        """Kaptan etkisi puan bonusu değil, moral etkisidir"""
        return 0.0  # Doğrudan puan etkisi yok, moral üzerinde etki
    
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        return enerji_kaybi  # Enerji etkisi yok


class Legend(OzelYetenek):
    """Bir maçta bir kez seçilen özelliği iki kat etkileyebilir - Aktif"""
    
    def ac_kla(self) -> str:
        return "⭐ Legend: Seçilen özelliği 1 kez iki kat etkileyebilir (Aktif)"
    
    def pasif_mi(self) -> bool:
        return False  # Aktif yetenek
    
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        """Eğer aktive edilmişse özellik puanını iki kat et"""
        if kart_durumu and kart_durumu.get('legend_aktive', False):
            return temel_puan  # +temel_puan = 2x
        return 0.0
    
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        return enerji_kaybi + 5  # Aktif yetenek kullandığında +5 ek enerji kaybı


class Defender(OzelYetenek):
    """Rakibin özel yetenek bonusunu yarıya düşürür - Pasif"""
    
    def ac_kla(self) -> str:
        return "🛡️ Defender: Rakibin özel yetenek bonusunu yarıya düşürür"
    
    def pasif_mi(self) -> bool:
        return True  # Pasif yetenek
    
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        """Defender kendi puanına etki yapmaz, rakip puanını azaltır"""
        return 0.0
    
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        return enerji_kaybi  # Enerji etkisi yok


class Veteran(OzelYetenek):
    """Enerji kaybını %50 azaltır - Pasif"""
    
    def ac_kla(self) -> str:
        return "🏆 Veteran: Enerji kaybını %50 azaltır"
    
    def pasif_mi(self) -> bool:
        return True  # Pasif yetenek
    
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        return 0.0  # Puan etkisi yok
    
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        """Enerji kaybını %50 azalt"""
        return int(enerji_kaybi * 0.5)


class Finisher(OzelYetenek):
    """Enerjisi düşükken +8 ek bonus alır - Pasif"""
    
    def ac_kla(self) -> str:
        return "⚡ Finisher: Enerjisi düşükken +8 ek bonus alır"
    
    def pasif_mi(self) -> bool:
        return True  # Pasif yetenek
    
    def puan_etkisi(self, temel_puan: float, kart_durumu: dict = None) -> float:
        """Enerji < 30 ise +8 bonus ver"""
        if kart_durumu and kart_durumu.get('enerji', 100) < 30:
            return 8.0
        return 0.0
    
    def enerji_etkisi(self, enerji_kaybi: int) -> int:
        return enerji_kaybi  # Enerji etkisi yok
