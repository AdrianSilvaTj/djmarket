
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    # Recupera un template, segun la ruta que le pasemos
    template = get_template(template_src)
    # Le pasamos el contexto al template
    html  = template.render(context_dict)
    # la función para convertir a PDF requiere de varios parametro adicionales
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # Verificamos si no hay ningún error al crear el pdf
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None