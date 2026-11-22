const menuToggle = document.querySelector(".mobile-menu-toggle");

if (menuToggle) {
  menuToggle.hidden = false;
  menuToggle.addEventListener("click", () => {
    const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isExpanded));
  });
}