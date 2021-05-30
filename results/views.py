from django.shortcuts import render
from django.conf import settings
# Create your views here.
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from questions.models import Student_Answer

def results(request, pk):
    user = request.user
    print(user)
    print(user.email)
    generate_pdf()
    return render(request, 'results/results.html', {})

from fpdf import FPDF

def generate_pdf():
    class PDF(FPDF):
        def header(self):
            # Logo
            #self.image(file_path, 10, 8, 33)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(30, 10, 'Title', 1, 0, 'C')
            # Line break
            self.ln(40)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, 'test1 ', 0, 1)
    pdf.cell(0, 10, 'test2 ', 0, 1)
    pdf.output('tuto2.pdf', 'F')


def render_pdf_view(request, pk):
    user = request.user
    answers = Student_Answer.objects.filter(user = user).values()
    score = 0
    for answer in answers:
        print(answer)
        score += 1

    template_path = 'results/test.html'
    context = {'myvar': 'this is your template context',
               'score': score,
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display:
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
