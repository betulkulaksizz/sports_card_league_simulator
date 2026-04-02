import random
from sporcu import Sporcu


class KartDagitici:
    """Kartları oyunculara dağıtmak için sınıf"""
    
    @staticmethod
    def kartlari_hazirla(futbolcular, basketbolcular, voleybolcular):
        """Tüm sporculardan kart nesneleri oluştur"""
        kartlar = []
        
        # Futbolcuların kartlarını ekle
        for futbolcu in futbolcular:
            kart = {
                'ad': futbolcu.sporcu_adi,
                'brans': 'Futbol',
                'seviye': futbolcu.seviye if futbolcu.seviye else 1,
                'deneyim': futbolcu.deneyim_puani if futbolcu.deneyim_puani else 0,
                'galibiyet_sayisi': 0,  # Kart bazında galibiyet sayısı
                'ozel_ozellik': futbolcu.penalti,
                'enerji': Sporcu.BASLANGIC_ENERJI,  # Başlangıç enerjisi
                'max_enerji': Sporcu.BASLANGIC_ENERJI,  # Maksimum enerji kapasitesi
                'oyundan_cikarildi': False,  # Oyundan çıkarıldı mı
                'sporcu_ref': futbolcu  # Sporcu referansı
            }
            kartlar.append(kart)
        
        # Basketbolcuların kartlarını ekle
        for basketbolcu in basketbolcular:
            kart = {
                'ad': basketbolcu.sporcu_adi,
                'brans': 'Basketbol',
                'seviye': basketbolcu.seviye if basketbolcu.seviye else 1,
                'deneyim': basketbolcu.deneyim_puani if basketbolcu.deneyim_puani else 0,
                'galibiyet_sayisi': 0,  # Kart bazında galibiyet sayısı
                'ozel_ozellik': basketbolcu.ucluk,
                'enerji': Sporcu.BASLANGIC_ENERJI,  # Başlangıç enerjisi
                'max_enerji': Sporcu.BASLANGIC_ENERJI,  # Maksimum enerji kapasitesi
                'oyundan_cikarildi': False,  # Oyundan çıkarıldı mı
                'sporcu_ref': basketbolcu  # Sporcu referansı
            }
            kartlar.append(kart)
        
        # Voleybolcuların kartlarını ekle
        for voleybolcu in voleybolcular:
            kart = {
                'ad': voleybolcu.sporcu_adi,
                'brans': 'Voleybol',
                'seviye': voleybolcu.seviye if voleybolcu.seviye else 1,
                'deneyim': voleybolcu.deneyim_puani if voleybolcu.deneyim_puani else 0,
                'galibiyet_sayisi': 0,  # Kart bazında galibiyet sayısı
                'ozel_ozellik': voleybolcu.servis,
                'enerji': Sporcu.BASLANGIC_ENERJI,  # Başlangıç enerjisi
                'max_enerji': Sporcu.BASLANGIC_ENERJI,  # Maksimum enerji kapasitesi
                'oyundan_cikarildi': False,  # Oyundan çıkarıldı mı
                'sporcu_ref': voleybolcu  # Sporcu referansı
            }
            kartlar.append(kart)
        
        return kartlar
    
    @staticmethod
    def kart_enerji_kritik_mi(kart):
        """Kartın enerjisinin kritik seviyede olup olmadığını kontrol et"""
        if kart is None:
            return False
        enerji = kart.get('enerji', 100)
        return enerji < Sporcu.KRITIK_ENERJI_ESIGI and enerji > 0
    
    @staticmethod
    def kart_enerji_sifir_mi(kart):
        """Kartın enerjisinin sıfır olup olmadığını kontrol et"""
        if kart is None:
            return True
        return kart.get('enerji', 0) <= 0
    
    @staticmethod
    def kart_enerji_guncelle(kart, sonuc, ozel_yetenek_kullanildi=False):
        """Kartın enerjisini tur sonucuna göre güncelle
        
        Args:
            kart (dict): Kart bilgileri
            sonuc (str): 'kazandi', 'kaybetti', 'berabere'
            ozel_yetenek_kullanildi (bool): Özel yetenek kullanıldı mı
            
        Returns:
            int: Toplam enerji kaybı
        """
        if kart is None:
            return 0
            
        enerji_kaybi = 0
        
        if sonuc == 'kazandi':
            enerji_kaybi = Sporcu.KAZANMA_ENERJI_KAYBI
        elif sonuc == 'kaybetti':
            enerji_kaybi = Sporcu.KAYBETME_ENERJI_KAYBI
        elif sonuc == 'berabere':
            enerji_kaybi = Sporcu.BERABERLIK_ENERJI_KAYBI
        
        # Özel yetenek kullanıldıysa ek enerji kaybı
        if ozel_yetenek_kullanildi:
            enerji_kaybi += Sporcu.OZEL_YETENEK_ENERJI_KAYBI
        
        # Veteran yeteneği: enerji kaybını %50 azalt
        sporcu = kart.get('sporcu_ref')
        if sporcu and hasattr(sporcu, 'ozel_yetenek') and sporcu.ozel_yetenek:
            from ozel_yetenek import Veteran
            if isinstance(sporcu.ozel_yetenek, Veteran):
                enerji_kaybi = sporcu.ozel_yetenek.enerji_etkisi(enerji_kaybi)
        
        kart['enerji'] = max(0, kart['enerji'] - enerji_kaybi)
        
        # Enerji sıfıra düştüyse kart oyundan çıkar
        if KartDagitici.kart_enerji_sifir_mi(kart):
            kart['oyundan_cikarildi'] = True
        
        return enerji_kaybi
    
    @staticmethod
    def kart_deneyim_ekle(kart, sonuc):
        """Tur sonucuna göre karta deneyim puanı ekle
        
        Args:
            kart (dict): Kart bilgileri
            sonuc (str): 'kazandi', 'kaybetti', 'berabere'
            
        Returns:
            dict: Deneyim değişim detayları
        """
        detaylar = {
            'onceki_deneyim': kart.get('deneyim', 0),
            'eklenen_deneyim': 0,
            'yeni_deneyim': 0,
            'seviye_atladi': False,
            'yeni_seviye': kart.get('seviye', 1)
        }
        
        if sonuc == 'kazandi':
            kart['galibiyet_sayisi'] = kart.get('galibiyet_sayisi', 0) + 1
            detaylar['eklenen_deneyim'] = Sporcu.GALIBIYET_DENEYIM
        elif sonuc == 'berabere':
            detaylar['eklenen_deneyim'] = Sporcu.BERABERLIK_DENEYIM
        else:  # kaybetti
            detaylar['eklenen_deneyim'] = Sporcu.MAGLUBIYET_DENEYIM
        
        kart['deneyim'] = kart.get('deneyim', 0) + detaylar['eklenen_deneyim']
        detaylar['yeni_deneyim'] = kart['deneyim']
        
        # Seviye atlama kontrolü
        seviye_sonucu = KartDagitici.kart_seviye_kontrol(kart)
        if seviye_sonucu['seviye_atladi']:
            detaylar['seviye_atladi'] = True
            detaylar['yeni_seviye'] = seviye_sonucu['yeni_seviye']
        
        return detaylar
    
    @staticmethod
    def kart_seviye_kontrol(kart):
        """Kartın seviye atlayıp atlamayacağını kontrol et ve gerekirse seviye atla
        
        Args:
            kart (dict): Kart bilgileri
            
        Returns:
            dict: Seviye değişim detayları
        """
        detaylar = {
            'onceki_seviye': kart.get('seviye', 1),
            'yeni_seviye': kart.get('seviye', 1),
            'seviye_atladi': False,
            'bonuslar': []
        }
        
        mevcut_seviye = kart.get('seviye', 1)
        deneyim = kart.get('deneyim', 0)
        galibiyet = kart.get('galibiyet_sayisi', 0)
        
        # Maksimum seviye kontrolü
        if mevcut_seviye >= Sporcu.MAX_SEVIYE:
            return detaylar
        
        yeni_seviye = mevcut_seviye
        
        # Seviye 2'ye atlama kontrolü
        if mevcut_seviye == 1:
            if galibiyet >= Sporcu.SEVIYE_2_GALIBIYET or deneyim >= Sporcu.SEVIYE_2_DENEYIM:
                yeni_seviye = 2
        
        # Seviye 3'e atlama kontrolü
        elif mevcut_seviye == 2:
            if galibiyet >= Sporcu.SEVIYE_3_GALIBIYET or deneyim >= Sporcu.SEVIYE_3_DENEYIM:
                yeni_seviye = 3
        
        # Seviye atladıysa bonusları uygula
        if yeni_seviye > mevcut_seviye:
            detaylar['seviye_atladi'] = True
            detaylar['yeni_seviye'] = yeni_seviye
            kart['seviye'] = yeni_seviye
            
            # Bonusları uygula
            bonuslar = KartDagitici.kart_seviye_bonusu_uygula(kart)
            detaylar['bonuslar'] = bonuslar
        
        return detaylar
    
    @staticmethod
    def kart_seviye_bonusu_uygula(kart):
        """Seviye atlayan karta bonusları uygula
        
        Args:
            kart (dict): Kart bilgileri
            
        Returns:
            list: Uygulanan bonusların listesi
        """
        bonuslar = []
        sporcu = kart.get('sporcu_ref')
        
        if sporcu is None:
            return bonuslar
        
        brans = kart['brans']
        
        # Branşa ait tüm özellikler +5
        if brans == 'Futbol':
            if hasattr(sporcu, 'penalti') and sporcu.penalti is not None:
                sporcu.penalti = float(sporcu.penalti) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Penaltı +{Sporcu.SEVIYE_OZELLIK_BONUS}")
            if hasattr(sporcu, 'serbestturus') and sporcu.serbestturus is not None:
                sporcu.serbestturus = float(sporcu.serbestturus) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Serbest Vuruş +{Sporcu.SEVIYE_OZELLIK_BONUS}")
            if hasattr(sporcu, 'kaleci_karsikarsiya') and sporcu.kaleci_karsikarsiya is not None:
                sporcu.kaleci_karsikarsiya = float(sporcu.kaleci_karsikarsiya) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Kaleci Karşı Karşıya +{Sporcu.SEVIYE_OZELLIK_BONUS}")
        
        elif brans == 'Basketbol':
            if hasattr(sporcu, 'ucluk') and sporcu.ucluk is not None:
                sporcu.ucluk = float(sporcu.ucluk) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Üçlük +{Sporcu.SEVIYE_OZELLIK_BONUS}")
            if hasattr(sporcu, 'ikilik') and sporcu.ikilik is not None:
                sporcu.ikilik = float(sporcu.ikilik) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"İkilik +{Sporcu.SEVIYE_OZELLIK_BONUS}")
            if hasattr(sporcu, 'serbest_atis') and sporcu.serbest_atis is not None:
                sporcu.serbest_atis = float(sporcu.serbest_atis) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Serbest Atış +{Sporcu.SEVIYE_OZELLIK_BONUS}")
        
        elif brans == 'Voleybol':
            if hasattr(sporcu, 'servis') and sporcu.servis is not None:
                sporcu.servis = float(sporcu.servis) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Servis +{Sporcu.SEVIYE_OZELLIK_BONUS}")
            if hasattr(sporcu, 'blok') and sporcu.blok is not None:
                sporcu.blok = float(sporcu.blok) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Blok +{Sporcu.SEVIYE_OZELLIK_BONUS}")
            if hasattr(sporcu, 'smac') and sporcu.smac is not None:
                sporcu.smac = float(sporcu.smac) + Sporcu.SEVIYE_OZELLIK_BONUS
                bonuslar.append(f"Smaç +{Sporcu.SEVIYE_OZELLIK_BONUS}")
        
        # Maksimum enerji kapasitesi +10
        kart['max_enerji'] = kart.get('max_enerji', Sporcu.BASLANGIC_ENERJI) + Sporcu.SEVIYE_ENERJI_BONUS
        bonuslar.append(f"Maksimum Enerji +{Sporcu.SEVIYE_ENERJI_BONUS}")
        
        # Dayanıklılık +5
        if hasattr(sporcu, 'dayaniklilik') and sporcu.dayaniklilik is not None:
            sporcu.dayaniklilik = float(sporcu.dayaniklilik) + Sporcu.SEVIYE_DAYANIKLILIK_BONUS
            bonuslar.append(f"Dayanıklılık +{Sporcu.SEVIYE_DAYANIKLILIK_BONUS}")
        
        return bonuslar
    
    @staticmethod
    def kartlari_dagit(kartlar):
        """Kartları oyunculara dağıt (her oyuncuya 12 kart, her branştan en az 4)"""
        
        # Kartları branşa göre ayır
        futbol_kartlar = [k for k in kartlar if k['brans'] == 'Futbol']
        basketbol_kartlar = [k for k in kartlar if k['brans'] == 'Basketbol']
        voleybol_kartlar = [k for k in kartlar if k['brans'] == 'Voleybol']
        
        # Şart kontrolü
        if len(futbol_kartlar) < 8 or len(basketbol_kartlar) < 8 or len(voleybol_kartlar) < 8:
            raise ValueError("Yeterli kart yok! Her branştan en az 8 kart gerekli.")
        
        # Kullanıcıya kart dağıt (her branştan 4)
        kullanici_kartlari = []
        kullanici_kartlari.extend(random.sample(futbol_kartlar, 4))
        kullanici_kartlari.extend(random.sample(basketbol_kartlar, 4))
        kullanici_kartlari.extend(random.sample(voleybol_kartlar, 4))
        
        # Kalan kartları bilgisayara dağıt
        bilgisayar_kartlari = []
        bilgisayar_kartlari.extend([k for k in futbol_kartlar if k not in kullanici_kartlari])
        bilgisayar_kartlari.extend([k for k in basketbol_kartlar if k not in kullanici_kartlari])
        bilgisayar_kartlari.extend([k for k in voleybol_kartlar if k not in kullanici_kartlari])
        
        # Bilgisayara tam olarak 12 kart ver
        bilgisayar_kartlari = bilgisayar_kartlari[:12]
        
        return kullanici_kartlari, bilgisayar_kartlari
    
    @staticmethod
    def kartlari_goster(oyuncu_adi, kartlar):
        """Oyuncunun kartlarını göster"""
        print(f"\n{oyuncu_adi}'nın Kartları:")
        print("=" * 80)
        
        # Aktif kartları filtrele (oyundan çıkarılmamış olanlar)
        aktif_kartlar = [k for k in kartlar if not k.get('oyundan_cikarildi', False)]
        cikarilan_kartlar = [k for k in kartlar if k.get('oyundan_cikarildi', False)]
        
        futbol_sayisi = len([k for k in aktif_kartlar if k['brans'] == 'Futbol'])
        basketbol_sayisi = len([k for k in aktif_kartlar if k['brans'] == 'Basketbol'])
        voleybol_sayisi = len([k for k in aktif_kartlar if k['brans'] == 'Voleybol'])
        
        print(f"Toplam Aktif Kart: {len(aktif_kartlar)}")
        print(f"  - Futbol: {futbol_sayisi}")
        print(f"  - Basketbol: {basketbol_sayisi}")
        print(f"  - Voleybol: {voleybol_sayisi}")
        
        if cikarilan_kartlar:
            print(f"\n⚠️  Oyundan Çıkarılan Kartlar: {len(cikarilan_kartlar)}")
        
        print("-" * 80)
        
        for i, kart in enumerate(aktif_kartlar, 1):
            enerji = kart.get('enerji', 100)
            max_enerji = kart.get('max_enerji', 100)
            seviye = kart.get('seviye', 1)
            deneyim = kart.get('deneyim', 0)
            galibiyet = kart.get('galibiyet_sayisi', 0)
            
            # Kritik enerji durumu kontrolü
            if KartDagitici.kart_enerji_kritik_mi(kart):
                enerji_durum = f"⚠️ KRİTİK {enerji}/{max_enerji}"
            else:
                enerji_durum = f"{enerji}/{max_enerji}"
            
            # Seviye gösterimi
            if seviye >= Sporcu.MAX_SEVIYE:
                seviye_durum = f"⭐ MAX {seviye}"
            else:
                seviye_durum = f"Sviy: {seviye}"
            
            print(f"{i}. {kart['ad']} | {kart['brans']} | {seviye_durum} | Dnm: {deneyim} | Gal: {galibiyet} | Enerji: {enerji_durum}")
        
        # Çıkarılan kartları da göster
        if cikarilan_kartlar:
            print("\n" + "-" * 80)
            print("❌ Oyundan Çıkarılan Kartlar:")
            for kart in cikarilan_kartlar:
                print(f"   • {kart['ad']} | {kart['brans']} | Seviye: {kart.get('seviye', 1)} (Enerji: 0)")
    
    @staticmethod
    def kartBilgisiYazdir(kart):
        """Tek bir kartın detaylı bilgilerini ekrana yazdır
        
        Args:
            kart (dict): Kart bilgileri
            
        Returns:
            dict: Kart bilgileri
        """
        print(f"\n{'='*60}")
        print(f"KART BİLGİSİ: {kart.get('ad', 'Bilinmiyor')}")
        print(f"{'='*60}")
        
        # Temel bilgiler
        print(f"  Branş: {kart.get('brans', 'Bilinmiyor')}")
        print(f"  Seviye: {kart.get('seviye', 1)}")
        print(f"  Deneyim: {kart.get('deneyim', 0)}")
        print(f"  Galibiyet Sayısı: {kart.get('galibiyet_sayisi', 0)}")
        
        # Enerji bilgisi
        enerji = kart.get('enerji', 100)
        max_enerji = kart.get('max_enerji', 100)
        print(f"  Enerji: {enerji}/{max_enerji}")
        
        # Durum
        if kart.get('oyundan_cikarildi', False):
            print(f"  ❌ DURUM: Oyundan çıkarıldı")
        elif KartDagitici.kart_enerji_kritik_mi(kart):
            print(f"  ⚠️ DURUM: Kritik enerji")
        else:
            print(f"  ✅ DURUM: Aktif")
        
        # Sporcu referansı varsa ek bilgiler
        sporcu = kart.get('sporcu_ref')
        if sporcu:
            print(f"\n  --- Sporcu Özellikleri ---")
            print(f"  Takım: {sporcu.takim_adi}")
            print(f"  Dayanıklılık: {sporcu.dayaniklilik}")
            print(f"  Özel Yetenek: {sporcu.ozel_yetenek or 'Yok'}")
            
            # Branşa özgü özellikler
            if kart['brans'] == 'Futbol':
                print(f"  Penaltı: {getattr(sporcu, 'penalti', 'N/A')}")
                print(f"  Serbest Vuruş: {getattr(sporcu, 'serbestturus', 'N/A')}")
                print(f"  Kaleci Karşı Karşıya: {getattr(sporcu, 'kaleci_karsikarsiya', 'N/A')}")
            elif kart['brans'] == 'Basketbol':
                print(f"  Üçlük: {getattr(sporcu, 'ucluk', 'N/A')}")
                print(f"  İkilik: {getattr(sporcu, 'ikilik', 'N/A')}")
                print(f"  Serbest Atış: {getattr(sporcu, 'serbest_atis', 'N/A')}")
            elif kart['brans'] == 'Voleybol':
                print(f"  Servis: {getattr(sporcu, 'servis', 'N/A')}")
                print(f"  Blok: {getattr(sporcu, 'blok', 'N/A')}")
                print(f"  Smaç: {getattr(sporcu, 'smac', 'N/A')}")
        
        print(f"{'='*60}")
        
        return kart
    
    @staticmethod
    def enerjiGuncelle(kart, sonuc, ozel_yetenek_kullanildi=False):
        """Kartın enerjisini güncelle (kart_enerji_guncelle ile aynı, alternatif isim)
        
        Args:
            kart (dict): Kart bilgileri
            sonuc (str): 'kazandi', 'kaybetti', 'berabere'
            ozel_yetenek_kullanildi (bool): Özel yetenek kullanıldı mı
            
        Returns:
            dict: Enerji güncelleme detayları
        """
        onceki_enerji = kart.get('enerji', 100)
        
        enerji_kaybi = KartDagitici.kart_enerji_guncelle(kart, sonuc, ozel_yetenek_kullanildi)
        
        yeni_enerji = kart.get('enerji', 100)
        
        return {
            'onceki_enerji': onceki_enerji,
            'yeni_enerji': yeni_enerji,
            'enerji_kaybi': enerji_kaybi,
            'kritik_mi': KartDagitici.kart_enerji_kritik_mi(kart),
            'oyundan_cikarildi': kart.get('oyundan_cikarildi', False)
        }
    
    @staticmethod
    def seviyeAtlaKontrol(kart):
        """Kartın seviye atlama durumunu kontrol et (kart_seviye_kontrol ile aynı, alternatif isim)
        
        Args:
            kart (dict): Kart bilgileri
            
        Returns:
            dict: Seviye atlama sonucu
        """
        return KartDagitici.kart_seviye_kontrol(kart)
    
    @staticmethod
    def performansHesapla(kart, ozellik_adi=None):
        """Kartın performans puanını hesapla
        
        Args:
            kart (dict): Kart bilgileri
            ozellik_adi (str, optional): Hesaplanacak özellik adı
            
        Returns:
            float: Hesaplanan performans puanı
        """
        # Temel değerler
        seviye = kart.get('seviye', 1)
        enerji = kart.get('enerji', 100)
        deneyim = kart.get('deneyim', 0)
        
        # Seviye bonusu
        seviye_bonus = (seviye - 1) * Sporcu.SEVIYE_OZELLIK_BONUS
        
        # Enerji çarpanı
        if enerji > 70:
            enerji_carpani = 1.0
        elif enerji >= 40:
            enerji_carpani = 0.9  # %10 düşüş
        elif enerji > 0:
            enerji_carpani = 0.8  # %20 düşüş
        else:
            enerji_carpani = 0  # Oynanamaz
        
        # Deneyim bonusu
        deneyim_bonus = deneyim * 0.10
        
        # Sporcu referansından özellik puanı al
        sporcu = kart.get('sporcu_ref')
        ozellik_puan = 0
        
        if sporcu and ozellik_adi:
            # Özellik puanını al
            ozellik_map = {
                'Penaltı': 'penalti',
                'Serbest Vuruş': 'serbestturus',
                'Kaleci Karşı Karşıya': 'kaleci_karsikarsiya',
                'Üçlük': 'ucluk',
                'İkilik': 'ikilik',
                'Serbest Atış': 'serbest_atis',
                'Servis': 'servis',
                'Blok': 'blok',
                'Smac': 'smac'
            }
            attr_name = ozellik_map.get(ozellik_adi)
            if attr_name and hasattr(sporcu, attr_name):
                ozellik_puan = float(getattr(sporcu, attr_name) or 0)
        
        # Toplam performans
        performans = (ozellik_puan + seviye_bonus + deneyim_bonus) * enerji_carpani
        
        return performans
    
    @staticmethod
    def ozelYetenekUygula(kart):
        """Kartın özel yeteneğini uygula
        
        Args:
            kart (dict): Kart bilgileri
            
        Returns:
            dict: Özel yetenek uygulama sonucu
        """
        sonuc = {
            'basarili': False,
            'yetenek': None,
            'bonus': 0,
            'enerji_maliyeti': Sporcu.OZEL_YETENEK_ENERJI_KAYBI,
            'aciklama': ''
        }
        
        sporcu = kart.get('sporcu_ref')
        if not sporcu:
            sonuc['aciklama'] = 'Sporcu referansı bulunamadı.'
            return sonuc
        
        # Özel yetenek yoksa
        if not sporcu.ozel_yetenek:
            sonuc['aciklama'] = 'Bu kartın özel yeteneği yok.'
            return sonuc
        
        # Enerji yeterli mi?
        enerji = kart.get('enerji', 100)
        if enerji < Sporcu.OZEL_YETENEK_ENERJI_KAYBI:
            sonuc['aciklama'] = f'Yeterli enerji yok. Gerekli: {Sporcu.OZEL_YETENEK_ENERJI_KAYBI}, Mevcut: {enerji}'
            return sonuc
        
        # Özel yetenek bonusunu hesapla
        sonuc['yetenek'] = sporcu.ozel_yetenek
        if hasattr(sporcu, 'ozel_yetenek_katsayisi') and sporcu.ozel_yetenek_katsayisi:
            sonuc['bonus'] = float(sporcu.ozel_yetenek_katsayisi)
        else:
            sonuc['bonus'] = 5  # Varsayılan bonus
        
        sonuc['basarili'] = True
        sonuc['aciklama'] = f"'{sporcu.ozel_yetenek}' yeteneği uygulandı. Bonus: +{sonuc['bonus']}"
        
        return sonuc
