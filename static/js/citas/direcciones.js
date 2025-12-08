export function cargarDirecciones(clienteId, direccionSelect) {
  direccionSelect.innerHTML = "<option value=''>--- Cargando... ---</option>";
  fetch(`/locations/direcciones/${clienteId}/`)
    .then(res => res.json())
    .then(data => {
      direccionSelect.innerHTML = data.length
        ? "<option value=''>--- Selecciona dirección ---</option>"
        : "<option value=''>Sin dirección definida</option>";
      data.forEach(dir => {
        direccionSelect.appendChild(new Option(
          dir.label ? `${dir.label} - ${dir.address}` : dir.address,
          dir.id
        ));
      });
    });
}
