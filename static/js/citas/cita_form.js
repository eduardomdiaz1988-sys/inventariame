import { initClienteCreate } from "./cliente_create.js";
import { cargarDirecciones } from "./direcciones.js";

document.addEventListener("DOMContentLoaded", () => {
  const clienteHidden = document.getElementById("id_cliente_hidden");
  const cardCliente = document.getElementById("card-cliente");
  const cardCita = document.getElementById("card-cita");
  const cardResumen = document.getElementById("card-resumen");
  const direccionSelect = document.getElementById("id_direccion");

  const tipoRadios = document.querySelectorAll('input[name="cliente_tipo"]');
  const busquedaCliente = document.getElementById("busquedaCliente");
  const buscadorInput = document.getElementById("buscador_cliente");
  const resultadosCliente = document.getElementById("resultados_cliente");

  const clienteForm = document.getElementById("clienteForm");
  const btnCrearCliente = document.getElementById("btnCrearCliente");
  const formNuevoCliente = document.getElementById("formNuevoCliente");

  flatpickr("#id_fecha", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: true,
    minDate: "today",
    locale: "es"
  });

  // Mostrar/ocultar según tipo de cliente
  tipoRadios.forEach(radio => {
    radio.addEventListener("change", () => {
      const tipo = radio.value;
      busquedaCliente.classList.toggle("d-none", tipo !== "existente");
      formNuevoCliente.classList.toggle("d-none", tipo !== "nuevo");
      resultadosCliente.innerHTML = "";
      clienteHidden.value = "";
      cardCita.classList.add("d-none");
      cardResumen.classList.add("d-none");
    });
  });

  // Búsqueda AJAX de cliente existente
  buscadorInput.addEventListener("input", async (e) => {
    const query = e.target.value;
    if (query.length < 2) return;

    const response = await fetch(`/clientes/api/buscar/?q=${encodeURIComponent(query)}`);
    const resultados = await response.json();

    resultadosCliente.innerHTML = "";
    resultados.forEach(cliente => {
      const item = document.createElement("button");
      item.className = "list-group-item list-group-item-action";
      item.textContent = `${cliente.nombre} (${cliente.telefono})`;
      item.addEventListener("click", () => {
        clienteHidden.value = cliente.id;
        clienteHidden.dataset.direccion = cliente.direccion || "";
        clienteHidden.dataset.label = cliente.label || "";
        cargarDirecciones(cliente.id, direccionSelect);
        cardCita.classList.remove("d-none");
      });
      resultadosCliente.appendChild(item);
    });
  });

  // Crear nuevo cliente
  initClienteCreate(
    btnCrearCliente,
    clienteForm,
    null,
    clienteHidden,
    cardCliente,
    cardCita,
    (id) => cargarDirecciones(id, direccionSelect)
  );

  // 🔥 NUEVO: Lógica para el paso 3 (resumen)
  const btnResumen = document.getElementById("btnResumen");
  if (btnResumen && cardResumen) {
    btnResumen.addEventListener("click", () => {
      // Rellenar resumen
      document.getElementById("resCliente").textContent =
        document.getElementById("id_nombre")?.value || "—";
      document.getElementById("resTelefono").textContent =
        document.getElementById("id_telefono")?.value || "—";

      const direccion = clienteHidden.dataset.direccion || "";
      const label = clienteHidden.dataset.label || "";
      document.getElementById("resDireccion").textContent =
        label ? `${label} — ${direccion}` : direccion || "—";

      document.getElementById("resFecha").textContent =
        document.getElementById("id_fecha").value;
      document.getElementById("resEstado").textContent =
        document.getElementById("id_estado").value;
      document.getElementById("resOferta").textContent =
        document.getElementById("id_oferta").value;
      document.getElementById("resRecordatorio").textContent =
        document.getElementById("id_recordatorio").checked ? "Sí" : "No";

      // 🔥 NUEVO: Copiar datos del cliente nuevo a los hidden del form final
      document.getElementById("id_nombre_hidden").value =
        document.getElementById("id_nombre")?.value || "";
      document.getElementById("id_telefono_hidden").value =
        document.getElementById("id_telefono")?.value || "";
      document.getElementById("id_address_hidden").value =
        document.getElementById("addressField")?.value || "";
      document.getElementById("id_lat_hidden").value =
        document.getElementById("latField")?.value || "";
      document.getElementById("id_lng_hidden").value =
        document.getElementById("lngField")?.value || "";
      document.getElementById("id_label_hidden").value =
        document.getElementById("labelField")?.value || "";

      cardCita.classList.add("d-none");
      cardResumen.classList.remove("d-none");
    });
  }
});
