import io
import datetime
from babel.dates import format_date
from plpygis import Geometry
from fpdf import FPDF
from django.db.models import Max, Min
from .models import *


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
        self.add_font('TNRoman', '', 'Times_New_Roman.ttf')
        self.set_font("TNRoman", "", 8)
        # Printing page number:
        self.cell(0, 10, f"{self.page_no()}", align="C")


def generate_well_inspection_acts(request):
    well_id = request.POST.get("well")
    date = request.POST.get("date")
    fillactfield = Wells.objects.get(well_id=well_id)
    g = Geometry(fillactfield.geom)
    filltepmfield = WellsTemperature.objects.get(well_id=well_id,
                                                 date=WellsTemperature.objects.filter(
                                                     well_id=well_id,
                                                     date__lt=date).latest(
                                                     'date').date)
    fillwatfield = WellsWaterdepth.objects.get(well_id=well_id,
                                               date=WellsWaterdepth.objects.filter(
                                                   well_id=well_id,
                                                   date__lt=date).latest(
                                                   'date').date)
    filllugfield = WellsLugheight.objects.get(well_id=well_id,
                                              date=WellsLugheight.objects.filter(
                                                  well_id=well_id,
                                                  date__lt=date).latest(
                                                  'date').date)
    filldepthfield = WellsDepth.objects.get(well_id=well_id,
                                            date=WellsDepth.objects.filter(
                                                well_id=well_id,
                                                date__lt=date).latest(
                                                'date').date)
    filldepthfield_pass = WellsDepth.objects.get(well_id=well_id,
                                                 date=WellsDepth.objects.filter(
                                                     well_id=well_id).earliest(
                                                     'date').date)

    fillsurveys1 = Workers.objects.get(worker_id=request.POST.get('survey1'))
    survey_f = fillsurveys1.name
    if request.POST.get('survey2') == '':
        we = '  Я, нижеподписавшийся, сотрудник Геологической службы ГПБУ "Мосэкомониторинг": **'
        survey_f += '** провёл'
        we += survey_f + ' инспекцию состояния скважины и режимные наблюдения.'
    else:
        we = '  Мы, нижеподписавшиеся, сотрудники Геологической службы ГПБУ "Мосэкомониторинг": **'
        fillsurveys2 = Workers.objects.get(worker_id=request.POST.get('survey2'))
        survey_s = ' и ' + fillsurveys2.name + '** провели'
        we += survey_f + survey_s + ' инспекцию состояния скважины и режимные наблюдения.'

    fillconsfield = WellsConstruction.objects.filter(well_id=well_id).exclude(
        construction_type=1)

    files = request.FILES.getlist('file_field')
    images = []
    if WellsInspection.objects.filter(well_id=well_id, date=date).exists():
        instance_wells_inspection = WellsInspection.objects.get(well_id=well_id,
                                                                date=date)
        instance_wi_attach = WellsInspectionAttach.objects.filter(rel_doc_id=instance_wells_inspection.doc_id)
        for img in instance_wi_attach:
            images.append(io.BytesIO(bytes(img.data)))
    for img in files:
        images.append(img)

    pass_data = (
        ("№ скважины", "Год бурения скважины", "Абсолютная отметка устья скважины, м",
         "Глубина скважины по паспорту (от поверхности земли), м",
         "Интервал установки фильтра от поверхности земли  (от – до), м"),
        (str(well_id), format_date(filldepthfield_pass.date, "yyyy"), fillactfield.head, filldepthfield_pass.depth,
         str((fillconsfield.aggregate(Min('depth_from'))['depth_from__min'])) + '-' + str(
             (fillconsfield.aggregate(Max('depth_till'))['depth_till__max'])))
    )
    measure_data = (well_id, filldepthfield.depth, request.POST.get("depth"), fillwatfield.water_depth,
                    request.POST.get("water_depth"),
                    filltepmfield.temperature, request.POST.get("temperature"), filllugfield.lug_height,
                    request.POST.get("lug_height"))
    condition_data = (
        ("№ скважины", "Покраска", "Маркировка",
         "Исправность патрубка",
         "Исправность оголовка", "Состояние устья скважины", "Оборудование автоматикой"),
        (str(well_id), define_condition_for_acts(request.POST.get("painting_condition")),
         define_condition_for_acts(request.POST.get("lable_condition")),
         define_condition_for_acts(request.POST.get("well_lug_condition")),
         define_condition_for_acts(request.POST.get("well_head_condition")),
         define_condition_for_acts(request.POST.get("well_collar_condition")),
         define_condition_for_acts(request.POST.get("automation_condition")))
    )
    elements = {'date': format_date(datetime.datetime.strptime(date, '%Y-%m-%d'), "d MMMM yyyy",
                                    locale='ru'), 'well': str(well_id),
                'position': str(fillactfield.position),
                'x': str(round(g.x, 6)), 'y': str(round(g.y, 6)),
                'we': we, 'pass_data': pass_data, 'measure_data': measure_data,
                'condition_data': condition_data,
                'logs_results': '' if request.POST.get("logs_results") is None else request.POST.get("logs_results"),
                'sanitation': request.POST.get("area_description"),
                'comments': request.POST.get("comments"),
                'recommendations': request.POST.get("recommendations"),
                'survey1': fillsurveys1.name,
                'survey2': '' if request.POST.get('survey2') == '' else fillsurveys2.name,
                'schema': None,
                'images': images,
                'weather': request.POST.get("weather"), }
    pdf = PDF()

    pdf.oversized_images = "DOWNSCALE"
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("TNRoman", "B", 14)
    pdf.cell(30)
    pdf.multi_cell(100, 6, "АКТ\nинспекции наблюдательной скважины", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.add_font('TNRoman', '', 'docs/Times_New_Roman.ttf', uni=True)
    pdf.set_font("TNRoman", size=12)
    pdf.cell(30, 10, "г.Москва", align="L", new_x="RMARGIN")
    pdf.cell(-32.5)
    pdf.cell(25, 10, elements['date'], align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(25, 6, "Cкважина № **" + elements['well'] + '**,', align="L", new_y="NEXT", new_x="LMARGIN", markdown=True)
    pdf.cell(25, 6, "расположена по адресу:", align="L", new_y="NEXT")
    pdf.set_x(30)
    pdf.multi_cell(165, 6, elements['position'], new_y="NEXT", new_x="LMARGIN")
    pdf.cell(25, 6, "географические координаты:", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(25, 8, "СШ " + elements['x'] + "  ВД " + elements['y'], align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 6, "Паспортные данные по скважине:", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.set_font("TNRoman", size=8)
    line_height = (pdf.font_size * 3.8) / 1.2
    col_width = pdf.epw / 5  # distribute content evenly
    for row in elements['pass_data']:
        for datum in row:
            pdf.multi_cell(col_width, line_height, str(datum), border=1, align="C",
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
        pdf.ln(line_height)
    pdf.ln(2)
    pdf.set_font("TNRoman", size=12)
    pdf.multi_cell(165, 6, elements['we'], new_y="NEXT", new_x="CENTER", markdown=True)
    pdf.set_font("TNRoman", 'B', size=12)
    pdf.ln(2)
    pdf.cell(165, 5, "При инспекции установлено следующее: ", align="C", new_y="NEXT", new_x="LMARGIN")
    pdf.ln(2)
    pdf.cell(25, 5, "1. Контрольные замеры", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.set_font("TNRoman", size=7)
    line_height = (pdf.font_size * 3.8) / 1.2
    col_width = pdf.epw / 9  # distribute content evenly
    headers = (("Глубина скважины (от патрубка), м ", "Глубина уровня воды в скважине (от патрубка), м",
                "Температура воды, о С", "Высота патрубка, м "),
               ("По предыдущей инспекции", "По контрольному замеру",
                "По последнему замеру", 'По контрольному замеру',
                "По последнему замеру", 'По контрольному замеру',
                "По предыдущей инспекции", "По контрольному замеру"),)
    start = pdf.get_y()
    for i, row in enumerate(headers):
        pdf.set_x(30 + col_width)
        if i == 0:
            mult = 2
        else:
            mult = 1
        for datum in row:
            pdf.multi_cell(col_width * mult, line_height, str(datum), border=1, align="C",
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
        pdf.ln(line_height)
    end = pdf.get_y()
    pdf.set_xy(30, start)
    pdf.cell(col_width, end - start, "№ скважины", border=1, align="C", new_y="NEXT")
    pdf.set_x(30)
    for datum in elements['measure_data']:
        pdf.multi_cell(col_width, line_height, str(datum), border=1, align="C",
                       new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
    pdf.ln(line_height)
    pdf.ln(2)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 5, "2. Состояние надземной части скважины", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.set_font("TNRoman", size=8)
    line_height = (pdf.font_size * 3.8) / 1.8
    col_width = pdf.epw / 7  # distribute content evenly
    for row in elements['condition_data']:
        for datum in row:
            pdf.multi_cell(col_width, line_height, str(datum), border=1, align="C",
                           new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
        pdf.ln(line_height)
    pdf.ln(2)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 3, '3. Результаты видеокаротажа', align="L", new_x="WCONT")
    pdf.set_font("TNRoman", size=8)
    pdf.cell(110, 3, ' (состояние обсадных, фильтровых труб, наличие коррозии, нарушение целостности',
             align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(110, 3, 'колонн, наличие посторонних объектов, кольматация)',
             align="L", new_y="NEXT")
    pdf.set_font("TNRoman", size=12)
    pdf.set_x(30)
    pdf.multi_cell(165, 6, elements['logs_results'], new_y="NEXT", new_x="LMARGIN")
    pdf.ln(2)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 3, "4. Экологическая оценка состояния территории, прилегающей к скважине", align="L", new_x="WCONT")
    pdf.set_font("TNRoman", size=8)
    pdf.cell(110, 3, ' (наличие свалок',
             align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.multi_cell(165, 3,
                   'промышленных и хозбытовых отходов, возможность попадания загрязненных сточных вод в приустьевую часть скважины, '
                   'земляные работы, нахождение скважины в зоне затопления в период паводков и другое)',
                   align="L", new_y="NEXT")
    pdf.set_font("TNRoman", size=12)
    pdf.set_x(30)
    pdf.multi_cell(165, 6, elements['sanitation'], new_y="NEXT", new_x="LMARGIN")
    pdf.ln(2)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 5, "5. Примечания", align="L", new_y="NEXT")
    pdf.set_font("TNRoman", size=12)
    pdf.set_x(30)
    pdf.multi_cell(165, 6, elements['comments'], new_y="NEXT", new_x="LMARGIN")
    pdf.ln(2)
    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 5, "6. Выводы и рекомендации по результатам инспекции", align="L", new_y="NEXT")
    pdf.set_font("TNRoman", size=12)
    pdf.set_x(30)
    pdf.multi_cell(145, 6, elements['recommendations'], new_y="NEXT", new_x="LMARGIN")
    pdf.ln(2)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(25, 5, "7. Приложения:", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.set_font("TNRoman", size=12)
    pdf.cell(25, 5, "1. Схема расположения скважины", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.cell(25, 5, "2. Фотодокументация", align="L", new_y="NEXT", new_x="LMARGIN")
    pdf.ln(8)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(20, 35, "Составил", align="L")
    pdf.image('docs/Auto/' + elements['survey1'] + '.png', w=25, h=18)
    pdf.set_font("TNRoman", size=12)
    pdf.cell(35, 2, '_______________')
    pdf.cell(20, 2, str(elements['survey1']))
    pdf.ln(8)

    pdf.set_font("TNRoman", 'B', size=12)
    pdf.cell(20, 35, "Проверил", align="L")
    if elements['survey2'] != '':
        pdf.image('docs/Auto/' + elements['survey2'] + '.png', w=25, h=18)
    else:
        pdf.ln(18)
        pdf.set_x(50)
    pdf.set_font("TNRoman", size=12)
    pdf.cell(35, 2, '_______________')
    pdf.cell(20, 2, str(elements['survey2']))

    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("TNRoman", "B", 14)
    pdf.cell(30)
    pdf.multi_cell(100, 6, "Схема расположения скважины\n№ " + elements['well'], align="C", new_y="NEXT",
                   new_x="LMARGIN")
    # pdf.image(elements['schema'],w=165)
    pdf.ln(3)

    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("TNRoman", "B", 14)
    pdf.cell(30)
    pdf.multi_cell(100, 6, "Фотодокументация по скважине\n№ " + elements['well'], align="C", new_y="NEXT",
                   new_x="LMARGIN")
    images = elements['images']
    for img in images:
        pdf.image(img, h=110, x=40)
        pdf.ln(1)
    pdf.ln(3)

    return pdf


def define_condition_for_acts(field):
    if field == '2':
        val = 'хор.'
    elif field == '0':
        val = 'удовл.'
    else:
        val = 'неудовл.'
    return val
