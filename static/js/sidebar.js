export function initSidebarToggle() {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");
  const overlay = document.getElementById("sidebar-overlay");

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("active");
      const isActive = sidebar.classList.contains("active");
      localStorage.setItem("sidebarActive", isActive ? "true" : "false");
    });

    // Restaurar estado al cargar
    const savedState = localStorage.getItem("sidebarActive");
    if (window.innerWidth >= 992) {
      if (savedState === "true") {
        sidebar.classList.add("active");
      } else {
        sidebar.classList.remove("active");
      }
    } else {
      sidebar.classList.remove("active");
    }
  }

  // Cerrar al pulsar overlay
  if (overlay) {
    overlay.addEventListener("click", () => {
      sidebar.classList.remove("active");
      localStorage.setItem("sidebarActive", "false");
    });
  }
}
