function switchTab(tabName, btnEl) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

    document.getElementById('tab-' + tabName).classList.remove('hidden');
    if (btnEl) btnEl.classList.add('active');
}

window.addEventListener('DOMContentLoaded', function () {
    const hash = window.location.hash;
    if (hash) {
        const tabName = hash.replace('#tab-', '').replace('#', '');
        const targetBtn = document.querySelector('.subnav-btn[onclick*="\'' + tabName + '\'"]');
        if (targetBtn) {
            switchTab(tabName, targetBtn);
        }
    }
});

function colorearNota(input) {
    const val = parseFloat(input.value);
    input.classList.remove('nota-aprobado', 'nota-reprobado');

    const idAlumno = input.name.replace('nota_', '');
    const dot = document.getElementById('dot-' + idAlumno);

    if (input.value === '' || isNaN(val)) {
        if (dot) { dot.classList.remove('dot-verde', 'dot-rojo'); }
        return;
    }

    if (val < 0 || val > 10) {
        input.value = Math.min(10, Math.max(0, val));
    }

    if (val >= 4) {
        input.classList.add('nota-aprobado');
        if (dot) { dot.classList.remove('dot-rojo'); dot.classList.add('dot-verde'); }
    } else {
        input.classList.add('nota-reprobado');
        if (dot) { dot.classList.remove('dot-verde'); dot.classList.add('dot-rojo'); }
    }

    recalcularPromedio();
}

function recalcularPromedio() {
    const inputs = document.querySelectorAll('.nota-input');
    let suma = 0;
    let count = 0;
    inputs.forEach(function (inp) {
        const val = parseFloat(inp.value);
        if (!isNaN(val)) {
            suma += val;
            count++;
        }
    });
    const display = document.getElementById('promedio-display');
    if (display) {
        display.textContent = count > 0 ? (suma / count).toFixed(1) : '—';
    }
}

function filtrarPorEquipo(equipoSeleccionado) {
    const cards = document.querySelectorAll('.grade-card');
    cards.forEach(function (card) {
        const equipoCard = card.getAttribute('data-equipo') || 'sin-equipo';
        if (!equipoSeleccionado || equipoSeleccionado === equipoCard) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
    recalcularPromedio();
}

/**
 * @param {string} nombreEval
 * @param {number} tieneNotas
 * @returns {boolean}
 */
function confirmarEliminarEval(nombreEval, cant) {
    var tieneNotas = parseInt(cant, 10) > 0;
    if (tieneNotas) {
        return confirm(
            '\u26A0\uFE0F \u00BFEst\u00E1s seguro de que quer\u00E9s eliminar la columna de "' + nombreEval + '"?\n\n' +
            'Esta acci\u00F3n eliminar\u00E1 todas las notas cargadas en esta evaluaci\u00F3n para todos los estudiantes.\n\n' +
            'Esta operaci\u00F3n no se puede deshacer.'
        );
    }
    return confirm('\u00BFEst\u00E1s seguro de que quer\u00E9s eliminar "' + nombreEval + '"?');
}

window.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.nota-input').forEach(function (input) {
        if (input.value !== '') {
            colorearNota(input);
        }
    });
    recalcularPromedio();
});

function toggleTeam(teamId) {
    const div = document.getElementById(`team-${teamId}`);
    if (!div) return;
    div.classList.toggle('hidden');
}