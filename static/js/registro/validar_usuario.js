export function initValidarUsuario() {
  const usernameInput = document.getElementById("id_username");
  if (!usernameInput) return;

  usernameInput.addEventListener("blur", () => {
    const username = usernameInput.value.trim();
    if (username.length > 2) {
      fetch(`/verificar-usuario/?username=${username}`)
        .then(res => res.json())
        .then(data => {
          const feedback = usernameInput.nextElementSibling;
          if (data.exists) {
            usernameInput.classList.add("is-invalid");
            feedback.textContent = "Este nombre de usuario ya está en uso.";
          } else {
            usernameInput.classList.remove("is-invalid");
            usernameInput.classList.add("is-valid");
            feedback.textContent = "";
          }
        });
    }
  });
}
