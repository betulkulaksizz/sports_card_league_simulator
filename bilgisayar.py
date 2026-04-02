import random
from oyuncu import Oyuncu
from kart_secme_stratejisi import KartSecmeStratejisi, KolayStrateji, OrtaStrateji, ZorStrateji


class Bilgisayar(Oyuncu):
    """Bilgisayar tarafından kontrol edilen yapay zeka sınıfı"""
    
    # Strateji sabitleri
    STRATEJILER = {
        "kolay": KolayStrateji,
        "orta": OrtaStrateji,
        "zor": ZorStrateji
    }
    
    def __init__(self, oyuncu_id, oyuncu_adi):
        super().__init__(oyuncu_id, oyuncu_adi)
        self.zorluk = "kolay"  # Varsayılan zorluk seviyesi: kolay
        self.strateji = KolayStrateji()  # Varsayılan strateji
        self.enerji = 100  # Başlangıç enerjisi (oyuncu seviyesinde)
        self.dayaniklilik = 80  # Başlangıç dayanıklılığı
        self.kartlar_gizli = True  # Kartların gizli olup olmadığı (test için)
    
    def kart_sec(self, brans=None):
        """Bilgisayar kartını seçer (strateji pattern kullanarak)
        
        Args:
            brans (str, optional): Seçilecek branş. None ise tüm kartlardan seçim yapılır.
            
        Returns:
            dict: Seçilen kart veya None
        """
        # Aktif kartları al (oyundan çıkarılmamış)
        aktif_kartlar = self.aktif_kartlari_al()
        
        if not aktif_kartlar:
            print(f"{self.oyuncu_adi}'nin kartı kalmadı!")
            return None
        
        # Strateji kullanarak kart seç
        secilen_kart = self.strateji.kart_sec(aktif_kartlar, brans)
        
        if secilen_kart is None:
            print(f"{self.oyuncu_adi}' {brans or 'herhangi bir'} branşta kartı kalmadı!")
            return None
        
        # Seçilen kartı bildir
        from kart_dagitici import KartDagitici
        enerji = secilen_kart.get('enerji', 100)
        seviye = secilen_kart.get('seviye', 1)
        
        if KartDagitici.kart_enerji_kritik_mi(secilen_kart):
            print(f"{self.oyuncu_adi} [{self.strateji.strateji_adi()}] '{secilen_kart['ad']}' kartını oynadı! (Sviy: {seviye}, ⚠️ Kritik Enerji: {enerji})")
        else:
            print(f"{self.oyuncu_adi} [{self.strateji.strateji_adi()}] '{secilen_kart['ad']}' kartını oynadı! (Sviy: {seviye}, Enerji: {enerji})")
        
        return secilen_kart
    
    def strateji_uygula(self, brans=None):
        """Bilgisayar stratejisini uygular"""
        return self.kart_sec(brans)
    
    def zorluk_ayarla(self, zorluk):
        """Zorluk seviyesini ve stratejisini ayarla
        
        Args:
            zorluk (str): 'kolay', 'orta' veya 'zor'
        """
        if zorluk in self.STRATEJILER:
            self.zorluk = zorluk
            self.strateji = self.STRATEJILER[zorluk]()
            print(f"Bilgisayar zorluk seviyesi '{zorluk}' olarak ayarlandı.")
            print(f"  Strateji: {self.strateji.strateji_adi()}")
        else:
            print("Geçersiz zorluk seviyesi! (kolay, orta, zor)")
    
    def strateji_ayarla(self, strateji: KartSecmeStratejisi):
        """Özel bir strateji ayarla
        
        Args:
            strateji (KartSecmeStratejisi): Kullanılacak strateji nesnesi
        """
        if isinstance(strateji, KartSecmeStratejisi):
            self.strateji = strateji
            print(f"Bilgisayar stratejisi '{strateji.strateji_adi()}' olarak ayarlandı.")
        else:
            print("Geçersiz strateji! KartSecmeStratejisi türünde olmalı.")
    
    # ==================== KART GÖSTERİM FONKSİYONLARI ====================
    
    def kartlari_goster(self):
        """Bilgisayarın kartlarını göster (test için)"""
        self.kartlar_gizli = False
        print(f"\n{'='*60}")
        print(f"🔓 {self.oyuncu_adi}'nin KARTLARI (Gösterildi)")
        print(f"{'='*60}")
        self._kartlari_listele()
    
    def kartlari_gizle(self):
        """Bilgisayarın kartlarını gizle"""
        self.kartlar_gizli = True
        print(f"🔒 {self.oyuncu_adi}'nin kartları gizlendi.")
    
    def kartlari_toggle(self):
        """Kartları göster/gizle arasında geçiş yap"""
        if self.kartlar_gizli:
            self.kartlari_goster()
        else:
            self.kartlari_gizle()
    
    def _kartlari_listele(self):
        """Kartları detaylı listele"""
        from kart_dagitici import KartDagitici
        from sporcu import Sporcu
        
        aktif_kartlar = self.aktif_kartlari_al()
        cikarilmis_kartlar = self.cikarilmis_kartlari_al()
        
        print(f"\nToplam Aktif Kart: {len(aktif_kartlar)}")
        print(f"  - Futbol: {len([k for k in aktif_kartlar if k['brans'] == 'Futbol'])}")
        print(f"  - Basketbol: {len([k for k in aktif_kartlar if k['brans'] == 'Basketbol'])}")
        print(f"  - Voleybol: {len([k for k in aktif_kartlar if k['brans'] == 'Voleybol'])}")
        
        print(f"\n{'-'*60}")
        print(f"{'No':<3} {'Ad':<20} {'Branş':<12} {'Sviy':<5} {'Dnm':<4} {'Gal':<4} {'Enerji':<12}")
        print(f"{'-'*60}")
        
        for i, kart in enumerate(aktif_kartlar, 1):
            enerji = kart.get('enerji', 100)
            max_enerji = kart.get('max_enerji', 100)
            seviye = kart.get('seviye', 1)
            deneyim = kart.get('deneyim', 0)
            galibiyet = kart.get('galibiyet_sayisi', 0)
            
            # Enerji durumu
            if KartDagitici.kart_enerji_kritik_mi(kart):
                enerji_str = f"⚠️ {enerji}/{max_enerji}"
            else:
                enerji_str = f"{enerji}/{max_enerji}"
            
            # Seviye gösterimi
            if seviye >= Sporcu.MAX_SEVIYE:
                seviye_str = f"⭐{seviye}"
            else:
                seviye_str = f"{seviye}"
            
            print(f"{i:<3} {kart['ad']:<20} {kart['brans']:<12} {seviye_str:<5} {deneyim:<4} {galibiyet:<4} {enerji_str:<12}")
        
        if cikarilmis_kartlar:
            print(f"\n❌ Oyundan Çıkarılan Kartlar ({len(cikarilmis_kartlar)}):")
            for kart in cikarilmis_kartlar:
                print(f"   • {kart['ad']} ({kart['brans']}) - Seviye: {kart.get('seviye', 1)}")
        
        print(f"{'='*60}\n")
    
    def kart_durumu_ozeti(self):
        """Kartların durumunun kısa özeti (gizli modda bile gösterilebilir)"""
        aktif = len(self.aktif_kartlari_al())
        cikarilmis = len(self.cikarilmis_kartlari_al())
        kritik = len(self.kritik_enerjili_kartlari_al())
        
        print(f"\n{self.oyuncu_adi} Kart Özeti:")
        print(f"  📊 Aktif: {aktif} | Kritik: {kritik} | Çıkarılan: {cikarilmis}")
        
        if not self.kartlar_gizli:
            self._kartlari_listele()
