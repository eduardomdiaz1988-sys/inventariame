from django.utils import timezone
from datetime import timedelta
from citas.models import Cita

def alertas_processor(request):
    if not request.user.is_authenticated:
        return {}
    ahora = timezone.now()
    proximas_con_recordatorio = Cita.objects.filter(
        usuario=request.user, recordatorio=True,
        fecha__gte=ahora, fecha__lte=ahora + timedelta(days=1)
    )
    if proximas_con_recordatorio.exists():
        return {"alertas": f"Tienes {proximas_con_recordatorio.count()} cita(s) con recordatorio en 24h"}
    return {}
