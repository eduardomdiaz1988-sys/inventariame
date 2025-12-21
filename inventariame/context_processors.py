from datetime import datetime
import locale

def fecha_hoy(request):
    try:
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    except:
        locale.setlocale(locale.LC_TIME, "es_ES")

    hoy = datetime.now().strftime("%A %d de %B").capitalize()
    return {"fecha_hoy": hoy}
