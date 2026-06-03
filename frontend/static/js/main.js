//modal
function openModal(id) {
  document.getElementById(id).classList.add("active");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("active");
}

document.addEventListener("click", function (event) {
  if (event.target.classList.contains("modal-container")) {
    event.target.classList.remove("active");
  }
});

//dropdown
function toggleDropdown(id) {
  document.getElementById(id).classList.toggle("active");
}

document.addEventListener("click", function (event) {
  document.querySelectorAll(".dropdown").forEach((dropdown) => {
    if (!dropdown.contains(event.target)) {
      const menu = dropdown.querySelector(".dropdown-menu");
      if (menu) {
        menu.classList.remove("active");
      }
    }
  });
});

function changeSubject(id) {
  if (id === "general") {
    window.location.href = window.location.pathname
  } else {
    window.location.href = window.location.pathname + "?subject=" + id
  }
}
