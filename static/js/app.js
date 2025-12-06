// Toggle de modo oscuro
(function() {
  const root = document.documentElement;
  const key = 'inventariame_theme';
  const saved = localStorage.getItem(key);
  if (saved) root.setAttribute('data-theme', saved);

  document.getElementById('darkModeToggle')?.addEventListener('click', () => {
    const current = root.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    localStorage.setItem(key, next);
  });

  document.getElementById("sidebarToggle")?.addEventListener("click", () => {
    document.getElementById("sidebar")?.classList.toggle("active");
  });

})();
