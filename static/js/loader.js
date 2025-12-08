// loader.js

// Librerías externas (CDN)
const externalScripts = [
  "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.js",
  "https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js",
];

const externalStyles = [
  "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css",
  "https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/main.min.css",
];

// Función para cargar CSS
function loadCSS(href) {
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = href;
  document.head.appendChild(link);
}

// Función para cargar JS
function loadJS(src, type = "text/javascript") {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.type = type;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });
}

// Cargar todo al inicio
document.addEventListener("DOMContentLoaded", async () => {
  externalStyles.forEach(loadCSS);
  for (const src of externalScripts) {
    await loadJS(src);
  }
  console.log("Dependencias externas cargadas ✅");
});
