export function initVoiceSearch(micButton, searchInput) {
  if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "es-ES";
    recognition.continuous = false;
    recognition.interimResults = false;

    micButton.addEventListener("click", () => {
      recognition.start();
      micButton.classList.add("btn-danger");
    });

    recognition.onresult = (event) => {
      let transcript = event.results[0][0].transcript.trim().toLowerCase();
      if (transcript.endsWith(".")) transcript = transcript.slice(0, -1);
      searchInput.value = transcript;
      searchInput.form.submit();
    };

    recognition.onend = () => micButton.classList.remove("btn-danger");
    recognition.onerror = () => micButton.classList.remove("btn-danger");
  } else {
    micButton.disabled = true;
    micButton.title = "Tu navegador no soporta búsqueda por voz";
  }
}
