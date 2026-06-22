var PRESET_ICONS = [
  'fa-solid fa-code', 'fa-solid fa-database', 'fa-solid fa-network-wired',
  'fa-solid fa-terminal', 'fa-solid fa-laptop-code', 'fa-solid fa-brain',
  'fa-solid fa-robot', 'fa-solid fa-shield-halved', 'fa-solid fa-chart-bar',
  'fa-solid fa-flask', 'fa-solid fa-microchip', 'fa-solid fa-layer-group',
  'fa-solid fa-sitemap', 'fa-solid fa-server', 'fa-solid fa-bug',
  'fa-solid fa-gear', 'fa-solid fa-calculator', 'fa-solid fa-book',
  'fa-solid fa-graduation-cap', 'fa-brands fa-github'
];

function buildIconOptions() {
  var none = '<button type="button" class="icon-option icon-option--none" title="Sin ícono" onclick="selectIcon(this, \'\')">—</button>';
  return none + PRESET_ICONS.map(function(icon) {
    return '<button type="button" class="icon-option" title="' + icon + '" onclick="selectIcon(this, \'' + icon + '\')">' +
           '<i class="' + icon + '"></i></button>';
  }).join('');
}

function addTemaRow() {
  var row = document.createElement('div');
  row.className = 'config-row tema-row';
  row.innerHTML =
    '<div class="config-field"><label class="config-label">Nombre</label>' +
    '<input class="config-input" type="text" name="temas_nombre[]" placeholder="Ej: Python" required></div>' +
    '<div class="config-field"><label class="config-label">Ícono</label>' +
    '<div class="icon-picker-wrapper">' +
    '<input type="hidden" name="temas_icono[]" value="">' +
    '<button type="button" class="icon-picker-btn" onclick="toggleIconPicker(this)">—</button>' +
    '<div class="icon-picker-dropdown">' + buildIconOptions() + '</div>' +
    '</div></div>' +
    '<button type="button" class="config-btn-remove" onclick="this.closest(\'.tema-row\').remove()">✕</button>';
  document.getElementById('temas-list').appendChild(row);
}

function toggleIconPicker(btn) {
  var dropdown = btn.nextElementSibling;
  var isOpen = dropdown.classList.contains('open');
  document.querySelectorAll('.icon-picker-dropdown.open').forEach(function(d) {
    d.classList.remove('open');
  });
  if (!isOpen) dropdown.classList.add('open');
}

function selectIcon(optionBtn, icon) {
  var dropdown = optionBtn.closest('.icon-picker-dropdown');
  var wrapper = dropdown.closest('.icon-picker-wrapper');
  wrapper.querySelector('input[type="hidden"]').value = icon;
  var previewBtn = wrapper.querySelector('.icon-picker-btn');
  if (icon) {
    previewBtn.innerHTML = '<i class="' + icon + '"></i>';
  } else {
    previewBtn.innerHTML = '—';
  }
  dropdown.classList.remove('open');
}

document.addEventListener('click', function(e) {
  if (!e.target.closest('.icon-picker-wrapper')) {
    document.querySelectorAll('.icon-picker-dropdown.open').forEach(function(d) {
      d.classList.remove('open');
    });
  }
});
