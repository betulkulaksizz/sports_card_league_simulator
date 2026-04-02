from futbolcu import Futbolcu
from basketbolcu import Basketbolcu
from voleybolcu import Voleybolcu
from dosya_yoneticisi import DosyaYoneticisi
from ozel_yetenek import (
    ClutchPlayer, Captain, Legend, Defender, Veteran, Finisher
)


class SporcuYonetimi:
    """Sporcu oluşturma ve yönetimi için sınıf"""
    
    # Özel yetenek listesi (sırayla atanacak)
    OZEL_YETENEKLER = [
        Legend, Captain, ClutchPlayer, Defender, Veteran, Finisher, ClutchPlayer, Captain
    ]
    
    @staticmethod
    def ozel_yetenek_ata(sporcu, index):
        """Sporcuya özel yetenek ata
        
        Args:
            sporcu: Sporcu nesnesi
            index: Sporcu indeksi (sıralı yetenek ataması için)
        """
        yetenekler = SporcuYonetimi.OZEL_YETENEKLER
        yetenek_class = yetenekler[index % len(yetenekler)]
        sporcu.ozel_yetenek = yetenek_class()
    
    @staticmethod
    def sporcu_olustur_dosyadan(dosya_adi="sporcular.txt"):
        """Dosyadan sporcu bilgilerini oku ve sporcu nesneleri oluştur"""
        
        # Dosyadan sporcu verilerini oku
        futbolcu_verileri, basketbolcu_verileri, voleybolcu_verileri = DosyaYoneticisi.sporcular_oku(dosya_adi)
        
        # Futbolcu nesnelerini oluştur
        futbolcular = []
        for i, veri in enumerate(futbolcu_verileri):
            futbolcu = Futbolcu()
            futbolcu.sporcu_id = veri['sporcu_id']
            futbolcu.sporcu_adi = veri['sporcu_adi']
            futbolcu.takim_adi = veri['takim_adi']
            futbolcu.brans = veri['brans']
            futbolcu.seviye = 1  # Başlangıç seviyesi
            futbolcu.deneyim_puani = 0  # Başlangıç deneyimi
            futbolcu.penalti = veri['ozellikler']
            futbolcu.serbestturus = veri['enerji']
            futbolcu.kaleci_karsikarsiya = veri['dayaniklilik']
            futbolcu.ozel_yetenek_katsayisi = veri['ozel_yetenek']
            # Özel yetenek ata
            SporcuYonetimi.ozel_yetenek_ata(futbolcu, i)
            futbolcular.append(futbolcu)
        
        # Basketbolcu nesnelerini oluştur
        basketbolcular = []
        for i, veri in enumerate(basketbolcu_verileri):
            basketbolcu = Basketbolcu()
            basketbolcu.sporcu_id = veri['sporcu_id']
            basketbolcu.sporcu_adi = veri['sporcu_adi']
            basketbolcu.takim_adi = veri['takim_adi']
            basketbolcu.brans = veri['brans']
            basketbolcu.seviye = 1  # Başlangıç seviyesi
            basketbolcu.deneyim_puani = 0  # Başlangıç deneyimi
            basketbolcu.ucluk = veri['ozellikler']
            basketbolcu.ikilik = veri['enerji']
            basketbolcu.serbest_atis = veri['dayaniklilik']
            basketbolcu.ozel_yetenek_katsayisi = veri['ozel_yetenek']
            # Özel yetenek ata
            SporcuYonetimi.ozel_yetenek_ata(basketbolcu, i)
            basketbolcular.append(basketbolcu)
        
        # Voleybolcu nesnelerini oluştur
        voleybolcular = []
        for i, veri in enumerate(voleybolcu_verileri):
            voleybolcu = Voleybolcu()
            voleybolcu.sporcu_id = veri['sporcu_id']
            voleybolcu.sporcu_adi = veri['sporcu_adi']
            voleybolcu.takim_adi = veri['takim_adi']
            voleybolcu.brans = veri['brans']
            voleybolcu.seviye = 1  # Başlangıç seviyesi
            voleybolcu.deneyim_puani = 0  # Başlangıç deneyimi
            voleybolcu.servis = veri['ozellikler']
            voleybolcu.blok = veri['enerji']
            voleybolcu.smac = veri['dayaniklilik']
            voleybolcu.ozel_yetenek_katsayisi = veri['ozel_yetenek']
            # Özel yetenek ata
            SporcuYonetimi.ozel_yetenek_ata(voleybolcu, i)
            voleybolcular.append(voleybolcu)
        
        return futbolcular, basketbolcular, voleybolcular
    
    @staticmethod
    def sporcu_olustur():
        """Tüm sporcu türlerinden 8'er adet nesne oluşturup döndür"""
        # Futbolcu Nesneleri
        futbolcular = []
        
        futbolcu1 = Futbolcu()
        futbolcu1.sporcu_id = 101
        futbolcu1.sporcu_adi = "Mehmet Yıldız"
        futbolcu1.takim_adi = "Galatasaray"
        futbolcu1.brans = "Futbol"
        futbolcu1.seviye = 95
        futbolcu1.deneyim_puani = 850
        futbolcu1.penalti = 92
        futbolcu1.serbestturus = 88
        futbolcu1.kaleci_karsikarsiya = 85
        futbolcu1.ozel_yetenek_katsayisi = 1.8
        futbolcular.append(futbolcu1)
        
        futbolcu2 = Futbolcu()
        futbolcu2.sporcu_id = 102
        futbolcu2.sporcu_adi = "Emre Kaya"
        futbolcu2.takim_adi = "Fenerbahçe"
        futbolcu2.brans = "Futbol"
        futbolcu2.seviye = 93
        futbolcu2.deneyim_puani = 820
        futbolcu2.penalti = 90
        futbolcu2.serbestturus = 87
        futbolcu2.kaleci_karsikarsiya = 83
        futbolcu2.ozel_yetenek_katsayisi = 1.7
        futbolcular.append(futbolcu2)
        
        futbolcu3 = Futbolcu()
        futbolcu3.sporcu_id = 103
        futbolcu3.sporcu_adi = "Ali Çetin"
        futbolcu3.takim_adi = "Beşiktaş"
        futbolcu3.brans = "Futbol"
        futbolcu3.seviye = 91
        futbolcu3.deneyim_puani = 800
        futbolcu3.penalti = 88
        futbolcu3.serbestturus = 85
        futbolcu3.kaleci_karsikarsiya = 82
        futbolcu3.ozel_yetenek_katsayisi = 1.6
        futbolcular.append(futbolcu3)
        
        futbolcu4 = Futbolcu()
        futbolcu4.sporcu_id = 104
        futbolcu4.sporcu_adi = "Serkan Demir"
        futbolcu4.takim_adi = "Trabzonspor"
        futbolcu4.brans = "Futbol"
        futbolcu4.seviye = 89
        futbolcu4.deneyim_puani = 780
        futbolcu4.penalti = 86
        futbolcu4.serbestturus = 84
        futbolcu4.kaleci_karsikarsiya = 80
        futbolcu4.ozel_yetenek_katsayisi = 1.5
        futbolcular.append(futbolcu4)
        
        futbolcu5 = Futbolcu()
        futbolcu5.sporcu_id = 105
        futbolcu5.sporcu_adi = "Oğuz Kaya"
        futbolcu5.takim_adi = "Göztepe"
        futbolcu5.brans = "Futbol"
        futbolcu5.seviye = 87
        futbolcu5.deneyim_puani = 760
        futbolcu5.penalti = 84
        futbolcu5.serbestturus = 82
        futbolcu5.kaleci_karsikarsiya = 79
        futbolcu5.ozel_yetenek_katsayisi = 1.4
        futbolcular.append(futbolcu5)
        
        futbolcu6 = Futbolcu()
        futbolcu6.sporcu_id = 106
        futbolcu6.sporcu_adi = "İbrahim Şahin"
        futbolcu6.takim_adi = "Bursaspor"
        futbolcu6.brans = "Futbol"
        futbolcu6.seviye = 85
        futbolcu6.deneyim_puani = 740
        futbolcu6.penalti = 82
        futbolcu6.serbestturus = 80
        futbolcu6.kaleci_karsikarsiya = 78
        futbolcu6.ozel_yetenek_katsayisi = 1.3
        futbolcular.append(futbolcu6)
        
        futbolcu7 = Futbolcu()
        futbolcu7.sporcu_id = 107
        futbolcu7.sporcu_adi = "Fatih Arslan"
        futbolcu7.takim_adi = "Kasımpaşa"
        futbolcu7.brans = "Futbol"
        futbolcu7.seviye = 83
        futbolcu7.deneyim_puani = 720
        futbolcu7.penalti = 80
        futbolcu7.serbestturus = 78
        futbolcu7.kaleci_karsikarsiya = 76
        futbolcu7.ozel_yetenek_katsayisi = 1.2
        futbolcular.append(futbolcu7)
        
        futbolcu8 = Futbolcu()
        futbolcu8.sporcu_id = 108
        futbolcu8.sporcu_adi = "Murat Güney"
        futbolcu8.takim_adi = "Sivasspor"
        futbolcu8.brans = "Futbol"
        futbolcu8.seviye = 81
        futbolcu8.deneyim_puani = 700
        futbolcu8.penalti = 78
        futbolcu8.serbestturus = 76
        futbolcu8.kaleci_karsikarsiya = 75
        futbolcu8.ozel_yetenek_katsayisi = 1.1
        futbolcular.append(futbolcu8)
        
        # Basketbolcu Nesneleri
        basketbolcular = []
        
        basketbolcu1 = Basketbolcu()
        basketbolcu1.sporcu_id = 201
        basketbolcu1.sporcu_adi = "Kerem Aydın"
        basketbolcu1.takim_adi = "Fenerbahçe Alagöz"
        basketbolcu1.brans = "Basketbol"
        basketbolcu1.seviye = 96
        basketbolcu1.deneyim_puani = 880
        basketbolcu1.ucluk = 94
        basketbolcu1.ikilik = 91
        basketbolcu1.serbest_atis = 89
        basketbolcu1.ozel_yetenek_katsayisi = 1.9
        basketbolcular.append(basketbolcu1)
        
        basketbolcu2 = Basketbolcu()
        basketbolcu2.sporcu_id = 202
        basketbolcu2.sporcu_adi = "Güray Tekiner"
        basketbolcu2.takim_adi = "Galatasaray"
        basketbolcu2.brans = "Basketbol"
        basketbolcu2.seviye = 94
        basketbolcu2.deneyim_puani = 860
        basketbolcu2.ucluk = 92
        basketbolcu2.ikilik = 89
        basketbolcu2.serbest_atis = 87
        basketbolcu2.ozel_yetenek_katsayisi = 1.8
        basketbolcular.append(basketbolcu2)
        
        basketbolcu3 = Basketbolcu()
        basketbolcu3.sporcu_id = 203
        basketbolcu3.sporcu_adi = "Sertaç Şanlı"
        basketbolcu3.takim_adi = "Anadolu Efes"
        basketbolcu3.brans = "Basketbol"
        basketbolcu3.seviye = 92
        basketbolcu3.deneyim_puani = 840
        basketbolcu3.ucluk = 90
        basketbolcu3.ikilik = 87
        basketbolcu3.serbest_atis = 85
        basketbolcu3.ozel_yetenek_katsayisi = 1.7
        basketbolcular.append(basketbolcu3)
        
        basketbolcu4 = Basketbolcu()
        basketbolcu4.sporcu_id = 204
        basketbolcu4.sporcu_adi = "Murat Doğru"
        basketbolcu4.takim_adi = "Beşiktaş"
        basketbolcu4.brans = "Basketbol"
        basketbolcu4.seviye = 90
        basketbolcu4.deneyim_puani = 820
        basketbolcu4.ucluk = 88
        basketbolcu4.ikilik = 85
        basketbolcu4.serbest_atis = 83
        basketbolcu4.ozel_yetenek_katsayisi = 1.6
        basketbolcular.append(basketbolcu4)
        
        basketbolcu5 = Basketbolcu()
        basketbolcu5.sporcu_id = 205
        basketbolcu5.sporcu_adi = "Ersin Kara"
        basketbolcu5.takim_adi = "Darüşşafaka"
        basketbolcu5.brans = "Basketbol"
        basketbolcu5.seviye = 88
        basketbolcu5.deneyim_puani = 800
        basketbolcu5.ucluk = 86
        basketbolcu5.ikilik = 83
        basketbolcu5.serbest_atis = 81
        basketbolcu5.ozel_yetenek_katsayisi = 1.5
        basketbolcular.append(basketbolcu5)
        
        basketbolcu6 = Basketbolcu()
        basketbolcu6.sporcu_id = 206
        basketbolcu6.sporcu_adi = "Canım Kardeş"
        basketbolcu6.takim_adi = "Merkezefendi"
        basketbolcu6.brans = "Basketbol"
        basketbolcu6.seviye = 86
        basketbolcu6.deneyim_puani = 780
        basketbolcu6.ucluk = 84
        basketbolcu6.ikilik = 81
        basketbolcu6.serbest_atis = 79
        basketbolcu6.ozel_yetenek_katsayisi = 1.4
        basketbolcular.append(basketbolcu6)
        
        basketbolcu7 = Basketbolcu()
        basketbolcu7.sporcu_id = 207
        basketbolcu7.sporcu_adi = "Tuğrul Turcan"
        basketbolcu7.takim_adi = "Pera"
        basketbolcu7.brans = "Basketbol"
        basketbolcu7.seviye = 84
        basketbolcu7.deneyim_puani = 760
        basketbolcu7.ucluk = 82
        basketbolcu7.ikilik = 79
        basketbolcu7.serbest_atis = 77
        basketbolcu7.ozel_yetenek_katsayisi = 1.3
        basketbolcular.append(basketbolcu7)
        
        basketbolcu8 = Basketbolcu()
        basketbolcu8.sporcu_id = 208
        basketbolcu8.sporcu_adi = "Arzu Arslan"
        basketbolcu8.takim_adi = "Çukurova"
        basketbolcu8.brans = "Basketbol"
        basketbolcu8.seviye = 82
        basketbolcu8.deneyim_puani = 740
        basketbolcu8.ucluk = 80
        basketbolcu8.ikilik = 77
        basketbolcu8.serbest_atis = 75
        basketbolcu8.ozel_yetenek_katsayisi = 1.2
        basketbolcular.append(basketbolcu8)
        
        # Voleybolcu Nesneleri
        voleybolcular = []
        
        voleybolcu1 = Voleybolcu()
        voleybolcu1.sporcu_id = 301
        voleybolcu1.sporcu_adi = "Neslihan Demir"
        voleybolcu1.takim_adi = "Fenerbahçe"
        voleybolcu1.brans = "Voleybol"
        voleybolcu1.seviye = 97
        voleybolcu1.deneyim_puani = 900
        voleybolcu1.servis = 95
        voleybolcu1.blok = 93
        voleybolcu1.smac = 91
        voleybolcu1.ozel_yetenek_katsayisi = 2.0
        voleybolcular.append(voleybolcu1)
        
        voleybolcu2 = Voleybolcu()
        voleybolcu2.sporcu_id = 302
        voleybolcu2.sporcu_adi = "Eda Erdem"
        voleybolcu2.takim_adi = "Galatasaray"
        voleybolcu2.brans = "Voleybol"
        voleybolcu2.seviye = 95
        voleybolcu2.deneyim_puani = 880
        voleybolcu2.servis = 93
        voleybolcu2.blok = 91
        voleybolcu2.smac = 89
        voleybolcu2.ozel_yetenek_katsayisi = 1.9
        voleybolcular.append(voleybolcu2)
        
        voleybolcu3 = Voleybolcu()
        voleybolcu3.sporcu_id = 303
        voleybolcu3.sporcu_adi = "Ayşe Güzel"
        voleybolcu3.takim_adi = "Zeytinburnu"
        voleybolcu3.brans = "Voleybol"
        voleybolcu3.seviye = 93
        voleybolcu3.deneyim_puani = 860
        voleybolcu3.servis = 91
        voleybolcu3.blok = 89
        voleybolcu3.smac = 87
        voleybolcu3.ozel_yetenek_katsayisi = 1.8
        voleybolcular.append(voleybolcu3)
        
        voleybolcu4 = Voleybolcu()
        voleybolcu4.sporcu_id = 304
        voleybolcu4.sporcu_adi = "Zeynep Aşçı"
        voleybolcu4.takim_adi = "Beşiktaş"
        voleybolcu4.brans = "Voleybol"
        voleybolcu4.seviye = 91
        voleybolcu4.deneyim_puani = 840
        voleybolcu4.servis = 89
        voleybolcu4.blok = 87
        voleybolcu4.smac = 85
        voleybolcu4.ozel_yetenek_katsayisi = 1.7
        voleybolcular.append(voleybolcu4)
        
        voleybolcu5 = Voleybolcu()
        voleybolcu5.sporcu_id = 305
        voleybolcu5.sporcu_adi = "Merve Tuna"
        voleybolcu5.takim_adi = "Ege"
        voleybolcu5.brans = "Voleybol"
        voleybolcu5.seviye = 89
        voleybolcu5.deneyim_puani = 820
        voleybolcu5.servis = 87
        voleybolcu5.blok = 85
        voleybolcu5.smac = 83
        voleybolcu5.ozel_yetenek_katsayisi = 1.6
        voleybolcular.append(voleybolcu5)
        
        voleybolcu6 = Voleybolcu()
        voleybolcu6.sporcu_id = 306
        voleybolcu6.sporcu_adi = "Burcu Yıldız"
        voleybolcu6.takim_adi = "Nilüfer"
        voleybolcu6.brans = "Voleybol"
        voleybolcu6.seviye = 87
        voleybolcu6.deneyim_puani = 800
        voleybolcu6.servis = 85
        voleybolcu6.blok = 83
        voleybolcu6.smac = 81
        voleybolcu6.ozel_yetenek_katsayisi = 1.5
        voleybolcular.append(voleybolcu6)
        
        voleybolcu7 = Voleybolcu()
        voleybolcu7.sporcu_id = 307
        voleybolcu7.sporcu_adi = "Serap Kaya"
        voleybolcu7.takim_adi = "Çukurova"
        voleybolcu7.brans = "Voleybol"
        voleybolcu7.seviye = 85
        voleybolcu7.deneyim_puani = 780
        voleybolcu7.servis = 83
        voleybolcu7.blok = 81
        voleybolcu7.smac = 79
        voleybolcu7.ozel_yetenek_katsayisi = 1.4
        voleybolcular.append(voleybolcu7)
        
        voleybolcu8 = Voleybolcu()
        voleybolcu8.sporcu_id = 308
        voleybolcu8.sporcu_adi = "Hatice Korkmaz"
        voleybolcu8.takim_adi = "Ankara"
        voleybolcu8.brans = "Voleybol"
        voleybolcu8.seviye = 83
        voleybolcu8.deneyim_puani = 760
        voleybolcu8.servis = 81
        voleybolcu8.blok = 79
        voleybolcu8.smac = 77
        voleybolcu8.ozel_yetenek_katsayisi = 1.3
        voleybolcular.append(voleybolcu8)
        
        # Tüm sporculara yetenekler ata
        SporcuYonetimi._yetenekleri_ata(futbolcular, basketbolcular, voleybolcular)
        
        return futbolcular, basketbolcular, voleybolcular
    
    @staticmethod
    def _yetenekleri_ata(futbolcular, basketbolcular, voleybolcular):
        """Sporculara özel yetenekler ata - Kart özelliklerine göre anlamlı atama
        
        İsterlere Göre Yetenek Ataması:
        ─────────────────────────────────────────────────────────────────
        ⭐ Legend: En yüksek seviyeli efsane oyuncular (1 kez 2x çarpan)
        👑 Captain: Takım kaptanları - liderlik özelliği (+5 moral etkisi)
        🎯 ClutchPlayer: Kritik anlarda performans gösterenler (+10 son 3 tur)
        🛡️ Defender: Savunma odaklı oyuncular (rakip bonus %50 azalt)
        🏆 Veteran: Tecrübeli oyuncular (enerji kaybı %50 azalt)
        ⚡ Finisher: Düşük enerjide güçlü oyuncular (+8 enerji<30)
        
        Bazı yetenekler pasif (her tur), bazıları aktif (1 kez/maç).
        Her kart en fazla 1 özel yetenek taşır.
        ─────────────────────────────────────────────────────────────────
        """
        
        # ═══════════════════════════════════════════════════════════════
        # FUTBOLCULARA YETENEK ATAMA
        # ═══════════════════════════════════════════════════════════════
        for i, futbolcu in enumerate(futbolcular):
            if i == 0:
                # En yüksek puanlı futbolcu → LEGEND (Efsane yıldız)
                futbolcu.ozel_yetenek = Legend()
            elif i == 1:
                # İkinci en iyi → CAPTAIN (Takım kaptanı)
                futbolcu.ozel_yetenek = Captain()
            elif i == 2:
                # Üçüncü → CLUTCH PLAYER (Kritik anlarda parlayan)
                futbolcu.ozel_yetenek = ClutchPlayer()
            elif i == 3:
                # Dördüncü → DEFENDER (Savunmacı)
                futbolcu.ozel_yetenek = Defender()
            elif i == 4:
                # Beşinci → VETERAN (Tecrübeli)
                futbolcu.ozel_yetenek = Veteran()
            elif i == 5:
                # Altıncı → FINISHER (Bitirici)
                futbolcu.ozel_yetenek = Finisher()
            elif i == 6:
                # Yedinci → CLUTCH PLAYER
                futbolcu.ozel_yetenek = ClutchPlayer()
            else:
                # Sekizinci → CAPTAIN
                futbolcu.ozel_yetenek = Captain()
        
        # ═══════════════════════════════════════════════════════════════
        # BASKETBOLCULARA YETENEK ATAMA
        # ═══════════════════════════════════════════════════════════════
        for i, basketbolcu in enumerate(basketbolcular):
            if i == 0:
                # En yüksek puanlı basketbolcu → LEGEND
                basketbolcu.ozel_yetenek = Legend()
            elif i == 1:
                # İkinci → CAPTAIN
                basketbolcu.ozel_yetenek = Captain()
            elif i == 2:
                # Üçüncü → DEFENDER (Savunma odaklı)
                basketbolcu.ozel_yetenek = Defender()
            elif i == 3:
                # Dördüncü → CLUTCH PLAYER
                basketbolcu.ozel_yetenek = ClutchPlayer()
            elif i == 4:
                # Beşinci → FINISHER
                basketbolcu.ozel_yetenek = Finisher()
            elif i == 5:
                # Altıncı → VETERAN
                basketbolcu.ozel_yetenek = Veteran()
            elif i == 6:
                # Yedinci → LEGEND (İkinci efsane)
                basketbolcu.ozel_yetenek = Legend()
            else:
                # Sekizinci → DEFENDER
                basketbolcu.ozel_yetenek = Defender()
        
        # ═══════════════════════════════════════════════════════════════
        # VOLEYBOLCULARA YETENEK ATAMA
        # ═══════════════════════════════════════════════════════════════
        for i, voleybolcu in enumerate(voleybolcular):
            if i == 0:
                # En yüksek puanlı voleybolcu → LEGEND
                voleybolcu.ozel_yetenek = Legend()
            elif i == 1:
                # İkinci → DEFENDER (Blok uzmanı)
                voleybolcu.ozel_yetenek = Defender()
            elif i == 2:
                # Üçüncü → CAPTAIN
                voleybolcu.ozel_yetenek = Captain()
            elif i == 3:
                # Dördüncü → FINISHER (Smaç bitirici)
                voleybolcu.ozel_yetenek = Finisher()
            elif i == 4:
                # Beşinci → CLUTCH PLAYER
                voleybolcu.ozel_yetenek = ClutchPlayer()
            elif i == 5:
                # Altıncı → VETERAN
                voleybolcu.ozel_yetenek = Veteran()
            elif i == 6:
                # Yedinci → CAPTAIN (İkinci kaptan)
                voleybolcu.ozel_yetenek = Captain()
            else:
                # Sekizinci → CLUTCH PLAYER
                voleybolcu.ozel_yetenek = ClutchPlayer()
        
        return futbolcular, basketbolcular, voleybolcular
