export function initClienteCreate(
  btnCrearCliente,
  clienteForm,
  clienteSelect,
  clienteHidden,
  cardCliente,
  cardCita,
  cargarDirecciones
) {
  btnCrearCliente.addEventListener("click", () => {
    const formData = new FormData(clienteForm);

    // Capturamos los campos del mapa
    const address = document.getElementById("addressField")?.value || "";
    const latitude = document.getElementById("latField")?.value || "";
    const longitude = document.getElementById("lngField")?.value || "";
    const label = document.getElementById("labelField")?.value || "";

    formData.append("address", address);
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);
    formData.append("label", label);

    fetch("/clientes/create-ajax/", {
      method: "POST",
      body: formData,
      headers: { "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value }
    })
    .then(res => res.json())
    .then(data => {
      if (data.id) {
        // Guardamos el id y la dirección en dataset
        clienteHidden.value = data.id;
        clienteHidden.dataset.direccion = data.direccion || "";
        clienteHidden.dataset.label = data.label || "";

        // Rellenar automáticamente el campo direccion del formulario de cita
        const direccionSelect = document.getElementById("id_direccion");
        if (direccionSelect) {
          direccionSelect.innerHTML = ""; // limpiar opciones previas
          const option = new Option(
            `${data.label ? data.label+" — " : ""}${data.direccion}`,
            data.id,
            true,
            true
          );
          direccionSelect.appendChild(option);
        }

        cardCliente.classList.add("d-none");
        cardCita.classList.remove("d-none");

        // cargar direcciones del cliente (si quieres refrescar más de una)
        cargarDirecciones(data.id);
      } else {
        alert("Error al crear cliente");
      }
    });
  });
}
