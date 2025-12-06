from django.shortcuts import render

def voice_search_view(request):
    query = request.GET.get("q")
    results = None
    if query:
        # Aquí podrías conectar con tu buscador interno
        # o simplemente devolver el texto capturado
        results = f"Resultados simulados para: {query}"
    return render(request, "voice_search.html", {"results": results})
