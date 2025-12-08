document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("agendaCalendar");
  if (!el || typeof FullCalendar === "undefined") return;

  const calendar = new FullCalendar.Calendar(el, {
    initialView: "dayGridMonth",
    height: "auto",
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek"
    },
    navLinks: true,
    selectable: true,
    weekends: true,
    nowIndicator: true,
    slotMinTime: "08:00:00",
    slotMaxTime: "20:00:00",
    locale: "es",
    firstDay: 1,
    eventSources: [
      { url: "/agenda/api/eventos/", method: "GET" }
    ],
    eventContent: window.eventContent,
    dateClick: window.handleDateClick,
    eventClick: window.handleEventClick,
  });

  calendar.render();

  // Filtros
  const filtroTodos = document.getElementById("filtroTodos");
  const filtroCitas = document.getElementById("filtroCitas");
  const filtroVentas = document.getElementById("filtroVentas");

  if (filtroTodos) filtroTodos.addEventListener("click", () => calendar.refetchEvents());
  if (filtroCitas) filtroCitas.addEventListener("click", () => {
    calendar.getEvents().forEach(ev => {
      ev.setProp("display", ev.extendedProps.tipo === "cita" ? "auto" : "none");
    });
  });
  if (filtroVentas) filtroVentas.addEventListener("click", () => {
    calendar.getEvents().forEach(ev => {
      ev.setProp("display", ev.extendedProps.tipo === "venta" ? "auto" : "none");
    });
  });
});
