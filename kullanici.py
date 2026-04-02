from oyuncu import Oyuncu


class Kullanici(Oyuncu):
    """Oyuncu tarafından kontrol edilen kullanıcı sınıfı"""
    
    def __init__(self, oyuncu_id, oyuncu_adi):
        super().__init__(oyuncu_id, oyuncu_adi)
        self.enerji = 100  # Başlangıç enerjisi (oyuncu seviyesinde)
        self.dayaniklilik = 80  # Başlangıç dayanıklılığı
    
    def kart_sec(self, brans=None):
        """Kullanıcı kartını seçer
        
        Args:
            brans (str, optional): Seçilecek branş. None ise tüm kartlardan seçim yapılır.
        """
        print(f"\n{self.oyuncu_adi} kartlarını seçiyor...")
        
        # Aktif kartları al (oyundan çıkarılmamış)
        aktif_kartlar = self.aktif_kartlari_al()
        
        # Branş belirtilmişse o branştaki kartları filtrele
        if brans:
            secim_kartlar = [k for k in aktif_kartlar if k['brans'] == brans]
        else:
            secim_kartlar = aktif_kartlar
        
        if not secim_kartlar:
            print(f"❌ {brans or 'Herhangi bir'} branşta oynanabilir kart kalmadı!")
            return None
        
        print("Mevcut kartlar:")
        for i, kart in enumerate(secim_kartlar):
            enerji = kart.get('enerji', 100)
            from kart_dagitici import KartDagitici
            if KartDagitici.kart_enerji_kritik_mi(kart):
                enerji_durum = f"⚠️ KRİTİK {enerji}"
            else:
                enerji_durum = f"{enerji}"
            print(f"{i + 1}. {kart['ad']} | Branş: {kart['brans']} | Seviye: {kart['seviye']} | Enerji: {enerji_durum}")
        
        secim = input("Hangi kartı oynamak istiyorsunuz? (Numara girin): ")
        try:
            index = int(secim) - 1
            if 0 <= index < len(secim_kartlar):
                seçilen_kart = secim_kartlar[index]
                print(f"{self.oyuncu_adi} '{seçilen_kart['ad']}' kartını oynadı!")
                return seçilen_kart
            else:
                print("Geçersiz seçim!")
                return self.kart_sec(brans)
        except ValueError:
            print("Lütfen geçerli bir numara girin!")
            return self.kart_sec(brans)
    
    def strateji_uygula(self, brans=None):
        """Kullanıcı kendi stratejisini uygular"""
        return self.kart_sec(brans)
