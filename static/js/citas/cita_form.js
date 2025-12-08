import { initClienteSelect } from "./cliente_select.js";
import { initClienteCreate } from "./cliente_create.js";
import { cargarDirecciones } from "./direcciones.js";


document.addEventListener("DOMContentLoaded", () => {

  const clienteSelect = document.getElementById("id_cliente");
  const clienteHidden = document.getElementById("id_cliente_hidden");
  const btnCrearCliente = document.getElementById("btnCrearCliente");
  const clienteForm = document.getElementById("clienteForm");
  const cardCliente = document.getElementById("card-cliente");
  const cardCita = document.getElementById("card-cita");
  const direccionSelect = document.getElementById("id_direccion");
  
  flatpickr("#id_fecha", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: true,
    minDate: "today",
    locale: "es"
  });

  initClienteSelect(clienteSelect, clienteHidden, cardCliente, cardCita, (id) => cargarDirecciones(id, direccionSelect));
  initClienteCreate(btnCrearCliente, clienteForm, clienteSelect, clienteHidden, cardCliente, cardCita, (id) => cargarDirecciones(id, direccionSelect));
  console.log("cardCliente:", cardCliente);
  console.log("cardCita:", cardCita);

});
