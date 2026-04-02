from kart_dagitici import KartDagitici


class TurYoneticisi:
    """Oyun turlarını yöneten sınıf"""
    
    # Branş sırası
    BRANS_SIRASI = ["Futbol", "Basketbol", "Voleybol"]
    
    # Her branşa ait özellikler
    BRANS_OZELLIKLERI = {
        "Futbol": ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"],
        "Basketbol": ["Üçlük", "İkilik", "Serbest Atış"],
        "Voleybol": ["Servis", "Blok", "Smac"]
    }
    
    # Özellik seçim modları
    OZELLIK_SECIM_RASTGELE = "rastgele"
    OZELLIK_SECIM_KULLANICI = "kullanici"
    
    def __init__(self):
        self.mevcut_tur = 0  # Kaçıncı tur olduğu
        self.mevcut_brans = self.BRANS_SIRASI[0]  # Hangi branş oynandığı
        self.ozellik_secim_modu = self.OZELLIK_SECIM_RASTGELE  # Varsayılan: Rastgele seçim
    
    def ozellik_secim_modunu_ayarla(self, mod):
        """Özellik seçim modunu ayarla
        
        Args:
            mod (str): 'rastgele' veya 'kullanici'
        """
        if mod in [self.OZELLIK_SECIM_RASTGELE, self.OZELLIK_SECIM_KULLANICI]:
            self.ozellik_secim_modu = mod
            print(f"Özellik seçim modu: {'Rastgele' if mod == self.OZELLIK_SECIM_RASTGELE else 'Kullanıcı Seçimi'}")
        else:
            print("Geçersiz mod! 'rastgele' veya 'kullanici' olmalı.")
    
    def sonraki_brans(self):
        """Sonraki branşa geç"""
        index = self.BRANS_SIRASI.index(self.mevcut_brans)
        self.mevcut_brans = self.BRANS_SIRASI[(index + 1) % len(self.BRANS_SIRASI)]
        self.mevcut_tur += 1
    
    def rastgele_ozellik_sec(self, brans):
        """Belirtilen branş için rastgele bir özellik seç
        
        Args:
            brans (str): Branşın adı (Futbol, Basketbol, Voleybol)
            
        Returns:
            str: Seçilen özellik
        """
        from random import choice
        return choice(self.BRANS_OZELLIKLERI[brans])
    
    def kullanici_ozellik_sec(self, brans):
        """Kullanıcıya branşa ait özellikleri göster ve seçim yaptır
        
        Args:
            brans (str): Branşın adı (Futbol, Basketbol, Voleybol)
            
        Returns:
            str: Seçilen özellik
        """
        ozellikler = self.BRANS_OZELLIKLERI[brans]
        
        print(f"\n🎯 {brans} branşı için özellik seçin:")
        for i, ozellik in enumerate(ozellikler, 1):
            print(f"  {i}. {ozellik}")
        
        while True:
            try:
                secim = input("Özellik numarasını girin (1-3): ").strip()
                index = int(secim) - 1
                if 0 <= index < len(ozellikler):
                    secilen = ozellikler[index]
                    print(f"✓ Seçilen özellik: {secilen}")
                    return secilen
                else:
                    print("Geçersiz seçim! 1-3 arasında bir numara girin.")
            except ValueError:
                print("Lütfen geçerli bir numara girin!")
    
    def ozellik_sec(self, brans):
        """Mevcut moda göre özellik seç
        
        Args:
            brans (str): Branşın adı
            
        Returns:
            str: Seçilen özellik
        """
        if self.ozellik_secim_modu == self.OZELLIK_SECIM_KULLANICI:
            return self.kullanici_ozellik_sec(brans)
        else:
            return self.rastgele_ozellik_sec(brans)
    
    def puan_hesapla(self, oyuncu, kart, secilen_ozellik, oyuncu_obj=None):
        """Seçilen özelliğe göre kartın güncel performans puanını hesapla
        
        İSTER FORMÜLÜ:
        Güncel Özellik Puanı = Temel Özellik + Moral Bonusu + Özel Yetenek Bonusu - Enerji Kaybı Cezası + Seviye Bonusu
        
        Enerji Cezası:
        - Enerji > 70: ceza yok
        - 40 ≤ Enerji ≤ 70: temel özellik %10 düşer
        - 0 < Enerji < 40: temel özellik %20 düşer
        - Enerji = 0: kart oynanamaz
        
        Moral Bonusu:
        - Moral ≥ 90 (çok yüksek): +10 bonus
        - 70 ≤ Moral < 90 (yüksek): +5 bonus
        - Moral < 40 (düşük): -5 ceza
        - Diğer: 0
        
        Seviye Bonusu:
        - Seviye 1: +0
        - Seviye 2: +5
        - Seviye 3: +10
        
        Args:
            oyuncu: Sporcu nesnesi (Futbolcu, Basketbolcu veya Voleybolcu)
            kart (dict): Kart bilgileri
            secilen_ozellik (str): Seçilen özellik adı
            oyuncu_obj: Oyuncu nesnesi (Kullanici veya Bilgisayar) - moral için
            
        Returns:
            float: Hesaplanan güncel performans puanı
        """
        # Sporcu ve kart None kontrolü
        if oyuncu is None:
            print("⚠️ Uyarı: Sporcu nesnesi None, puan hesaplanamıyor.")
            return 0.0
        
        if kart is None:
            print("⚠️ Uyarı: Kart bilgisi None, puan hesaplanamıyor.")
            return 0.0
        
        if not secilen_ozellik:
            print("⚠️ Uyarı: Seçilen özellik belirtilmedi.")
            return 0.0
        
        # 1. Seçilen özelliğin temel puanını al
        temel_puan = self._ozellik_puanini_al(oyuncu, secilen_ozellik)
        
        # 2. Moral Bonusu Hesapla (oyuncu_obj'dan)
        moral_bonusu = 0
        if oyuncu_obj is not None and hasattr(oyuncu_obj, 'moral'):
            moral_bonusu = self._moral_bonusu_hesapla(oyuncu_obj.moral)
        
        # 3. Özel Yetenek Bonusu Hesapla
        ozel_yetenek_bonusu = self._ozel_yetenek_bonusu_hesapla(oyuncu)
        
        # 4. Enerji Kaybı Cezası Hesapla (kartın enerjisini kullan)
        kart_enerji = kart.get('enerji', 100)
        enerji_cezasi = self._enerji_cezasi_hesapla(kart_enerji, temel_puan)
        
        # 5. Seviye Bonusu Hesapla
        seviye_bonusu = self._seviye_bonusu_hesapla(kart['seviye'])
        
        # 6. Güncel Puan Hesapla (İster Formülü)
        # Güncel Puan = Temel Özellik + Moral Bonusu + Özel Yetenek Bonusu - Enerji Cezası + Seviye Bonusu
        guncel_puan = temel_puan + moral_bonusu + ozel_yetenek_bonusu - enerji_cezasi + seviye_bonusu
        
        return guncel_puan
    
    def puan_hesapla_detayli(self, oyuncu, kart, secilen_ozellik, oyuncu_obj=None, rakip_oyuncu=None):
        """Puan hesaplamasını detaylı olarak döndür (arayüz için)
        
        Args:
            oyuncu: Sporcu nesnesi
            kart: Kart bilgileri
            secilen_ozellik: Seçilen özellik
            oyuncu_obj: Oyuncu nesnesi (Kullanici/Bilgisayar)
            rakip_oyuncu: Rakip oyuncu (Captain moral etkisi için)
            
        Returns:
            dict: Tüm hesaplama detayları
        """
        # Sporcu ve kart None kontrolü - varsayılan değerlerle döndür
        varsayilan_sonuc = {
            'temel_puan': 0,
            'moral': 50,
            'moral_bonusu': 0,
            'ozel_yetenek_bonusu': 0,
            'enerji': 0,
            'enerji_cezasi': 0,
            'seviye': 1,
            'seviye_bonusu': 0,
            'guncel_puan': 0
        }
        
        if oyuncu is None or kart is None or not secilen_ozellik:
            return varsayilan_sonuc
        
        temel_puan = self._ozellik_puanini_al(oyuncu, secilen_ozellik)
        
        moral_bonusu = 0
        moral = 50  # varsayılan
        if oyuncu_obj is not None and hasattr(oyuncu_obj, 'moral'):
            moral = oyuncu_obj.moral
            moral_bonusu = self._moral_bonusu_hesapla(moral)
        
        # Captain yeteneği: Rakip takımda Captain varsa +5 moral bonus
        if rakip_oyuncu and hasattr(rakip_oyuncu, 'ozel_yetenek'):
            from ozel_yetenek import Captain
            if isinstance(rakip_oyuncu.ozel_yetenek, Captain):
                moral_bonusu += 5  # Captain'ın etkisi
        
        ozel_yetenek_bonusu = self._ozel_yetenek_bonusu_hesapla(oyuncu)
        
        kart_enerji = kart.get('enerji', 100)
        enerji_cezasi = self._enerji_cezasi_hesapla(kart_enerji, temel_puan)
        
        seviye = kart.get('seviye', 1)
        seviye_bonusu = self._seviye_bonusu_hesapla(seviye)
        
        # Pasif Özel Yetenek Etkisini Hesapla
        yetenek_bonusu = 0.0
        yetenek_adi = ""
        if oyuncu is not None and hasattr(oyuncu, 'ozel_yetenek') and oyuncu.ozel_yetenek:
            yetenek = oyuncu.ozel_yetenek
            yetenek_adi = yetenek.ac_kla()
            
            # Sadece pasif yetenekler otomatik uygulanır
            if yetenek.pasif_mi():
                kart_durumu = {
                    'enerji': kart_enerji,
                    'seviye': seviye,
                    'son_3_turda_oynanmis': False  # Bu UI'dan set edilecek
                }
                yetenek_bonusu = yetenek.puan_etkisi(temel_puan, kart_durumu)
        
        guncel_puan = temel_puan + moral_bonusu + ozel_yetenek_bonusu - enerji_cezasi + seviye_bonusu + yetenek_bonusu
        
        return {
            'temel_puan': temel_puan,
            'moral': moral,
            'moral_bonusu': moral_bonusu,
            'ozel_yetenek_bonusu': ozel_yetenek_bonusu,
            'yetenek_bonusu': yetenek_bonusu,
            'yetenek_adi': yetenek_adi,
            'enerji': kart_enerji,
            'enerji_cezasi': enerji_cezasi,
            'seviye': seviye,
            'seviye_bonusu': seviye_bonusu,
            'guncel_puan': guncel_puan
        }
    
    def _ozellik_puanini_al(self, oyuncu, ozellik_adi):
        """Oyuncunun belirtilen özelliğinin temel puanını al
        
        Args:
            oyuncu: Oyuncu nesnesi
            ozellik_adi (str): Özellik adı (ör: "Penaltı", "Üçlük", "Servis")
            
        Returns:
            float: Özelliğin temel puanı
        """
        # None kontrolü
        if oyuncu is None:
            return 0.0
        
        if not ozellik_adi:
            return 0.0
        
        # Futbol özellikleri
        if ozellik_adi == "Penaltı":
            return float(oyuncu.penalti) if hasattr(oyuncu, 'penalti') else 0
        elif ozellik_adi == "Serbest Vuruş":
            return float(oyuncu.serbestturus) if hasattr(oyuncu, 'serbestturus') else 0
        elif ozellik_adi == "Kaleci Karşı Karşıya":
            return float(oyuncu.kaleci_karsikarsiya) if hasattr(oyuncu, 'kaleci_karsikarsiya') else 0
        
        # Basketbol özellikleri
        elif ozellik_adi == "Üçlük":
            return float(oyuncu.ucluk) if hasattr(oyuncu, 'ucluk') else 0
        elif ozellik_adi == "İkilik":
            return float(oyuncu.ikilik) if hasattr(oyuncu, 'ikilik') else 0
        elif ozellik_adi == "Serbest Atış":
            return float(oyuncu.serbest_atis) if hasattr(oyuncu, 'serbest_atis') else 0
        
        # Voleybol özellikleri
        elif ozellik_adi == "Servis":
            return float(oyuncu.servis) if hasattr(oyuncu, 'servis') else 0
        elif ozellik_adi == "Blok":
            return float(oyuncu.blok) if hasattr(oyuncu, 'blok') else 0
        elif ozellik_adi == "Smac":
            return float(oyuncu.smac) if hasattr(oyuncu, 'smac') else 0
        
        return 0
    
    def _enerji_cezasi_hesapla(self, enerji, temel_puan):
        """Enerjiye göre ceza hesapla
        
        Args:
            enerji (int): Oyuncunun enerji seviyesi
            temel_puan (float): Özelliğin temel puanı
            
        Returns:
            float: Enerji nedeniyle düşülecek puan
        """
        if enerji > 70:
            return 0  # Ceza yok
        elif 40 <= enerji <= 70:
            return temel_puan * 0.10  # %10 düşüş
        elif 0 < enerji < 40:
            return temel_puan * 0.20  # %20 düşüş
        else:  # Enerji = 0
            return temel_puan  # Kart oynanamaz, tam ceza
    
    def _moral_bonusu_hesapla(self, moral):
        """Morale göre bonus hesapla
        
        Args:
            moral (int): Oyuncunun moral seviyesi
            
        Returns:
            float: Moral bonusu
        """
        if moral >= 90:
            return 10  # Çok yüksek moral
        elif moral >= 70:
            return 5   # Yüksek moral
        elif moral < 40:
            return -5  # Düşük moral
        else:
            return 0   # Normal moral
    
    def _seviye_bonusu_hesapla(self, seviye):
        """Seviyeye göre bonus hesapla
        
        Args:
            seviye (int): Oyuncunun seviye numarası
            
        Returns:
            float: Seviye bonusu
        """
        if seviye == 1:
            return 0
        elif seviye == 2:
            return 5
        elif seviye == 3:
            return 10
        else:
            return 0
    
    def _ozel_yetenek_bonusu_hesapla(self, oyuncu):
        """Özel yeteneğe göre bonus hesapla
        
        Args:
            oyuncu: Oyuncu nesnesi
            
        Returns:
            float: Özel yetenek bonusu
        """
        # Özel yetenek katsayısı varsa kullan
        if hasattr(oyuncu, 'ozel_yetenek_katsayisi') and oyuncu.ozel_yetenek_katsayisi:
            return float(oyuncu.ozel_yetenek_katsayisi)
        elif hasattr(oyuncu, 'deneyim_puani') and oyuncu.deneyim_puani:
            # Deneyim puanının %10'u bonus olarak ekle
            return float(oyuncu.deneyim_puani) * 0.10
        else:
            return 0
    
    def kazanani_belirle(self, oyuncu1, oyuncu2, oyuncu1_karti, oyuncu2_karti, secilen_ozellik, brans):
        """Tur kazananını belirle - 7 aşamalı karar mekanizması
        
        Args:
            oyuncu1: Birinci oyuncu (Kullanici/Bilgisayar)
            oyuncu2: İkinci oyuncu (Kullanici/Bilgisayar)
            oyuncu1_karti (dict): Oyuncu 1'in kartı
            oyuncu2_karti (dict): Oyuncu 2'nin kartı
            secilen_ozellik (str): Seçilen ana özellik
            brans (str): Branşın adı
            
        Returns:
            str: 'oyuncu1', 'oyuncu2' veya 'berabere'
        """
        
        # Sporcu referanslarını al
        oyuncu1_sporcu = oyuncu1_karti.get('sporcu_ref') if oyuncu1_karti else None
        oyuncu2_sporcu = oyuncu2_karti.get('sporcu_ref') if oyuncu2_karti else None
        
        # 1. Aşama - Ana Özellik Karşılaştırması
        oyuncu1_ana_puan = self.puan_hesapla(oyuncu1_sporcu, oyuncu1_karti, secilen_ozellik, oyuncu1) if oyuncu1_sporcu else 0
        oyuncu2_ana_puan = self.puan_hesapla(oyuncu2_sporcu, oyuncu2_karti, secilen_ozellik, oyuncu2) if oyuncu2_sporcu else 0
        
        print(f"\n{'─'*60}")
        print(f"1. AŞAMA - Ana Özellik Karşılaştırması ({secilen_ozellik})")
        print(f"  {oyuncu1.oyuncu_adi}: {oyuncu1_ana_puan:.2f}")
        print(f"  {oyuncu2.oyuncu_adi}: {oyuncu2_ana_puan:.2f}")
        
        if oyuncu1_ana_puan > oyuncu2_ana_puan:
            print(f"✓ {oyuncu1.oyuncu_adi} kazandı!")
            return 'oyuncu1'
        elif oyuncu2_ana_puan > oyuncu1_ana_puan:
            print(f"✓ {oyuncu2.oyuncu_adi} kazandı!")
            return 'oyuncu2'
        
        # 2. Aşama - Branş İçi Yedek Özellik Karşılaştırması
        yedek_ozellikler = self._yedek_ozellikleri_al(brans, secilen_ozellik)
        
        for yedek_ozellik in yedek_ozellikler:
            oyuncu1_yedek_puan = self.puan_hesapla(oyuncu1_sporcu, oyuncu1_karti, yedek_ozellik, oyuncu1) if oyuncu1_sporcu else 0
            oyuncu2_yedek_puan = self.puan_hesapla(oyuncu2_sporcu, oyuncu2_karti, yedek_ozellik, oyuncu2) if oyuncu2_sporcu else 0
            
            print(f"\n2. AŞAMA - Yedek Özellik Karşılaştırması ({yedek_ozellik})")
            print(f"  {oyuncu1.oyuncu_adi}: {oyuncu1_yedek_puan:.2f}")
            print(f"  {oyuncu2.oyuncu_adi}: {oyuncu2_yedek_puan:.2f}")
            
            if oyuncu1_yedek_puan > oyuncu2_yedek_puan:
                print(f"✓ {oyuncu1.oyuncu_adi} kazandı!")
                return 'oyuncu1'
            elif oyuncu2_yedek_puan > oyuncu1_yedek_puan:
                print(f"✓ {oyuncu2.oyuncu_adi} kazandı!")
                return 'oyuncu2'
        
        # 3. Aşama - Özel Yetenek Etkisi
        oyuncu1_ozel_bonus = self._ozel_yetenek_bonusu_hesapla(oyuncu1_sporcu) if oyuncu1_sporcu else 0
        oyuncu2_ozel_bonus = self._ozel_yetenek_bonusu_hesapla(oyuncu2_sporcu) if oyuncu2_sporcu else 0
        
        # Defender yeteneği: Rakibin özel yetenek bonusunu yarı yarıya azalt
        from ozel_yetenek import Defender
        
        if oyuncu1_sporcu and hasattr(oyuncu1_sporcu, 'ozel_yetenek') and isinstance(oyuncu1_sporcu.ozel_yetenek, Defender):
            oyuncu2_ozel_bonus *= 0.5  # Rakip bonusu yarısına iner
        
        if oyuncu2_sporcu and hasattr(oyuncu2_sporcu, 'ozel_yetenek') and isinstance(oyuncu2_sporcu.ozel_yetenek, Defender):
            oyuncu1_ozel_bonus *= 0.5  # Rakip bonusu yarısına iner
        
        print(f"\n3. AŞAMA - Özel Yetenek Bonusu")
        print(f"  {oyuncu1.oyuncu_adi}: {oyuncu1_ozel_bonus:.2f}")
        print(f"  {oyuncu2.oyuncu_adi}: {oyuncu2_ozel_bonus:.2f}")
        
        if oyuncu1_ozel_bonus > oyuncu2_ozel_bonus:
            print(f"✓ {oyuncu1.oyuncu_adi} kazandı!")
            return 'oyuncu1'
        elif oyuncu2_ozel_bonus > oyuncu1_ozel_bonus:
            print(f"✓ {oyuncu2.oyuncu_adi} kazandı!")
            return 'oyuncu2'
        
        # 4. Aşama - Dayanıklılık Kontrolü
        oyuncu1_dayaniklilik = oyuncu1.dayaniklilik if hasattr(oyuncu1, 'dayaniklilik') else 0
        oyuncu2_dayaniklilik = oyuncu2.dayaniklilik if hasattr(oyuncu2, 'dayaniklilik') else 0
        
        print(f"\n4. AŞAMA - Dayanıklılık Kontrolü")
        print(f"  {oyuncu1.oyuncu_adi}: {oyuncu1_dayaniklilik}")
        print(f"  {oyuncu2.oyuncu_adi}: {oyuncu2_dayaniklilik}")
        
        if oyuncu1_dayaniklilik > oyuncu2_dayaniklilik:
            print(f"✓ {oyuncu1.oyuncu_adi} kazandı!")
            return 'oyuncu1'
        elif oyuncu2_dayaniklilik > oyuncu1_dayaniklilik:
            print(f"✓ {oyuncu2.oyuncu_adi} kazandı!")
            return 'oyuncu2'
        
        # 5. Aşama - Enerji Kontrolü
        print(f"\n5. AŞAMA - Enerji Kontrolü")
        print(f"  {oyuncu1.oyuncu_adi}: {oyuncu1.enerji}")
        print(f"  {oyuncu2.oyuncu_adi}: {oyuncu2.enerji}")
        
        if oyuncu1.enerji > oyuncu2.enerji:
            print(f"✓ {oyuncu1.oyuncu_adi} kazandı!")
            return 'oyuncu1'
        elif oyuncu2.enerji > oyuncu1.enerji:
            print(f"✓ {oyuncu2.oyuncu_adi} kazandı!")
            return 'oyuncu2'
        
        # 6. Aşama - Seviye Kontrolü
        oyuncu1_seviye = oyuncu1_karti['seviye'] if oyuncu1_karti else 0
        oyuncu2_seviye = oyuncu2_karti['seviye'] if oyuncu2_karti else 0
        
        print(f"\n6. AŞAMA - Seviye Kontrolü")
        print(f"  {oyuncu1.oyuncu_adi}: {oyuncu1_seviye}")
        print(f"  {oyuncu2.oyuncu_adi}: {oyuncu2_seviye}")
        
        if oyuncu1_seviye > oyuncu2_seviye:
            print(f"✓ {oyuncu1.oyuncu_adi} kazandı!")
            return 'oyuncu1'
        elif oyuncu2_seviye > oyuncu1_seviye:
            print(f"✓ {oyuncu2.oyuncu_adi} kazandı!")
            return 'oyuncu2'
        
        # 7. Aşama - Beraberlik
        print(f"\n7. AŞAMA - Beraberlik")
        print(f"⊕ Tur berabere! Hiçbir oyuncu tur puanı almıyor.")
        return 'berabere'
    
    def _yedek_ozellikleri_al(self, brans, ana_ozellik):
        """Belirtilen branşın ana özellik hariç yedek özelliklerini al
        
        Args:
            brans (str): Branşın adı
            ana_ozellik (str): Ana özelliğin adı
            
        Returns:
            list: Yedek özellikler listesi
        """
        tum_ozellikler = self.BRANS_OZELLIKLERI.get(brans, [])
        return [oz for oz in tum_ozellikler if oz != ana_ozellik]
    
    def puan_ver(self, kazanan, ozel_yetenek_etkili=False, hukmen=False):
        """Kazanan oyuncuya tur sonucu puanını ver
        
        Args:
            kazanan (str): 'oyuncu1' veya 'oyuncu2'
            ozel_yetenek_etkili (bool): Özel yeteneğin etkili olduğu galibiyet
            hukmen (bool): Hükmen galibiyet mi
            
        Returns:
            int: Verilen puan
        """
        puan = 0
        
        # Kazanma puanını belirle
        if kazanan in ['oyuncu1', 'oyuncu2']:
            if hukmen:
                puan = 8  # Hükmen galibiyet
            elif ozel_yetenek_etkili:
                puan = 15  # Özel yetenek etkili galibiyet
            else:
                puan = 10  # Normal galibiyet
        elif kazanan == 'berabere':
            puan = 0  # Beraberlik
            
        return puan
    
    def galibiyetler_kontrol_et(self, oyuncu):
        """Oyuncunun galibiyetler serisini kontrol et ve bonus ver
        
        Args:
            oyuncu: Oyuncu nesnesi
            
        Returns:
            int: Seri bonusu
        """
        bonus = 0
        
        # Üst üste 5 galibiyet serisi kontrolü
        if oyuncu.galibiyet_serisi >= 5:
            bonus = 20
        # Üst üste 3 galibiyet serisi kontrolü
        elif oyuncu.galibiyet_serisi >= 3:
            bonus = 10
        
        return bonus
    
    def enerji_bonusu_hesapla(self, oyuncu, kart_enerji):
        """Düşük enerji ile kazanmanın bonusunu hesapla
        
        Args:
            oyuncu: Oyuncu nesnesi
            kart_enerji (int): Kartın enerji seviyesi
            
        Returns:
            int: Enerji bonusu
        """
        if kart_enerji < 30:
            return 5  # Düşük enerjiye rağmen kazanma bonusu
        return 0
    
    def seviye_atlama_bonusu(self, oyuncu):
        """Seviye atladıktan hemen sonra ilk galibiyetin bonusunu hesapla
        
        Args:
            oyuncu: Oyuncu nesnesi
            
        Returns:
            int: Seviye atlama bonusu
        """
        # Eğer oyuncu yeni seviyeye atladıysa ve bu ilk galibiyetiyse
        if hasattr(oyuncu, 'yeni_seviye_atladi') and oyuncu.yeni_seviye_atladi:
            oyuncu.yeni_seviye_atladi = False
            return 5
        return 0
    
    def clutch_player_bonusu(self, oyuncu, kart, son_tuzlular=None):
        """Clutch Player yetenekli kartla kazanmanın bonusunu hesapla
        
        Args:
            oyuncu: Oyuncu nesnesi
            kart (dict): Kullanılan kart
            son_tuzlular (list): Son 3 turda kullanılan kartlar
            
        Returns:
            int: Clutch Player bonusu
        """
        if son_tuzlular is None:
            son_tuzlular = []
        
        # Kart son 3 turda kullanıldıysa ve "Clutch Player" etiketine sahipse
        if kart in son_tuzlular and hasattr(kart, 'etiketi') and 'Clutch Player' in kart.get('etiketi', ''):
            return 5
        return 0
    
    def puan_cezasi_uygula(self, oyuncu, ceza_tipi):
        """Oyuncuya puan cezası uygula
        
        Args:
            oyuncu: Oyuncu nesnesi
            ceza_tipi (str): Ceza tipi ('gecersiz_kart', 'sure_asilmis', vs)
            
        Returns:
            int: Uygulanan ceza
        """
        ceza = 0
        
        if ceza_tipi == 'gecersiz_kart':
            ceza = -5
        
        if ceza != 0:
            oyuncu.skor += ceza
        
        return ceza
    
    def toplam_tur_puanini_hesapla(self, kazanan, oyuncu_enerji, oyuncu, kart, 
                                    ozel_yetenek_etkili=False, hukmen=False, 
                                    son_tuzlular=None):
        """Tür sonundaki toplam puanı hesapla (tüm bonuslar dahil)
        
        Args:
            kazanan (str): 'oyuncu1', 'oyuncu2' veya 'berabere'
            oyuncu_enerji (int): Oyuncunun enerji seviyesi
            oyuncu: Oyuncu nesnesi
            kart (dict): Kullanılan kart
            ozel_yetenek_etkili (bool): Özel yetenek etkili mi
            hukmen (bool): Hükmen galibiyet mi
            son_tuzlular (list): Son 3 turda kullanılan kartlar
            
        Returns:
            dict: Puanlama detayları
        """
        if son_tuzlular is None:
            son_tuzlular = []
        
        detaylar = {
            'temel_puan': 0,
            'galibiyet_serisi_bonusu': 0,
            'enerji_bonusu': 0,
            'seviye_atlama_bonusu': 0,
            'clutch_player_bonusu': 0,
            'toplam_puan': 0
        }
        
        # Kazanansa puan ver
        if kazanan in ['oyuncu1', 'oyuncu2']:
            detaylar['temel_puan'] = self.puan_ver(kazanan, ozel_yetenek_etkili, hukmen)
            detaylar['galibiyet_serisi_bonusu'] = self.galibiyetler_kontrol_et(oyuncu)
            detaylar['enerji_bonusu'] = self.enerji_bonusu_hesapla(oyuncu, oyuncu_enerji)
            detaylar['seviye_atlama_bonusu'] = self.seviye_atlama_bonusu(oyuncu)
            detaylar['clutch_player_bonusu'] = self.clutch_player_bonusu(oyuncu, kart, son_tuzlular)
            
            # Skoru güncelle
            oyuncu.skor += detaylar['temel_puan']
        
        detaylar['toplam_puan'] = (detaylar['temel_puan'] + 
                                   detaylar['galibiyet_serisi_bonusu'] + 
                                   detaylar['enerji_bonusu'] + 
                                   detaylar['seviye_atlama_bonusu'] + 
                                   detaylar['clutch_player_bonusu'])
        
        return detaylar
    
    def mevcut_brans_al(self):
        """Mevcut branşı döndür"""
        return self.mevcut_brans
    
    def tur_oyna(self, oyuncu1, oyuncu2):
        """Bir turu oynayan fonksiyon. Kuralları kontrol eder ve sonucu döndürür.
        
        Dönüş değerleri:
        - ('oynan', oyuncu1_kartı, oyuncu2_kartı): Tur normale oynanabilir
        - ('atlan', None, None): Her iki oyuncuda da kart yok, tur atlanır
        - ('oyuncu1_kazandi', None, None): Oyuncu 2'nin kartı yok, oyuncu 1 hükmen kazanır
        - ('oyuncu2_kazandi', None, None): Oyuncu 1'nin kartı yok, oyuncu 2 hükmen kazanır
        """
        
        print(f"\n{'='*60}")
        print(f"TUR {self.mevcut_tur + 1} - BRANS: {self.mevcut_brans}")
        print(f"{'='*60}")
        
        # Oyuncu 1'in o branşa ait kartı var mı kontrol et
        oyuncu1_kart_var = self._oyuncunun_brans_karti_var(oyuncu1, self.mevcut_brans)
        
        # Oyuncu 2'nin o branşa ait kartı var mı kontrol et
        oyuncu2_kart_var = self._oyuncunun_brans_karti_var(oyuncu2, self.mevcut_brans)
        
        # Kural 1: Her iki oyuncuda da o branşa ait kart yoksa tur atlanır
        if not oyuncu1_kart_var and not oyuncu2_kart_var:
            print(f"Her iki oyuncuda da {self.mevcut_brans} kartı kalmadı!")
            print("Tur otomatik atlanıyor...")
            self.sonraki_brans()
            return ('atlan', None, None)
        
        # Kural 2: Yalnızca oyuncu 1'de kart yoksa oyuncu 2 hükmen kazanır
        if not oyuncu1_kart_var:
            print(f"{oyuncu1.oyuncu_adi}'nin {self.mevcut_brans} kartı kalmadı!")
            print(f"{oyuncu2.oyuncu_adi} hükmen kazandı!")
            
            # Hükmen galibiyete puan ver
            oyuncu2.galibiyet_serisi += 1
            oyuncu1.kaybetme_serisi += 1
            oyuncu1.galibiyet_serisi = 0
            
            hukmen_puan = 8  # Hükmen galibiyet puanı
            oyuncu2.skor += hukmen_puan
            
            print(f"\n{'='*60}")
            print(f"PUAN DAĞITIMI")
            print(f"{'='*60}")
            print(f"{oyuncu2.oyuncu_adi} - Hükmen Kazandı!")
            print(f"  Hükmen Galibiyet Puanı: +{hukmen_puan}")
            print(f"  Yeni Skor: {oyuncu2.skor}")
            print(f"\n{oyuncu1.oyuncu_adi} - Kaybetti. Puan yok.")
            print(f"  Yeni Skor: {oyuncu1.skor}")
            
            self.sonraki_brans()
            return ('oyuncu2_kazandi', None, None)
        
        # Kural 3: Yalnızca oyuncu 2'de kart yoksa oyuncu 1 hükmen kazanır
        if not oyuncu2_kart_var:
            print(f"{oyuncu2.oyuncu_adi}'nin {self.mevcut_brans} kartı kalmadı!")
            print(f"{oyuncu1.oyuncu_adi} hükmen kazandı!")
            
            # Hükmen galibiyete puan ver
            oyuncu1.galibiyet_serisi += 1
            oyuncu2.kaybetme_serisi += 1
            oyuncu2.galibiyet_serisi = 0
            
            hukmen_puan = 8  # Hükmen galibiyet puanı
            oyuncu1.skor += hukmen_puan
            
            print(f"\n{'='*60}")
            print(f"PUAN DAĞITIMI")
            print(f"{'='*60}")
            print(f"{oyuncu1.oyuncu_adi} - Hükmen Kazandı!")
            print(f"  Hükmen Galibiyet Puanı: +{hukmen_puan}")
            print(f"  Yeni Skor: {oyuncu1.skor}")
            print(f"\n{oyuncu2.oyuncu_adi} - Kaybetti. Puan yok.")
            print(f"  Yeni Skor: {oyuncu2.skor}")
            
            self.sonraki_brans()
            return ('oyuncu1_kazandi', None, None)
        
        # Kural 4: Her iki oyuncuda da o branşa ait kart varsa tur oynanabilir
        print(f"{oyuncu1.oyuncu_adi} ve {oyuncu2.oyuncu_adi} {self.mevcut_brans} kartı oynayabilir.")
        
        # Adım 2: Kullanıcı bu branşa ait kartlarından birini seçer
        # Adım 3: Bilgisayar stratejisine göre uygun kartını seçer
        oyuncu1_karti = oyuncu1.kart_sec(self.mevcut_brans)
        oyuncu2_karti = oyuncu2.kart_sec(self.mevcut_brans)
        
        # Adım 4: Sistem bu turda karşılaştırılacak özelliği belirler
        # Moda göre rastgele veya kullanıcı seçimi yapılır
        secilen_ozellik = self.ozellik_sec(self.mevcut_brans)
        if self.ozellik_secim_modu == self.OZELLIK_SECIM_RASTGELE:
            print(f"🎲 Rastgele seçilen özellik: {secilen_ozellik}")
        
        # Adım 5: Kartların güncel performans puanları hesaplanır
        # Sporcu referansını kullanarak puan hesapla
        oyuncu1_sporcu = oyuncu1_karti.get('sporcu_ref') if oyuncu1_karti else None
        oyuncu2_sporcu = oyuncu2_karti.get('sporcu_ref') if oyuncu2_karti else None
        
        oyuncu1_puani = self.puan_hesapla(oyuncu1_sporcu, oyuncu1_karti, secilen_ozellik, oyuncu1) if oyuncu1_sporcu else 0
        oyuncu2_puani = self.puan_hesapla(oyuncu2_sporcu, oyuncu2_karti, secilen_ozellik, oyuncu2) if oyuncu2_sporcu else 0
        
        print(f"\n{oyuncu1.oyuncu_adi} - Seçilen özellik puanı: {oyuncu1_puani:.2f}")
        print(f"{oyuncu2.oyuncu_adi} - Seçilen özellik puanı: {oyuncu2_puani:.2f}")
        
        # Kazananı belirle
        kazanan = self.kazanani_belirle(oyuncu1, oyuncu2, oyuncu1_karti, oyuncu2_karti, 
                                         secilen_ozellik, self.mevcut_brans)
        
        # Puanlama işlemleri
        self._puanları_guncelle(oyuncu1, oyuncu2, kazanan, oyuncu1_karti, oyuncu2_karti)
        
        self.sonraki_brans()
        return ('oynan', oyuncu1_karti, oyuncu2_karti, kazanan)
    
    def _puanları_guncelle(self, oyuncu1, oyuncu2, kazanan, oyuncu1_karti, oyuncu2_karti):
        """Her tur sonrası oyuncuların puanlarını, enerjilerini ve morallerini güncelle
        
        Args:
            oyuncu1: Birinci oyuncu
            oyuncu2: İkinci oyuncu
            kazanan (str): 'oyuncu1', 'oyuncu2' veya 'berabere'
            oyuncu1_karti (dict): Oyuncu 1'in kartı
            oyuncu2_karti (dict): Oyuncu 2'nin kartı
        """
        
        # Özel yetenek etkisini kontrol et (3. aşamada çözüldüyse)
        ozel_yetenek_etkili = False
        
        # Enerji ve moral güncelleme için sonuç belirle
        if kazanan == 'oyuncu1':
            oyuncu1_sonuc = 'kazandi'
            oyuncu2_sonuc = 'kaybetti'
        elif kazanan == 'oyuncu2':
            oyuncu1_sonuc = 'kaybetti'
            oyuncu2_sonuc = 'kazandi'
        else:
            oyuncu1_sonuc = 'berabere'
            oyuncu2_sonuc = 'berabere'
        
        # Tur sonuçlarını istatistiklere kaydet
        oyuncu1.tur_sonucu_kaydet(oyuncu1_sonuc, ozel_yetenek_etkili)
        oyuncu2.tur_sonucu_kaydet(oyuncu2_sonuc, ozel_yetenek_etkili)
        
        # Kartların enerjisini güncelle
        if oyuncu1_karti:
            enerji_kaybi1 = KartDagitici.kart_enerji_guncelle(
                oyuncu1_karti, oyuncu1_sonuc, ozel_yetenek_etkili
            )
            # Kart deneyim puanını güncelle
            deneyim_detay1 = KartDagitici.kart_deneyim_ekle(oyuncu1_karti, oyuncu1_sonuc)
        else:
            enerji_kaybi1 = 0
            deneyim_detay1 = None
            
        if oyuncu2_karti:
            enerji_kaybi2 = KartDagitici.kart_enerji_guncelle(
                oyuncu2_karti, oyuncu2_sonuc, ozel_yetenek_etkili
            )
            # Kart deneyim puanını güncelle
            deneyim_detay2 = KartDagitici.kart_deneyim_ekle(oyuncu2_karti, oyuncu2_sonuc)
        else:
            enerji_kaybi2 = 0
            deneyim_detay2 = None
        
        # Oyuncuların moralini güncelle
        moral_detay1 = oyuncu1.moral_guncelle(oyuncu1_sonuc, self.mevcut_brans, ozel_yetenek_etkili)
        moral_detay2 = oyuncu2.moral_guncelle(oyuncu2_sonuc, self.mevcut_brans, ozel_yetenek_etkili)
        
        # Oyuncu 1 kazandıysa
        if kazanan == 'oyuncu1':
            # Puanları hesapla ve ekle
            detaylar1 = self.toplam_tur_puanini_hesapla(
                kazanan, oyuncu1_karti.get('enerji', 100) if oyuncu1_karti else 100, 
                oyuncu1, oyuncu1_karti, 
                ozel_yetenek_etkili=ozel_yetenek_etkili, hukmen=False
            )
            
            print(f"\n{'='*60}")
            print(f"PUAN DAĞITIMI VE DURUM GÜNCELLEMESİ")
            print(f"{'='*60}")
            
            # Oyuncu 1 bilgileri
            print(f"\n{oyuncu1.oyuncu_adi} - Kazandı! 🏆")
            print(f"  Temel Puan: {detaylar1['temel_puan']}")
            if detaylar1['galibiyet_serisi_bonusu'] > 0:
                print(f"  Galibiyet Serisi Bonusu: +{detaylar1['galibiyet_serisi_bonusu']}")
            if detaylar1['enerji_bonusu'] > 0:
                print(f"  Düşük Enerji Bonusu: +{detaylar1['enerji_bonusu']}")
            if detaylar1['seviye_atlama_bonusu'] > 0:
                print(f"  Seviye Atlama Bonusu: +{detaylar1['seviye_atlama_bonusu']}")
            if detaylar1['clutch_player_bonusu'] > 0:
                print(f"  Clutch Player Bonusu: +{detaylar1['clutch_player_bonusu']}")
            print(f"  ─────────────────")
            print(f"  TOPLAM PUAN: +{detaylar1['toplam_puan']}")
            print(f"  Yeni Skor: {oyuncu1.skor}")
            
            # Enerji durumu
            if oyuncu1_karti:
                self._enerji_durumu_goster(oyuncu1.oyuncu_adi, oyuncu1_karti, enerji_kaybi1)
            
            # Deneyim ve seviye durumu
            if deneyim_detay1:
                self._deneyim_durumu_goster(oyuncu1.oyuncu_adi, oyuncu1_karti, deneyim_detay1)
            
            # Moral durumu
            self._moral_durumu_goster(oyuncu1.oyuncu_adi, moral_detay1)
            
            # Oyuncu 2 bilgileri
            print(f"\n{oyuncu2.oyuncu_adi} - Kaybetti. Puan yok.")
            print(f"  Yeni Skor: {oyuncu2.skor}")
            
            # Enerji durumu
            if oyuncu2_karti:
                self._enerji_durumu_goster(oyuncu2.oyuncu_adi, oyuncu2_karti, enerji_kaybi2)
            
            # Deneyim ve seviye durumu
            if deneyim_detay2:
                self._deneyim_durumu_goster(oyuncu2.oyuncu_adi, oyuncu2_karti, deneyim_detay2)
            
            # Moral durumu
            self._moral_durumu_goster(oyuncu2.oyuncu_adi, moral_detay2)
        
        # Oyuncu 2 kazandıysa
        elif kazanan == 'oyuncu2':
            # Puanları hesapla ve ekle
            detaylar2 = self.toplam_tur_puanini_hesapla(
                kazanan, oyuncu2_karti.get('enerji', 100) if oyuncu2_karti else 100,
                oyuncu2, oyuncu2_karti, 
                ozel_yetenek_etkili=ozel_yetenek_etkili, hukmen=False
            )
            
            print(f"\n{'='*60}")
            print(f"PUAN DAĞITIMI VE DURUM GÜNCELLEMESİ")
            print(f"{'='*60}")
            
            # Oyuncu 1 bilgileri
            print(f"\n{oyuncu1.oyuncu_adi} - Kaybetti. Puan yok.")
            print(f"  Yeni Skor: {oyuncu1.skor}")
            
            # Enerji durumu
            if oyuncu1_karti:
                self._enerji_durumu_goster(oyuncu1.oyuncu_adi, oyuncu1_karti, enerji_kaybi1)
            
            # Deneyim ve seviye durumu
            if deneyim_detay1:
                self._deneyim_durumu_goster(oyuncu1.oyuncu_adi, oyuncu1_karti, deneyim_detay1)
            
            # Moral durumu
            self._moral_durumu_goster(oyuncu1.oyuncu_adi, moral_detay1)
            
            # Oyuncu 2 bilgileri
            print(f"\n{oyuncu2.oyuncu_adi} - Kazandı! 🏆")
            print(f"  Temel Puan: {detaylar2['temel_puan']}")
            if detaylar2['galibiyet_serisi_bonusu'] > 0:
                print(f"  Galibiyet Serisi Bonusu: +{detaylar2['galibiyet_serisi_bonusu']}")
            if detaylar2['enerji_bonusu'] > 0:
                print(f"  Düşük Enerji Bonusu: +{detaylar2['enerji_bonusu']}")
            if detaylar2['seviye_atlama_bonusu'] > 0:
                print(f"  Seviye Atlama Bonusu: +{detaylar2['seviye_atlama_bonusu']}")
            if detaylar2['clutch_player_bonusu'] > 0:
                print(f"  Clutch Player Bonusu: +{detaylar2['clutch_player_bonusu']}")
            print(f"  ─────────────────")
            print(f"  TOPLAM PUAN: +{detaylar2['toplam_puan']}")
            print(f"  Yeni Skor: {oyuncu2.skor}")
            
            # Enerji durumu
            if oyuncu2_karti:
                self._enerji_durumu_goster(oyuncu2.oyuncu_adi, oyuncu2_karti, enerji_kaybi2)
            
            # Deneyim ve seviye durumu
            if deneyim_detay2:
                self._deneyim_durumu_goster(oyuncu2.oyuncu_adi, oyuncu2_karti, deneyim_detay2)
            
            # Moral durumu
            self._moral_durumu_goster(oyuncu2.oyuncu_adi, moral_detay2)
        
        # Beraberlik
        else:
            print(f"\n{'='*60}")
            print(f"PUAN DAĞITIMI VE DURUM GÜNCELLEMESİ")
            print(f"{'='*60}")
            
            print(f"\n{oyuncu1.oyuncu_adi} - Berabere. Puan yok.")
            print(f"  Yeni Skor: {oyuncu1.skor}")
            if oyuncu1_karti:
                self._enerji_durumu_goster(oyuncu1.oyuncu_adi, oyuncu1_karti, enerji_kaybi1)
            if deneyim_detay1:
                self._deneyim_durumu_goster(oyuncu1.oyuncu_adi, oyuncu1_karti, deneyim_detay1)
            self._moral_durumu_goster(oyuncu1.oyuncu_adi, moral_detay1)
            
            print(f"\n{oyuncu2.oyuncu_adi} - Berabere. Puan yok.")
            print(f"  Yeni Skor: {oyuncu2.skor}")
            if oyuncu2_karti:
                self._enerji_durumu_goster(oyuncu2.oyuncu_adi, oyuncu2_karti, enerji_kaybi2)
            if deneyim_detay2:
                self._deneyim_durumu_goster(oyuncu2.oyuncu_adi, oyuncu2_karti, deneyim_detay2)
            self._moral_durumu_goster(oyuncu2.oyuncu_adi, moral_detay2)
        
        # Oyundan çıkarılan kartları kontrol et ve bildir
        self._oyundan_cikan_kartlari_kontrol_et(oyuncu1, oyuncu1_karti)
        self._oyundan_cikan_kartlari_kontrol_et(oyuncu2, oyuncu2_karti)
    
    def _enerji_durumu_goster(self, oyuncu_adi, kart, enerji_kaybi):
        """Kartın enerji durumunu göster"""
        yeni_enerji = kart.get('enerji', 100)
        max_enerji = kart.get('max_enerji', 100)
        
        if kart.get('oyundan_cikarildi', False):
            print(f"  ⚡ Enerji: {yeni_enerji + enerji_kaybi}/{max_enerji} → {yeni_enerji}/{max_enerji} (-{enerji_kaybi}) ❌ KART OYUNDAN ÇIKARILDI!")
        elif KartDagitici.kart_enerji_kritik_mi(kart):
            print(f"  ⚡ Enerji: {yeni_enerji + enerji_kaybi}/{max_enerji} → {yeni_enerji}/{max_enerji} (-{enerji_kaybi}) ⚠️ KRİTİK!")
        else:
            print(f"  ⚡ Enerji: {yeni_enerji + enerji_kaybi}/{max_enerji} → {yeni_enerji}/{max_enerji} (-{enerji_kaybi})")
    
    def _deneyim_durumu_goster(self, oyuncu_adi, kart, deneyim_detay):
        """Kartın deneyim ve seviye durumunu göster"""
        if deneyim_detay['eklenen_deneyim'] > 0:
            print(f"  📊 Deneyim: {deneyim_detay['onceki_deneyim']} → {deneyim_detay['yeni_deneyim']} (+{deneyim_detay['eklenen_deneyim']})")
        
        # Seviye atladıysa bildir
        if deneyim_detay.get('seviye_atladi', False):
            yeni_seviye = deneyim_detay['yeni_seviye']
            print(f"\n  🎉 SEVİYE ATLADI! → Seviye {yeni_seviye}")
            print(f"      Kart: {kart['ad']}")
            
            # Seviye atlama bonuslarını göster
            seviye_sonucu = KartDagitici.kart_seviye_kontrol(kart)
            if seviye_sonucu.get('bonuslar'):
                print(f"      Bonuslar:")
                for bonus in seviye_sonucu['bonuslar']:
                    print(f"        • {bonus}")
    
    def _moral_durumu_goster(self, oyuncu_adi, moral_detay):
        """Moral değişimini göster"""
        if moral_detay['degisim'] != 0:
            isaret = "+" if moral_detay['degisim'] > 0 else ""
            print(f"  💪 Moral: {moral_detay['onceki_moral']} → {moral_detay['yeni_moral']} ({isaret}{moral_detay['degisim']})")
            for sebep in moral_detay['sebep']:
                print(f"      • {sebep}")
        else:
            print(f"  💪 Moral: {moral_detay['yeni_moral']} (değişmedi)")
    
    def _oyundan_cikan_kartlari_kontrol_et(self, oyuncu, kart):
        """Oyundan çıkan kartları kontrol et ve kart listesinden çıkar"""
        if kart and kart.get('oyundan_cikarildi', False):
            print(f"\n⚠️  {oyuncu.oyuncu_adi}'nin '{kart['ad']}' kartı enerjisi tükendiği için oyundan çıkarıldı!")
            print(f"    Bu kart artık kullanılamaz.")
    
    def _oyuncunun_brans_karti_var(self, oyuncu, brans):
        """Oyuncunun belirli bir branşa ait oynanabilir kartı olup olmadığını kontrol et
        
        Oyundan çıkarılmış kartlar hesaba katılmaz.
        """
        for kart in oyuncu.kart_listesi:
            if kart['brans'] == brans and not kart.get('oyundan_cikarildi', False):
                return True
        return False
    
    def _oyuncunun_branstaki_karti_al(self, oyuncu, brans):
        """Oyuncunun belirtilen branştaki oynanabilir kartını al
        
        Args:
            oyuncu: Oyuncu nesnesi
            brans (str): Branş adı
            
        Returns:
            dict: Kartın bilgileri (oyundan çıkarılmamış)
        """
        for kart in oyuncu.kart_listesi:
            if kart['brans'] == brans and not kart.get('oyundan_cikarildi', False):
                return kart
        return None
    
    def oyuncunun_kalan_brans_kartlari(self, oyuncu):
        """Oyuncunun kalan tüm oynanabilir branş kartlarını döndür
        
        Oyundan çıkarılmış kartlar hesaba katılmaz.
        """
        kalan_branslar = {}
        for kart in oyuncu.kart_listesi:
            if not kart.get('oyundan_cikarildi', False):
                brans = kart['brans']
                if brans not in kalan_branslar:
                    kalan_branslar[brans] = 0
                kalan_branslar[brans] += 1
        return kalan_branslar
    
    def tur_bilgisi_goster(self, oyuncu1, oyuncu2):
        """Tur bilgilerini göster"""
        print(f"\n{'='*60}")
        print(f"TUR BİLGİSİ")
        print(f"{'='*60}")
        print(f"Mevcut Tur: {self.mevcut_tur}")
        print(f"Mevcut Branş: {self.mevcut_brans}")
        
        # Oyuncu 1 bilgileri
        print(f"\n{oyuncu1.oyuncu_adi}:")
        print(f"  Skor: {oyuncu1.skor}")
        print(f"  {oyuncu1.moral_durum_goster()}")
        kalan1 = self.oyuncunun_kalan_brans_kartlari(oyuncu1)
        print(f"  Kalan Kartlar:")
        for brans, sayi in kalan1.items():
            print(f"    • {brans}: {sayi}")
        
        # Kritik enerjili kartları göster
        kritik1 = oyuncu1.kritik_enerjili_kartlari_al()
        if kritik1:
            print(f"  ⚠️ Kritik Enerjili Kartlar:")
            for k in kritik1:
                print(f"    • {k['ad']} ({k['brans']}) - Enerji: {k.get('enerji', 0)}")
        
        # Çıkarılmış kartları göster
        cikarilmis1 = oyuncu1.cikarilmis_kartlari_al()
        if cikarilmis1:
            print(f"  ❌ Oyundan Çıkarılan Kartlar: {len(cikarilmis1)}")
        
        # Oyuncu 2 bilgileri
        print(f"\n{oyuncu2.oyuncu_adi}:")
        print(f"  Skor: {oyuncu2.skor}")
        print(f"  {oyuncu2.moral_durum_goster()}")
        kalan2 = self.oyuncunun_kalan_brans_kartlari(oyuncu2)
        print(f"  Kalan Kartlar:")
        for brans, sayi in kalan2.items():
            print(f"    • {brans}: {sayi}")
        
        # Kritik enerjili kartları göster
        kritik2 = oyuncu2.kritik_enerjili_kartlari_al()
        if kritik2:
            print(f"  ⚠️ Kritik Enerjili Kartlar:")
            for k in kritik2:
                print(f"    • {k['ad']} ({k['brans']}) - Enerji: {k.get('enerji', 0)}")
        
        # Çıkarılmış kartları göster
        cikarilmis2 = oyuncu2.cikarilmis_kartlari_al()
        if cikarilmis2:
            print(f"  ❌ Oyundan Çıkarılan Kartlar: {len(cikarilmis2)}")
    
    # ==================== OYUN SONU KAZANAN BELİRLEME ====================
    
    def oyun_sonu_kazanani_belirle(self, oyuncu1, oyuncu2):
        """Oyun sonu kazananını belirle (7 aşamalı)
        
        Args:
            oyuncu1: Birinci oyuncu
            oyuncu2: İkinci oyuncu
            
        Returns:
            dict: Kazanan bilgisi ve karşılaştırma detayları
        """
        # İstatistikleri al
        istat1 = oyuncu1.oyun_sonu_istatistikleri()
        istat2 = oyuncu2.oyun_sonu_istatistikleri()
        
        sonuc = {
            'kazanan': None,
            'asama': 0,
            'aciklama': '',
            'oyuncu1_istatistik': istat1,
            'oyuncu2_istatistik': istat2
        }
        
        # 1. Aşama - Toplam Puan
        if istat1['toplam_puan'] != istat2['toplam_puan']:
            if istat1['toplam_puan'] > istat2['toplam_puan']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 1
                sonuc['aciklama'] = f"Toplam Puan: {istat1['toplam_puan']} > {istat2['toplam_puan']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 1
                sonuc['aciklama'] = f"Toplam Puan: {istat2['toplam_puan']} > {istat1['toplam_puan']}"
            return sonuc
        
        # 2. Aşama - Kazanılan Tur Sayısı
        if istat1['kazanilan_tur_sayisi'] != istat2['kazanilan_tur_sayisi']:
            if istat1['kazanilan_tur_sayisi'] > istat2['kazanilan_tur_sayisi']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 2
                sonuc['aciklama'] = f"Kazanılan Tur: {istat1['kazanilan_tur_sayisi']} > {istat2['kazanilan_tur_sayisi']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 2
                sonuc['aciklama'] = f"Kazanılan Tur: {istat2['kazanilan_tur_sayisi']} > {istat1['kazanilan_tur_sayisi']}"
            return sonuc
        
        # 3. Aşama - Toplam Galibiyet Serisi Sayısı
        if istat1['toplam_galibiyet_serisi'] != istat2['toplam_galibiyet_serisi']:
            if istat1['toplam_galibiyet_serisi'] > istat2['toplam_galibiyet_serisi']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 3
                sonuc['aciklama'] = f"Galibiyet Serisi: {istat1['toplam_galibiyet_serisi']} > {istat2['toplam_galibiyet_serisi']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 3
                sonuc['aciklama'] = f"Galibiyet Serisi: {istat2['toplam_galibiyet_serisi']} > {istat1['toplam_galibiyet_serisi']}"
            return sonuc
        
        # 4. Aşama - Kalan Toplam Enerji
        if istat1['kalan_toplam_enerji'] != istat2['kalan_toplam_enerji']:
            if istat1['kalan_toplam_enerji'] > istat2['kalan_toplam_enerji']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 4
                sonuc['aciklama'] = f"Kalan Enerji: {istat1['kalan_toplam_enerji']} > {istat2['kalan_toplam_enerji']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 4
                sonuc['aciklama'] = f"Kalan Enerji: {istat2['kalan_toplam_enerji']} > {istat1['kalan_toplam_enerji']}"
            return sonuc
        
        # 5. Aşama - En Yüksek Seviyeli Kart Sayısı
        if istat1['en_yuksek_seviyeli_kart_sayisi'] != istat2['en_yuksek_seviyeli_kart_sayisi']:
            if istat1['en_yuksek_seviyeli_kart_sayisi'] > istat2['en_yuksek_seviyeli_kart_sayisi']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 5
                sonuc['aciklama'] = f"Seviye 3 Kart: {istat1['en_yuksek_seviyeli_kart_sayisi']} > {istat2['en_yuksek_seviyeli_kart_sayisi']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 5
                sonuc['aciklama'] = f"Seviye 3 Kart: {istat2['en_yuksek_seviyeli_kart_sayisi']} > {istat1['en_yuksek_seviyeli_kart_sayisi']}"
            return sonuc
        
        # 6. Aşama - Özel Yetenekle Kazanılan Tur Sayısı
        if istat1['ozel_yetenekle_kazanilan_tur'] != istat2['ozel_yetenekle_kazanilan_tur']:
            if istat1['ozel_yetenekle_kazanilan_tur'] > istat2['ozel_yetenekle_kazanilan_tur']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 6
                sonuc['aciklama'] = f"Özel Yetenek Galibiyeti: {istat1['ozel_yetenekle_kazanilan_tur']} > {istat2['ozel_yetenekle_kazanilan_tur']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 6
                sonuc['aciklama'] = f"Özel Yetenek Galibiyeti: {istat2['ozel_yetenekle_kazanilan_tur']} > {istat1['ozel_yetenekle_kazanilan_tur']}"
            return sonuc
        
        # 7. Aşama - Beraberliği Az Olan Oyuncu
        if istat1['beraberlik_sayisi'] != istat2['beraberlik_sayisi']:
            if istat1['beraberlik_sayisi'] < istat2['beraberlik_sayisi']:
                sonuc['kazanan'] = oyuncu1
                sonuc['asama'] = 7
                sonuc['aciklama'] = f"Beraberlik Sayısı: {istat1['beraberlik_sayisi']} < {istat2['beraberlik_sayisi']}"
            else:
                sonuc['kazanan'] = oyuncu2
                sonuc['asama'] = 7
                sonuc['aciklama'] = f"Beraberlik Sayısı: {istat2['beraberlik_sayisi']} < {istat1['beraberlik_sayisi']}"
            return sonuc
        
        # 8. Aşama - Beraberlik (tüm kriterler eşit)
        sonuc['kazanan'] = None
        sonuc['asama'] = 8
        sonuc['aciklama'] = "Tüm kriterler eşit - BERABERE"
        return sonuc
    
    def oyun_sonu_raporu_goster(self, oyuncu1, oyuncu2):
        """Oyun sonu raporunu ekrana yazdır
        
        Args:
            oyuncu1: Birinci oyuncu
            oyuncu2: İkinci oyuncu
        """
        # Kazananı belirle
        sonuc = self.oyun_sonu_kazanani_belirle(oyuncu1, oyuncu2)
        
        istat1 = sonuc['oyuncu1_istatistik']
        istat2 = sonuc['oyuncu2_istatistik']
        
        print(f"\n{'='*70}")
        print(f"{'OYUN SONU RAPORU':^70}")
        print(f"{'='*70}")
        
        # İstatistik tablosu başlığı
        print(f"\n{'Kriter':<35} {oyuncu1.oyuncu_adi:<15} {oyuncu2.oyuncu_adi:<15}")
        print(f"{'-'*70}")
        
        # 1. Toplam Puan
        puan_isaret = self._karsilastirma_isareti(istat1['toplam_puan'], istat2['toplam_puan'])
        print(f"{'1. Toplam Puan':<35} {istat1['toplam_puan']:<15} {istat2['toplam_puan']:<15} {puan_isaret}")
        
        # 2. Kazanılan Tur Sayısı
        tur_isaret = self._karsilastirma_isareti(istat1['kazanilan_tur_sayisi'], istat2['kazanilan_tur_sayisi'])
        print(f"{'2. Kazanılan Tur Sayısı':<35} {istat1['kazanilan_tur_sayisi']:<15} {istat2['kazanilan_tur_sayisi']:<15} {tur_isaret}")
        
        # 3. Toplam Galibiyet Serisi
        seri_isaret = self._karsilastirma_isareti(istat1['toplam_galibiyet_serisi'], istat2['toplam_galibiyet_serisi'])
        print(f"{'3. Toplam Galibiyet Serisi':<35} {istat1['toplam_galibiyet_serisi']:<15} {istat2['toplam_galibiyet_serisi']:<15} {seri_isaret}")
        
        # 4. Kalan Toplam Enerji
        enerji_isaret = self._karsilastirma_isareti(istat1['kalan_toplam_enerji'], istat2['kalan_toplam_enerji'])
        print(f"{'4. Kalan Toplam Enerji':<35} {istat1['kalan_toplam_enerji']:<15} {istat2['kalan_toplam_enerji']:<15} {enerji_isaret}")
        
        # 5. En Yüksek Seviyeli Kart
        seviye_isaret = self._karsilastirma_isareti(istat1['en_yuksek_seviyeli_kart_sayisi'], istat2['en_yuksek_seviyeli_kart_sayisi'])
        print(f"{'5. Seviye 3 Kart Sayısı':<35} {istat1['en_yuksek_seviyeli_kart_sayisi']:<15} {istat2['en_yuksek_seviyeli_kart_sayisi']:<15} {seviye_isaret}")
        
        # 6. Özel Yetenekle Kazanılan
        ozel_isaret = self._karsilastirma_isareti(istat1['ozel_yetenekle_kazanilan_tur'], istat2['ozel_yetenekle_kazanilan_tur'])
        print(f"{'6. Özel Yetenek Galibiyeti':<35} {istat1['ozel_yetenekle_kazanilan_tur']:<15} {istat2['ozel_yetenekle_kazanilan_tur']:<15} {ozel_isaret}")
        
        # 7. Beraberlik Sayısı (az olan kazanır)
        beraberlik_isaret = self._karsilastirma_isareti(istat2['beraberlik_sayisi'], istat1['beraberlik_sayisi'])  # Ters çünkü az olan kazanır
        print(f"{'7. Beraberlik Sayısı (az iyi)':<35} {istat1['beraberlik_sayisi']:<15} {istat2['beraberlik_sayisi']:<15} {beraberlik_isaret}")
        
        print(f"{'-'*70}")
        
        # Ek istatistikler
        print(f"\n{'Ek İstatistikler':<35} {oyuncu1.oyuncu_adi:<15} {oyuncu2.oyuncu_adi:<15}")
        print(f"{'-'*70}")
        print(f"{'Kayıp Sayısı':<35} {istat1['kayip_sayisi']:<15} {istat2['kayip_sayisi']:<15}")
        print(f"{'Max Galibiyet Serisi':<35} {oyuncu1.max_galibiyet_serisi:<15} {oyuncu2.max_galibiyet_serisi:<15}")
        print(f"{'Final Moral':<35} {oyuncu1.moral:<15} {oyuncu2.moral:<15}")
        
        # Kazanan açıklaması
        print(f"\n{'='*70}")
        if sonuc['kazanan']:
            print(f"🏆 KAZANAN: {sonuc['kazanan'].oyuncu_adi}")
            print(f"   Aşama {sonuc['asama']}: {sonuc['aciklama']}")
        else:
            print(f"🤝 OYUN BERABERE!")
            print(f"   {sonuc['aciklama']}")
        print(f"{'='*70}")
        
        return sonuc
    
    def _karsilastirma_isareti(self, deger1, deger2):
        """İki değeri karşılaştır ve işaret döndür"""
        if deger1 > deger2:
            return "◀ Kazandı"
        elif deger2 > deger1:
            return "Kazandı ▶"
        else:
            return "= Eşit"

