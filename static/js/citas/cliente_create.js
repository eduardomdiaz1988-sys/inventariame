export function initClienteCreate(btnCrearCliente, clienteForm, clienteSelect, clienteHidden, cardCliente, cardCita, cargarDirecciones) {
  btnCrearCliente.addEventListener("click", () => {
    const formData = new FormData(clienteForm);
    fetch("/clientes/create-ajax/", {
      method: "POST",
      body: formData,
      headers: { "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value }
    })
    .then(res => res.json())
    .then(data => {
      if (data.id) {
        clienteHidden.value = data.id;
        const option = new Option(
          `${data.nombre}${data.telefono ? " ("+data.telefono+")" : ""} — ${data.direccion || "Sin dirección definida"}`,
          data.id,
          true,
          true
        );
        clienteSelect.appendChild(option);
        cardCliente.classList.add("d-none");
        cardCita.classList.remove("d-none");
        cargarDirecciones(data.id);
      } else {
        alert("Error al crear cliente");
      }
    });
  });
}
