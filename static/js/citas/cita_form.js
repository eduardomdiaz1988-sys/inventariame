document.addEventListener("DOMContentLoaded", () => {
  console.log("¿JS cargado?");

  // ============================
  //  FLATPICKR
  // ============================
  if (document.getElementById("id_fecha")) {
    flatpickr("#id_fecha", {
      enableTime: true,
      dateFormat: "Y-m-d H:i",
      time_24hr: true,
      locale: flatpickr.l10ns.es
    });
  }

  // ============================
  //  BUSCADOR DE OFERTAS
  // ============================
  const buscador = document.getElementById("buscador_oferta");
  const resultados = document.getElementById("resultados_oferta");
  const contenedor = document.getElementById("ofertas_seleccionadas");
  const btnAgregar = document.getElementById("btnAgregarOferta");

  let ofertaSeleccionada = null;

  if (buscador) {
    buscador.addEventListener("input", async () => {
      const q = buscador.value.trim();
      if (q.length < 2) {
        resultados.innerHTML = "";
        ofertaSeleccionada = null;
        return;
      }

      try {
        const response = await fetch(`/citas/buscar-ofertas/?q=${encodeURIComponent(q)}`);
        const data = await response.json();

        resultados.innerHTML = "";

        data.forEach(oferta => {
          const item = document.createElement("button");
          item.type = "button";
          item.className = "list-group-item list-group-item-action";
          item.textContent = `${oferta.nombre} (${oferta.valor} €)`;

          item.addEventListener("click", () => {
            buscador.value = oferta.nombre;
            ofertaSeleccionada = oferta;
            resultados.innerHTML = "";
          });

          resultados.appendChild(item);
        });

        if (data.length === 0) {
          const empty = document.createElement("div");
          empty.className = "list-group-item";
          empty.textContent = "Sin resultados";
          resultados.appendChild(empty);
        }

      } catch (err) {
        console.error("Error buscando oferta:", err);
      }
    });
  }

  // ============================
  //  AGREGAR OFERTA
  // ============================
  if (btnAgregar) {
    btnAgregar.addEventListener("click", () => {
      if (!ofertaSeleccionada) {
        alert("Debes seleccionar una oferta primero.");
        return;
      }

      // Si ya existe, aumentar cantidad
      const existente = document.getElementById(`oferta_${ofertaSeleccionada.id}`);
      if (existente) {
        const cantidadInput = existente.querySelector("input[name='cantidad']");
        cantidadInput.value = parseInt(cantidadInput.value) + 1;
        return;
      }

      // Crear bloque
      const div = document.createElement("div");
      div.className = "input-group mb-2";
      div.id = `oferta_${ofertaSeleccionada.id}`;

      div.innerHTML = `
        <span class="input-group-text">${ofertaSeleccionada.nombre}</span>
        <input type="hidden" name="ofertas" value="${ofertaSeleccionada.id}">
        <input type="number" name="cantidad" value="1" min="1" class="form-control" style="max-width:100px;">
        <button type="button" class="btn btn-outline-danger">x</button>
      `;

      div.querySelector("button").addEventListener("click", () => div.remove());

      contenedor.appendChild(div);

      buscador.value = "";
      ofertaSeleccionada = null;
    });
  }

  // ============================
  //  ELIMINAR OFERTAS PRECARGADAS
  // ============================
  document.querySelectorAll("#ofertas_seleccionadas .input-group").forEach(div => {
    const btn = div.querySelector("button");
    if (btn) {
      btn.addEventListener("click", () => div.remove());
    }
  });

  // ============================
  //  DEBUG ANTES DE ENVIAR
  // ============================
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault(); // ⛔ Detenemos el envío para ver los datos

    console.log("🧪 DEBUG: Datos antes de enviar el formulario");

    const formData = new FormData(e.target);

    const ofertas = formData.getAll("ofertas");
    const cantidades = formData.getAll("cantidad");

    console.log("→ Ofertas:", ofertas);
    console.log("→ Cantidades:", cantidades);

    // Mostrar todos los campos del formulario
    for (const [key, value] of formData.entries()) {
      console.log(`→ ${key}: ${value}`);
    }

    console.log("🧪 Fin del debug\n");

    // Si quieres enviar el formulario después del debug:
    e.target.submit();
  });

});
