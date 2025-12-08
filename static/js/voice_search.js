export function initVoiceSearch(micButton, searchInput) {
  if (!("webkitSpeechRecognition" in window)) {
    console.warn("Reconocimiento de voz no soportado");
    return;
  }

  const recognition = new webkitSpeechRecognition();
  recognition.lang = "es-ES";
  recognition.continuous = false;
  recognition.interimResults = false;

  micButton.addEventListener("click", () => {
    recognition.start();
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    searchInput.value = transcript;
  };

  recognition.onerror = (event) => {
    console.error("Error en reconocimiento de voz:", event.error);
  };
}
