from sporcu import Sporcu


class Basketbolcu(Sporcu):
    def __init__(self):
        super().__init__()
        # Basketbolcu Özellikleri
        self.ucluk = None                  # Ucluk
        self.ikilik = None                 # Ikilik
        self.serbest_atis = None           # SerbestAtis
        self.dayaniklilik = None           # Dayanıklılık
        self.ozel_yetenek_katsayisi = None # OzelYetenekKatsayisi (eski, uyum için)
        self.ozel_yetenek = None           # Özel Yetenek (OzelYetenek nesnesi)
