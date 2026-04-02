"""
PyQt5 ile Kart Karşılaştırma Arayüzü
İki kartı yan yana gösterir ve özelliklerini karşılaştırır
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QProgressBar, QGridLayout, QPushButton,
    QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter


class KartWidget(QFrame):
    """Tek bir kartı gösteren widget"""
    
    # Branş renkleri
    BRANS_RENKLERI = {
        'Futbol': ('#2E7D32', '#4CAF50'),      # Yeşil
        'Basketbol': ('#E65100', '#FF9800'),   # Turuncu
        'Voleybol': ('#1565C0', '#2196F3'),    # Mavi
    }
    
    def __init__(self, kart_data=None, oyuncu_adi="Oyuncu", parent=None):
        super().__init__(parent)
        self.kart_data = kart_data
        self.oyuncu_adi = oyuncu_adi
        self.init_ui()
        
    def init_ui(self):
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(3)
        self.setMinimumSize(320, 500)
        self.setMaximumWidth(400)
        
        # Ana layout
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Oyuncu adı başlığı
        self.oyuncu_label = QLabel(self.oyuncu_adi)
        self.oyuncu_label.setAlignment(Qt.AlignCenter)
        self.oyuncu_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.oyuncu_label.setStyleSheet("""
            QLabel {
                background-color: #333;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.oyuncu_label)
        
        if self.kart_data:
            self._kart_icerigi_olustur(layout)
        else:
            self._bos_kart_goster(layout)
    
    def _kart_icerigi_olustur(self, layout):
        """Kart içeriğini oluştur"""
        brans = self.kart_data.get('brans', 'Futbol')
        renkler = self.BRANS_RENKLERI.get(brans, ('#555', '#777'))
        
        # Kart arka plan stili
        self.setStyleSheet(f"""
            KartWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {renkler[0]}, stop:1 {renkler[1]}
                );
                border-radius: 15px;
                border: 3px solid #333;
            }}
        """)
        
        # Sporcu adı
        ad_label = QLabel(self.kart_data.get('ad', 'Bilinmeyen'))
        ad_label.setAlignment(Qt.AlignCenter)
        ad_label.setFont(QFont('Arial', 18, QFont.Bold))
        ad_label.setStyleSheet("color: white; padding: 5px;")
        layout.addWidget(ad_label)
        
        # Takım adı
        takim_label = QLabel(f"🏟️ {self.kart_data.get('takim', 'Bilinmeyen Takım')}")
        takim_label.setAlignment(Qt.AlignCenter)
        takim_label.setFont(QFont('Arial', 12))
        takim_label.setStyleSheet("color: #DDD; padding: 3px;")
        layout.addWidget(takim_label)
        
        # Branş etiketi
        brans_label = QLabel(f"⚽ {brans}" if brans == 'Futbol' else 
                            f"🏀 {brans}" if brans == 'Basketbol' else f"🏐 {brans}")
        brans_label.setAlignment(Qt.AlignCenter)
        brans_label.setFont(QFont('Arial', 14, QFont.Bold))
        brans_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 0.3);
            padding: 5px 15px;
            border-radius: 10px;
        """)
        layout.addWidget(brans_label)
        
        layout.addSpacing(10)
        
        # Temel bilgiler kutusu
        temel_group = self._grup_olustur("📊 Temel Bilgiler")
        temel_layout = QGridLayout()
        
        # Seviye
        temel_layout.addWidget(self._bilgi_etiketi("Seviye:"), 0, 0)
        temel_layout.addWidget(self._deger_etiketi(str(self.kart_data.get('seviye', 1)), "#FFD700"), 0, 1)
        
        # Deneyim
        temel_layout.addWidget(self._bilgi_etiketi("Deneyim:"), 1, 0)
        temel_layout.addWidget(self._deger_etiketi(str(self.kart_data.get('deneyim', 0)), "#9C27B0"), 1, 1)
        
        temel_group.setLayout(temel_layout)
        layout.addWidget(temel_group)
        
        # Enerji barı
        enerji_group = self._grup_olustur("⚡ Enerji")
        enerji_layout = QVBoxLayout()
        
        enerji = self.kart_data.get('enerji', 100)
        max_enerji = self.kart_data.get('max_enerji', 100)
        
        enerji_bar = QProgressBar()
        enerji_bar.setRange(0, max_enerji)
        enerji_bar.setValue(enerji)
        enerji_bar.setTextVisible(True)
        enerji_bar.setFormat(f"{enerji}/{max_enerji}")
        
        # Enerji durumuna göre renk
        if enerji < 20:
            bar_renk = "#F44336"  # Kırmızı
        elif enerji < 50:
            bar_renk = "#FF9800"  # Turuncu
        else:
            bar_renk = "#4CAF50"  # Yeşil
            
        enerji_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #333;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                background-color: #333;
                height: 25px;
            }}
            QProgressBar::chunk {{
                background-color: {bar_renk};
                border-radius: 6px;
            }}
        """)
        enerji_layout.addWidget(enerji_bar)
        enerji_group.setLayout(enerji_layout)
        layout.addWidget(enerji_group)
        
        # Branş özellikleri
        ozellik_group = self._grup_olustur("🎯 Branş Özellikleri")
        ozellik_layout = QGridLayout()
        
        ozellikler = self._brans_ozelliklerini_al()
        for i, (ozellik_adi, ozellik_degeri) in enumerate(ozellikler):
            ozellik_layout.addWidget(self._bilgi_etiketi(f"{ozellik_adi}:"), i, 0)
            ozellik_layout.addWidget(self._deger_etiketi(str(ozellik_degeri), "#2196F3"), i, 1)
            
            # Özellik barı
            ozellik_bar = QProgressBar()
            ozellik_bar.setRange(0, 100)
            ozellik_bar.setValue(min(int(float(ozellik_degeri)), 100))
            ozellik_bar.setTextVisible(False)
            ozellik_bar.setMaximumHeight(10)
            ozellik_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: #333;
                }
                QProgressBar::chunk {
                    background-color: #2196F3;
                    border-radius: 3px;
                }
            """)
            ozellik_layout.addWidget(ozellik_bar, i, 2)
        
        ozellik_group.setLayout(ozellik_layout)
        layout.addWidget(ozellik_group)
        
        # Dayanıklılık ve Özel Yetenek
        ekstra_group = self._grup_olustur("💪 Ekstra")
        ekstra_layout = QGridLayout()
        
        ekstra_layout.addWidget(self._bilgi_etiketi("Dayanıklılık:"), 0, 0)
        ekstra_layout.addWidget(self._deger_etiketi(
            str(self.kart_data.get('dayaniklilik', 80)), "#E91E63"), 0, 1)
        
        ekstra_layout.addWidget(self._bilgi_etiketi("Özel Yetenek:"), 1, 0)
        ekstra_layout.addWidget(self._deger_etiketi(
            str(self.kart_data.get('ozel_yetenek_katsayisi', 1.0)), "#9C27B0"), 1, 1)
        
        ekstra_group.setLayout(ekstra_layout)
        layout.addWidget(ekstra_group)
        
        layout.addStretch()
    
    def _brans_ozelliklerini_al(self):
        """Branşa özgü özellikleri döndür"""
        brans = self.kart_data.get('brans', '')
        
        if brans == 'Futbol':
            return [
                ('Penaltı', self.kart_data.get('penalti', 0)),
                ('Serbest Vuruş', self.kart_data.get('serbest_vurus', 0)),
                ('Kaleci K.K.', self.kart_data.get('kaleci_kk', 0)),
            ]
        elif brans == 'Basketbol':
            return [
                ('Üçlük', self.kart_data.get('ucluk', 0)),
                ('İkilik', self.kart_data.get('ikilik', 0)),
                ('Serbest Atış', self.kart_data.get('serbest_atis', 0)),
            ]
        elif brans == 'Voleybol':
            return [
                ('Servis', self.kart_data.get('servis', 0)),
                ('Blok', self.kart_data.get('blok', 0)),
                ('Smaç', self.kart_data.get('smac', 0)),
            ]
        return []
    
    def _grup_olustur(self, baslik):
        """Stilize edilmiş grup kutusu oluştur"""
        group = QGroupBox(baslik)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: rgba(0, 0, 0, 0.2);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        return group
    
    def _bilgi_etiketi(self, text):
        """Bilgi etiketi oluştur"""
        label = QLabel(text)
        label.setStyleSheet("color: #DDD; font-size: 11px;")
        return label
    
    def _deger_etiketi(self, text, renk="#FFF"):
        """Değer etiketi oluştur"""
        label = QLabel(text)
        label.setStyleSheet(f"color: {renk}; font-weight: bold; font-size: 13px;")
        label.setAlignment(Qt.AlignRight)
        return label
    
    def _bos_kart_goster(self, layout):
        """Boş kart göster"""
        self.setStyleSheet("""
            KartWidget {
                background-color: #555;
                border-radius: 15px;
                border: 3px dashed #888;
            }
        """)
        
        bos_label = QLabel("❓\nKart Yok")
        bos_label.setAlignment(Qt.AlignCenter)
        bos_label.setFont(QFont('Arial', 24))
        bos_label.setStyleSheet("color: #888;")
        layout.addWidget(bos_label)
        layout.addStretch()
    
    def kart_guncelle(self, kart_data, oyuncu_adi=None):
        """Kartı güncelle"""
        self.kart_data = kart_data
        if oyuncu_adi:
            self.oyuncu_adi = oyuncu_adi
        
        # Mevcut layout'u temizle
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Yeniden oluştur
        self.oyuncu_label = QLabel(self.oyuncu_adi)
        self.oyuncu_label.setAlignment(Qt.AlignCenter)
        self.oyuncu_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.oyuncu_label.setStyleSheet("""
            QLabel {
                background-color: #333;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)
        self.layout().addWidget(self.oyuncu_label)
        
        if self.kart_data:
            self._kart_icerigi_olustur(self.layout())
        else:
            self._bos_kart_goster(self.layout())


class KarsilastirmaWidget(QWidget):
    """İki kartı karşılaştırma widget'ı"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Başlık
        baslik = QLabel("⚔️ KART KARŞILAŞTIRMA ⚔️")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setFont(QFont('Arial', 24, QFont.Bold))
        baslik.setStyleSheet("""
            color: #FFD700;
            padding: 15px;
            background-color: #1a1a2e;
            border-radius: 10px;
            margin-bottom: 10px;
        """)
        layout.addWidget(baslik)
        
        # Kartlar için horizontal layout
        kartlar_layout = QHBoxLayout()
        kartlar_layout.setSpacing(30)
        
        # Sol kart (Kullanıcı)
        self.sol_kart = KartWidget(oyuncu_adi="👤 Kullanıcı")
        kartlar_layout.addWidget(self.sol_kart)
        
        # VS etiketi
        vs_label = QLabel("VS")
        vs_label.setAlignment(Qt.AlignCenter)
        vs_label.setFont(QFont('Arial', 36, QFont.Bold))
        vs_label.setStyleSheet("""
            color: #FF5722;
            background-color: #1a1a2e;
            padding: 20px;
            border-radius: 50px;
            min-width: 80px;
            min-height: 80px;
        """)
        vs_label.setFixedSize(100, 100)
        kartlar_layout.addWidget(vs_label)
        
        # Sağ kart (Bilgisayar)
        self.sag_kart = KartWidget(oyuncu_adi="🤖 Bilgisayar")
        kartlar_layout.addWidget(self.sag_kart)
        
        layout.addLayout(kartlar_layout)
        
        # Sonuç paneli
        self.sonuc_label = QLabel("")
        self.sonuc_label.setAlignment(Qt.AlignCenter)
        self.sonuc_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.sonuc_label.setStyleSheet("""
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        """)
        self.sonuc_label.hide()
        layout.addWidget(self.sonuc_label)
    
    def kartlari_goster(self, kart1_data, kart2_data, oyuncu1_adi="Kullanıcı", oyuncu2_adi="Bilgisayar"):
        """İki kartı göster"""
        self.sol_kart.kart_guncelle(kart1_data, f"👤 {oyuncu1_adi}")
        self.sag_kart.kart_guncelle(kart2_data, f"🤖 {oyuncu2_adi}")
    
    def sonuc_goster(self, kazanan, mesaj=""):
        """Karşılaştırma sonucunu göster"""
        self.sonuc_label.show()
        
        if kazanan == "oyuncu1":
            self.sonuc_label.setText(f"🏆 KULLANICI KAZANDI! {mesaj}")
            self.sonuc_label.setStyleSheet("""
                color: white;
                background-color: #4CAF50;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
            """)
        elif kazanan == "oyuncu2":
            self.sonuc_label.setText(f"💻 BİLGİSAYAR KAZANDI! {mesaj}")
            self.sonuc_label.setStyleSheet("""
                color: white;
                background-color: #F44336;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
            """)
        else:
            self.sonuc_label.setText(f"🤝 BERABERE! {mesaj}")
            self.sonuc_label.setStyleSheet("""
                color: white;
                background-color: #FF9800;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
            """)


class KartKarsilastirmaWindow(QMainWindow):
    """Ana pencere"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("🎮 Spor Kartları Karşılaştırma")
        self.setMinimumSize(900, 700)
        
        # Arka plan rengi
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f23;
            }
        """)
        
        # Merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Karşılaştırma widget'ı
        self.karsilastirma = KarsilastirmaWidget()
        layout.addWidget(self.karsilastirma)
        
        # Butonlar
        buton_layout = QHBoxLayout()
        
        self.demo_btn = QPushButton("🎲 Demo Kartları Göster")
        self.demo_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.demo_btn.setStyleSheet("""
            QPushButton {
                background-color: #673AB7;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7C4DFF;
            }
            QPushButton:pressed {
                background-color: #512DA8;
            }
        """)
        self.demo_btn.clicked.connect(self.demo_kartlari_goster)
        buton_layout.addWidget(self.demo_btn)
        
        self.karsilastir_btn = QPushButton("⚔️ Karşılaştır")
        self.karsilastir_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.karsilastir_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF7043;
            }
            QPushButton:pressed {
                background-color: #E64A19;
            }
        """)
        self.karsilastir_btn.clicked.connect(self.karsilastir)
        buton_layout.addWidget(self.karsilastir_btn)
        
        layout.addLayout(buton_layout)
        
        # İlk demo kartlarını göster
        self.demo_kartlari_goster()
    
    def demo_kartlari_goster(self):
        """Demo kartlarını göster"""
        kart1 = {
            'ad': 'Mehmet Yıldız',
            'takim': 'Galatasaray',
            'brans': 'Futbol',
            'seviye': 2,
            'deneyim': 850,
            'enerji': 85,
            'max_enerji': 100,
            'penalti': 92,
            'serbest_vurus': 88,
            'kaleci_kk': 85,
            'dayaniklilik': 80,
            'ozel_yetenek_katsayisi': 1.15
        }
        
        kart2 = {
            'ad': 'Kerem Aydın',
            'takim': 'Fenerbahçe Alagöz',
            'brans': 'Basketbol',
            'seviye': 3,
            'deneyim': 890,
            'enerji': 70,
            'max_enerji': 100,
            'ucluk': 94,
            'ikilik': 91,
            'serbest_atis': 88,
            'dayaniklilik': 85,
            'ozel_yetenek_katsayisi': 1.20
        }
        
        self.karsilastirma.kartlari_goster(kart1, kart2)
        self.karsilastirma.sonuc_label.hide()
    
    def karsilastir(self):
        """Kartları karşılaştır ve sonucu göster"""
        import random
        kazananlar = ["oyuncu1", "oyuncu2", "berabere"]
        mesajlar = [
            "Penaltı özelliği ile!",
            "Üçlük atışı ile!",
            "Dayanıklılık farkı ile!",
            "Özel yetenek bonusu ile!"
        ]
        
        kazanan = random.choice(kazananlar)
        mesaj = random.choice(mesajlar)
        
        self.karsilastirma.sonuc_goster(kazanan, mesaj)


def kart_dict_olustur(sporcu):
    """Sporcu nesnesinden kart dictionary'si oluştur"""
    kart = {
        'ad': sporcu.sporcu_adi,
        'takim': sporcu.takim_adi,
        'brans': sporcu.brans,
        'seviye': sporcu.seviye,
        'deneyim': sporcu.deneyim_puani,
        'enerji': sporcu.enerji,
        'max_enerji': sporcu.max_enerji,
        'dayaniklilik': sporcu.dayaniklilik,
        'ozel_yetenek_katsayisi': getattr(sporcu, 'ozel_yetenek_katsayisi', 1.0)
    }
    
    # Branşa özgü özellikler
    if sporcu.brans == 'Futbol':
        kart['penalti'] = getattr(sporcu, 'penalti', 0)
        kart['serbest_vurus'] = getattr(sporcu, 'serbestturus', 0)
        kart['kaleci_kk'] = getattr(sporcu, 'kaleci_karsikarsiya', 0)
    elif sporcu.brans == 'Basketbol':
        kart['ucluk'] = getattr(sporcu, 'ucluk', 0)
        kart['ikilik'] = getattr(sporcu, 'ikilik', 0)
        kart['serbest_atis'] = getattr(sporcu, 'serbest_atis', 0)
    elif sporcu.brans == 'Voleybol':
        kart['servis'] = getattr(sporcu, 'servis', 0)
        kart['blok'] = getattr(sporcu, 'blok', 0)
        kart['smac'] = getattr(sporcu, 'smac', 0)
    
    return kart


def arayuz_baslat():
    """Arayüzü başlat"""
    app = QApplication(sys.argv)
    
    # Koyu tema
    app.setStyle('Fusion')
    
    window = KartKarsilastirmaWindow()
    window.show()
    
    sys.exit(app.exec_())


# Test için doğrudan çalıştırma
if __name__ == "__main__":
    arayuz_baslat()
