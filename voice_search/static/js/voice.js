document.addEventListener("DOMContentLoaded", () => {
  const micButton = document.getElementById("micButton");
  const searchInput = document.getElementById("searchInput");

  if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "es-ES";
    recognition.continuous = false;
    recognition.interimResults = false;

    micButton.addEventListener("click", () => {
      recognition.start();
      micButton.classList.add("btn-danger"); // feedback visual
    });

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      searchInput.value = transcript;
      micButton.classList.remove("btn-danger");
      // Opcional: enviar automáticamente
      searchInput.form.submit();
    };

    recognition.onerror = () => {
      micButton.classList.remove("btn-danger");
    };

    recognition.onend = () => {
      micButton.classList.remove("btn-danger");
    };
  } else {
    micButton.disabled = true;
    micButton.title = "Tu navegador no soporta búsqueda por voz";
  }
});
