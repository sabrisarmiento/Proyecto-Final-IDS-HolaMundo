//modal
function openModal(id) {
  document.getElementById(id).classList.add("active");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("active");
}

document.addEventListener("click", function(event){
  if (event.target.classList.contains("modal-container")) {
    event.target.classList.remove("active")
  }
})

//dropdown
function toggleDropdown() {
  document.getElementById("dropdown-menu").classList.toggle("active")
}

document.addEventListener("click", function(event){
  const dropdown = document.querySelector(".dropdown")
  if (dropdown && !dropdown.contains(event.target)) {
    document.getElementById("dropdown-menu").classList.remove("active")
  }
})

function changeCourse(id) {
  if (id) {
    const currentPage = encodeURIComponent(window.location.pathname);
    window.location.href = "/set-course/" + id + "?next=" + currentPage;
  }
}