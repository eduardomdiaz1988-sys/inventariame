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

  // Calendario para fecha de cita
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

    try {
      const response = await fetch(`/clientes/api/buscar/?q=${encodeURIComponent(query)}`);
      const resultados = await response.json();

      resultadosCliente.innerHTML = "";
      resultados.forEach(cliente => {
        const item = document.createElement("button");
        item.className = "list-group-item list-group-item-action";
        item.textContent = `${cliente.nombre} (${cliente.telefono})`;
        item.addEventListener("click", () => {
          // Guardar cliente existente en hidden
          clienteHidden.value = cliente.id;
          clienteHidden.dataset.direccion = cliente.direccion || "";
          clienteHidden.dataset.label = cliente.label || "";

          cargarDirecciones(cliente.id, direccionSelect);
          cardCliente.classList.add("d-none");
          cardCita.classList.remove("d-none");
        });
        resultadosCliente.appendChild(item);
      });
    } catch (err) {
      console.error("Error buscando cliente:", err);
    }
  });

  // Crear nuevo cliente (solo copia datos, no AJAX)
  initClienteCreate(
    btnCrearCliente,
    clienteForm,
    clienteHidden,
    cardCliente,
    cardCita
  );

  // Paso 3: Resumen
  const btnResumen = document.getElementById("btnResumen");
  if (btnResumen && cardResumen) {
    btnResumen.addEventListener("click", () => {
      // Validación mínima antes de avanzar
      const nombre = document.getElementById("id_nombre_hidden").value.trim();
      const fecha = document.getElementById("id_fecha").value;

      if (!nombre) {
        alert("El nombre del cliente es obligatorio");
        return;
      }
      if (!fecha) {
        alert("La fecha de la cita es obligatoria");
        return;
      }

      // Usar SIEMPRE los hidden para rellenar el resumen
      const telefono = document.getElementById("id_telefono_hidden").value || "—";
      const direccion = document.getElementById("id_address_hidden").value || "";
      const label = document.getElementById("id_label_hidden").value || "";

      document.getElementById("resCliente").textContent = nombre;
      document.getElementById("resTelefono").textContent = telefono;
      document.getElementById("resDireccion").textContent =
        label ? `${label} — ${direccion}` : direccion || "—";

      document.getElementById("resFecha").textContent = fecha;
      document.getElementById("resOferta").textContent =
        document.getElementById("id_oferta").value || "—";

      // NUEVO: número de instalación
      const numeroInstalacionInput = document.getElementById("id_numero_instalacion");
      if (numeroInstalacionInput) {
        document.getElementById("resNumeroInstalacion").textContent =
          numeroInstalacionInput.value || "0";
      }

      cardCita.classList.add("d-none");
      cardResumen.classList.remove("d-none");
    });
  }
});
