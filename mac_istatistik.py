"""
MacIstatistik Sınıfı
Tüm maç verilerini tutar ve rapor oluşturur
"""

from datetime import datetime


class MacIstatistik:
    """Maç istatistiklerini tutan ve rapor oluşturan sınıf"""
    
    def __init__(self):
        # Maç bilgileri
        self.mac_baslangic_zamani = None
        self.mac_bitis_zamani = None
        self.toplam_tur_sayisi = 0
        
        # Oyuncu istatistikleri
        self.kullanici_istatistikleri = {
            'toplam_puan': 0,
            'kazanilan_tur': 0,
            'kaybedilen_tur': 0,
            'beraberlik': 0,
            'max_galibiyet_serisi': 0,
            'ozel_yetenekle_kazanilan': 0,
            'hukmen_galibiyet': 0,
            'kullanilan_kartlar': [],
            'brans_performans': {
                'Futbol': {'kazanilan': 0, 'kaybedilen': 0, 'berabere': 0},
                'Basketbol': {'kazanilan': 0, 'kaybedilen': 0, 'berabere': 0},
                'Voleybol': {'kazanilan': 0, 'kaybedilen': 0, 'berabere': 0}
            }
        }
        
        self.bilgisayar_istatistikleri = {
            'toplam_puan': 0,
            'kazanilan_tur': 0,
            'kaybedilen_tur': 0,
            'beraberlik': 0,
            'max_galibiyet_serisi': 0,
            'ozel_yetenekle_kazanilan': 0,
            'hukmen_galibiyet': 0,
            'kullanilan_kartlar': [],
            'brans_performans': {
                'Futbol': {'kazanilan': 0, 'kaybedilen': 0, 'berabere': 0},
                'Basketbol': {'kazanilan': 0, 'kaybedilen': 0, 'berabere': 0},
                'Voleybol': {'kazanilan': 0, 'kaybedilen': 0, 'berabere': 0}
            }
        }
        
        # Tur detayları
        self.tur_gecmisi = []
        
        # Kazanan bilgisi
        self.kazanan = None
        self.kazanma_asama = None
        self.kazanma_detay = None
    
    def mac_baslat(self):
        """Maçı başlat ve zamanı kaydet"""
        self.mac_baslangic_zamani = datetime.now()
        self.toplam_tur_sayisi = 0
        self.tur_gecmisi = []
        print(f"📍 Maç başladı: {self.mac_baslangic_zamani.strftime('%H:%M:%S')}")
    
    def mac_bitir(self, kazanan, asama, detay):
        """Maçı bitir ve sonucu kaydet"""
        self.mac_bitis_zamani = datetime.now()
        self.kazanan = kazanan
        self.kazanma_asama = asama
        self.kazanma_detay = detay
        print(f"🏁 Maç bitti: {self.mac_bitis_zamani.strftime('%H:%M:%S')}")
    
    def tur_kaydet(self, tur_no, brans, ozellik, kullanici_kart, bilgisayar_kart, 
                   kullanici_puan, bilgisayar_puan, kazanan, kazanilan_puan=0):
        """Tur sonucunu kaydet
        
        Args:
            tur_no (int): Tur numarası
            brans (str): Oynanan branş
            ozellik (str): Karşılaştırılan özellik
            kullanici_kart (dict): Kullanıcının oynadığı kart
            bilgisayar_kart (dict): Bilgisayarın oynadığı kart
            kullanici_puan (float): Kullanıcının güncel puanı
            bilgisayar_puan (float): Bilgisayarın güncel puanı
            kazanan (str): 'kullanici', 'bilgisayar' veya 'berabere'
            kazanilan_puan (int): Kazanılan puan
        """
        self.toplam_tur_sayisi = tur_no
        
        tur_detay = {
            'tur_no': tur_no,
            'brans': brans,
            'ozellik': ozellik,
            'kullanici_kart': kullanici_kart.get('ad', '?') if kullanici_kart else 'Yok',
            'bilgisayar_kart': bilgisayar_kart.get('ad', '?') if bilgisayar_kart else 'Yok',
            'kullanici_puan': kullanici_puan,
            'bilgisayar_puan': bilgisayar_puan,
            'kazanan': kazanan,
            'kazanilan_puan': kazanilan_puan
        }
        self.tur_gecmisi.append(tur_detay)
        
        # İstatistikleri güncelle
        if kazanan == 'kullanici':
            self.kullanici_istatistikleri['kazanilan_tur'] += 1
            self.kullanici_istatistikleri['toplam_puan'] += kazanilan_puan
            self.kullanici_istatistikleri['brans_performans'][brans]['kazanilan'] += 1
            self.bilgisayar_istatistikleri['kaybedilen_tur'] += 1
            self.bilgisayar_istatistikleri['brans_performans'][brans]['kaybedilen'] += 1
            if kullanici_kart:
                self.kullanici_istatistikleri['kullanilan_kartlar'].append(kullanici_kart.get('ad', '?'))
        elif kazanan == 'bilgisayar':
            self.bilgisayar_istatistikleri['kazanilan_tur'] += 1
            self.bilgisayar_istatistikleri['toplam_puan'] += kazanilan_puan
            self.bilgisayar_istatistikleri['brans_performans'][brans]['kazanilan'] += 1
            self.kullanici_istatistikleri['kaybedilen_tur'] += 1
            self.kullanici_istatistikleri['brans_performans'][brans]['kaybedilen'] += 1
            if bilgisayar_kart:
                self.bilgisayar_istatistikleri['kullanilan_kartlar'].append(bilgisayar_kart.get('ad', '?'))
        else:  # berabere
            self.kullanici_istatistikleri['beraberlik'] += 1
            self.kullanici_istatistikleri['brans_performans'][brans]['berabere'] += 1
            self.bilgisayar_istatistikleri['beraberlik'] += 1
            self.bilgisayar_istatistikleri['brans_performans'][brans]['berabere'] += 1
    
    def hukmen_galibiyet_kaydet(self, kazanan, brans, puan):
        """Hükmen galibiyeti kaydet"""
        if kazanan == 'kullanici':
            self.kullanici_istatistikleri['hukmen_galibiyet'] += 1
            self.kullanici_istatistikleri['toplam_puan'] += puan
        else:
            self.bilgisayar_istatistikleri['hukmen_galibiyet'] += 1
            self.bilgisayar_istatistikleri['toplam_puan'] += puan
    
    def ozel_yetenek_galibiyet_kaydet(self, kazanan):
        """Özel yetenekle kazanılan turu kaydet"""
        if kazanan == 'kullanici':
            self.kullanici_istatistikleri['ozel_yetenekle_kazanilan'] += 1
        else:
            self.bilgisayar_istatistikleri['ozel_yetenekle_kazanilan'] += 1
    
    def max_seri_guncelle(self, kullanici_seri, bilgisayar_seri):
        """Maksimum galibiyet serilerini güncelle"""
        if kullanici_seri > self.kullanici_istatistikleri['max_galibiyet_serisi']:
            self.kullanici_istatistikleri['max_galibiyet_serisi'] = kullanici_seri
        if bilgisayar_seri > self.bilgisayar_istatistikleri['max_galibiyet_serisi']:
            self.bilgisayar_istatistikleri['max_galibiyet_serisi'] = bilgisayar_seri
    
    def rapor_olustur(self):
        """Detaylı maç raporu oluştur
        
        Returns:
            str: Formatlı rapor metni
        """
        if not self.mac_baslangic_zamani:
            return "❌ Henüz maç başlamadı!"
        
        # Maç süresi hesapla
        if self.mac_bitis_zamani:
            sure = self.mac_bitis_zamani - self.mac_baslangic_zamani
            dakika = int(sure.total_seconds() // 60)
            saniye = int(sure.total_seconds() % 60)
            sure_str = f"{dakika} dakika {saniye} saniye"
        else:
            sure_str = "Devam ediyor..."
        
        rapor = f"""
{'='*70}
                    📊 MAÇ İSTATİSTİK RAPORU 📊
{'='*70}

📅 Maç Başlangıcı: {self.mac_baslangic_zamani.strftime('%d.%m.%Y %H:%M:%S') if self.mac_baslangic_zamani else 'Bilinmiyor'}
📅 Maç Bitişi:     {self.mac_bitis_zamani.strftime('%d.%m.%Y %H:%M:%S') if self.mac_bitis_zamani else 'Devam ediyor'}
⏱️ Maç Süresi:     {sure_str}
🔄 Toplam Tur:     {self.toplam_tur_sayisi}

{'─'*70}
                        👤 KULLANICI İSTATİSTİKLERİ
{'─'*70}
  🏆 Toplam Puan:           {self.kullanici_istatistikleri['toplam_puan']}
  ✅ Kazanılan Tur:         {self.kullanici_istatistikleri['kazanilan_tur']}
  ❌ Kaybedilen Tur:        {self.kullanici_istatistikleri['kaybedilen_tur']}
  🤝 Beraberlik:            {self.kullanici_istatistikleri['beraberlik']}
  🔥 Max Galibiyet Serisi:  {self.kullanici_istatistikleri['max_galibiyet_serisi']}
  ⭐ Özel Yetenekle Kazanılan: {self.kullanici_istatistikleri['ozel_yetenekle_kazanilan']}
  📋 Hükmen Galibiyet:      {self.kullanici_istatistikleri['hukmen_galibiyet']}

  📊 Branş Performansı:
     ⚽ Futbol:     K:{self.kullanici_istatistikleri['brans_performans']['Futbol']['kazanilan']} | Y:{self.kullanici_istatistikleri['brans_performans']['Futbol']['kaybedilen']} | B:{self.kullanici_istatistikleri['brans_performans']['Futbol']['berabere']}
     🏀 Basketbol: K:{self.kullanici_istatistikleri['brans_performans']['Basketbol']['kazanilan']} | Y:{self.kullanici_istatistikleri['brans_performans']['Basketbol']['kaybedilen']} | B:{self.kullanici_istatistikleri['brans_performans']['Basketbol']['berabere']}
     🏐 Voleybol:  K:{self.kullanici_istatistikleri['brans_performans']['Voleybol']['kazanilan']} | Y:{self.kullanici_istatistikleri['brans_performans']['Voleybol']['kaybedilen']} | B:{self.kullanici_istatistikleri['brans_performans']['Voleybol']['berabere']}

{'─'*70}
                        🤖 BİLGİSAYAR İSTATİSTİKLERİ
{'─'*70}
  🏆 Toplam Puan:           {self.bilgisayar_istatistikleri['toplam_puan']}
  ✅ Kazanılan Tur:         {self.bilgisayar_istatistikleri['kazanilan_tur']}
  ❌ Kaybedilen Tur:        {self.bilgisayar_istatistikleri['kaybedilen_tur']}
  🤝 Beraberlik:            {self.bilgisayar_istatistikleri['beraberlik']}
  🔥 Max Galibiyet Serisi:  {self.bilgisayar_istatistikleri['max_galibiyet_serisi']}
  ⭐ Özel Yetenekle Kazanılan: {self.bilgisayar_istatistikleri['ozel_yetenekle_kazanilan']}
  📋 Hükmen Galibiyet:      {self.bilgisayar_istatistikleri['hukmen_galibiyet']}

  📊 Branş Performansı:
     ⚽ Futbol:     K:{self.bilgisayar_istatistikleri['brans_performans']['Futbol']['kazanilan']} | Y:{self.bilgisayar_istatistikleri['brans_performans']['Futbol']['kaybedilen']} | B:{self.bilgisayar_istatistikleri['brans_performans']['Futbol']['berabere']}
     🏀 Basketbol: K:{self.bilgisayar_istatistikleri['brans_performans']['Basketbol']['kazanilan']} | Y:{self.bilgisayar_istatistikleri['brans_performans']['Basketbol']['kaybedilen']} | B:{self.bilgisayar_istatistikleri['brans_performans']['Basketbol']['berabere']}
     🏐 Voleybol:  K:{self.bilgisayar_istatistikleri['brans_performans']['Voleybol']['kazanilan']} | Y:{self.bilgisayar_istatistikleri['brans_performans']['Voleybol']['kaybedilen']} | B:{self.bilgisayar_istatistikleri['brans_performans']['Voleybol']['berabere']}

{'─'*70}
                            🏁 SONUÇ
{'─'*70}"""
        
        if self.kazanan:
            kazanan_str = "KULLANICI" if self.kazanan == 'kullanici' or (hasattr(self.kazanan, 'oyuncu_adi') and 'Kullanıcı' in str(self.kazanan.oyuncu_adi)) else "BİLGİSAYAR" if self.kazanan != 'berabere' else "BERABERE"
            rapor += f"""
  🏆 Kazanan: {kazanan_str}
  📋 Kazanma Aşaması: {self.kazanma_asama}
  📝 Detay: {self.kazanma_detay}
"""
        else:
            rapor += "\n  ⏳ Maç devam ediyor...\n"
        
        rapor += f"""
{'='*70}
"""
        return rapor
    
    def tur_gecmisi_raporu(self):
        """Tur geçmişi raporu oluştur
        
        Returns:
            str: Tur geçmişi metni
        """
        if not self.tur_gecmisi:
            return "❌ Henüz tur oynanmadı!"
        
        rapor = f"""
{'='*70}
                    📜 TUR GEÇMİŞİ
{'='*70}
"""
        
        for tur in self.tur_gecmisi:
            kazanan_emoji = "👤" if tur['kazanan'] == 'kullanici' else "🤖" if tur['kazanan'] == 'bilgisayar' else "🤝"
            brans_emoji = "⚽" if tur['brans'] == 'Futbol' else "🏀" if tur['brans'] == 'Basketbol' else "🏐"
            
            rapor += f"""
{brans_emoji} TUR {tur['tur_no']}: {tur['brans']} - {tur['ozellik']}
   Kullanıcı: {tur['kullanici_kart']} ({tur['kullanici_puan']:.1f})
   Bilgisayar: {tur['bilgisayar_kart']} ({tur['bilgisayar_puan']:.1f})
   {kazanan_emoji} Kazanan: {tur['kazanan'].upper()} (+{tur['kazanilan_puan']} puan)
{'─'*40}"""
        
        return rapor
    
    def ozet_rapor(self):
        """Kısa özet rapor oluştur
        
        Returns:
            dict: Özet istatistikler
        """
        return {
            'toplam_tur': self.toplam_tur_sayisi,
            'kullanici': {
                'puan': self.kullanici_istatistikleri['toplam_puan'],
                'kazanilan': self.kullanici_istatistikleri['kazanilan_tur'],
                'kaybedilen': self.kullanici_istatistikleri['kaybedilen_tur'],
                'berabere': self.kullanici_istatistikleri['beraberlik']
            },
            'bilgisayar': {
                'puan': self.bilgisayar_istatistikleri['toplam_puan'],
                'kazanilan': self.bilgisayar_istatistikleri['kazanilan_tur'],
                'kaybedilen': self.bilgisayar_istatistikleri['kaybedilen_tur'],
                'berabere': self.bilgisayar_istatistikleri['beraberlik']
            },
            'kazanan': self.kazanan,
            'kazanma_asama': self.kazanma_asama
        }
    
    def __str__(self):
        """String gösterimi"""
        return self.rapor_olustur()


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("    MacIstatistik SINIFI TESTİ")
    print("=" * 70)
    
    # İstatistik nesnesi oluştur
    istatistik = MacIstatistik()
    
    # Maçı başlat
    istatistik.mac_baslat()
    
    # Örnek turlar kaydet
    istatistik.tur_kaydet(
        tur_no=1,
        brans="Futbol",
        ozellik="Penaltı",
        kullanici_kart={'ad': 'Messi'},
        bilgisayar_kart={'ad': 'Ronaldo'},
        kullanici_puan=85.5,
        bilgisayar_puan=82.3,
        kazanan='kullanici',
        kazanilan_puan=10
    )
    
    istatistik.tur_kaydet(
        tur_no=2,
        brans="Basketbol",
        ozellik="Üçlük",
        kullanici_kart={'ad': 'LeBron'},
        bilgisayar_kart={'ad': 'Curry'},
        kullanici_puan=78.0,
        bilgisayar_puan=92.5,
        kazanan='bilgisayar',
        kazanilan_puan=10
    )
    
    istatistik.tur_kaydet(
        tur_no=3,
        brans="Voleybol",
        ozellik="Servis",
        kullanici_kart={'ad': 'Eda'},
        bilgisayar_kart={'ad': 'Zehra'},
        kullanici_puan=80.0,
        bilgisayar_puan=80.0,
        kazanan='berabere',
        kazanilan_puan=0
    )
    
    # Max serileri güncelle
    istatistik.max_seri_guncelle(2, 1)
    
    # Maçı bitir
    istatistik.mac_bitir('kullanici', 1, 'Toplam puan farkı')
    
    # Rapor yazdır
    print(istatistik.rapor_olustur())
    print(istatistik.tur_gecmisi_raporu())
    
    print("\n✅ MacIstatistik sınıfı çalışıyor!")
