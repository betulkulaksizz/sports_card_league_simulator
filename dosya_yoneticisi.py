import os


class DosyaYoneticisi:
    """Dosya işlemleri için sınıf"""
    
    # Geçerli sporcu türleri
    GECERLI_SPORCU_TURLERI = ["futbol", "basketbol", "voleybol"]
    
    # Geçerli özel yetenek türleri
    GECERLI_YETENEKLER = ["clutchplayer", "captain", "legend", "defender", "veteran", "finisher", ""]
    
    @staticmethod
    def sporcular_oku(dosya_adi):
        """sporcular.txt dosyasından sporcu bilgilerini oku
        
        Dosya formatı: sporcu_türü,sporcu_adı,takım_adı,özellik1,özellik2,özellik3,özel_yetenek_katsayısı
        
        Args:
            dosya_adi: Okunacak dosyanın adı
            
        Returns:
            tuple: (futbolcular, basketbolcular, voleybolcular) listeleri
            
        Raises:
            FileNotFoundError: Dosya bulunamadığında
            ValueError: Dosya formatı hatalı olduğunda
            IOError: Dosya okuma hatası olduğunda
        """
        
        # Dosya varlık kontrolü
        if not os.path.exists(dosya_adi):
            raise FileNotFoundError(f"❌ HATA: Dosya bulunamadı: '{dosya_adi}'\nLütfen 'sporcular.txt' dosyasının mevcut olduğundan emin olun.")
        
        futbolcular = []
        basketbolcular = []
        voleybolcular = []
        
        sporcu_id_futbol = 101
        sporcu_id_basketbol = 201
        sporcu_id_voleybol = 301
        
        hatali_satirlar = []
        
        try:
            with open(dosya_adi, 'r', encoding='utf-8') as dosya:
                lines = dosya.readlines()
            
            # Dosya boş mu kontrol et
            if not lines:
                raise ValueError(f"❌ HATA: '{dosya_adi}' dosyası boş!")
            
            for satir_no, line in enumerate(lines, 1):
                line = line.strip()
                
                # Boş satırları atla
                if not line:
                    continue
                
                # Yorum satırlarını atla (# ile başlayan)
                if line.startswith('#'):
                    continue
                
                # Sporcu verilerini işle
                try:
                    parts = line.split(',')
                    
                    # Minimum alan sayısı kontrolü
                    if len(parts) < 7:
                        hatali_satirlar.append(f"Satır {satir_no}: Eksik veri - en az 7 alan gerekli, {len(parts)} alan bulundu: '{line}'")
                        continue
                    
                    sporcu_turu = parts[0].strip().lower()
                    sporcu_adi = parts[1].strip()
                    takim_adi = parts[2].strip()
                    
                    # Sporcu türü kontrolü
                    if sporcu_turu not in DosyaYoneticisi.GECERLI_SPORCU_TURLERI:
                        hatali_satirlar.append(f"Satır {satir_no}: Geçersiz sporcu türü '{sporcu_turu}'. Geçerli türler: {', '.join(DosyaYoneticisi.GECERLI_SPORCU_TURLERI)}")
                        continue
                    
                    # Sporcu adı kontrolü
                    if not sporcu_adi:
                        hatali_satirlar.append(f"Satır {satir_no}: Sporcu adı boş olamaz!")
                        continue
                    
                    # Takım adı kontrolü
                    if not takim_adi:
                        hatali_satirlar.append(f"Satır {satir_no}: Takım adı boş olamaz!")
                        continue
                    
                    # Sayısal değerleri parse et
                    try:
                        ozellik1 = float(parts[3].strip())
                        ozellik2 = float(parts[4].strip())
                        ozellik3 = float(parts[5].strip())
                        ozel_yetenek_katsayi = float(parts[6].strip())
                    except ValueError as e:
                        hatali_satirlar.append(f"Satır {satir_no}: Sayısal değer hatası - '{line}'")
                        continue
                    
                    # Değer aralığı kontrolleri
                    if not (0 <= ozellik1 <= 100):
                        hatali_satirlar.append(f"Satır {satir_no}: Özellik 1 değeri 0-100 arasında olmalı: {ozellik1}")
                        continue
                    if not (0 <= ozellik2 <= 100):
                        hatali_satirlar.append(f"Satır {satir_no}: Özellik 2 değeri 0-100 arasında olmalı: {ozellik2}")
                        continue
                    if not (0 <= ozellik3 <= 100):
                        hatali_satirlar.append(f"Satır {satir_no}: Özellik 3 değeri 0-100 arasında olmalı: {ozellik3}")
                        continue
                    if not (0.0 <= ozel_yetenek_katsayi <= 5.0):
                        hatali_satirlar.append(f"Satır {satir_no}: Özel yetenek katsayısı 0.0-5.0 arasında olmalı: {ozel_yetenek_katsayi}")
                        continue
                    
                    # Branş adını düzelt (ilk harf büyük)
                    brans_adi = sporcu_turu.capitalize()
                    
                    sporcu_data = {
                        'sporcu_adi': sporcu_adi,
                        'takim_adi': takim_adi,
                        'brans': brans_adi,
                        'ozellikler': ozellik1,
                        'dayaniklilik': ozellik2,
                        'enerji': ozellik3,
                        'ozel_yetenek': ozel_yetenek_katsayi
                    }
                    
                    if sporcu_turu == "futbol":
                        sporcu_data['sporcu_id'] = sporcu_id_futbol
                        sporcu_id_futbol += 1
                        futbolcular.append(sporcu_data)
                    
                    elif sporcu_turu == "basketbol":
                        sporcu_data['sporcu_id'] = sporcu_id_basketbol
                        sporcu_id_basketbol += 1
                        basketbolcular.append(sporcu_data)
                    
                    elif sporcu_turu == "voleybol":
                        sporcu_data['sporcu_id'] = sporcu_id_voleybol
                        sporcu_id_voleybol += 1
                        voleybolcular.append(sporcu_data)
                
                except Exception as e:
                    hatali_satirlar.append(f"Satır {satir_no}: Beklenmeyen hata - {str(e)}: '{line}'")
                    continue
            
            # Hatalı satırları raporla
            if hatali_satirlar:
                print(f"\n⚠️ UYARI: {len(hatali_satirlar)} satırda hata bulundu:")
                for hata in hatali_satirlar[:10]:  # İlk 10 hatayı göster
                    print(f"  • {hata}")
                if len(hatali_satirlar) > 10:
                    print(f"  ... ve {len(hatali_satirlar) - 10} hata daha")
            
            # En az bir sporcu okundu mu kontrol et
            toplam_sporcu = len(futbolcular) + len(basketbolcular) + len(voleybolcular)
            if toplam_sporcu == 0:
                raise ValueError(f"❌ HATA: '{dosya_adi}' dosyasından hiç geçerli sporcu okunamadı!")
            
            # Başarılı okuma mesajı
            print(f"\n✅ Dosya başarıyla okundu: '{dosya_adi}'")
            print(f"   Futbolcu: {len(futbolcular)}, Basketbolcu: {len(basketbolcular)}, Voleybolcu: {len(voleybolcular)}")
            
            return futbolcular, basketbolcular, voleybolcular
        
        except IOError as e:
            raise IOError(f"❌ HATA: Dosya okuma hatası: {e}")
    
    @staticmethod
    def sporcular_yaz(dosya_adi, futbolcular, basketbolcular, voleybolcular):
        """Sporcu bilgilerini dosyaya yaz"""
        
        try:
            with open(dosya_adi, 'w', encoding='utf-8') as dosya:
                # Futbolcuları yaz
                for f in futbolcular:
                    line = f"Futbol,{f['sporcu_adi']},{f['takim_adi']},{f['ozellikler']},{f['dayaniklilik']},{f['enerji']},{f['ozel_yetenek']}\n"
                    dosya.write(line)
                
                # Basketbolcuları yaz
                for b in basketbolcular:
                    line = f"Basketbol,{b['sporcu_adi']},{b['takim_adi']},{b['ozellikler']},{b['dayaniklilik']},{b['enerji']},{b['ozel_yetenek']}\n"
                    dosya.write(line)
                
                # Voleybolcuları yaz
                for v in voleybolcular:
                    line = f"Voleybol,{v['sporcu_adi']},{v['takim_adi']},{v['ozellikler']},{v['dayaniklilik']},{v['enerji']},{v['ozel_yetenek']}\n"
                    dosya.write(line)
            
            print(f"Veriler başarıyla '{dosya_adi}' dosyasına yazıldı.")
        
        except IOError as e:
            raise IOError(f"Dosya yazma hatası: {e}")
