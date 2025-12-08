export function initDarkModeToggle() {
  const darkModeBtns = [
    document.getElementById("darkModeToggle"),
    document.getElementById("darkModeToggleMobile")
  ].filter(Boolean);

  darkModeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const html = document.documentElement;
      const currentTheme = html.getAttribute("data-theme");
      const newTheme = currentTheme === "light" ? "dark" : "light";
      html.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
    });
  });

  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }
}
