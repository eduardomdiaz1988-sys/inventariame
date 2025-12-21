from datetime import datetime
from django.utils import formats

def fecha_hoy(request):
    hoy = formats.date_format(datetime.now(), "l d F", use_l10n=True)
    return {"fecha_hoy": hoy.capitalize()}

def mes_y_anio(request):
    fecha = formats.date_format(datetime.now(), "F Y", use_l10n=True)
    return {"mes_y_anio": fecha.capitalize()}