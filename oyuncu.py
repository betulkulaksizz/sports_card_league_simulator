from abc import ABC, abstractmethod


class Oyuncu(ABC):
    """Kart oyununda oyuncu için abstract sınıf"""
    
    # Moral sabitleri
    BASLANGIC_MORAL = 100
    MAX_MORAL = 100
    MIN_MORAL = 0
    
    # Moral seviyeleri
    YUKSEK_MORAL_ALT = 80
    NORMAL_MORAL_ALT = 50
    DUSUK_MORAL_UST = 49
    
    # Moral değişim miktarları
    UST_USTE_2_GALIBIYET_BONUS = 10
    UST_USTE_3_GALIBIYET_BONUS = 15
    UST_USTE_2_MAGLUBIYET_CEZA = 10
    AYNI_BRANS_2_KAYIP_CEZA = 5
    
    # ===== PUANLAMA SABİTLERİ =====
    NORMAL_GALIBIYET_PUAN = 10
    OZEL_YETENEK_GALIBIYET_PUAN = 15
    HUKMEN_GALIBIYET_PUAN = 8
    BERABERLIK_PUAN = 0
    
    # Seri bonusları
    SERI_3_BONUS = 10      # Üst üste 3 galibiyet serisi: ekstra 10 puan
    SERI_5_BONUS = 20      # Üst üste 5 galibiyet serisi: ekstra 20 puan
    
    # Ek bonuslar
    DUSUK_ENERJI_GALIBIYET_BONUS = 5    # Enerjisi 30 altı kartla kazanma: +5
    SEVIYE_ATLADI_GALIBIYET_BONUS = 5   # Seviye atladıktan sonraki ilk galibiyet: +5
    CLUTCH_PLAYER_BONUS = 5             # Son 3 turda Clutch Player yetenekli kartla kazanma: +5
    
    # Cezalar
    GECERSIZ_KART_SECIMI_CEZA = 5       # Geçersiz kart seçimi: -5 puan
    
    def __init__(self, oyuncu_id, oyuncu_adi):
        self.oyuncu_id = oyuncu_id              # Oyuncu ID
        self.oyuncu_adi = oyuncu_adi            # Oyuncu adı
        self.skor = 0                           # Skor
        self.moral = self.BASLANGIC_MORAL       # Moral (başlangıç: 100)
        self.kart_listesi = []                  # Kart Listesi
        self.galibiyet_serisi = 0               # Galibiyetlerinin serisi
        self.kaybetme_serisi = 0                # Kayıplarının serisi
        
        # Branş bazlı kayıp takibi (moral sistemi için)
        self.brans_kayip_serisi = {
            "Futbol": 0,
            "Basketbol": 0,
            "Voleybol": 0
        }
        self.son_oynanan_brans = None           # Son oynanan branş
        
        # Oyun sonu istatistikleri
        self.kazanilan_tur_sayisi = 0           # Kazanılan tur sayısı
        self.toplam_galibiyet_serisi = 0        # Toplam galibiyet serisi sayısı
        self.max_galibiyet_serisi = 0           # En yüksek galibiyet serisi
        self.ozel_yetenekle_kazanilan_tur = 0   # Özel yetenekle kazanılan tur sayısı
        self.beraberlik_sayisi = 0              # Beraberlik sayısı
        self.kayip_sayisi = 0                   # Kayıp sayısı
        
        # Bonus takibi
        self.son_seviye_atlayan_kartlar = set()  # Seviye atlayan kart ad'ları (ilk galibiyet bonusu için)
        self.clutch_player_kartlar = []          # Son 3 turda Clutch Player yetenekli oynanan kartlar
    
    def moral_seviyesi_al(self):
        """Mevcut moral seviyesini string olarak döndür
        
        Returns:
            str: 'yuksek', 'normal' veya 'dusuk'
        """
        if self.moral >= self.YUKSEK_MORAL_ALT:
            return 'yuksek'
        elif self.moral >= self.NORMAL_MORAL_ALT:
            return 'normal'
        else:
            return 'dusuk'
    
    def moral_puan_etkisi(self):
        """Moralin puan üzerindeki etkisini hesapla
        
        Returns:
            float: Puana eklenecek/çıkarılacak değer (çarpan olarak)
        """
        seviye = self.moral_seviyesi_al()
        if seviye == 'yuksek':
            return 1.10  # %10 bonus
        elif seviye == 'normal':
            return 1.00  # Değişiklik yok
        else:  # dusuk
            return 0.90  # %10 ceza
    
    def moral_guncelle(self, sonuc, brans, ozel_yetenek_kullanildi=False):
        """Tur sonucuna göre morali güncelle
        
        Args:
            sonuc (str): 'kazandi', 'kaybetti', 'berabere'
            brans (str): Oynanan branş
            ozel_yetenek_kullanildi (bool): Özel yetenek kullanıldı mı
            
        Returns:
            dict: Moral değişim detayları
        """
        detaylar = {
            'onceki_moral': self.moral,
            'degisim': 0,
            'sebep': []
        }
        
        if sonuc == 'kazandi':
            # Galibiyet serisi güncelle
            self.galibiyet_serisi += 1
            self.kaybetme_serisi = 0
            
            # Branş kayıp serisini sıfırla
            self.brans_kayip_serisi[brans] = 0
            
            # Üst üste galibiyet bonusları
            if self.galibiyet_serisi >= 3:
                self.moral = min(self.MAX_MORAL, self.moral + self.UST_USTE_3_GALIBIYET_BONUS)
                detaylar['degisim'] += self.UST_USTE_3_GALIBIYET_BONUS
                detaylar['sebep'].append(f"Üst üste 3 galibiyet: +{self.UST_USTE_3_GALIBIYET_BONUS}")
            elif self.galibiyet_serisi >= 2:
                self.moral = min(self.MAX_MORAL, self.moral + self.UST_USTE_2_GALIBIYET_BONUS)
                detaylar['degisim'] += self.UST_USTE_2_GALIBIYET_BONUS
                detaylar['sebep'].append(f"Üst üste 2 galibiyet: +{self.UST_USTE_2_GALIBIYET_BONUS}")
        
        elif sonuc == 'kaybetti':
            # Kayıp serisi güncelle
            self.kaybetme_serisi += 1
            self.galibiyet_serisi = 0
            
            # Branş kayıp serisini güncelle
            self.brans_kayip_serisi[brans] += 1
            
            # Üst üste mağlubiyet cezası
            if self.kaybetme_serisi >= 2:
                self.moral = max(self.MIN_MORAL, self.moral - self.UST_USTE_2_MAGLUBIYET_CEZA)
                detaylar['degisim'] -= self.UST_USTE_2_MAGLUBIYET_CEZA
                detaylar['sebep'].append(f"Üst üste 2 mağlubiyet: -{self.UST_USTE_2_MAGLUBIYET_CEZA}")
            
            # Aynı branşta art arda 2 kayıp ek cezası
            if self.brans_kayip_serisi[brans] >= 2:
                self.moral = max(self.MIN_MORAL, self.moral - self.AYNI_BRANS_2_KAYIP_CEZA)
                detaylar['degisim'] -= self.AYNI_BRANS_2_KAYIP_CEZA
                detaylar['sebep'].append(f"Aynı branşta ({brans}) 2 kayıp: -{self.AYNI_BRANS_2_KAYIP_CEZA}")
        
        # Beraberlikte moral değişmez
        elif sonuc == 'berabere':
            self.galibiyet_serisi = 0
            self.kaybetme_serisi = 0
            detaylar['sebep'].append("Beraberlik: Moral değişmedi")
        
        self.son_oynanan_brans = brans
        detaylar['yeni_moral'] = self.moral
        
        return detaylar
    
    def aktif_kartlari_al(self):
        """Oyundan çıkarılmamış kartları döndür"""
        return [k for k in self.kart_listesi if not k.get('oyundan_cikarildi', False)]
    
    def cikarilmis_kartlari_al(self):
        """Oyundan çıkarılmış kartları döndür"""
        return [k for k in self.kart_listesi if k.get('oyundan_cikarildi', False)]
    
    def kritik_enerjili_kartlari_al(self):
        """Kritik enerjili kartları döndür (enerji < 20)"""
        from sporcu import Sporcu
        return [k for k in self.aktif_kartlari_al() 
                if k.get('enerji', 100) < Sporcu.KRITIK_ENERJI_ESIGI and k.get('enerji', 100) > 0]
    
    def moral_durum_goster(self):
        """Moral durumunu görsel olarak göster"""
        seviye = self.moral_seviyesi_al()
        if seviye == 'yuksek':
            return f"🟢 Yüksek Moral ({self.moral}/100)"
        elif seviye == 'normal':
            return f"🟡 Normal Moral ({self.moral}/100)"
        else:
            return f"🔴 Düşük Moral ({self.moral}/100)"
    
    # ==================== OYUN SONU İSTATİSTİKLERİ ====================
    
    def tur_sonucu_kaydet(self, sonuc, ozel_yetenek_etkili=False):
        """Tur sonucunu istatistiklere kaydet
        
        Args:
            sonuc (str): 'kazandi', 'kaybetti', 'berabere'
            ozel_yetenek_etkili (bool): Özel yetenek etkili mi
        """
        if sonuc == 'kazandi':
            self.kazanilan_tur_sayisi += 1
            
            # Galibiyet serisi takibi
            if self.galibiyet_serisi > self.max_galibiyet_serisi:
                self.max_galibiyet_serisi = self.galibiyet_serisi
            
            # Özel yetenekle kazanılan tur
            if ozel_yetenek_etkili:
                self.ozel_yetenekle_kazanilan_tur += 1
        
        elif sonuc == 'kaybetti':
            self.kayip_sayisi += 1
            
            # Galibiyet serisi bittiyse toplama ekle
            if self.galibiyet_serisi > 0:
                self.toplam_galibiyet_serisi += self.galibiyet_serisi
        
        elif sonuc == 'berabere':
            self.beraberlik_sayisi += 1
            
            # Galibiyet serisi bittiyse toplama ekle
            if self.galibiyet_serisi > 0:
                self.toplam_galibiyet_serisi += self.galibiyet_serisi
    
    def kalan_toplam_enerji(self):
        """Kalan toplam enerji hesapla
        
        Returns:
            int: Tüm aktif kartların toplam enerjisi
        """
        aktif_kartlar = self.aktif_kartlari_al()
        return sum(k.get('enerji', 0) for k in aktif_kartlar)
    
    def en_yuksek_seviyeli_kart_sayisi(self):
        """En yüksek seviyeli (seviye 3) kart sayısını döndür
        
        Returns:
            int: Seviye 3 kart sayısı
        """
        from sporcu import Sporcu
        aktif_kartlar = self.aktif_kartlari_al()
        return len([k for k in aktif_kartlar if k.get('seviye', 1) >= Sporcu.MAX_SEVIYE])
    
    def oyun_sonu_istatistikleri(self):
        """Oyun sonu istatistiklerini döndür
        
        Returns:
            dict: İstatistikler
        """
        # Son galibiyet serisini toplama ekle
        if self.galibiyet_serisi > 0:
            self.toplam_galibiyet_serisi += self.galibiyet_serisi
        
        return {
            'toplam_puan': self.skor,
            'kazanilan_tur_sayisi': self.kazanilan_tur_sayisi,
            'toplam_galibiyet_serisi': self.toplam_galibiyet_serisi,
            'max_galibiyet_serisi': self.max_galibiyet_serisi,
            'kalan_toplam_enerji': self.kalan_toplam_enerji(),
            'en_yuksek_seviyeli_kart_sayisi': self.en_yuksek_seviyeli_kart_sayisi(),
            'ozel_yetenekle_kazanilan_tur': self.ozel_yetenekle_kazanilan_tur,
            'beraberlik_sayisi': self.beraberlik_sayisi,
            'kayip_sayisi': self.kayip_sayisi
        }
    
    @abstractmethod
    def kart_sec(self):
        """Oyuncu tarafından kart seçme işlemi"""
        pass
    
    @abstractmethod
    def strateji_uygula(self):
        """Oyuncu stratejisini uygulama"""
        pass
