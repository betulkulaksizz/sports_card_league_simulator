from sporcu import Sporcu


class Voleybolcu(Sporcu):
    def __init__(self):
        super().__init__()
        # Voleybolcu Özellikleri
        self.servis = None                 # Servis
        self.blok = None                   # Blok
        self.smac = None                   # Smac
        self.dayaniklilik = None           # Dayanıklılık
        self.ozel_yetenek_katsayisi = None # OzelYetenekKatsayisi (eski, uyum için)
        self.ozel_yetenek = None           # Özel Yetenek (OzelYetenek nesnesi)
