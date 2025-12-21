// cliente_create.js
export function initClienteCreate(
  btnCrearCliente,
  clienteHidden,
  cardCliente,
  cardCita
) {
  if (!btnCrearCliente) return;

  btnCrearCliente.addEventListener("click", () => {

    const nombre = document.getElementById("id_nombre")?.value.trim() || "";
    const telefono = document.getElementById("id_telefono")?.value.trim() || "";
    const address = document.getElementById("addressField")?.value || "";
    const lat = document.getElementById("latField")?.value || "";
    const lng = document.getElementById("lngField")?.value || "";
    const label = document.getElementById("labelField")?.value || "";

    if (!nombre) {
      alert("El nombre del cliente es obligatorio");
      return;
    }

    // Copiar valores a los hidden del formulario final
    document.getElementById("id_nombre_hidden").value = nombre;
    document.getElementById("id_telefono_hidden").value = telefono;
    document.getElementById("id_address_hidden").value = address;
    document.getElementById("id_lat_hidden").value = lat;
    document.getElementById("id_lng_hidden").value = lng;
    document.getElementById("id_label_hidden").value = label;

    // Avanzar al paso de cita
    cardCliente.classList.add("d-none");
    cardCita.classList.remove("d-none");
  });
}
