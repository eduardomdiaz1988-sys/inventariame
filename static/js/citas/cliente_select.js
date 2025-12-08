export function initClienteSelect(clienteSelect, clienteHidden, cardCliente, cardCita, cargarDirecciones) {
  clienteSelect.addEventListener("change", () => {
    if (clienteSelect.value) {
      clienteHidden.value = clienteSelect.value;
      cardCliente.classList.add("d-none");
      cardCita.classList.remove("d-none");
      cargarDirecciones(clienteSelect.value);
    }
  });
}
