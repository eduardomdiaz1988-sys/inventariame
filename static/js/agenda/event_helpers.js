window.eventContent = function(arg) {
  const tipo = arg.event.extendedProps?.tipo || "";
  const title = arg.event.title || "";
  const el = document.createElement("div");
  el.innerHTML = `
    <div class="fc-event-custom">
      <strong>${title}</strong><br>
      <small class="text-muted">${tipo}</small>
    </div>
  `;
  return { domNodes: [el] };
};

window.handleDateClick = function(info) {
  const fecha = info.dateStr;
  window.location.href = `/citas/nueva/?fecha=${encodeURIComponent(fecha)}`;
};

window.handleEventClick = function(info) {
  if (info.event.url) {
    info.jsEvent.preventDefault();
    window.location.href = info.event.url;
  }
};
