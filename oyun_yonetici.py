from tur_yoneticisi import TurYoneticisi
from kart_dagitici import KartDagitici


class OyunYonetici:
    """Oyun akışını yöneten ana sınıf
    
    Sorumluluklar:
    - Oyun akışını yönetir
    - Tur başlatır
    - Kartları karşılaştırır
    - Puanları günceller
    - Kazananı belirler
    """
    
    # Oyun durumları
    DURUM_BASLAMADI = 'baslamadi'
    DURUM_DEVAM_EDIYOR = 'devam_ediyor'
    DURUM_BITTI = 'bitti'
    
    def __init__(self):
        self.tur_yoneticisi = TurYoneticisi()
        self.oyuncu1 = None
        self.oyuncu2 = None
        self.oyun_durumu = self.DURUM_BASLAMADI
        self.toplam_tur = 0
        self.oynanan_turlar = []
        self.kazanan = None
    
    def ozellik_secim_modunu_ayarla(self, mod):
        """Özellik seçim modunu ayarla
        
        Args:
            mod (str): 'rastgele' veya 'kullanici'
        """
        self.tur_yoneticisi.ozellik_secim_modunu_ayarla(mod)
    
    def oyunu_baslat(self, oyuncu1, oyuncu2):
        """Oyunu başlat
        
        Args:
            oyuncu1: Birinci oyuncu (Kullanici)
            oyuncu2: İkinci oyuncu (Bilgisayar)
        """
        self.oyuncu1 = oyuncu1
        self.oyuncu2 = oyuncu2
        self.oyun_durumu = self.DURUM_DEVAM_EDIYOR
        self.toplam_tur = 0
        self.oynanan_turlar = []
        self.kazanan = None
        
        print(f"\n{'='*60}")
        print(f"{'OYUN BAŞLADI':^60}")
        print(f"{'='*60}")
        print(f"\n{oyuncu1.oyuncu_adi} vs {oyuncu2.oyuncu_adi}")
        print(f"\nOyuncular hazır. İlk tur başlıyor...")
    
    def tur_baslat(self):
        """Yeni bir tur başlat
        
        Returns:
            dict: Tur sonucu
        """
        if self.oyun_durumu != self.DURUM_DEVAM_EDIYOR:
            print("Oyun başlatılmadı veya bitti!")
            return None
        
        # Oynanabilir kart kontrolü
        if not self._oyun_devam_edebilir_mi():
            self.oyunu_bitir()
            return {'durum': 'bitti', 'sebep': 'kart_bitti'}
        
        self.toplam_tur += 1
        
        # Turu oyna
        tur_sonucu = self.tur_yoneticisi.tur_oyna(self.oyuncu1, self.oyuncu2)
        
        # Tur sonucunu kaydet
        tur_kayit = {
            'tur_no': self.toplam_tur,
            'brans': self.tur_yoneticisi.mevcut_brans,
            'sonuc': tur_sonucu[0],
            'oyuncu1_karti': tur_sonucu[1] if len(tur_sonucu) > 1 else None,
            'oyuncu2_karti': tur_sonucu[2] if len(tur_sonucu) > 2 else None,
            'kazanan': tur_sonucu[3] if len(tur_sonucu) > 3 else None
        }
        self.oynanan_turlar.append(tur_kayit)
        
        return tur_kayit
    
    def kartlari_karsilastir(self, kart1, kart2, ozellik):
        """İki kartı belirli bir özelliğe göre karşılaştır
        
        Args:
            kart1 (dict): Birinci kart
            kart2 (dict): İkinci kart
            ozellik (str): Karşılaştırılacak özellik
            
        Returns:
            dict: Karşılaştırma sonucu
        """
        # Performans hesapla
        puan1 = KartDagitici.performansHesapla(kart1, ozellik)
        puan2 = KartDagitici.performansHesapla(kart2, ozellik)
        
        sonuc = {
            'kart1_puan': puan1,
            'kart2_puan': puan2,
            'kazanan': None,
            'fark': abs(puan1 - puan2)
        }
        
        if puan1 > puan2:
            sonuc['kazanan'] = 'kart1'
        elif puan2 > puan1:
            sonuc['kazanan'] = 'kart2'
        else:
            sonuc['kazanan'] = 'berabere'
        
        return sonuc
    
    def puanlari_guncelle(self, kazanan_oyuncu, puan):
        """Kazanan oyuncunun puanını güncelle
        
        Args:
            kazanan_oyuncu: Kazanan oyuncu
            puan (int): Eklenecek puan
        """
        if kazanan_oyuncu:
            kazanan_oyuncu.skor += puan
            print(f"  {kazanan_oyuncu.oyuncu_adi} +{puan} puan kazandı!")
            print(f"  Yeni skor: {kazanan_oyuncu.skor}")
    
    def kazanani_belirle(self):
        """Oyun sonu kazananını belirle
        
        Returns:
            dict: Kazanan bilgisi
        """
        sonuc = self.tur_yoneticisi.oyun_sonu_kazanani_belirle(
            self.oyuncu1, self.oyuncu2
        )
        self.kazanan = sonuc['kazanan']
        return sonuc
    
    def oyunu_bitir(self):
        """Oyunu bitir ve sonuçları göster"""
        self.oyun_durumu = self.DURUM_BITTI
        
        print(f"\n{'='*60}")
        print(f"{'OYUN BİTTİ':^60}")
        print(f"{'='*60}")
        
        # Oyun sonu raporu
        sonuc = self.tur_yoneticisi.oyun_sonu_raporu_goster(
            self.oyuncu1, self.oyuncu2
        )
        
        self.kazanan = sonuc['kazanan']
        
        return sonuc
    
    def oyun_durumu_goster(self):
        """Mevcut oyun durumunu göster"""
        print(f"\n{'='*60}")
        print(f"OYUN DURUMU")
        print(f"{'='*60}")
        print(f"Durum: {self.oyun_durumu}")
        print(f"Toplam Oynanan Tur: {self.toplam_tur}")
        print(f"Mevcut Branş: {self.tur_yoneticisi.mevcut_brans}")
        
        if self.oyuncu1 and self.oyuncu2:
            print(f"\n{self.oyuncu1.oyuncu_adi}:")
            print(f"  Skor: {self.oyuncu1.skor}")
            print(f"  Aktif Kart: {len(self.oyuncu1.aktif_kartlari_al())}")
            print(f"  {self.oyuncu1.moral_durum_goster()}")
            
            print(f"\n{self.oyuncu2.oyuncu_adi}:")
            print(f"  Skor: {self.oyuncu2.skor}")
            print(f"  Aktif Kart: {len(self.oyuncu2.aktif_kartlari_al())}")
            print(f"  {self.oyuncu2.moral_durum_goster()}")
        
        if self.kazanan:
            print(f"\n🏆 Kazanan: {self.kazanan.oyuncu_adi}")
    
    def tur_gecmisi_goster(self):
        """Oynanan turların geçmişini göster"""
        print(f"\n{'='*60}")
        print(f"TUR GEÇMİŞİ")
        print(f"{'='*60}")
        
        if not self.oynanan_turlar:
            print("Henüz tur oynanmadı.")
            return
        
        print(f"{'Tur':<5} {'Branş':<12} {'Sonuç':<15} {'Kazanan':<15}")
        print(f"{'-'*60}")
        
        for tur in self.oynanan_turlar:
            kazanan_str = tur.get('kazanan', 'N/A')
            if kazanan_str == 'oyuncu1':
                kazanan_str = self.oyuncu1.oyuncu_adi
            elif kazanan_str == 'oyuncu2':
                kazanan_str = self.oyuncu2.oyuncu_adi
            elif kazanan_str == 'berabere':
                kazanan_str = 'Berabere'
            
            print(f"{tur['tur_no']:<5} {tur.get('brans', 'N/A'):<12} {tur['sonuc']:<15} {kazanan_str:<15}")
    
    def istatistikleri_goster(self):
        """Oyun istatistiklerini göster"""
        print(f"\n{'='*60}")
        print(f"OYUN İSTATİSTİKLERİ")
        print(f"{'='*60}")
        
        # Tur istatistikleri
        oyuncu1_kazandigi = len([t for t in self.oynanan_turlar if t.get('kazanan') == 'oyuncu1'])
        oyuncu2_kazandigi = len([t for t in self.oynanan_turlar if t.get('kazanan') == 'oyuncu2'])
        beraberlik = len([t for t in self.oynanan_turlar if t.get('kazanan') == 'berabere'])
        atlanan = len([t for t in self.oynanan_turlar if t['sonuc'] == 'atlan'])
        
        print(f"\nTur Sonuçları:")
        print(f"  {self.oyuncu1.oyuncu_adi} Kazandığı: {oyuncu1_kazandigi}")
        print(f"  {self.oyuncu2.oyuncu_adi} Kazandığı: {oyuncu2_kazandigi}")
        print(f"  Beraberlik: {beraberlik}")
        print(f"  Atlanan Tur: {atlanan}")
        
        # Branş bazlı istatistikler
        print(f"\nBranş Bazlı:")
        for brans in TurYoneticisi.BRANS_SIRASI:
            brans_turlari = [t for t in self.oynanan_turlar if t.get('brans') == brans]
            print(f"  {brans}: {len(brans_turlari)} tur oynandı")
    
    def _oyun_devam_edebilir_mi(self):
        """Oyunun devam edip edemeyeceğini kontrol et
        
        Returns:
            bool: Oyun devam edebilir mi
        """
        oyuncu1_aktif = len(self.oyuncu1.aktif_kartlari_al())
        oyuncu2_aktif = len(self.oyuncu2.aktif_kartlari_al())
        
        # Her iki oyuncunun da kartı varsa devam edilebilir
        return oyuncu1_aktif > 0 and oyuncu2_aktif > 0
    
    def tam_oyun_oyna(self, max_tur=12):
        """Tam bir oyun oyna (baştan sona)
        
        Args:
            max_tur (int): Maksimum tur sayısı
            
        Returns:
            dict: Oyun sonucu
        """
        print(f"\n{'='*60}")
        print(f"{'TAM OYUN BAŞLIYOR':^60}")
        print(f"{'='*60}")
        print(f"Maksimum {max_tur} tur oynanacak.\n")
        
        for i in range(max_tur):
            # Oyun devam edebilir mi?
            if not self._oyun_devam_edebilir_mi():
                print(f"\nOyunculardan birinin kartı bitti. Oyun sona eriyor...")
                break
            
            # Turu oyna
            tur_sonucu = self.tur_baslat()
            
            if tur_sonucu and tur_sonucu.get('durum') == 'bitti':
                break
            
            print(f"\n--- Tur {i+1} tamamlandı ---")
        
        # Oyunu bitir
        return self.oyunu_bitir()
    
    def interaktif_oyun_oyna(self, max_tur=12):
        """İnteraktif oyun oyna (kullanıcı kontrolü ile)
        
        Args:
            max_tur (int): Maksimum tur sayısı
            
        Returns:
            dict: Oyun sonucu
        """
        for i in range(max_tur):
            # Oyun devam edebilir mi?
            if not self._oyun_devam_edebilir_mi():
                print(f"\nOyunculardan birinin kartı bitti. Oyun sona eriyor...")
                break
            
            # Tur bilgisini göster
            self.tur_yoneticisi.tur_bilgisi_goster(self.oyuncu1, self.oyuncu2)
            
            # Turu oyna
            tur_sonucu = self.tur_baslat()
            
            if tur_sonucu and tur_sonucu.get('durum') == 'bitti':
                break
            
            # Kullanıcı girişi
            print(f"\n[Tur {i+1}/{max_tur}]")
            secim = input("Devam: Enter | Durum: 'd' | Geçmiş: 'g' | İstatistik: 'i' | Çıkış: 'q': ").strip().lower()
            
            if secim == 'd':
                self.oyun_durumu_goster()
                input("\nDevam etmek için Enter'a basın...")
            elif secim == 'g':
                self.tur_gecmisi_goster()
                input("\nDevam etmek için Enter'a basın...")
            elif secim == 'i':
                self.istatistikleri_goster()
                input("\nDevam etmek için Enter'a basın...")
            elif secim == 'q':
                print("Oyundan çıkılıyor...")
                break
        
        # Oyunu bitir
        return self.oyunu_bitir()
