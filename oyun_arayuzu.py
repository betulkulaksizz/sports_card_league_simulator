"""
PyQt5 ile Tam Oyun Arayüzü
Kart oyununu görsel olarak oynatır
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QProgressBar, QPushButton, QListWidget, 
    QListWidgetItem, QMessageBox, QSizePolicy, QDialog, QRadioButton,
    QButtonGroup, QComboBox, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from sporcu_yonetimi import SporcuYonetimi
from kullanici import Kullanici
from bilgisayar import Bilgisayar
from kart_dagitici import KartDagitici
from tur_yoneticisi import TurYoneticisi
from mac_istatistik import MacIstatistik


class KartSecimDialog(QDialog):
    """Kullanıcının kart seçmesi için dialog penceresi - Güncel puanları gösterir"""
    
    def __init__(self, kartlar, brans, parent=None, tur_yoneticisi=None, oyuncu_obj=None):
        super().__init__(parent)
        self.setWindowTitle(f"🎴 {brans} Kartı Seç")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.secilen_kart = None
        self.kartlar = kartlar
        self.brans = brans
        self.tur_yoneticisi = tur_yoneticisi
        self.oyuncu_obj = oyuncu_obj
        
        self.setStyleSheet("""
            QDialog { background-color: #1a1a2e; }
            QLabel { color: white; }
            QGroupBox { 
                color: white; 
                border: 2px solid #4CAF50; 
                border-radius: 10px; 
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px; 
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Başlık
        baslik = QLabel(f"🎯 {brans} branşında oynayacağınız kartı seçin:")
        baslik.setFont(QFont('Arial', 12, QFont.Bold))
        baslik.setStyleSheet("color: #FFD700;")
        layout.addWidget(baslik)
        
        # Kart listesi
        self.kart_listesi = QListWidget()
        self.kart_listesi.setStyleSheet("""
            QListWidget {
                background-color: #0f0f23;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
            }
            QListWidget::item:hover {
                background-color: #2E7D32;
            }
        """)
        self.kart_listesi.setMinimumHeight(250)
        self.kart_listesi.itemSelectionChanged.connect(self.kart_secildi)
        
        # Yetenek bilgi paneli
        self.yetenek_panel = QGroupBox("🔷 Yetenek Bilgisi")
        self.yetenek_panel.setStyleSheet("""
            QGroupBox {
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        yetenek_layout = QVBoxLayout()
        self.yetenek_label = QLabel("Yetenek seçmek için bir kart seçin...")
        self.yetenek_label.setStyleSheet("color: #999; font-size: 12px;")
        self.yetenek_label.setWordWrap(True)
        yetenek_layout.addWidget(self.yetenek_label)
        self.yetenek_panel.setLayout(yetenek_layout)
        
        # Branşa göre özellik listesi
        ozellik_listesi = {
            "Futbol": ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"],
            "Basketbol": ["Üçlük", "İkilik", "Serbest Atış"],
            "Voleybol": ["Servis", "Blok", "Smac"]
        }
        
        for kart in kartlar:
            enerji = kart.get('enerji', 100)
            seviye = kart.get('seviye', 1)
            sporcu = kart.get('sporcu_ref')
            
            # Kart özelliklerini ve güncel puanları hesapla
            ozellik_bilgi = ""
            guncel_puanlar = ""
            yetenek_bilgi = ""
            
            if sporcu and self.tur_yoneticisi:
                ozellikler = ozellik_listesi.get(brans, [])
                puan_listesi = []
                
                for ozellik in ozellikler:
                    detay = self.tur_yoneticisi.puan_hesapla_detayli(
                        sporcu, kart, ozellik, self.oyuncu_obj
                    )
                    temel = detay['temel_puan']
                    guncel = detay['guncel_puan']
                    puan_listesi.append(f"{ozellik[:6]}: {temel:.0f}→{guncel:.0f}")
                
                guncel_puanlar = " | ".join(puan_listesi)
                
                # Yetenek bilgisini al
                if hasattr(sporcu, 'ozel_yetenek') and sporcu.ozel_yetenek:
                    yetenek_bilgi = f"\n   🔷 {sporcu.ozel_yetenek.ac_kla()}"
            elif sporcu:
                # Fallback: sadece temel puanları göster
                if brans == "Futbol":
                    ozellik_bilgi = f"Penaltı: {sporcu.penalti} | Serbest: {sporcu.serbestturus} | Kaleci: {sporcu.kaleci_karsikarsiya}"
                elif brans == "Basketbol":
                    ozellik_bilgi = f"Üçlük: {sporcu.ucluk} | İkilik: {sporcu.ikilik} | Serbest: {sporcu.serbest_atis}"
                elif brans == "Voleybol":
                    ozellik_bilgi = f"Servis: {sporcu.servis} | Blok: {sporcu.blok} | Smaç: {sporcu.smac}"
                
                # Yetenek bilgisini al (fallback)
                if hasattr(sporcu, 'ozel_yetenek') and sporcu.ozel_yetenek:
                    yetenek_bilgi = f"\n   🔷 {sporcu.ozel_yetenek.ac_kla()}"
            
            durum = "❌" if enerji <= 0 else "⚠️" if enerji < 20 else "✓"
            
            if guncel_puanlar:
                metin = f"{kart['ad']} | Sv:{seviye} | ⚡{enerji} {durum}\n   📊 {guncel_puanlar}{yetenek_bilgi}"
            else:
                metin = f"{kart['ad']} | Sv:{seviye} | ⚡{enerji} {durum}\n   {ozellik_bilgi}{yetenek_bilgi}"
            
            item = QListWidgetItem(metin)
            if enerji <= 0:
                item.setForeground(QColor("#666"))
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            elif enerji < 20:
                item.setForeground(QColor("#FF9800"))
            else:
                item.setForeground(QColor("#FFF"))
            
            self.kart_listesi.addItem(item)
        
        layout.addWidget(self.kart_listesi)
        
        # Yetenek panelini layout'a ekle
        layout.addWidget(self.yetenek_panel)
        
        # Seç butonu
        self.sec_btn = QPushButton("✓ Bu Kartı Seç")
        self.sec_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.sec_btn.setMinimumHeight(45)
        self.sec_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #66BB6A; }
        """)
        self.sec_btn.clicked.connect(self.kart_sec)
        layout.addWidget(self.sec_btn)
    
    def kart_secildi(self):
        """Kart seçildiğinde yetenek bilgisini güncelle"""
        index = self.kart_listesi.currentRow()
        if index >= 0 and index < len(self.kartlar):
            kart = self.kartlar[index]
            sporcu = kart.get('sporcu_ref')
            
            if sporcu and hasattr(sporcu, 'ozel_yetenek') and sporcu.ozel_yetenek:
                yetenek = sporcu.ozel_yetenek
                yetenek_aciklama = yetenek.ac_kla()
                
                # Yetenek türünü belirle
                if yetenek.pasif_mi():
                    yetenek_turu = "📍 PASİF YETENEK"
                else:
                    yetenek_turu = "⚡ AKTİF YETENEK (1x kullanım)"
                
                # Yetenek özellikleri
                bilgi = f"{yetenek_turu}\n\n{yetenek_aciklama}\n\n"
                
                # Yetenek açıklamalarını ekle
                from ozel_yetenek import ClutchPlayer, Captain, Legend, Defender, Veteran, Finisher
                
                if isinstance(yetenek, ClutchPlayer):
                    bilgi += "• Son 3 turda oynanması durumunda +10 puan bonus alır\n• Tur numarası takip edilir"
                elif isinstance(yetenek, Captain):
                    bilgi += "• Aynı branştaki takım kartlarına +5 moral bonusu verir\n• Pasif olarak çalışır"
                elif isinstance(yetenek, Legend):
                    bilgi += "• Maç başında 1 kez aktive edilebilir\n• Seçilen özelliğin puanını 2x yapar\n• +5 ek enerji kaybına neden olur"
                elif isinstance(yetenek, Defender):
                    bilgi += "• Rakibin özel yetenek bonusunu %50 azaltır\n• Pasif olarak her tur çalışır"
                elif isinstance(yetenek, Veteran):
                    bilgi += "• Enerji kaybını %50 azaltır\n• Kazanma, kayıp ve berabere tüm durumlarda etkin"
                elif isinstance(yetenek, Finisher):
                    bilgi += "• Enerjisi 30'dan az olduğunda +8 puan bonus alır\n• Pasif olarak çalışır"
                
                self.yetenek_label.setText(bilgi)
                self.yetenek_label.setStyleSheet("color: #FFD700; font-size: 11px; font-weight: bold;")
            else:
                self.yetenek_label.setText("❌ Bu kart özel yeteneğe sahip değildir")
                self.yetenek_label.setStyleSheet("color: #999; font-size: 12px;")
    
    def kart_sec(self):
        index = self.kart_listesi.currentRow()
        if index >= 0 and index < len(self.kartlar):
            self.secilen_kart = self.kartlar[index]
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kart seçin!")


class OzellikSecimDialog(QDialog):
    """Kullanıcının özellik seçmesi için dialog penceresi"""
    
    def __init__(self, brans, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"🎯 {brans} Özelliği Seç")
        self.setModal(True)
        self.setMinimumWidth(350)
        self.secilen_ozellik = None
        
        # Branşa göre özellikler
        self.ozellikler = {
            "Futbol": ["Penaltı", "Serbest Vuruş", "Kaleci Karşı Karşıya"],
            "Basketbol": ["Üçlük", "İkilik", "Serbest Atış"],
            "Voleybol": ["Servis", "Blok", "Smac"]
        }
        
        self.setStyleSheet("""
            QDialog { background-color: #1a1a2e; }
            QLabel { color: white; }
            QRadioButton { 
                color: white; 
                font-size: 14px;
                padding: 10px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Başlık
        baslik = QLabel(f"🎲 {brans} için karşılaştırma özelliği seçin:")
        baslik.setFont(QFont('Arial', 12, QFont.Bold))
        baslik.setStyleSheet("color: #FFD700;")
        layout.addWidget(baslik)
        
        # Özellik radio butonları
        self.button_group = QButtonGroup(self)
        
        ozellik_listesi = self.ozellikler.get(brans, [])
        for i, ozellik in enumerate(ozellik_listesi):
            emoji = "🎯" if i == 0 else "⚡" if i == 1 else "🔥"
            radio = QRadioButton(f"{emoji} {ozellik}")
            radio.setFont(QFont('Arial', 13))
            radio.setStyleSheet("""
                QRadioButton {
                    background-color: #0f0f23;
                    border: 1px solid #333;
                    border-radius: 8px;
                    padding: 12px;
                }
                QRadioButton:hover {
                    background-color: #2E7D32;
                    border-color: #4CAF50;
                }
                QRadioButton:checked {
                    background-color: #4CAF50;
                    border-color: #66BB6A;
                }
            """)
            self.button_group.addButton(radio, i)
            layout.addWidget(radio)
        
        # İlk seçeneği seç
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)
        
        # Seç butonu
        self.sec_btn = QPushButton("✓ Bu Özelliği Seç")
        self.sec_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.sec_btn.setMinimumHeight(45)
        self.sec_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #42A5F5; }
        """)
        self.sec_btn.clicked.connect(self.ozellik_sec)
        layout.addWidget(self.sec_btn)
    
    def ozellik_sec(self):
        secili = self.button_group.checkedButton()
        if secili:
            # Emoji'yi kaldır ve özellik adını al
            self.secilen_ozellik = secili.text().split(" ", 1)[1]
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir özellik seçin!")


class ZorlukSecimDialog(QDialog):
    """Oyun başlamadan önce zorluk seviyesi seçimi için dialog penceresi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎮 Zorluk Seviyesi Seç")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setMinimumHeight(400)
        self.secilen_zorluk = None
        
        self.setStyleSheet("""
            QDialog { background-color: #1a1a2e; }
            QLabel { color: white; }
            QRadioButton { 
                color: white; 
                font-size: 14px;
                padding: 15px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Başlık
        baslik = QLabel("🤖 Bilgisayar Zorluk Seviyesini Seçin")
        baslik.setFont(QFont('Arial', 16, QFont.Bold))
        baslik.setStyleSheet("color: #FFD700;")
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Alt başlık
        alt_baslik = QLabel("Seçtiğiniz zorluk seviyesi, bilgisayarın\nkart seçme stratejisini belirler.")
        alt_baslik.setFont(QFont('Arial', 11))
        alt_baslik.setStyleSheet("color: #888;")
        alt_baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(alt_baslik)
        
        # Zorluk seçenekleri
        self.button_group = QButtonGroup(self)
        
        zorluklar = [
            ("kolay", "🎲 KOLAY", "Rastgele kart seçer - Yeni başlayanlar için ideal", "#4CAF50"),
            ("orta", "📊 ORTA", "En yüksek ortalama performanslı kartı seçer", "#FF9800"),
            ("zor", "🎯 ZOR", "En yüksek seviye ve enerjili kartı seçer - Uzmanlar için", "#F44336")
        ]
        
        for i, (key, ad, aciklama, renk) in enumerate(zorluklar):
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: #0f0f23;
                    border: 2px solid {renk};
                    border-radius: 12px;
                    padding: 10px;
                }}
                QFrame:hover {{
                    background-color: #1a1a3e;
                }}
            """)
            frame_layout = QVBoxLayout(frame)
            frame_layout.setSpacing(5)
            
            radio = QRadioButton(ad)
            radio.setFont(QFont('Arial', 14, QFont.Bold))
            radio.setStyleSheet(f"""
                QRadioButton {{
                    color: {renk};
                    padding: 5px;
                }}
                QRadioButton::indicator {{
                    width: 22px;
                    height: 22px;
                }}
                QRadioButton::indicator:checked {{
                    background-color: {renk};
                    border: 2px solid white;
                    border-radius: 11px;
                }}
            """)
            radio.setProperty("zorluk_key", key)
            self.button_group.addButton(radio, i)
            frame_layout.addWidget(radio)
            
            aciklama_label = QLabel(aciklama)
            aciklama_label.setFont(QFont('Arial', 10))
            aciklama_label.setStyleSheet("color: #AAA; padding-left: 30px;")
            frame_layout.addWidget(aciklama_label)
            
            layout.addWidget(frame)
        
        # İlk seçeneği seç (Kolay)
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)
        
        # Başlat butonu
        self.baslat_btn = QPushButton("🎮 OYUNU BAŞLAT")
        self.baslat_btn.setFont(QFont('Arial', 14, QFont.Bold))
        self.baslat_btn.setMinimumHeight(55)
        self.baslat_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover { background-color: #66BB6A; }
        """)
        self.baslat_btn.clicked.connect(self.zorluk_sec)
        layout.addWidget(self.baslat_btn)
    
    def zorluk_sec(self):
        secili = self.button_group.checkedButton()
        if secili:
            self.secilen_zorluk = secili.property("zorluk_key")
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir zorluk seviyesi seçin!")


class PuanDetayDialog(QDialog):
    """Puan hesaplama detaylarını gösteren dialog"""
    
    def __init__(self, kullanici_detay, bilgisayar_detay, secilen_ozellik, kazanan, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 Puan Hesaplama Detayları")
        self.setModal(True)
        self.setMinimumWidth(600)
        
        self.setStyleSheet("""
            QDialog { background-color: #1a1a2e; }
            QLabel { color: white; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Başlık
        baslik = QLabel(f"🎯 Karşılaştırılan Özellik: {secilen_ozellik}")
        baslik.setFont(QFont('Arial', 14, QFont.Bold))
        baslik.setStyleSheet("color: #FFD700;")
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # İki sütunlu layout
        iki_sutun = QHBoxLayout()
        
        # Kullanıcı detayları
        kullanici_frame = QFrame()
        kullanici_frame.setStyleSheet("""
            QFrame { 
                background-color: #2E7D32; 
                border: 2px solid #4CAF50; 
                border-radius: 10px; 
                padding: 10px;
            }
        """)
        kullanici_layout = QVBoxLayout(kullanici_frame)
        
        k_baslik = QLabel("👤 KULLANICI")
        k_baslik.setFont(QFont('Arial', 12, QFont.Bold))
        k_baslik.setStyleSheet("color: white; border: none;")
        k_baslik.setAlignment(Qt.AlignCenter)
        kullanici_layout.addWidget(k_baslik)
        
        k_detay = QLabel(self._detay_metni_olustur(kullanici_detay))
        k_detay.setStyleSheet("color: white; border: none; font-family: Courier;")
        kullanici_layout.addWidget(k_detay)
        
        iki_sutun.addWidget(kullanici_frame)
        
        # VS
        vs = QLabel("VS")
        vs.setFont(QFont('Arial', 20, QFont.Bold))
        vs.setStyleSheet("color: #FF5722;")
        vs.setAlignment(Qt.AlignCenter)
        iki_sutun.addWidget(vs)
        
        # Bilgisayar detayları
        bilgisayar_frame = QFrame()
        bilgisayar_frame.setStyleSheet("""
            QFrame { 
                background-color: #C62828; 
                border: 2px solid #F44336; 
                border-radius: 10px; 
                padding: 10px;
            }
        """)
        bilgisayar_layout = QVBoxLayout(bilgisayar_frame)
        
        b_baslik = QLabel("🤖 BİLGİSAYAR")
        b_baslik.setFont(QFont('Arial', 12, QFont.Bold))
        b_baslik.setStyleSheet("color: white; border: none;")
        b_baslik.setAlignment(Qt.AlignCenter)
        bilgisayar_layout.addWidget(b_baslik)
        
        b_detay = QLabel(self._detay_metni_olustur(bilgisayar_detay))
        b_detay.setStyleSheet("color: white; border: none; font-family: Courier;")
        bilgisayar_layout.addWidget(b_detay)
        
        iki_sutun.addWidget(bilgisayar_frame)
        
        layout.addLayout(iki_sutun)
        
        # Sonuç
        if kazanan == 'oyuncu1':
            sonuc_text = "🏆 KULLANICI KAZANDI!"
            sonuc_renk = "#4CAF50"
        elif kazanan == 'oyuncu2':
            sonuc_text = "💻 BİLGİSAYAR KAZANDI!"
            sonuc_renk = "#F44336"
        else:
            sonuc_text = "🤝 BERABERE!"
            sonuc_renk = "#FF9800"
        
        sonuc = QLabel(sonuc_text)
        sonuc.setFont(QFont('Arial', 16, QFont.Bold))
        sonuc.setStyleSheet(f"color: {sonuc_renk}; border: none;")
        sonuc.setAlignment(Qt.AlignCenter)
        layout.addWidget(sonuc)
        
        # Tamam butonu
        tamam_btn = QPushButton("✓ Tamam")
        tamam_btn.setFont(QFont('Arial', 12, QFont.Bold))
        tamam_btn.setMinimumHeight(40)
        tamam_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #42A5F5; }
        """)
        tamam_btn.clicked.connect(self.accept)
        layout.addWidget(tamam_btn)
    
    def _detay_metni_olustur(self, detay):
        """Detay dictionary'sinden metin oluştur"""
        metin = f"""
Temel Puan:        {detay['temel_puan']:.1f}
─────────────────────────
Moral ({detay['moral']}):       {'+' if detay['moral_bonusu'] >= 0 else ''}{detay['moral_bonusu']:.1f}
Özel Yetenek:      +{detay['ozel_yetenek_bonusu']:.1f}
Seviye ({detay['seviye']}):        +{detay['seviye_bonusu']:.1f}
Enerji ({detay['enerji']}):       -{detay['enerji_cezasi']:.1f}
─────────────────────────
GÜNCEL PUAN:       {detay['guncel_puan']:.1f}
"""
        # Bonus detayları varsa ekle
        bonus_list = detay.get('bonus_detay', [])
        if bonus_list:
            metin += "─────────────────────────\n"
            metin += "BONUSLAR:\n"
            for bonus in bonus_list:
                metin += f"  {bonus}\n"
        
        return metin


class OyunSonucDialog(QDialog):
    """Oyun sonu sonuç ekranı - büyük ve detaylı"""
    
    def __init__(self, kullanici, bilgisayar, kazanan, asama, detay, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏁 OYUN BİTTİ")
        self.setModal(True)
        self.setMinimumSize(1000, 750)
        self.resize(1100, 850)
        
        self.setStyleSheet("""
            QDialog { background-color: #0f0f23; }
            QLabel { color: white; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # ===== KAZANAN BAŞLIĞI (BÜYÜK) =====
        if kazanan == kullanici:
            kazanan_text = "🏆 KULLANICI KAZANDI! 🏆"
            kazanan_renk = "#4CAF50"
            kazanan_bg = "#1B5E20"
        elif kazanan == bilgisayar:
            kazanan_text = "💻 BİLGİSAYAR KAZANDI! 💻"
            kazanan_renk = "#F44336"
            kazanan_bg = "#B71C1C"
        else:
            kazanan_text = "🤝 BERABERE! 🤝"
            kazanan_renk = "#FF9800"
            kazanan_bg = "#E65100"
        
        kazanan_label = QLabel(kazanan_text)
        kazanan_label.setFont(QFont('Arial', 24, QFont.Bold))
        kazanan_label.setAlignment(Qt.AlignCenter)
        kazanan_label.setStyleSheet(f"""
            color: {kazanan_renk};
            background-color: {kazanan_bg};
            border: 3px solid {kazanan_renk};
            border-radius: 15px;
            padding: 15px;
        """)
        kazanan_label.setMinimumHeight(70)
        layout.addWidget(kazanan_label)
        
        # ===== SKOR TABLOSU =====
        skor_frame = QFrame()
        skor_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 2px solid #FFD700;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        skor_frame.setMinimumHeight(250)
        skor_layout = QHBoxLayout(skor_frame)
        skor_layout.setSpacing(20)
        
        # Kullanıcı Skor Kartı
        k_frame = QFrame()
        k_frame.setStyleSheet("""
            QFrame {
                background-color: #2E7D32;
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        k_frame.setMinimumHeight(200)
        k_layout = QVBoxLayout(k_frame)
        k_layout.setSpacing(10)
        
        k_baslik = QLabel("👤 KULLANICI")
        k_baslik.setFont(QFont('Arial', 16, QFont.Bold))
        k_baslik.setAlignment(Qt.AlignCenter)
        k_baslik.setStyleSheet("color: white; background: transparent;")
        k_baslik.setMinimumHeight(30)
        k_layout.addWidget(k_baslik)
        
        k_skor = QLabel(f"{kullanici.skor}")
        k_skor.setFont(QFont('Arial', 56, QFont.Bold))
        k_skor.setAlignment(Qt.AlignCenter)
        k_skor.setMinimumHeight(90)
        k_skor.setStyleSheet("color: #FFD700; background: transparent;")
        k_layout.addWidget(k_skor)
        
        k_skor_label = QLabel("PUAN")
        k_skor_label.setFont(QFont('Arial', 13))
        k_skor_label.setAlignment(Qt.AlignCenter)
        k_skor_label.setStyleSheet("color: #AAA; background: transparent;")
        k_skor_label.setMinimumHeight(25)
        k_layout.addWidget(k_skor_label)
        
        skor_layout.addWidget(k_frame)
        
        # VS ortası
        vs_label = QLabel("VS")
        vs_label.setFont(QFont('Arial', 32, QFont.Bold))
        vs_label.setAlignment(Qt.AlignCenter)
        vs_label.setStyleSheet("color: #FF5722;")
        vs_label.setMaximumWidth(80)
        skor_layout.addWidget(vs_label)
        
        # Bilgisayar Skor Kartı
        b_frame = QFrame()
        b_frame.setStyleSheet("""
            QFrame {
                background-color: #C62828;
                border: 2px solid #F44336;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        b_frame.setMinimumHeight(200)
        b_layout = QVBoxLayout(b_frame)
        b_layout.setSpacing(10)
        
        b_baslik = QLabel("🤖 BİLGİSAYAR")
        b_baslik.setFont(QFont('Arial', 16, QFont.Bold))
        b_baslik.setAlignment(Qt.AlignCenter)
        b_baslik.setStyleSheet("color: white; background: transparent;")
        b_baslik.setMinimumHeight(30)
        b_layout.addWidget(b_baslik)
        
        b_skor = QLabel(f"{bilgisayar.skor}")
        b_skor.setFont(QFont('Arial', 56, QFont.Bold))
        b_skor.setAlignment(Qt.AlignCenter)
        b_skor.setMinimumHeight(90)
        b_skor.setStyleSheet("color: #FFD700; background: transparent;")
        b_layout.addWidget(b_skor)
        
        b_skor_label = QLabel("PUAN")
        b_skor_label.setFont(QFont('Arial', 13))
        b_skor_label.setAlignment(Qt.AlignCenter)
        b_skor_label.setStyleSheet("color: #AAA; background: transparent;")
        b_skor_label.setMinimumHeight(25)
        b_layout.addWidget(b_skor_label)
        
        skor_layout.addWidget(b_frame)
        layout.addWidget(skor_frame)
        
        # ===== İSTATİSTİKLER =====
        istatistik_frame = QFrame()
        istatistik_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 2px solid #9C27B0;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        ist_layout = QHBoxLayout(istatistik_frame)
        
        # Kullanıcı istatistikleri
        k_ist = QLabel(f"""📊 KULLANICI İSTATİSTİKLERİ
─────────────────────────
🏆 Kazanılan Tur:   {kullanici.kazanilan_tur_sayisi}
😐 Beraberlik:       {kullanici.beraberlik_sayisi}
❌ Kayıp:            {kullanici.kayip_sayisi}
🔥 Max Seri:         {kullanici.max_galibiyet_serisi}
💪 Moral:            {kullanici.moral}
⚡ Kalan Enerji:     {kullanici.kalan_toplam_enerji()}
📋 Aktif Kart:       {len(kullanici.aktif_kartlari_al())}""")
        k_ist.setFont(QFont('Courier', 12))
        k_ist.setStyleSheet("color: #4CAF50; border: none;")
        ist_layout.addWidget(k_ist)
        
        # Bilgisayar istatistikleri
        b_ist = QLabel(f"""📊 BİLGİSAYAR İSTATİSTİKLERİ
─────────────────────────
🏆 Kazanılan Tur:   {bilgisayar.kazanilan_tur_sayisi}
😐 Beraberlik:       {bilgisayar.beraberlik_sayisi}
❌ Kayıp:            {bilgisayar.kayip_sayisi}
🔥 Max Seri:         {bilgisayar.max_galibiyet_serisi}
💪 Moral:            {bilgisayar.moral}
⚡ Kalan Enerji:     {bilgisayar.kalan_toplam_enerji()}
📋 Aktif Kart:       {len(bilgisayar.aktif_kartlari_al())}""")
        b_ist.setFont(QFont('Courier', 12))
        b_ist.setStyleSheet("color: #F44336; border: none;")
        ist_layout.addWidget(b_ist)
        
        layout.addWidget(istatistik_frame)
        
        # ===== KAZANMA DETAYI =====
        detay_label = QLabel(f"📋 Aşama {asama}: {detay}")
        detay_label.setFont(QFont('Arial', 12))
        detay_label.setAlignment(Qt.AlignCenter)
        detay_label.setWordWrap(True)
        detay_label.setStyleSheet("color: #9C27B0; background-color: #1a1a2e; padding: 10px; border: 1px solid #9C27B0; border-radius: 8px;")
        layout.addWidget(detay_label)
        
        # ===== YENİ OYUN BUTONU =====
        yeni_oyun_btn = QPushButton("🎮 Yeni Oyun Başlat")
        yeni_oyun_btn.setFont(QFont('Arial', 14, QFont.Bold))
        yeni_oyun_btn.setMinimumHeight(50)
        yeni_oyun_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {kazanan_renk};
                color: white;
                border-radius: 12px;
                border: none;
            }}
            QPushButton:hover {{ background-color: #FFD700; color: black; }}
        """)
        yeni_oyun_btn.clicked.connect(self.accept)
        layout.addWidget(yeni_oyun_btn)


class OyunArayuzu(QMainWindow):
    """Ana oyun penceresi"""
    
    def __init__(self):
        super().__init__()
        self.kullanici = None
        self.bilgisayar = None
        self.tur_yoneticisi = None
        self.mevcut_tur = 0
        self.oyun_aktif = False
        self.ozellik_secim_modu = "kullanici"  # Kullanıcı özellik seçsin
        self.mac_istatistik = MacIstatistik()  # Maç istatistikleri
        
        self.init_ui()
        self.oyunu_hazirla()
    
    def init_ui(self):
        self.setWindowTitle("🎮 Spor Kartları Oyunu")
        self.setGeometry(50, 50, 1600, 900)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #0f0f23; }
            QLabel { color: white; }
        """)
        
        # Merkezi widget
        central = QWidget()
        self.setCentralWidget(central)
        
        ana_layout = QHBoxLayout(central)
        ana_layout.setSpacing(20)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        
        # ========== SOL PANEL ==========
        sol_frame = QFrame()
        sol_frame.setStyleSheet("""
            QFrame { 
                background-color: #1a1a2e; 
                border: 2px solid #4CAF50; 
                border-radius: 10px; 
            }
        """)
        sol_frame.setMinimumWidth(300)
        sol_layout = QVBoxLayout(sol_frame)
        sol_layout.setSpacing(10)
        sol_layout.setContentsMargins(10, 10, 10, 10)
        
        # Kullanıcı başlık
        kullanici_baslik = QLabel("👤 KULLANICI")
        kullanici_baslik.setFont(QFont('Arial', 16, QFont.Bold))
        kullanici_baslik.setStyleSheet("color: #4CAF50; border: none;")
        kullanici_baslik.setAlignment(Qt.AlignCenter)
        sol_layout.addWidget(kullanici_baslik)
        
        # Kullanıcı skor
        self.kullanici_skor = QLabel("Skor: 0")
        self.kullanici_skor.setFont(QFont('Arial', 14, QFont.Bold))
        self.kullanici_skor.setStyleSheet("color: #FFD700; border: none;")
        self.kullanici_skor.setAlignment(Qt.AlignCenter)
        sol_layout.addWidget(self.kullanici_skor)
        
        # Kullanıcı moral
        self.kullanici_moral = QLabel("Moral: 70")
        self.kullanici_moral.setStyleSheet("color: white; border: none;")
        self.kullanici_moral.setAlignment(Qt.AlignCenter)
        sol_layout.addWidget(self.kullanici_moral)
        
        # Kartlar başlık
        kartlar_baslik = QLabel("📋 KARTLARIM")
        kartlar_baslik.setFont(QFont('Arial', 12, QFont.Bold))
        kartlar_baslik.setStyleSheet("color: #9C27B0; border: none; margin-top: 10px;")
        kartlar_baslik.setAlignment(Qt.AlignCenter)
        sol_layout.addWidget(kartlar_baslik)
        
        # Kullanıcı kart listesi
        self.kullanici_liste = QListWidget()
        self.kullanici_liste.setMinimumHeight(400)
        self.kullanici_liste.setStyleSheet("""
            QListWidget {
                background-color: #0f0f23;
                border: 1px solid #333;
                border-radius: 5px;
                color: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
            }
        """)
        sol_layout.addWidget(self.kullanici_liste)
        
        ana_layout.addWidget(sol_frame)
        
        # ========== ORTA PANEL ==========
        orta_frame = QFrame()
        orta_frame.setStyleSheet("""
            QFrame { 
                background-color: #1a1a2e; 
                border: 2px solid #FF9800; 
                border-radius: 10px; 
            }
        """)
        orta_layout = QVBoxLayout(orta_frame)
        orta_layout.setSpacing(15)
        orta_layout.setContentsMargins(20, 20, 20, 20)
        
        # Ana Başlık - Başlangıçta görünür
        self.ana_baslik = QLabel("🏆 SPORCU KART OYUNU 🏆")
        self.ana_baslik.setFont(QFont('Arial', 32, QFont.Bold))
        self.ana_baslik.setStyleSheet("color: #FFD700; border: none; padding: 20px;")
        self.ana_baslik.setAlignment(Qt.AlignCenter)
        orta_layout.addWidget(self.ana_baslik)
        
        # Hoşgeldiniz mesajı
        self.hosgeldin_mesaj = QLabel("Sporcu kartlarıyla heyecanlı bir mücadeleye hazır mısınız?\nOyunu başlatmak için aşağıdaki butona tıklayın!")
        self.hosgeldin_mesaj.setFont(QFont('Arial', 14))
        self.hosgeldin_mesaj.setStyleSheet("color: #AAA; border: none; padding: 10px;")
        self.hosgeldin_mesaj.setAlignment(Qt.AlignCenter)
        self.hosgeldin_mesaj.setWordWrap(True)
        orta_layout.addWidget(self.hosgeldin_mesaj)
        
        # Tur bilgisi - Başlangıçta gizli
        self.tur_label = QLabel("⚔️ KART SAVAŞI ⚔️")
        self.tur_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.tur_label.setStyleSheet("color: #FFD700; border: none;")
        self.tur_label.setAlignment(Qt.AlignCenter)
        self.tur_label.setVisible(False)
        orta_layout.addWidget(self.tur_label)
        
        self.brans_label = QLabel("Tur: 0 | Branş: -")
        self.brans_label.setFont(QFont('Arial', 14))
        self.brans_label.setStyleSheet("color: #9C27B0; border: none;")
        self.brans_label.setAlignment(Qt.AlignCenter)
        self.brans_label.setVisible(False)
        orta_layout.addWidget(self.brans_label)
        
        orta_layout.addStretch()
        
        # Karşılaştırma alanı - Başlangıçta gizli
        karsilastirma_layout = QHBoxLayout()
        self.karsilastirma_widget = QWidget()
        self.karsilastirma_widget.setLayout(karsilastirma_layout)
        self.karsilastirma_widget.setVisible(False)
        
        # Sol kart
        self.sol_kart_frame = QFrame()
        self.sol_kart_frame.setMinimumSize(200, 280)
        self.sol_kart_frame.setStyleSheet("""
            QFrame { 
                background-color: #2E7D32; 
                border: 3px solid #4CAF50; 
                border-radius: 15px; 
            }
        """)
        sol_kart_layout = QVBoxLayout(self.sol_kart_frame)
        
        self.sol_kart_ad = QLabel("Kart Bekleniyor")
        self.sol_kart_ad.setFont(QFont('Arial', 14, QFont.Bold))
        self.sol_kart_ad.setStyleSheet("color: white; border: none;")
        self.sol_kart_ad.setAlignment(Qt.AlignCenter)
        self.sol_kart_ad.setWordWrap(True)
        sol_kart_layout.addWidget(self.sol_kart_ad)
        
        self.sol_kart_brans = QLabel("")
        self.sol_kart_brans.setFont(QFont('Arial', 12))
        self.sol_kart_brans.setStyleSheet("color: #DDD; border: none;")
        self.sol_kart_brans.setAlignment(Qt.AlignCenter)
        sol_kart_layout.addWidget(self.sol_kart_brans)
        
        self.sol_kart_bilgi = QLabel("")
        self.sol_kart_bilgi.setStyleSheet("color: #AAA; border: none;")
        self.sol_kart_bilgi.setAlignment(Qt.AlignCenter)
        sol_kart_layout.addWidget(self.sol_kart_bilgi)
        
        karsilastirma_layout.addWidget(self.sol_kart_frame)
        
        # VS
        vs_label = QLabel("VS")
        vs_label.setFont(QFont('Arial', 32, QFont.Bold))
        vs_label.setStyleSheet("color: #FF5722; border: none;")
        vs_label.setAlignment(Qt.AlignCenter)
        karsilastirma_layout.addWidget(vs_label)
        
        # Sağ kart
        self.sag_kart_frame = QFrame()
        self.sag_kart_frame.setMinimumSize(200, 280)
        self.sag_kart_frame.setStyleSheet("""
            QFrame { 
                background-color: #C62828; 
                border: 3px solid #F44336; 
                border-radius: 15px; 
            }
        """)
        sag_kart_layout = QVBoxLayout(self.sag_kart_frame)
        
        self.sag_kart_ad = QLabel("Kart Bekleniyor")
        self.sag_kart_ad.setFont(QFont('Arial', 14, QFont.Bold))
        self.sag_kart_ad.setStyleSheet("color: white; border: none;")
        self.sag_kart_ad.setAlignment(Qt.AlignCenter)
        self.sag_kart_ad.setWordWrap(True)
        sag_kart_layout.addWidget(self.sag_kart_ad)
        
        self.sag_kart_brans = QLabel("")
        self.sag_kart_brans.setFont(QFont('Arial', 12))
        self.sag_kart_brans.setStyleSheet("color: #DDD; border: none;")
        self.sag_kart_brans.setAlignment(Qt.AlignCenter)
        sag_kart_layout.addWidget(self.sag_kart_brans)
        
        self.sag_kart_bilgi = QLabel("")
        self.sag_kart_bilgi.setStyleSheet("color: #AAA; border: none;")
        self.sag_kart_bilgi.setAlignment(Qt.AlignCenter)
        sag_kart_layout.addWidget(self.sag_kart_bilgi)
        
        karsilastirma_layout.addWidget(self.sag_kart_frame)
        
        orta_layout.addWidget(self.karsilastirma_widget)
        
        orta_layout.addStretch()
        
        # Sonuç - Başlangıçta gizli
        self.sonuc_label = QLabel("Oyunu başlatmak için butona tıklayın")
        self.sonuc_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.sonuc_label.setStyleSheet("""
            color: white; 
            background-color: #333; 
            padding: 15px; 
            border-radius: 10px;
            border: none;
        """)
        self.sonuc_label.setAlignment(Qt.AlignCenter)
        self.sonuc_label.setVisible(False)
        orta_layout.addWidget(self.sonuc_label)
        
        # Butonlar
        buton_layout = QHBoxLayout()
        
        self.baslat_btn = QPushButton("🎮 Oyunu Başlat")
        self.baslat_btn.setFont(QFont('Arial', 16, QFont.Bold))
        self.baslat_btn.setMinimumHeight(60)
        self.baslat_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #66BB6A; }
        """)
        self.baslat_btn.clicked.connect(self.oyunu_baslat)
        buton_layout.addWidget(self.baslat_btn)
        
        self.tur_btn = QPushButton("▶️ Tur Oyna")
        self.tur_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.tur_btn.setMinimumHeight(50)
        self.tur_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #42A5F5; }
            QPushButton:disabled { background-color: #555; }
        """)
        self.tur_btn.clicked.connect(self.tur_oyna)
        self.tur_btn.setEnabled(False)
        self.tur_btn.setVisible(False)
        buton_layout.addWidget(self.tur_btn)
        
        self.bitir_btn = QPushButton("🏁 Bitir")
        self.bitir_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.bitir_btn.setMinimumHeight(50)
        self.bitir_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #EF5350; }
            QPushButton:disabled { background-color: #555; }
        """)
        self.bitir_btn.clicked.connect(self.oyunu_bitir)
        self.bitir_btn.setEnabled(False)
        self.bitir_btn.setVisible(False)
        buton_layout.addWidget(self.bitir_btn)
        
        orta_layout.addLayout(buton_layout)
        
        # Özellik seçim modu göstergesi - Başlangıçta gizli
        self.mod_label = QLabel("🎯 Mod: Kullanıcı Seçimi (Kart + Özellik)")
        self.mod_label.setFont(QFont('Arial', 10))
        self.mod_label.setStyleSheet("color: #9C27B0; border: none;")
        self.mod_label.setAlignment(Qt.AlignCenter)
        self.mod_label.setVisible(False)
        orta_layout.addWidget(self.mod_label)
        
        ana_layout.addWidget(orta_frame)
        
        # ========== SAĞ PANEL ==========
        sag_frame = QFrame()
        sag_frame.setStyleSheet("""
            QFrame { 
                background-color: #1a1a2e; 
                border: 2px solid #F44336; 
                border-radius: 10px; 
            }
        """)
        sag_frame.setMinimumWidth(300)
        sag_layout = QVBoxLayout(sag_frame)
        sag_layout.setSpacing(10)
        sag_layout.setContentsMargins(10, 10, 10, 10)
        
        # Bilgisayar başlık
        bilgisayar_baslik = QLabel("🤖 BİLGİSAYAR")
        bilgisayar_baslik.setFont(QFont('Arial', 16, QFont.Bold))
        bilgisayar_baslik.setStyleSheet("color: #F44336; border: none;")
        bilgisayar_baslik.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(bilgisayar_baslik)
        
        # Bilgisayar skor
        self.bilgisayar_skor = QLabel("Skor: 0")
        self.bilgisayar_skor.setFont(QFont('Arial', 14, QFont.Bold))
        self.bilgisayar_skor.setStyleSheet("color: #FFD700; border: none;")
        self.bilgisayar_skor.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(self.bilgisayar_skor)
        
        # Bilgisayar moral
        self.bilgisayar_moral = QLabel("Moral: 70")
        self.bilgisayar_moral.setStyleSheet("color: white; border: none;")
        self.bilgisayar_moral.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(self.bilgisayar_moral)
        
        # Kartlar başlık
        kartlar_baslik2 = QLabel("📋 BİLGİSAYAR KARTLARI")
        kartlar_baslik2.setFont(QFont('Arial', 12, QFont.Bold))
        kartlar_baslik2.setStyleSheet("color: #9C27B0; border: none; margin-top: 10px;")
        kartlar_baslik2.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(kartlar_baslik2)
        
        # Bilgisayar kart listesi
        self.bilgisayar_liste = QListWidget()
        self.bilgisayar_liste.setMinimumHeight(400)
        self.bilgisayar_liste.setStyleSheet("""
            QListWidget {
                background-color: #0f0f23;
                border: 1px solid #333;
                border-radius: 5px;
                color: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #F44336;
            }
        """)
        sag_layout.addWidget(self.bilgisayar_liste)
        
        # Bilgisayar kartlarını göster/gizle butonu (test için)
        self.kart_goster_btn = QPushButton("👁️ Kartları Göster")
        self.kart_goster_btn.setFont(QFont('Arial', 10, QFont.Bold))
        self.kart_goster_btn.setMinimumHeight(35)
        self.kart_goster_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #AB47BC; }
        """)
        self.kart_goster_btn.clicked.connect(self.bilgisayar_kartlari_toggle)
        sag_layout.addWidget(self.kart_goster_btn)
        
        # Zorluk seviyesi seçimi
        zorluk_layout = QHBoxLayout()
        zorluk_label = QLabel("🎮 Zorluk:")
        zorluk_label.setStyleSheet("color: #FFD700; border: none;")
        zorluk_label.setFont(QFont('Arial', 10, QFont.Bold))
        zorluk_layout.addWidget(zorluk_label)
        
        self.zorluk_combo = QComboBox()
        self.zorluk_combo.addItems(["Kolay", "Orta", "Zor"])
        self.zorluk_combo.setCurrentIndex(0)  # Varsayılan: Kolay
        self.zorluk_combo.setStyleSheet("""
            QComboBox {
                background-color: #0f0f23;
                color: white;
                border: 1px solid #FF9800;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QComboBox:hover {
                border-color: #FFD700;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a2e;
                color: white;
                selection-background-color: #FF9800;
            }
        """)
        self.zorluk_combo.currentIndexChanged.connect(self.zorluk_degistir)
        zorluk_layout.addWidget(self.zorluk_combo)
        sag_layout.addLayout(zorluk_layout)
        
        # Strateji açıklaması
        self.strateji_aciklama = QLabel("📝 Rastgele kart seçer")
        self.strateji_aciklama.setStyleSheet("color: #888; border: none; font-size: 10px;")
        self.strateji_aciklama.setAlignment(Qt.AlignCenter)
        self.strateji_aciklama.setWordWrap(True)
        sag_layout.addWidget(self.strateji_aciklama)
        
        # Kartlar başlangıçta gizli
        self.bilgisayar_kartlari_gizli = True
        
        ana_layout.addWidget(sag_frame)
    
    def oyunu_hazirla(self):
        """Oyunu hazırla"""
        # Sporcuları yükle
        try:
            futbolcular, basketbolcular, voleybolcular = SporcuYonetimi.sporcu_olustur_dosyadan("sporcular.txt")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Hata", f"Dosya bulunamadı: {e}\nLütfen 'sporcular.txt' dosyasının mevcut olduğundan emin olun.")
            return
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Sporcu verileri yüklenirken hata oluştu:\n{e}")
            return
        
        # Sporcu verilerinin geçerliliğini kontrol et
        if not futbolcular and not basketbolcular and not voleybolcular:
            QMessageBox.warning(self, "Uyarı", "Hiç sporcu verisi bulunamadı!")
            return
        
        # Oyuncuları oluştur
        self.kullanici = Kullanici(1, "Kullanıcı")
        self.bilgisayar = Bilgisayar(2, "Bilgisayar")
        
        # Kartları hazırla ve dağıt
        tum_kartlar = KartDagitici.kartlari_hazirla(futbolcular, basketbolcular, voleybolcular)
        kullanici_kartlari, bilgisayar_kartlari = KartDagitici.kartlari_dagit(tum_kartlar)
        
        self.kullanici.kart_listesi = kullanici_kartlari
        self.bilgisayar.kart_listesi = bilgisayar_kartlari
        
        # Tur yöneticisi
        self.tur_yoneticisi = TurYoneticisi()
        
        # Kartları listele
        self.kartlari_listele()
        self.panelleri_guncelle()
    
    def kartlari_listele(self):
        """Kart listelerini güncelle - Güncel puanlarla ve özel yeteneklerle birlikte"""
        # Kullanıcı kartları
        self.kullanici_liste.clear()
        for kart in self.kullanici.kart_listesi:
            emoji = "⚽" if kart['brans'] == "Futbol" else "🏀" if kart['brans'] == "Basketbol" else "🏐"
            enerji = kart.get('enerji', 100)
            seviye = kart.get('seviye', 1)
            durum = "❌" if enerji <= 0 else "⚠️" if enerji < 20 else "✓"
            
            # Güncel puanı hesapla (branşın birincil özelliği için)
            sporcu = kart.get('sporcu_ref')
            guncel_puan_str = ""
            yetenek_str = ""
            if sporcu and self.tur_yoneticisi:
                birincil_ozellik = {"Futbol": "Penaltı", "Basketbol": "Üçlük", "Voleybol": "Servis"}.get(kart['brans'], "")
                if birincil_ozellik:
                    detay = self.tur_yoneticisi.puan_hesapla_detayli(sporcu, kart, birincil_ozellik, self.kullanici)
                    guncel_puan_str = f" | 📊{detay['guncel_puan']:.0f}"
                
                # Özel yetenek bilgisi
                if hasattr(sporcu, 'ozel_yetenek') and sporcu.ozel_yetenek:
                    yetenek_kisaltma = type(sporcu.ozel_yetenek).__name__[:3]
                    yetenek_str = f" | 🔷{yetenek_kisaltma}"
            
            metin = f"{emoji} {kart['ad']} | Sv:{seviye} | ⚡{enerji}{guncel_puan_str}{yetenek_str} {durum}"
            item = QListWidgetItem(metin)
            
            if enerji <= 0:
                item.setForeground(QColor("#666"))
            elif enerji < 20:
                item.setForeground(QColor("#FF9800"))
            else:
                item.setForeground(QColor("#FFF"))
            
            self.kullanici_liste.addItem(item)
        
        # Bilgisayar kartları
        self.bilgisayar_liste.clear()
        for kart in self.bilgisayar.kart_listesi:
            emoji = "⚽" if kart['brans'] == "Futbol" else "🏀" if kart['brans'] == "Basketbol" else "🏐"
            enerji = kart.get('enerji', 100)
            seviye = kart.get('seviye', 1)
            durum = "❌" if enerji <= 0 else "⚠️" if enerji < 20 else "✓"
            
            # Kartlar gizli ise sadece branş ve durum göster
            if self.bilgisayar_kartlari_gizli:
                metin = f"{emoji} ??? | Sv:? | ⚡? {durum}"
                item = QListWidgetItem(metin)
                item.setForeground(QColor("#666"))
            else:
                # Güncel puanı hesapla (branşın birincil özelliği için)
                sporcu = kart.get('sporcu_ref')
                guncel_puan_str = ""
                yetenek_str = ""
                if sporcu and self.tur_yoneticisi:
                    birincil_ozellik = {"Futbol": "Penaltı", "Basketbol": "Üçlük", "Voleybol": "Servis"}.get(kart['brans'], "")
                    if birincil_ozellik:
                        detay = self.tur_yoneticisi.puan_hesapla_detayli(sporcu, kart, birincil_ozellik, self.bilgisayar)
                        guncel_puan_str = f" | 📊{detay['guncel_puan']:.0f}"
                    
                    # Özel yetenek bilgisi
                    if hasattr(sporcu, 'ozel_yetenek') and sporcu.ozel_yetenek:
                        yetenek_kisaltma = type(sporcu.ozel_yetenek).__name__[:3]
                        yetenek_str = f" | 🔷{yetenek_kisaltma}"
                
                metin = f"{emoji} {kart['ad']} | Sv:{seviye} | ⚡{enerji}{guncel_puan_str}{yetenek_str} {durum}"
                item = QListWidgetItem(metin)
                
                if enerji <= 0:
                    item.setForeground(QColor("#666"))
                elif enerji < 20:
                    item.setForeground(QColor("#FF9800"))
                else:
                    item.setForeground(QColor("#FFF"))
            
            self.bilgisayar_liste.addItem(item)
    
    def bilgisayar_kartlari_toggle(self):
        """Bilgisayar kartlarını göster/gizle"""
        self.bilgisayar_kartlari_gizli = not self.bilgisayar_kartlari_gizli
        
        if self.bilgisayar_kartlari_gizli:
            self.kart_goster_btn.setText("👁️ Kartları Göster")
            self.kart_goster_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9C27B0;
                    color: white;
                    border-radius: 8px;
                    border: none;
                }
                QPushButton:hover { background-color: #AB47BC; }
            """)
        else:
            self.kart_goster_btn.setText("🔒 Kartları Gizle")
            self.kart_goster_btn.setStyleSheet("""
                QPushButton {
                    background-color: #E91E63;
                    color: white;
                    border-radius: 8px;
                    border: none;
                }
                QPushButton:hover { background-color: #F06292; }
            """)
        
        # Kart listesini güncelle
        self.kartlari_listele()
    
    def zorluk_degistir(self, index):
        """Zorluk seviyesini değiştir"""
        zorluklar = ["kolay", "orta", "zor"]
        aciklamalar = {
            "kolay": "📝 Rastgele kart seçer",
            "orta": "📝 En yüksek ortalama performanslı kartı seçer",
            "zor": "📝 En yüksek seviye ve enerjili kartı seçer"
        }
        if self.bilgisayar:
            self.bilgisayar.zorluk_ayarla(zorluklar[index])
            self.strateji_aciklama.setText(aciklamalar[zorluklar[index]])
            print(f"🎮 Zorluk seviyesi değiştirildi: {zorluklar[index].upper()}")
    
    def panelleri_guncelle(self):
        """Panelleri güncelle"""
        self.kullanici_skor.setText(f"Skor: {self.kullanici.skor}")
        seri_k = f"🔥{self.kullanici.galibiyet_serisi}" if self.kullanici.galibiyet_serisi >= 2 else ""
        self.kullanici_moral.setText(f"💪 Moral: {self.kullanici.moral} | 🏆 Kazanılan: {self.kullanici.kazanilan_tur_sayisi} {seri_k}")
        
        self.bilgisayar_skor.setText(f"Skor: {self.bilgisayar.skor}")
        seri_b = f"🔥{self.bilgisayar.galibiyet_serisi}" if self.bilgisayar.galibiyet_serisi >= 2 else ""
        self.bilgisayar_moral.setText(f"💪 Moral: {self.bilgisayar.moral} | 🏆 Kazanılan: {self.bilgisayar.kazanilan_tur_sayisi} {seri_b}")
    
    def ilk_kartlari_goster(self):
        """Oyun başladığında ilk kartları göster"""
        # Kullanıcının ilk aktif kartını bul
        kullanici_aktif = self.kullanici.aktif_kartlari_al()
        bilgisayar_aktif = self.bilgisayar.aktif_kartlari_al()
        
        if kullanici_aktif:
            kart = kullanici_aktif[0]
            self.sol_kart_ad.setText(kart.get('ad', '?'))
            brans = kart.get('brans', '?')
            emoji = "⚽" if brans == "Futbol" else "🏀" if brans == "Basketbol" else "🏐"
            self.sol_kart_brans.setText(f"{emoji} {brans}")
            self.sol_kart_bilgi.setText(f"Seviye: {kart.get('seviye', 1)}\nEnerji: {kart.get('enerji', 100)}")
        
        if bilgisayar_aktif:
            kart = bilgisayar_aktif[0]
            self.sag_kart_ad.setText(kart.get('ad', '?'))
            brans = kart.get('brans', '?')
            emoji = "⚽" if brans == "Futbol" else "🏀" if brans == "Basketbol" else "🏐"
            self.sag_kart_brans.setText(f"{emoji} {brans}")
            self.sag_kart_bilgi.setText(f"Seviye: {kart.get('seviye', 1)}\nEnerji: {kart.get('enerji', 100)}")
    
    def kart_goster(self, kart, taraf, secilen_ozellik=None):
        """Belirtilen kartı sol veya sağ tarafta göster - Güncel puanla birlikte"""
        if kart is None:
            return
            
        ad = kart.get('ad', '?')
        brans = kart.get('brans', '?')
        seviye = kart.get('seviye', 1)
        enerji = kart.get('enerji', 100)
        emoji = "⚽" if brans == "Futbol" else "🏀" if brans == "Basketbol" else "🏐"
        
        # Güncel puanı hesapla
        sporcu = kart.get('sporcu_ref')
        guncel_puan_str = ""
        
        if sporcu and self.tur_yoneticisi:
            # Seçilen özellik varsa onu kullan, yoksa birincil özelliği kullan
            ozellik = secilen_ozellik or {"Futbol": "Penaltı", "Basketbol": "Üçlük", "Voleybol": "Servis"}.get(brans, "")
            oyuncu = self.kullanici if taraf == 'sol' else self.bilgisayar
            if ozellik:
                detay = self.tur_yoneticisi.puan_hesapla_detayli(sporcu, kart, ozellik, oyuncu)
                guncel_puan_str = f"\n📊 Güncel Puan: {detay['guncel_puan']:.1f}"
        
        if taraf == 'sol':
            self.sol_kart_ad.setText(ad)
            self.sol_kart_brans.setText(f"{emoji} {brans}")
            self.sol_kart_bilgi.setText(f"Seviye: {seviye}\nEnerji: {enerji}{guncel_puan_str}")
        else:
            self.sag_kart_ad.setText(ad)
            self.sag_kart_brans.setText(f"{emoji} {brans}")
            self.sag_kart_bilgi.setText(f"Seviye: {seviye}\nEnerji: {enerji}{guncel_puan_str}")
    
    def oyunu_baslat(self):
        """Oyunu başlat - Önce zorluk seviyesi seçimi"""
        # Zorluk seçim dialogunu göster
        zorluk_dialog = ZorlukSecimDialog(self)
        if zorluk_dialog.exec_() != QDialog.Accepted:
            # Kullanıcı iptal ettiyse başlatma
            return
        
        # Seçilen zorluk seviyesini uygula
        secilen_zorluk = zorluk_dialog.secilen_zorluk
        if self.bilgisayar:
            self.bilgisayar.zorluk_ayarla(secilen_zorluk)
            
            # ComboBox'ı güncelle
            zorluk_index = {"kolay": 0, "orta": 1, "zor": 2}.get(secilen_zorluk, 0)
            self.zorluk_combo.setCurrentIndex(zorluk_index)
            
            # Strateji açıklamasını güncelle
            aciklamalar = {
                "kolay": "📝 Rastgele kart seçer",
                "orta": "📝 En yüksek ortalama performanslı kartı seçer",
                "zor": "📝 En yüksek seviye ve enerjili kartı seçer"
            }
            self.strateji_aciklama.setText(aciklamalar.get(secilen_zorluk, ""))
            
            print(f"🎮 Oyun başlatıldı - Zorluk: {secilen_zorluk.upper()}")
        
        self.oyun_aktif = True
        self.mevcut_tur = 0
        
        # Maç istatistiklerini sıfırla ve başlat
        self.mac_istatistik = MacIstatistik()
        self.mac_istatistik.mac_baslat()
        
        # Başlangıç ekranını gizle
        self.ana_baslik.setVisible(False)
        self.hosgeldin_mesaj.setVisible(False)
        self.baslat_btn.setVisible(False)
        
        # Oyun ekranını göster
        self.tur_label.setVisible(True)
        self.brans_label.setVisible(True)
        self.karsilastirma_widget.setVisible(True)
        self.sonuc_label.setVisible(True)
        self.tur_btn.setVisible(True)
        self.bitir_btn.setVisible(True)
        self.mod_label.setVisible(True)
        
        # Butonları güncelle
        self.tur_btn.setEnabled(True)
        self.bitir_btn.setEnabled(True)
        
        # Zorluk combo'yu devre dışı bırak (oyun başladıktan sonra değiştirilemez)
        self.zorluk_combo.setEnabled(False)
        
        # İlk kartları göster
        self.ilk_kartlari_goster()
        
        zorluk_mesaj = {"kolay": "Kolay 🎲", "orta": "Orta 📊", "zor": "Zor 🎯"}.get(secilen_zorluk, "")
        self.sonuc_label.setText(f"🎮 Oyun başladı! Zorluk: {zorluk_mesaj}\n'Tur Oyna' butonuna basın.")
        self.sonuc_label.setStyleSheet("""
            color: white;
            background-color: #4CAF50;
            padding: 15px;
            border-radius: 10px;
            border: none;
        """)
    
    def tur_oyna(self):
        """Bir tur oyna - Kullanıcı kart ve özellik seçer"""
        if not self.oyun_aktif:
            return
        
        mevcut_brans = self.tur_yoneticisi.mevcut_brans
        
        # Aktif kart kontrolü
        kullanici_aktif = self.kullanici.aktif_kartlari_al()
        bilgisayar_aktif = self.bilgisayar.aktif_kartlari_al()
        
        if len(kullanici_aktif) == 0 or len(bilgisayar_aktif) == 0:
            self.oyunu_bitir()
            return
        
        # Kullanıcının bu branştaki kartlarını al
        kullanici_brans_kartlari = [k for k in kullanici_aktif if k['brans'] == mevcut_brans and not k.get('oyundan_cikarildi', False) and k.get('enerji', 100) > 0]
        bilgisayar_brans_kartlari = [k for k in bilgisayar_aktif if k['brans'] == mevcut_brans and not k.get('oyundan_cikarildi', False) and k.get('enerji', 100) > 0]
        
        # Her iki tarafta da kart yoksa tur atla
        if not kullanici_brans_kartlari and not bilgisayar_brans_kartlari:
            self.mevcut_tur += 1
            self.brans_label.setText(f"Tur: {self.mevcut_tur} | Branş: {mevcut_brans}")
            self.sonuc_label.setText(f"⏭️ TUR {self.mevcut_tur}: Her iki tarafta da {mevcut_brans} kartı yok, tur atlandı!")
            self.sonuc_label.setStyleSheet("color: white; background-color: #9E9E9E; padding: 15px; border-radius: 10px; border: none;")
            self.tur_yoneticisi.sonraki_brans()
            return
        
        # Kullanıcının kartı yoksa bilgisayar hükmen kazanır
        if not kullanici_brans_kartlari:
            self.mevcut_tur += 1
            self.brans_label.setText(f"Tur: {self.mevcut_tur} | Branş: {mevcut_brans}")
            from oyuncu import Oyuncu
            hukmen_puan = Oyuncu.HUKMEN_GALIBIYET_PUAN
            self.bilgisayar.skor += hukmen_puan
            self.bilgisayar.kazanilan_tur_sayisi += 1
            self.bilgisayar.galibiyet_serisi += 1
            self.kullanici.galibiyet_serisi = 0
            self.sonuc_label.setText(f"💻 TUR {self.mevcut_tur}: {mevcut_brans} kartınız yok, Bilgisayar hükmen kazandı! (+{hukmen_puan})")
            self.sonuc_label.setStyleSheet("color: white; background-color: #F44336; padding: 15px; border-radius: 10px; border: none;")
            self.tur_yoneticisi.sonraki_brans()
            self.kartlari_listele()
            self.panelleri_guncelle()
            return
        
        # Bilgisayarın kartı yoksa kullanıcı hükmen kazanır
        if not bilgisayar_brans_kartlari:
            self.mevcut_tur += 1
            self.brans_label.setText(f"Tur: {self.mevcut_tur} | Branş: {mevcut_brans}")
            from oyuncu import Oyuncu
            hukmen_puan = Oyuncu.HUKMEN_GALIBIYET_PUAN
            self.kullanici.skor += hukmen_puan
            self.kullanici.kazanilan_tur_sayisi += 1
            self.kullanici.galibiyet_serisi += 1
            self.bilgisayar.galibiyet_serisi = 0
            self.sonuc_label.setText(f"🏆 TUR {self.mevcut_tur}: Bilgisayarın {mevcut_brans} kartı yok, Hükmen kazandınız! (+{hukmen_puan})")
            self.sonuc_label.setStyleSheet("color: white; background-color: #4CAF50; padding: 15px; border-radius: 10px; border: none;")
            self.tur_yoneticisi.sonraki_brans()
            self.kartlari_listele()
            self.panelleri_guncelle()
            return
        
        # ========== KULLANICI KART SEÇİMİ (Güncel Puanlarla) ==========
        kart_dialog = KartSecimDialog(
            kullanici_brans_kartlari, 
            mevcut_brans, 
            self,
            tur_yoneticisi=self.tur_yoneticisi,
            oyuncu_obj=self.kullanici
        )
        if kart_dialog.exec_() != QDialog.Accepted or kart_dialog.secilen_kart is None:
            QMessageBox.warning(self, "Uyarı", "Kart seçmelisiniz!")
            return
        
        kullanici_karti = kart_dialog.secilen_kart
        
        # ========== KULLANICI ÖZELLİK SEÇİMİ ==========
        ozellik_dialog = OzellikSecimDialog(mevcut_brans, self)
        if ozellik_dialog.exec_() != QDialog.Accepted or ozellik_dialog.secilen_ozellik is None:
            QMessageBox.warning(self, "Uyarı", "Özellik seçmelisiniz!")
            return
        
        secilen_ozellik = ozellik_dialog.secilen_ozellik
        
        # ========== BİLGİSAYAR KART SEÇİMİ ==========
        # Bilgisayar stratejisine göre kart seç
        bilgisayar_karti = self.bilgisayar.strateji.kart_sec(bilgisayar_brans_kartlari, mevcut_brans)
        
        if bilgisayar_karti is None:
            bilgisayar_karti = bilgisayar_brans_kartlari[0]
        
        self.mevcut_tur += 1
        self.brans_label.setText(f"Tur: {self.mevcut_tur} | Branş: {mevcut_brans} | Özellik: {secilen_ozellik}")
        
        # ========== PUAN HESAPLAMA (DETAYLI) ==========
        kullanici_sporcu = kullanici_karti.get('sporcu_ref')
        bilgisayar_sporcu = bilgisayar_karti.get('sporcu_ref')
        
        # Detaylı puan hesaplama
        kullanici_detay = self.tur_yoneticisi.puan_hesapla_detayli(
            kullanici_sporcu, kullanici_karti, secilen_ozellik, self.kullanici
        ) if kullanici_sporcu else {'temel_puan': 0, 'moral': 50, 'moral_bonusu': 0, 'ozel_yetenek_bonusu': 0, 'enerji': 0, 'enerji_cezasi': 0, 'seviye': 1, 'seviye_bonusu': 0, 'guncel_puan': 0}
        
        bilgisayar_detay = self.tur_yoneticisi.puan_hesapla_detayli(
            bilgisayar_sporcu, bilgisayar_karti, secilen_ozellik, self.bilgisayar
        ) if bilgisayar_sporcu else {'temel_puan': 0, 'moral': 50, 'moral_bonusu': 0, 'ozel_yetenek_bonusu': 0, 'enerji': 0, 'enerji_cezasi': 0, 'seviye': 1, 'seviye_bonusu': 0, 'guncel_puan': 0}
        
        kullanici_puan = kullanici_detay['guncel_puan']
        bilgisayar_puan = bilgisayar_detay['guncel_puan']
        
        # Kartları göster (seçilen özellikle birlikte güncel puanı göster)
        self.kart_goster(kullanici_karti, 'sol', secilen_ozellik)
        self.kart_goster(bilgisayar_karti, 'sag', secilen_ozellik)
        
        # ========== KAZANAN BELİRLE VE PUANLAMA ==========
        # Özel yetenek etkili mi kontrol et
        ozel_yetenek_etkili_k = kullanici_detay.get('ozel_yetenek_bonusu', 0) > 0
        ozel_yetenek_etkili_b = bilgisayar_detay.get('ozel_yetenek_bonusu', 0) > 0
        
        # Enerji durumlarını kaydet (bonus hesaplaması için - enerji güncellemeden ÖNCE)
        kullanici_enerji_onceki = kullanici_karti.get('enerji', 100)
        bilgisayar_enerji_onceki = bilgisayar_karti.get('enerji', 100)
        kullanici_seviye_onceki = kullanici_karti.get('seviye', 1)
        bilgisayar_seviye_onceki = bilgisayar_karti.get('seviye', 1)
        
        # Puan detayları için bonus listesi
        kullanici_bonus_detay = []
        bilgisayar_bonus_detay = []
        
        from oyuncu import Oyuncu
        
        if kullanici_puan > bilgisayar_puan:
            kazanan = 'oyuncu1'
            
            # --- KULLANICI KAZANDI: Puan hesapla ---
            # Normal mi yoksa özel yetenek etkili galibiyet mi?
            if ozel_yetenek_etkili_k:
                kazanilan_puan = Oyuncu.OZEL_YETENEK_GALIBIYET_PUAN
                kullanici_bonus_detay.append(f"⭐ Özel Yetenek Galibiyeti: +{Oyuncu.OZEL_YETENEK_GALIBIYET_PUAN}")
            else:
                kazanilan_puan = Oyuncu.NORMAL_GALIBIYET_PUAN
                kullanici_bonus_detay.append(f"🏆 Normal Galibiyet: +{Oyuncu.NORMAL_GALIBIYET_PUAN}")
            
            self.kullanici.kazanilan_tur_sayisi += 1
            self.kullanici.galibiyet_serisi += 1
            self.bilgisayar.galibiyet_serisi = 0
            
            # Galibiyet serisi bonusları
            if self.kullanici.galibiyet_serisi == 5:
                kazanilan_puan += Oyuncu.SERI_5_BONUS
                kullanici_bonus_detay.append(f"🔥 5 Galibiyet Serisi: +{Oyuncu.SERI_5_BONUS}")
            elif self.kullanici.galibiyet_serisi == 3:
                kazanilan_puan += Oyuncu.SERI_3_BONUS
                kullanici_bonus_detay.append(f"🔥 3 Galibiyet Serisi: +{Oyuncu.SERI_3_BONUS}")
            
            # Ek Bonus: Enerjisi 30 altında kartla kazanma
            if kullanici_enerji_onceki < 30:
                kazanilan_puan += Oyuncu.DUSUK_ENERJI_GALIBIYET_BONUS
                kullanici_bonus_detay.append(f"💪 Düşük Enerji Bonusu (<30): +{Oyuncu.DUSUK_ENERJI_GALIBIYET_BONUS}")
            
            # Ek Bonus: Seviye atladıktan sonraki ilk galibiyet
            kart_adi = kullanici_karti.get('ad', '')
            if kart_adi in self.kullanici.son_seviye_atlayan_kartlar:
                kazanilan_puan += Oyuncu.SEVIYE_ATLADI_GALIBIYET_BONUS
                kullanici_bonus_detay.append(f"📈 Seviye Atlama Bonusu: +{Oyuncu.SEVIYE_ATLADI_GALIBIYET_BONUS}")
                self.kullanici.son_seviye_atlayan_kartlar.discard(kart_adi)
            
            # Ek Bonus: Clutch Player yetenekli kartla kazanma (son 3 turda)
            sporcu_ref = kullanici_karti.get('sporcu_ref')
            if sporcu_ref and hasattr(sporcu_ref, 'ozel_yetenek') and sporcu_ref.ozel_yetenek == 'Clutch Player':
                kazanilan_puan += Oyuncu.CLUTCH_PLAYER_BONUS
                kullanici_bonus_detay.append(f"🎯 Clutch Player Bonusu: +{Oyuncu.CLUTCH_PLAYER_BONUS}")
            
            self.kullanici.skor += kazanilan_puan
            
            # Enerji güncelle (KartDagitici kullan)
            KartDagitici.kart_enerji_guncelle(kullanici_karti, 'kazandi', ozel_yetenek_etkili_k)
            KartDagitici.kart_enerji_guncelle(bilgisayar_karti, 'kaybetti')
            
            # Deneyim ve seviye güncelle
            k_deneyim = KartDagitici.kart_deneyim_ekle(kullanici_karti, 'kazandi')
            b_deneyim = KartDagitici.kart_deneyim_ekle(bilgisayar_karti, 'kaybetti')
            
            # Seviye atlama takibi
            if k_deneyim.get('seviye_atladi', False):
                self.kullanici.son_seviye_atlayan_kartlar.add(kullanici_karti.get('ad', ''))
                kullanici_bonus_detay.append(f"📈 SEVİYE ATLADI! → Seviye {k_deneyim['yeni_seviye']}")
            
            # Moral güncelle
            self.kullanici.moral_guncelle('kazandi', mevcut_brans, ozel_yetenek_etkili_k)
            self.bilgisayar.moral_guncelle('kaybetti', mevcut_brans)
            
            bonus_str = "\n".join(kullanici_bonus_detay)
            sonuc_mesaj = f"🏆 TUR {self.mevcut_tur}: Kazandınız! (+{kazanilan_puan} puan)\n{secilen_ozellik}: {kullanici_puan:.1f} vs {bilgisayar_puan:.1f}\n{bonus_str}"
            self.sonuc_label.setStyleSheet("color: white; background-color: #4CAF50; padding: 15px; border-radius: 10px; border: none;")
            
        elif bilgisayar_puan > kullanici_puan:
            kazanan = 'oyuncu2'
            
            # --- BİLGİSAYAR KAZANDI: Puan hesapla ---
            if ozel_yetenek_etkili_b:
                kazanilan_puan = Oyuncu.OZEL_YETENEK_GALIBIYET_PUAN
                bilgisayar_bonus_detay.append(f"⭐ Özel Yetenek Galibiyeti: +{Oyuncu.OZEL_YETENEK_GALIBIYET_PUAN}")
            else:
                kazanilan_puan = Oyuncu.NORMAL_GALIBIYET_PUAN
                bilgisayar_bonus_detay.append(f"🏆 Normal Galibiyet: +{Oyuncu.NORMAL_GALIBIYET_PUAN}")
            
            self.bilgisayar.kazanilan_tur_sayisi += 1
            self.bilgisayar.galibiyet_serisi += 1
            self.kullanici.galibiyet_serisi = 0
            
            # Galibiyet serisi bonusları
            if self.bilgisayar.galibiyet_serisi == 5:
                kazanilan_puan += Oyuncu.SERI_5_BONUS
                bilgisayar_bonus_detay.append(f"🔥 5 Galibiyet Serisi: +{Oyuncu.SERI_5_BONUS}")
            elif self.bilgisayar.galibiyet_serisi == 3:
                kazanilan_puan += Oyuncu.SERI_3_BONUS
                bilgisayar_bonus_detay.append(f"🔥 3 Galibiyet Serisi: +{Oyuncu.SERI_3_BONUS}")
            
            # Ek Bonus: Enerjisi 30 altında kartla kazanma
            if bilgisayar_enerji_onceki < 30:
                kazanilan_puan += Oyuncu.DUSUK_ENERJI_GALIBIYET_BONUS
                bilgisayar_bonus_detay.append(f"💪 Düşük Enerji Bonusu (<30): +{Oyuncu.DUSUK_ENERJI_GALIBIYET_BONUS}")
            
            self.bilgisayar.skor += kazanilan_puan
            
            # Enerji güncelle
            KartDagitici.kart_enerji_guncelle(kullanici_karti, 'kaybetti')
            KartDagitici.kart_enerji_guncelle(bilgisayar_karti, 'kazandi', ozel_yetenek_etkili_b)
            
            # Deneyim ve seviye güncelle
            k_deneyim = KartDagitici.kart_deneyim_ekle(kullanici_karti, 'kaybetti')
            b_deneyim = KartDagitici.kart_deneyim_ekle(bilgisayar_karti, 'kazandi')
            
            # Moral güncelle
            self.kullanici.moral_guncelle('kaybetti', mevcut_brans)
            self.bilgisayar.moral_guncelle('kazandi', mevcut_brans, ozel_yetenek_etkili_b)
            
            bonus_str = "\n".join(bilgisayar_bonus_detay)
            sonuc_mesaj = f"💻 TUR {self.mevcut_tur}: Bilgisayar kazandı! (+{kazanilan_puan} puan)\n{secilen_ozellik}: {kullanici_puan:.1f} vs {bilgisayar_puan:.1f}\n{bonus_str}"
            self.sonuc_label.setStyleSheet("color: white; background-color: #F44336; padding: 15px; border-radius: 10px; border: none;")
            
        else:
            kazanan = 'berabere'
            
            # Beraberlik: 0 puan, seri sıfırlanır
            self.kullanici.galibiyet_serisi = 0
            self.bilgisayar.galibiyet_serisi = 0
            
            # Enerji güncelle
            KartDagitici.kart_enerji_guncelle(kullanici_karti, 'berabere')
            KartDagitici.kart_enerji_guncelle(bilgisayar_karti, 'berabere')
            
            # Deneyim güncelle
            KartDagitici.kart_deneyim_ekle(kullanici_karti, 'berabere')
            KartDagitici.kart_deneyim_ekle(bilgisayar_karti, 'berabere')
            
            # Moral güncelle
            self.kullanici.moral_guncelle('berabere', mevcut_brans)
            self.bilgisayar.moral_guncelle('berabere', mevcut_brans)
            
            sonuc_mesaj = f"🤝 TUR {self.mevcut_tur}: Berabere! (0 puan)\n{secilen_ozellik}: {kullanici_puan:.1f} vs {bilgisayar_puan:.1f}"
            self.sonuc_label.setStyleSheet("color: white; background-color: #FF9800; padding: 15px; border-radius: 10px; border: none;")
        
        self.sonuc_label.setText(sonuc_mesaj)
        
        # ========== MAÇ İSTATİSTİKLERİNİ KAYDET ==========
        # Tur sonucunu kaydet
        kazanan_str = 'kullanici' if kazanan == 'oyuncu1' else 'bilgisayar' if kazanan == 'oyuncu2' else 'berabere'
        self.mac_istatistik.tur_kaydet(
            tur_no=self.mevcut_tur,
            brans=mevcut_brans,
            ozellik=secilen_ozellik,
            kullanici_kart=kullanici_karti,
            bilgisayar_kart=bilgisayar_karti,
            kullanici_puan=kullanici_puan,
            bilgisayar_puan=bilgisayar_puan,
            kazanan=kazanan_str,
            kazanilan_puan=kazanilan_puan if kazanan != 'berabere' else 0
        )
        
        # Özel yetenek galibiyetini kaydet
        if kazanan == 'oyuncu1' and ozel_yetenek_etkili_k:
            self.mac_istatistik.ozel_yetenek_galibiyet_kaydet('kullanici')
        elif kazanan == 'oyuncu2' and ozel_yetenek_etkili_b:
            self.mac_istatistik.ozel_yetenek_galibiyet_kaydet('bilgisayar')
        
        # Max serileri güncelle
        self.mac_istatistik.max_seri_guncelle(
            self.kullanici.galibiyet_serisi,
            self.bilgisayar.galibiyet_serisi
        )
        
        # ========== PUAN DETAY DİALOG GÖSTER ==========
        # Bonus detaylarını da dialog'a ekle
        kullanici_detay['bonus_detay'] = kullanici_bonus_detay if kazanan == 'oyuncu1' else []
        bilgisayar_detay['bonus_detay'] = bilgisayar_bonus_detay if kazanan == 'oyuncu2' else []
        
        detay_dialog = PuanDetayDialog(kullanici_detay, bilgisayar_detay, secilen_ozellik, kazanan, self)
        detay_dialog.exec_()
        
        # Enerjisi biten kartları işaretle (kart_enerji_guncelle zaten bunu yapıyor ama garanti olsun)
        if kullanici_karti.get('enerji', 0) <= 0:
            kullanici_karti['oyundan_cikarildi'] = True
        if bilgisayar_karti.get('enerji', 0) <= 0:
            bilgisayar_karti['oyundan_cikarildi'] = True
        
        # Sonraki branşa geç
        self.tur_yoneticisi.sonraki_brans()
        
        # Güncelle
        self.kartlari_listele()
        self.panelleri_guncelle()
        
        # Max tur kontrolü
        if self.mevcut_tur >= 15:
            self.oyunu_bitir()
    
    def oyunu_bitir(self):
        """Oyunu bitir"""
        self.oyun_aktif = False
        
        # Oyun ekranını gizle
        self.tur_label.setVisible(False)
        self.brans_label.setVisible(False)
        self.karsilastirma_widget.setVisible(False)
        self.sonuc_label.setVisible(False)
        self.tur_btn.setVisible(False)
        self.bitir_btn.setVisible(False)
        self.mod_label.setVisible(False)
        
        # Zorluk combo'yu tekrar aktif et (yeni oyun için)
        self.zorluk_combo.setEnabled(True)
        
        # Başlangıç ekranını göster
        self.ana_baslik.setVisible(True)
        self.hosgeldin_mesaj.setVisible(True)
        self.baslat_btn.setVisible(True)
        self.baslat_btn.setEnabled(True)
        
        # Kazananı belirle (dict döndürüyor)
        sonuc = self.tur_yoneticisi.oyun_sonu_kazanani_belirle(
            self.kullanici, self.bilgisayar
        )
        
        kazanan = sonuc['kazanan']
        asama = sonuc['asama']
        detay = sonuc['aciklama']
        
        # İstatistikleri güncelle (max seri)
        if self.kullanici.galibiyet_serisi > self.kullanici.max_galibiyet_serisi:
            self.kullanici.max_galibiyet_serisi = self.kullanici.galibiyet_serisi
        if self.bilgisayar.galibiyet_serisi > self.bilgisayar.max_galibiyet_serisi:
            self.bilgisayar.max_galibiyet_serisi = self.bilgisayar.galibiyet_serisi
        
        # ========== MAÇ İSTATİSTİKLERİNİ TAMAMLA ==========
        # Kazananı belirle ve maç istatistiklerini bitir
        kazanan_str = 'kullanici' if kazanan == self.kullanici else 'bilgisayar' if kazanan == self.bilgisayar else 'berabere'
        self.mac_istatistik.mac_bitir(kazanan_str, asama, detay)
        
        # Raporu konsola yazdır
        print(self.mac_istatistik.rapor_olustur())
        print(self.mac_istatistik.tur_gecmisi_raporu())
        
        # Sonuç label güncelle
        if kazanan == self.kullanici:
            self.sonuc_label.setText("🏆 KULLANICI KAZANDI!")
            self.sonuc_label.setStyleSheet("color: white; background-color: #4CAF50; padding: 15px; border-radius: 10px; border: none;")
        elif kazanan == self.bilgisayar:
            self.sonuc_label.setText("💻 BİLGİSAYAR KAZANDI!")
            self.sonuc_label.setStyleSheet("color: white; background-color: #F44336; padding: 15px; border-radius: 10px; border: none;")
        else:
            self.sonuc_label.setText("🤝 BERABERE!")
            self.sonuc_label.setStyleSheet("color: white; background-color: #FF9800; padding: 15px; border-radius: 10px; border: none;")
        
        # Büyük sonuç dialogunu göster
        sonuc_dialog = OyunSonucDialog(
            self.kullanici, self.bilgisayar,
            kazanan, asama, detay, self
        )
        sonuc_dialog.exec_()
        
        # Yeni oyun için hazırla
        self.oyunu_hazirla()


def oyun_arayuzu_baslat():
    """Oyun arayüzünü başlat"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = OyunArayuzu()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    oyun_arayuzu_baslat()
