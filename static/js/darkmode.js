export function initDarkModeToggle() {
  const toggle = document.getElementById("darkModeToggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.documentElement.dataset.theme =
        document.documentElement.dataset.theme === "light" ? "dark" : "light";
    });
  }
}
