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