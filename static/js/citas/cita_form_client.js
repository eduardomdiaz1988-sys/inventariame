import { initClienteCreate } from "./cliente_create.js";
import { cargarDirecciones } from "./direcciones.js";

document.addEventListener("DOMContentLoaded", () => {

  // ============================================================
  //  ELEMENTOS DEL WIZARD
  // ============================================================
  const cardCliente = document.getElementById("card-cliente");
  const cardCita = document.getElementById("card-cita");
  const cardResumen = document.getElementById("card-resumen");

  const clienteHidden = document.getElementById("id_cliente_hidden");
  const nombreHidden = document.getElementById("id_nombre_hidden");
  const telefonoHidden = document.getElementById("id_telefono_hidden");
  const addressHidden = document.getElementById("id_address_hidden");
  const latHidden = document.getElementById("id_lat_hidden");
  const lngHidden = document.getElementById("id_lng_hidden");
  const labelHidden = document.getElementById("id_label_hidden");

  // ============================================================
  //  TIPO DE CLIENTE (SÍ / NO)
  // ============================================================
  const tipoRadios = document.querySelectorAll('input[name="cliente_tipo"]');
  const busquedaCliente = document.getElementById("busquedaCliente");
  const formNuevoCliente = document.getElementById("formNuevoCliente");
  const resultadosCliente = document.getElementById("resultados_cliente");

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

  // ============================================================
  //  CLIENTE NUEVO → initClienteCreate()
  // ============================================================
  initClienteCreate(
    document.getElementById("btnCrearCliente"),
    clienteHidden,
    cardCliente,
    cardCita
  );

  // ============================================================
  //  BUSCADOR DE CLIENTE EXISTENTE
  // ============================================================
  const buscadorCliente = document.getElementById("buscador_cliente");

  if (buscadorCliente) {
    buscadorCliente.addEventListener("input", async () => {
      const q = buscadorCliente.value.trim();
      if (q.length < 2) {
        resultadosCliente.innerHTML = "";
        return;
      }

      const res = await fetch(`/clientes/api/buscar/?q=${encodeURIComponent(q)}`);
      const data = await res.json();

      resultadosCliente.innerHTML = "";

      data.forEach(cliente => {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "list-group-item list-group-item-action";
        item.textContent = `${cliente.nombre} (${cliente.telefono})`;

        item.addEventListener("click", () => {
          clienteHidden.value = cliente.id;
          nombreHidden.value = cliente.nombre || "";
          telefonoHidden.value = cliente.telefono || "";

          if (cliente.direccion) {
            addressHidden.value = cliente.direccion.address || "";
            latHidden.value = cliente.direccion.latitude || "";
            lngHidden.value = cliente.direccion.longitude || "";
            labelHidden.value = cliente.direccion.label || "";
          }

          cardCliente.classList.add("d-none");
          cardCita.classList.remove("d-none");

          resultadosCliente.innerHTML = "";
          buscadorCliente.value = "";
        });

        resultadosCliente.appendChild(item);
      });
    });
  }

  // ============================================================
  //  CALENDARIO
  // ============================================================
  if (document.getElementById("id_fecha")) {
    flatpickr("#id_fecha", {
      enableTime: true,
      dateFormat: "Y-m-d H:i",
      time_24hr: true,
      minDate: "today",
      locale: "es"
    });
  }

  // ============================================================
  //  OFERTAS (PASO 2)
  // ============================================================
  const buscador = document.getElementById("buscador_oferta");
  const resultados = document.getElementById("resultados_oferta");
  const btnAgregar = document.getElementById("btnAgregarOferta");
  const contenedor = document.getElementById("ofertas_seleccionadas");

  let ofertaSeleccionada = null;

  buscador.addEventListener("input", function () {
    const q = this.value;
    if (q.length < 2) {
      resultados.innerHTML = "";
      ofertaSeleccionada = null;
      return;
    }

    fetch(`/citas/buscar-ofertas/?q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(data => {
        resultados.innerHTML = "";

        data.forEach(oferta => {
          const item = document.createElement("button");
          item.type = "button";
          item.className = "list-group-item list-group-item-action";
          item.textContent = `${oferta.nombre} (${oferta.valor} €)`;

          item.onclick = () => {
            buscador.value = oferta.nombre;
            ofertaSeleccionada = oferta;
            resultados.innerHTML = "";
          };

          resultados.appendChild(item);
        });

        if (data.length === 0) {
          const empty = document.createElement("div");
          empty.className = "list-group-item";
          empty.textContent = "Sin resultados";
          resultados.appendChild(empty);
        }
      });
  });

  btnAgregar.addEventListener("click", function () {
    if (!ofertaSeleccionada) {
      alert("Debes seleccionar una oferta primero.");
      return;
    }

    const existente = document.querySelector(`#oferta_${ofertaSeleccionada.id}`);
    if (existente) {
      const cantidadInput = existente.querySelector("input[name='cantidad[]']");
      cantidadInput.value = parseInt(cantidadInput.value) + 1;
      return;
    }

    const div = document.createElement("div");
    div.className = "input-group mb-2";
    div.id = `oferta_${ofertaSeleccionada.id}`;

    div.innerHTML = `
      <span class="input-group-text">${ofertaSeleccionada.nombre}</span>
      <input type="hidden" name="ofertas[]" value="${ofertaSeleccionada.id}">
      <input type="number" name="cantidad[]" value="1" min="1" class="form-control" style="max-width:100px;">
      <button type="button" class="btn btn-outline-danger">x</button>
    `;

    div.querySelector("button").addEventListener("click", () => div.remove());

    contenedor.appendChild(div);

    buscador.value = "";
    ofertaSeleccionada = null;
  });

  // ============================================================
  //  PASO 3: RESUMEN FINAL
  // ============================================================
  const btnResumen = document.getElementById("btnResumen");

  btnResumen.addEventListener("click", () => {
    const ofertasSeleccionadas = document.querySelectorAll("#ofertas_seleccionadas .input-group");

    if (ofertasSeleccionadas.length === 0) {
      alert("Debes seleccionar al menos una oferta antes de continuar.");
      return;
    }

    cardCita.classList.add("d-none");
    cardResumen.classList.remove("d-none");

    document.getElementById("resCliente").textContent = nombreHidden.value;
    document.getElementById("resTelefono").textContent = telefonoHidden.value;
    document.getElementById("resDireccion").textContent = addressHidden.value;
    document.getElementById("resFecha").textContent = document.getElementById("id_fecha").value;
    document.getElementById("resNumeroInstalacion").textContent = document.getElementById("id_numero_instalacion").value;
    document.getElementById("resObservaciones").textContent = document.getElementById("id_observaciones").value;

    const resumenOfertas = document.getElementById("resOfertas");
    resumenOfertas.innerHTML = "";

    ofertasSeleccionadas.forEach(div => {
      const nombre = div.querySelector(".input-group-text").textContent;
      const cantidad = div.querySelector("input[name='cantidad[]']").value;

      const li = document.createElement("li");
      li.textContent = `${nombre} x${cantidad}`;
      resumenOfertas.appendChild(li);
    });
  });

});
