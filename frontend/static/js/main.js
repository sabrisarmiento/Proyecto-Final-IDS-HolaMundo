//modal
function openModal(id) {
  document.getElementById(id).classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeModal(id) {
  document.getElementById(id).classList.remove("active");
  document.body.style.overflow = "";
}

document.addEventListener("click", function(event){
  if (event.target.classList.contains("modal-container")) {
    closeModal(event.target.id);
  }
})

//dropdown
function toggleDropdown(id) {
  document.getElementById(id).classList.toggle("active")
}

document.addEventListener("click", function(event){
  document.querySelectorAll(".dropdown").forEach(dropdown => {
    if (!dropdown.contains(event.target)) {
      const menu=dropdown.querySelector(".dropdown-menu")
      if (menu) {
        menu.classList.remove("active");
      }
    }
  });
});