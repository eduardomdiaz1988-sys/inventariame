import { initTipoUsuarioForm } from "./tipo_usuario.js";
import { initValidarUsuario } from "./validar_usuario.js";
import { initValidarPassword } from "./validar_password.js";

document.addEventListener("DOMContentLoaded", () => {
  initTipoUsuarioForm();
  initValidarUsuario();
  initValidarPassword();
});
