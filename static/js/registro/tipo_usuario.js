export function initTipoUsuarioForm() {
  const tipoForm = document.getElementById("tipoUsuarioForm");
  const registroForm = document.getElementById("registroForm");
  const tipoHidden = document.getElementById("tipoUsuarioSeleccionado");

  if (!tipoForm || !registroForm || !tipoHidden) return;

  tipoForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const tipo = document.querySelector('input[name="tipo_usuario"]:checked');
    if (!tipo) {
      alert("Por favor selecciona una opción.");
      return;
    }
    tipoHidden.value = tipo.value;
    tipoForm.classList.add("d-none");
    registroForm.classList.remove("d-none");
  });
}
