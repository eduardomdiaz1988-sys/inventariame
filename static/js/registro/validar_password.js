export function initValidarPassword() {
  const passwordInput = document.getElementById("id_password1");
  if (!passwordInput) return;

  passwordInput.addEventListener("input", () => {
    const value = passwordInput.value;
    const feedback = passwordInput.nextElementSibling;
    const strong = /(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}/.test(value);

    if (!strong) {
      passwordInput.classList.add("is-invalid");
      feedback.textContent = "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.";
    } else {
      passwordInput.classList.remove("is-invalid");
      passwordInput.classList.add("is-valid");
      feedback.textContent = "";
    }
  });
}
