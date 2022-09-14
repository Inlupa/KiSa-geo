from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_margins(30, 10, 15)
        self.add_font('TNRoman', 'B', 'docs/Times_New_Roman_b.ttf')
        self.set_font("TNRoman", "B", 16)
        self.cell(40)
        self.set_line_width(0.1)
        self.set_draw_color(0, 0, 0)
        self.line(x1=30, y1=21, x2=195, y2=21)
        self.cell(80, 6, "ГПБУ «Мосэкомониторинг»", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("TNRoman", "B", 14)
        self.cell(40)
        self.cell(80, 6, "Геологическая служба", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.add_font('TNRoman', '', 'Times_New_Roman.ttf')
        self.set_font("TNRoman", "", 8)
        self.cell(0, 10, f"{self.page_no()}", align="C")


def generate_well_pumping_acts(elements):
    pdf = PDF()
    pdf.oversized_images = "DOWNSCALE"
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("TNRoman", "B", 14)
    pdf.cell(30)
    pdf.multi_cell(100, 6, "АКТ\nпрокачки наблюдательного пункта (скважины)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.add_font('TNRoman', '', 'docs/Times_New_Roman.ttf', uni=True)
    pdf.set_font("TNRoman", size=11)
    pdf.cell(30, 10, "г.Москва", align="L", new_x="RMARGIN")
    pdf.cell(-32.5)
    pdf.cell(25, 10, elements['date'], align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(165, 5, "Скважина № **" + elements['well'] + "**", align="L", new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.multi_cell(165, 5, "расположена по адресу:\n" + elements['position'], align="L", new_y="NEXT", new_x="LMARGIN",
                   markdown=True)
    pdf.multi_cell(165, 5, "географические координаты:\n" + "СШ " + elements['x'] + "   ВД " + elements['y'], align="L",
                   new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.ln(2)
    pdf.set_font("TNRoman", size=10)
    line_height = (pdf.font_size * 3.8)
    col_width = pdf.epw / 6  # distribute content evenly
    for row in elements['condition_data']:
        for datum in row:
            pdf.multi_cell(col_width, line_height, datum, border=1, align="C",
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
        pdf.ln(line_height)
    pdf.ln(2)
    pdf.set_font("TNRoman", size=10)
    line_height = pdf.font_size * 3.8
    col_width = pdf.epw / 6  # distribute content evenly
    for row in elements['pump_data']:
        for datum in row:
            pdf.multi_cell(col_width, line_height, datum, border=1, align="C",
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
        pdf.ln(line_height)
    pdf.ln(2)
    pdf.set_font("TNRoman", size=11)
    pdf.multi_cell(165, 5, "**Примечания:** " + elements['comments'], align="L", new_y="NEXT", new_x="LMARGIN",
                   markdown=True)

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
    # pdf.multi_cell(100, 6, "Схема расположения скважина\n№ "+elements['well'], align="C",new_y="NEXT",new_x="LMARGIN")
    # pdf.image('100003.JPG',w=165)
    # pdf.ln(3)

    return bytes(pdf.output())
