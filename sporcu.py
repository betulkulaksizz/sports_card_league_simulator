class Sporcu:
    # Enerji sabitleri
    BASLANGIC_ENERJI = 100
    KRITIK_ENERJI_ESIGI = 20
    
    # Enerji değişim sabitleri
    KAZANMA_ENERJI_KAYBI = 5
    KAYBETME_ENERJI_KAYBI = 10
    BERABERLIK_ENERJI_KAYBI = 3
    OZEL_YETENEK_ENERJI_KAYBI = 5
    
    # Deneyim ve seviye sabitleri
    GALIBIYET_DENEYIM = 2
    BERABERLIK_DENEYIM = 1
    MAGLUBIYET_DENEYIM = 0
    
    # Seviye atlama gereksinimleri
    SEVIYE_2_GALIBIYET = 2
    SEVIYE_2_DENEYIM = 4
    SEVIYE_3_GALIBIYET = 4
    SEVIYE_3_DENEYIM = 8
    
    # Seviye atlama bonusları
    SEVIYE_OZELLIK_BONUS = 5
    SEVIYE_ENERJI_BONUS = 10
    SEVIYE_DAYANIKLILIK_BONUS = 5
    
    # Maksimum seviye
    MAX_SEVIYE = 3
    
    def __init__(self):
        # Temel Bilgiler
        self.sporcu_id = None              # Sporcu ID
        self.sporcu_adi = None             # Sporcu adı
        self.takim_adi = None              # Takım adı
        self.brans = None                  # Branş
        
        # Temel Özellik Puanları
        self.temel_ozellik_puanlari = None # Temel özellik puanları
        self.dayaniklilik = None           # Dayanıklılık
        self.enerji = self.BASLANGIC_ENERJI  # Başlangıç enerjisi = 100
        self.max_enerji = self.BASLANGIC_ENERJI  # Maksimum enerji kapasitesi
        self.seviye = 1                    # Başlangıç seviyesi
        
        # Deneyim ve Yetenekler
        self.deneyim_puani = 0             # Deneyim puanı (başlangıç: 0)
        self.ozel_yetenek = None           # Özel yetenek
        
        # İstatistikler
        self.kullanimsayisi = 0            # Kullanım sayısı
        self.galibiyet_sayisi = 0          # Galibiyet sayısı
        self.kazanma_kaybetme_sayisi = None  # Kazanma / kaybetme sayısı
        
        # Oyun durumu
        self.oyundan_cikarildi = False     # Enerjisi 0'a düşen kart oyundan çıkar
        self.kart_kullanildi_mi = False    # Bu turda kart kullanıldı mı
    
    def enerji_kritik_mi(self):
        """Enerjinin kritik seviyede olup olmadığını kontrol et"""
        return self.enerji < self.KRITIK_ENERJI_ESIGI and self.enerji > 0
    
    def enerji_sifir_mi(self):
        """Enerjinin sıfır olup olmadığını kontrol et"""
        return self.enerji <= 0
    
    def enerji_guncelle(self, sonuc, ozel_yetenek_kullanildi=False):
        """Tur sonucuna göre enerji güncelle
        
        Args:
            sonuc (str): 'kazandi', 'kaybetti', 'berabere'
            ozel_yetenek_kullanildi (bool): Özel yetenek kullanıldı mı
            
        Returns:
            int: Toplam enerji kaybı
        """
        enerji_kaybi = 0
        
        if sonuc == 'kazandi':
            enerji_kaybi = self.KAZANMA_ENERJI_KAYBI
        elif sonuc == 'kaybetti':
            enerji_kaybi = self.KAYBETME_ENERJI_KAYBI
        elif sonuc == 'berabere':
            enerji_kaybi = self.BERABERLIK_ENERJI_KAYBI
        
        # Özel yetenek kullanıldıysa ek enerji kaybı
        if ozel_yetenek_kullanildi:
            enerji_kaybi += self.OZEL_YETENEK_ENERJI_KAYBI
        
        self.enerji = max(0, self.enerji - enerji_kaybi)
        
        # Enerji sıfıra düştüyse kart oyundan çıkar
        if self.enerji_sifir_mi():
            self.oyundan_cikarildi = True
        
        return enerji_kaybi
    
    def sporcuPuaniGoster(self):
        """Sporcunun tüm puanlarını ekrana yazdır
        
        Returns:
            dict: Sporcu puan bilgileri
        """
        print(f"\n{'='*50}")
        print(f"SPORCU PUAN BİLGİLERİ: {self.sporcu_adi}")
        print(f"{'='*50}")
        print(f"  ID: {self.sporcu_id}")
        print(f"  Takım: {self.takim_adi}")
        print(f"  Branş: {self.brans}")
        print(f"  Seviye: {self.seviye}")
        print(f"  Deneyim Puanı: {self.deneyim_puani}")
        print(f"  Enerji: {self.enerji}/{self.max_enerji}")
        print(f"  Dayanıklılık: {self.dayaniklilik}")
        print(f"  Galibiyet Sayısı: {self.galibiyet_sayisi}")
        print(f"  Kullanım Sayısı: {self.kullanimsayisi}")
        
        if self.oyundan_cikarildi:
            print(f"  ❌ DURUM: Oyundan çıkarıldı")
        elif self.enerji_kritik_mi():
            print(f"  ⚠️ DURUM: Kritik enerji")
        else:
            print(f"  ✅ DURUM: Aktif")
        
        print(f"{'='*50}")
        
        return {
            'sporcu_id': self.sporcu_id,
            'sporcu_adi': self.sporcu_adi,
            'seviye': self.seviye,
            'deneyim_puani': self.deneyim_puani,
            'enerji': self.enerji,
            'max_enerji': self.max_enerji,
            'dayaniklilik': self.dayaniklilik,
            'galibiyet_sayisi': self.galibiyet_sayisi
        }
    
    def kartBilgisiYazdir(self):
        """Kart bilgilerini ekrana yazdır
        
        Returns:
            str: Kart bilgisi metni
        """
        durum = "❌ Çıkarıldı" if self.oyundan_cikarildi else "⚠️ Kritik" if self.enerji_kritik_mi() else "✅ Aktif"
        kullanim = "Evet" if self.kart_kullanildi_mi else "Hayır"
        
        bilgi = f"""
{'─'*40}
📋 KART BİLGİSİ
{'─'*40}
  Ad: {self.sporcu_adi}
  Takım: {self.takim_adi}
  Branş: {self.brans}
  Seviye: {self.seviye}
  Enerji: {self.enerji}/{self.max_enerji}
  Dayanıklılık: {self.dayaniklilik}
  Özel Yetenek: {self.ozel_yetenek.ac_kla() if self.ozel_yetenek else 'Yok'}
  Bu Turda Kullanıldı: {kullanim}
  Durum: {durum}
{'─'*40}"""
        
        print(bilgi)
        return bilgi
    
    def performansHesapla(self, ozellik_adi=None):
        """Sporcunun performans puanını hesapla
        
        Args:
            ozellik_adi (str, optional): Hesaplanacak özellik adı
            
        Returns:
            float: Hesaplanan performans puanı
        """
        # Temel performans puanı
        temel_puan = 0
        
        # Seviye bonusu
        seviye_bonus = (self.seviye - 1) * self.SEVIYE_OZELLIK_BONUS
        
        # Enerji cezası
        if self.enerji > 70:
            enerji_carpani = 1.0
        elif self.enerji >= 40:
            enerji_carpani = 0.9  # %10 düşüş
        elif self.enerji > 0:
            enerji_carpani = 0.8  # %20 düşüş
        else:
            enerji_carpani = 0  # Oynanamaz
        
        # Deneyim bonusu (%10'u)
        deneyim_bonus = (self.deneyim_puani or 0) * 0.10
        
        # Dayanıklılık bonusu
        dayaniklilik_bonus = (self.dayaniklilik or 0) * 0.05
        
        # Toplam performans
        performans = (temel_puan + seviye_bonus + deneyim_bonus + dayaniklilik_bonus) * enerji_carpani
        
        return performans
    
    def seviyeAtlaKontrol(self):
        """Seviye atlama koşullarını kontrol et ve gerekirse seviye atla
        
        Returns:
            dict: Seviye atlama sonucu
        """
        sonuc = {
            'seviye_atladi': False,
            'onceki_seviye': self.seviye,
            'yeni_seviye': self.seviye,
            'bonuslar': []
        }
        
        # Maksimum seviye kontrolü
        if self.seviye >= self.MAX_SEVIYE:
            return sonuc
        
        yeni_seviye = self.seviye
        
        # Seviye 2'ye atlama kontrolü
        if self.seviye == 1:
            if self.galibiyet_sayisi >= self.SEVIYE_2_GALIBIYET or self.deneyim_puani >= self.SEVIYE_2_DENEYIM:
                yeni_seviye = 2
        
        # Seviye 3'e atlama kontrolü
        elif self.seviye == 2:
            if self.galibiyet_sayisi >= self.SEVIYE_3_GALIBIYET or self.deneyim_puani >= self.SEVIYE_3_DENEYIM:
                yeni_seviye = 3
        
        # Seviye atladıysa
        if yeni_seviye > self.seviye:
            sonuc['seviye_atladi'] = True
            sonuc['yeni_seviye'] = yeni_seviye
            self.seviye = yeni_seviye
            
            # Maksimum enerji artışı
            self.max_enerji += self.SEVIYE_ENERJI_BONUS
            sonuc['bonuslar'].append(f"Maksimum Enerji +{self.SEVIYE_ENERJI_BONUS}")
            
            # Dayanıklılık artışı
            if self.dayaniklilik is not None:
                self.dayaniklilik += self.SEVIYE_DAYANIKLILIK_BONUS
                sonuc['bonuslar'].append(f"Dayanıklılık +{self.SEVIYE_DAYANIKLILIK_BONUS}")
        
        return sonuc
    
    def ozelYetenekUygula(self, hedef=None):
        """Özel yeteneği uygula
        
        Args:
            hedef: Yeteneğin uygulanacağı hedef (varsa)
            
        Returns:
            dict: Özel yetenek uygulama sonucu
        """
        sonuc = {
            'basarili': False,
            'yetenek': self.ozel_yetenek,
            'bonus': 0,
            'enerji_maliyeti': self.OZEL_YETENEK_ENERJI_KAYBI,
            'aciklama': ''
        }
        
        # Özel yetenek yoksa
        if not self.ozel_yetenek:
            sonuc['aciklama'] = 'Bu sporcunun özel yeteneği yok.'
            return sonuc
        
        # Enerji yeterli mi?
        if self.enerji < self.OZEL_YETENEK_ENERJI_KAYBI:
            sonuc['aciklama'] = f'Yeterli enerji yok. Gerekli: {self.OZEL_YETENEK_ENERJI_KAYBI}, Mevcut: {self.enerji}'
            return sonuc
        
        # Özel yetenek bonusunu hesapla
        if hasattr(self, 'ozel_yetenek_katsayisi') and self.ozel_yetenek_katsayisi:
            sonuc['bonus'] = float(self.ozel_yetenek_katsayisi)
        else:
            sonuc['bonus'] = 5  # Varsayılan bonus
        
        sonuc['basarili'] = True
        sonuc['aciklama'] = f"'{self.ozel_yetenek}' yeteneği uygulandı. Bonus: +{sonuc['bonus']}"
        
        return sonuc
