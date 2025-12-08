import { initSidebarToggle } from "./sidebar.js";
import { initDarkModeToggle } from "./darkmode.js";
import { initVoiceSearch } from "./voice_search.js";

document.addEventListener("DOMContentLoaded", () => {
  initSidebarToggle();
  initDarkModeToggle();

  const micButton = document.getElementById("micButton");
  const searchInput = document.getElementById("searchInput");
  if (micButton && searchInput) {
    initVoiceSearch(micButton, searchInput);
  }
});

