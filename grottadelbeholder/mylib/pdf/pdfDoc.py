from fpdf import FPDF


class PDF(FPDF):
    pdf_w = 210
    pdf_h = 297

    txt_x = 1.5

    txt_font = 'Arial'

    def defaultLayout(self):
        self.set_fill_color(50, 50, 50)
        self.rect(0, 0, self.pdf_w, 20, 'DF')

        self.set_xy(0.0, 0.0)
        self.set_font(self.txt_font, 'B', 25)
        self.set_text_color(255, 255, 255)
        self.cell(w = self.pdf_w - (self.txt_x * 2), h = 18, align='C', txt="LA GROTTA DEL BEHOLDER", border=0)

        self.set_xy(0.0, 12.0)
        self.set_font(self.txt_font, 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(w = self.pdf_w - (self.txt_x * 2), h = 7, align='C', txt="localhost:8000/grottadelbeholder", border=0, link='http://localhost:8000/grottadelbeholder')

        self.rect(0, 282, self.pdf_w, self.pdf_h, 'DF')

    def writeCategory(self, category):
        self.set_xy(self.txt_x, 20.0)
        self.set_font(self.txt_font, 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(w=self.pdf_w - 2, h=10.0, align='L', txt=category, border=0)

    def writeName(self, name):
        self.set_xy(self.txt_x, 25.0)
        self.set_font(self.txt_font, 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(w=self.pdf_w - self.txt_x, h=10.0, align='L', txt=name, border=0)

    def writeDescription(self, descr):
        self.set_xy(self.txt_x, 35)
        self.set_font(self.txt_font, '', 12)
        self.set_text_color(40, 40, 40)
        multiCell = self.multi_cell(w=self.pdf_w - (self.txt_x * 2), h=0, txt=descr, split_only=True)
        for cell in multiCell:
            self.set_xy(self.txt_x, self.y + 6)
            self.cell(w=self.pdf_w - (self.txt_x * 2), h=0, txt=cell)

    def writeRaceDetails(self, detail):
        w = self.pdf_w - (self.txt_x * 2)

        self.set_xy(self.txt_x, self.y + 12)
        self.set_font(self.txt_font, 'I', 12)
        self.set_text_color(40, 40, 40)
        self.cell(w=w, h=0, txt="Età: " + detail.age)

        self.set_xy(self.txt_x, self.y + 6)
        self.cell(w=w, h=0, txt="Allineamento: " + detail.alignment)

        self.set_xy(self.txt_x, self.y + 6)
        self.cell(w=w, h=0, txt="Dimensioni: " + detail.size)

        self.set_xy(self.txt_x, self.y + 6)
        self.cell(w=w, h=0, txt="Velocità: " + detail.speed)

        self.set_xy(self.txt_x, self.y + 6)
        self.cell(w=w, h=0, txt="Linguaggi: " + detail.languages)

        self.set_draw_color(150, 150, 150)
        self.line(self.txt_x, self.y + 8, w, self.y + 8)

        self.set_font(self.txt_font, 'B', 12)
        self.set_xy(self.txt_x, self.y + 14)
        self.cell(w=w, h=0, txt="Incremento dei punteggi di caratteristica")

        x = 5
        augm = 35
        self.ellipse(x, self.y + 5, 20, 15)
        x += augm
        self.ellipse(x, self.y + 5, 20, 15)
        x += augm
        self.ellipse(x, self.y + 5, 20, 15)
        x += augm
        self.ellipse(x, self.y + 5, 20, 15)
        x += augm
        self.ellipse(x, self.y + 5, 20, 15)
        x += augm
        self.ellipse(x, self.y + 5, 20, 15)


        self.set_font(self.txt_font, 'B', 10)
        self.set_text_color(150, 150, 150)
        x=5
        self.set_xy(x, self.y + 8)
        self.cell(w=20, h=0, align="C", txt="FOR")
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt="DES")
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt="COS")
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt="INT")
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt="SAG")
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt="CAR")

        self.set_text_color(40, 40, 40)
        self.set_font(self.txt_font, 'B', 20)
        x=5
        self.set_xy(x, self.y + 6)
        self.cell(w=20, h=0, align="C", txt=str(detail.strScoreInc))
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt=str(detail.dexScoreInc))
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt=str(detail.conScoreInc))
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt=str(detail.intScoreInc))
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt=str(detail.wisScoreInc))
        x += augm
        self.set_xy(x, self.y)
        self.cell(w=20, h=0, align="C", txt=str(detail.chaScoreInc))

        self.line(self.txt_x, self.y + 12, w, self.y + 12)

        self.set_font(self.txt_font, 'B', 12)
        self.set_xy(self.txt_x, self.y + 18)
        self.cell(w=w, h=0, txt="Sottorazze")

        self.set_font(self.txt_font, '', 12)

        self.set_xy(self.txt_x, self.y + 2)
        multiCell = self.multi_cell(w=self.pdf_w - (self.txt_x * 2), h=0, txt=str(detail.subraces), split_only=True)
        for cell in multiCell:
            self.set_xy(self.txt_x, self.y + 6)
            self.cell(w=self.pdf_w - (self.txt_x * 2), h=0, txt=cell)