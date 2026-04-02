from sporcu import Sporcu


class Futbolcu(Sporcu):
    def __init__(self):
        super().__init__()
        # Futbolcu Özellikleri
        self.penalti = None                # Penaltı
        self.serbestturus = None           # SerbestVurus
        self.kaleci_karsikarsiya = None    # KaleciKarsiKarsiya
        self.dayaniklilik = None           # Dayanıklılık
        self.ozel_yetenek_katsayisi = None # OzelYetenekKatsayisi (eski, uyum için)
        self.ozel_yetenek = None           # Özel Yetenek (OzelYetenek nesnesi)
