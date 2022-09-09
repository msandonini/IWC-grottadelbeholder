from fpdf import FPDF


class PDF(FPDF):
    pdf_w = 210
    pdf_h = 297

    def defaultLayout(self):
        self.set_fill_color(50, 50, 50)
        self.rect(0, 0, self.pdf_w, 20, 'DF')

        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 25)
        self.set_text_color(255, 255, 255)
        self.cell(w = 210, h = 18, align='C', txt="LA GROTTA DEL BEHOLDER", border=0)

        self.set_xy(0.0, 12.0)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(w = 210, h = 7, align='C', txt="localhost:8000/grottadelbeholder", border=0)

    def writeCategory(self, category):
        self.set_xy(1.5, 20.0)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(w=self.pdf_w - 2, h=10.0, align='L', txt=category, border=0)

    def writeName(self, name):
        self.set_xy(1.5, 25.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(w=self.pdf_w - 2, h=10.0, align='L', txt=name, border=0)