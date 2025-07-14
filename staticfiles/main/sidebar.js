let sidebarOpen = false;
let accountMenuOpen = false;
let isMobile = false;

// Initialize the app
document.addEventListener("DOMContentLoaded", () => {
  // Check screen size
  checkScreenSize();

  // Add event listeners
  window.addEventListener("resize", checkScreenSize);
  document.addEventListener("click", handleOutsideClick);
});

// Screen size detection
function checkScreenSize() {
  isMobile = window.innerWidth < 768;
  if (!isMobile) {
    closeSidebar();
  }
}

// Sidebar functions
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
}

// Account menu functions
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

// Handle clicks outside of menus
function handleOutsideClick(event) {
  const accountBox = document.querySelector(".account-box");
  const accountDropdown = document.getElementById("accountDropdown");

  // Close account menu if clicking outside
  if (accountMenuOpen && !accountBox.contains(event.target)) {
    closeAccountMenu();
  }

  // Close sidebar if clicking outside
  if (sidebarOpen && !sidebar.contains(event.target)) {
    closeSidebar();
  }
}
