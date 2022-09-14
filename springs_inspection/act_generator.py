# coding: utf8
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_margins(30, 10, 15)
        # Rendering logo:
        # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15

        self.add_font('TNRoman', 'B', 'docs/Times_New_Roman_b.ttf')
        self.set_font("TNRoman", "B", 16)
        self.cell(40)
        # Printing title:
        self.set_line_width(0.1)
        self.set_draw_color(0, 0, 0)
        self.line(x1=30, y1=21, x2=195, y2=21)
        self.cell(80, 6, "ГПБУ «Мосэкомониторинг»", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("TNRoman", "B", 14)
        self.cell(40)
        self.cell(80, 6, "Геологическая служба", align="C")
        # Performing a line break:
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.add_font('TNRoman', '', 'docs/Times_New_Roman.ttf')
        self.set_font("TNRoman", "", 8)
        # Printing page number:
        self.cell(0, 10, f"{self.page_no()}", align="C")


def generate_spring_inspection_acts(elements):
    pdf = PDF()
    pdf.oversized_images = "DOWNSCALE"
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("TNRoman", "B", 14)
    pdf.cell(30)
    pdf.multi_cell(100, 6, "АКТ\nобследования родника", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.add_font('TNRoman', '', 'docs/Times_New_Roman.ttf', uni=True)
    pdf.set_font("TNRoman", size=11)
    pdf.cell(30, 10, "г.Москва", align="L", new_x="RMARGIN")
    pdf.cell(-32.5)
    pdf.cell(25, 10, elements['date'], align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(165, 5, "Родник № --" + elements['well'] + "-- название родника --" + elements['name'] + "--", align="L",
             new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.multi_cell(165, 5, "Расположен по адресу: --" + elements['position'] + "--", align="L", new_y="NEXT",
                   new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.multi_cell(165, 5, elements['we'], new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(25, 5, "При обследовании установлено:", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(165, 5, "**1. Координаты:** --" + elements['x'] + " СШ    " + elements['y'] + " ВД--", align="L",
             new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**2. Погодные условия:** --" + elements['weather'] + "--", align="L", new_y="NEXT",
             new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**3. Тип родника:** --" + str(elements['type']) + "--", align="L", new_y="NEXT", new_x="LMARGIN",
             markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**4. Режим функционирования родника:** --" + str(elements['function']) + "--", align="L",
             new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**5. Характер использования родника:** --" + elements['usage'] + "--", align="L", new_y="NEXT",
             new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**6. Местоположение в рельефе:** --" + elements['geomorph'] + "--", align="L", new_y="NEXT",
             new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**7. Название и индекс водоносного горизонта:** --" + elements['aquifer'] + "--", align="L",
             new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**8. Водовмещающие породы:** --" + elements['lithology'] + "--", align="L", new_y="NEXT",
             new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(165, 5, "**9. Характеристика родника:**", align="L", new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.set_font("TNRoman", size=10)
    col_width = pdf.epw / 2  # distribute content evenly
    for row in elements['condition_data']:
        if int((len(row[1]) * 3 / 165)) == 0:
            height = pdf.font_size * 1.8
        else:
            height = pdf.font_size * (int((len(row[1]) * 3 / 165)) + 1)
        for datum in row:
            pdf.multi_cell(col_width, height, datum, border=1, align="C",
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
        pdf.ln(height)
    pdf.ln(2)

    pdf.set_font("TNRoman", size=11)
    pdf.cell(25, 5, "**10. Примечания:**", align="L", new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.multi_cell(165, 5, elements['comments'], new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(25, 5, "**11. Рекомендации:**", align="L", new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.multi_cell(165, 5, elements['recommendations'], new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.cell(25, 5, "**12. Приложения:**", align="L", new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.cell(25, 5, "1. Схема расположения родника", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(25, 5, "2. Фотодокументация", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.ln(2)

    pdf.set_font("TNRoman", 'B', size=11)
    pdf.cell(20, 35, "Составил", align="L")
    pdf.image('docs/Auto/' + elements['survey1'] + '.png', w=25, h=18)
    pdf.set_font("TNRoman", size=12)
    pdf.cell(35, 2, '_______________')
    pdf.cell(20, 2, str(elements['survey1']))
    pdf.ln(8)

    pdf.set_font("TNRoman", 'B', size=11)
    pdf.cell(20, 35, "Проверил", align="L")
    if elements['survey2']!='':
        pdf.image('docs/Auto/' + elements['survey2'] + '.png', w=25, h=18)
    else:
        pdf.ln(18)
        pdf.set_x(50)
    pdf.set_font("TNRoman", size=12)
    pdf.cell(35, 2, '_______________')
    pdf.cell(20, 2, str(elements['survey2']))

    # pdf.add_page()
    # pdf.set_y(30)
    # pdf.set_font("TNRoman", "B", 14)
    # pdf.cell(30)
    # pdf.multi_cell(100, 6, "Схема расположения родника\n№ "+elements['well'], align="C",new_y="NEXT",new_x="LMARGIN")
    # pdf.image('100003.JPG',w=165)
    # pdf.ln(3)

    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("TNRoman", "B", 14)
    pdf.cell(30)
    pdf.multi_cell(100, 6, "Фотодокументация по роднику\n№ " + elements['well'], align="C", new_y="NEXT",
                   new_x="LMARGIN")
    images = elements['images']
    for img in images:
        pdf.image(img, h=110, x=40)
        pdf.ln(1)
    pdf.ln(3)
    return bytes(pdf.output())
