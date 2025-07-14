let sidebarOpen = false;
let accountMenuOpen = false;
let isMobile = false;

document.addEventListener("DOMContentLoaded", () => {
  function initLucide() {
    if (window.lucide && typeof window.lucide.replace === "function") {
      window.lucide.replace();
    } else {
      setTimeout(initLucide, 50);
    }
  }
  initLucide();

  window.addEventListener("resize", checkScreenSize);
  document.addEventListener("click", handleOutsideClick);
  checkScreenSize();
});

function checkScreenSize() {
  isMobile = window.innerWidth < 768;
  if (!isMobile) {
    closeSidebar();
  }
}

function toggleSidebar() {
  sidebarOpen = !sidebarOpen;
  updateSidebarState();
}

function closeSidebar() {
  sidebarOpen = false;
  updateSidebarState();
}

function updateSidebarState() {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.querySelector(".sidebar-overlay");
  const menuIcon = document.querySelector(".menu-icon");
  const closeIcon = document.querySelector(".close-icon");

  if (sidebarOpen) {
    sidebar.classList.add("open");
    overlay.classList.add("show");
    menuIcon.classList.add("hidden");
    closeIcon.classList.remove("hidden");
  } else {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
    menuIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
  }

  if (window.lucide && typeof window.lucide.replace === "function") {
    window.lucide.replace();
  }
}

function toggleAccountMenu() {
  accountMenuOpen = !accountMenuOpen;
  updateAccountMenuState();
}

function closeAccountMenu() {
  accountMenuOpen = false;
  updateAccountMenuState();
}

function updateAccountMenuState() {
  const dropdown = document.getElementById("accountDropdown");

  if (accountMenuOpen) {
    dropdown.classList.add("show");
  } else {
    dropdown.classList.remove("show");
  }
}

function handleOutsideClick(event) {
  const accountBox = document.querySelector(".account-box");
  const accountDropdown = document.getElementById("accountDropdown");
  const sidebar = document.getElementById("sidebar");

  if (accountMenuOpen && !accountBox.contains(event.target)) {
    closeAccountMenu();
  }

  if (sidebarOpen && !sidebar.contains(event.target) && !event.target.closest(".mobile-menu-btn")) {
    closeSidebar();
  }
}
