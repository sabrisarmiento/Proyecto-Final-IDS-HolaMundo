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

function confirmarEliminarEval(nombreEval, cant) {
    var tieneNotas = parseInt(cant, 10) > 0;
    if (tieneNotas) {
        return confirm(
            'Estas seguro de que queres eliminar la columna de "' + nombreEval + '"?\n\n' +
            'Esta accion eliminara todas las notas cargadas en esta evaluacion para todos los estudiantes\n\n' +
            'Esta operacin no se puede deshacer'
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

let removeStudentForm = null;
function openRemoveStudentModal(form) {
    removeStudentForm = form;
    openModal("remove-student-modal");
}

function confirmRemoveStudent() {
    if (removeStudentForm) {
        removeStudentForm.submit();
    }
}

function toggleDeleteMode() {
    const form = document.getElementById("delete-teams-form");
    document.querySelectorAll(".team-checkbox").forEach(cb => cb.classList.toggle("hidden"));
    form.classList.toggle("hidden");
    const warning = document.getElementById("delete-warning");
    if (form.classList.contains("hidden")) {
        warning.classList.add("hidden");
    } else {
        warning.innerHTML = "Seleccioná uno o más equipos y luego presioná <strong>Confirmar eliminación</strong>.";
        warning.classList.remove("hidden");
    }
    document.querySelector(".btn-danger").textContent = form.classList.contains("hidden") ? "Eliminar equipos" : "Cancelar";
}

function submitDeleteTeams() {
    closeModal("delete-teams-modal");
    document.getElementById("delete-teams-form").submit();
}

document.addEventListener("DOMContentLoaded", () => {
    const deleteForm = document.getElementById("delete-teams-form");
    if (!deleteForm) return;
    deleteForm.addEventListener("submit", (e) => {
        const selected = [...document.querySelectorAll(".team-checkbox:checked")].map(cb => cb.value);
        if (!selected.length) {
            e.preventDefault();
            const warning = document.getElementById("delete-warning");
            warning.innerHTML = "<strong>⚠ Atención:</strong> Seleccioná al menos un equipo para continuar.";
            warning.classList.remove("hidden");
            return;
        }
        e.preventDefault();
        document.getElementById("selected-teams").value = selected.join(",");
        openModal("delete-teams-modal");
    });
});

function filterTeams() {
    const searchInput = document
        .getElementById("team-search")
        .value
        .toLowerCase();
    const teams = document.querySelectorAll(".searchable-team");
    teams.forEach(team => {
        const teamName =
            team.dataset.teamName.toLowerCase();
        if (teamName.includes(searchInput)) {
            team.style.display = "";
        } else {
            team.style.display = "none";
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".padron-input").forEach(input => {
        input.addEventListener("input", async () => {
            const padron = input.value;
            const preview = input.closest("form").querySelector(".student-preview");
            if (!padron) return preview.innerHTML = "";
            try {
                const res = await fetch(`/cursos/${input.dataset.courseId}/buscar-alumno?padron=${padron}`);
                const data = await res.json();
                if (!data.found) {
                    preview.innerHTML = `<span class="student-not-found">Padrón inexistente en este curso</span>`;
                    return;
                }
                preview.innerHTML = `
                    <div class="student-found">
                        Alumno encontrado: <strong>${data.nombre} ${data.apellido}</strong><br>
                        Estado: <strong>${data.estado}</strong>
                    </div>`;
            } catch (error) {
                preview.innerHTML = `<span class="student-not-found">Error al buscar alumno</span>`;
            }
        });
    });
});

function togglePromocionable(checked) {
    var wrapper = document.getElementById('promo-table-wrapper');
    var hidden = document.getElementById('hidden-es-promocionable');

    if (hidden) hidden.value = checked ? '1' : '0';

    if (wrapper) {
        wrapper.style.display = checked ? '' : 'none';
    }

    var form = document.getElementById('form-toggle-promo');
    if (form) form.submit();
}

function toggleNotaMinima(checkbox) {
    var id = checkbox.dataset.id;
    var minInput = document.getElementById('min-' + id);
    var dash = document.getElementById('dash-' + id);
    if (!minInput || !dash) return;

    if (checkbox.checked) {
        minInput.classList.remove('hidden');
        dash.classList.add('hidden');
    } else {
        minInput.classList.add('hidden');
        dash.classList.remove('hidden');
        minInput.value = '';
    }
}

function filtrarPlanilla() {
    var equipoSel    = (document.getElementById('filtro-planilla-equipo')    || {}).value || '';
    var correctorSel = ((document.getElementById('filtro-planilla-corrector') || {}).value || '').trim().toLowerCase();
    var estadoSel    = (document.getElementById('filtro-planilla-estado')     || {}).value || '';

    document.querySelectorAll('.planilla-body-row').forEach(function (row) {
        var equipo     = (row.dataset.equipo     || '').toLowerCase();
        var correctoresRaw = (row.dataset.correctores || '').toLowerCase();
        var correctoresList = correctoresRaw
            ? correctoresRaw.split(',').map(function (c) { return c.trim(); }).filter(Boolean)
            : [];
        var estado = row.dataset.estado || '';

        var visible = true;

        if (equipoSel) {
            var buscarEquipo = equipoSel === '__sin_equipo__' ? '' : equipoSel.toLowerCase();
            if (equipo !== buscarEquipo) visible = false;
        }

        if (visible && correctorSel) {
            if (!correctoresList.some(function (c) { return c === correctorSel; })) {
                visible = false;
            }
        }

        if (visible && estadoSel) {
            if (estado !== estadoSel) visible = false;
        }

        row.style.display = visible ? '' : 'none';
    });

    document.querySelectorAll('.nota-by').forEach(function(el) {
    if (!correctorSel) {
        el.style.display = '';
        return;
    }
    var texto = (el.textContent || '').toLowerCase().replace('por ', '').trim();
    el.style.display = (texto === correctorSel) ? '' : 'none';
    });
}

function recalcularEstadoPlanilla() {
    var tabla = document.getElementById('planilla-table');
    if (!tabla) return;

    var esPromocionable = tabla.dataset.esPromocionable === '1';

    var promoConfig = {};
    try {
        promoConfig = JSON.parse(tabla.dataset.promoConfig || '{}');
    } catch (e) {
        promoConfig = {};
    }

    document.querySelectorAll('.planilla-body-row').forEach(function (row) {
        var tdEstado = row.querySelector('.td-estado-final');
        if (!tdEstado) return;

        var notas = {};
        try { notas = JSON.parse(row.dataset.notas || '{}'); } catch (e) {}

        var notasStr = {};
        Object.keys(notas).forEach(function (k) { notasStr[String(k)] = notas[k]; });

        var vals = Object.values(notasStr).filter(function (v) {
            return v !== '' && v !== null && v !== undefined;
        });

        var recursa = vals.some(function (v) { return parseFloat(v) < 4; });

        var estado;

        if (recursa) {
            estado = 'recursa';
        } else if (!esPromocionable) {
            estado = vals.length > 0 ? 'final' : 'final';
        } else {
            var puedePromo = true;

            Object.keys(promoConfig).forEach(function (idEvalStr) {
                var cfg = promoConfig[idEvalStr];
                if (!cfg || !cfg.cuenta) return;

                var notaAlumno = notasStr[idEvalStr];
                if (notaAlumno === '' || notaAlumno === null || notaAlumno === undefined) return;

                var minima = (cfg.nota_minima !== null && cfg.nota_minima !== undefined)
                    ? parseFloat(cfg.nota_minima)
                    : 4;

                if (parseFloat(notaAlumno) < minima) {
                    puedePromo = false;
                }
            });

            estado = puedePromo ? 'promociona' : 'final';
        }

        row.dataset.estado = estado;

        var badges = {
            'promociona': '<span class="estado-badge estado-promociona">Promociona</span>',
            'final':      '<span class="estado-badge estado-final">Final</span>',
            'recursa':    '<span class="estado-badge estado-recursa">Recursa</span>'
        };
        tdEstado.innerHTML = badges[estado] || '<span class="nota-vacia">—</span>';
    });
}

window.addEventListener('DOMContentLoaded', function () {
    recalcularEstadoPlanilla();
});

function createClass() {
    const data={
        fecha: document.getElementById("fecha-clase").value,
        semana:document.getElementById("semana-clase").value,
        temas:document.getElementById("temas-clase").value,
        tipo:document.getElementById("tipo-clase").value,
        modalidad:document.getElementById("modalidad-clase").value,
    }
    const courseId =document.getElementById("tab-calendar").dataset.courseId;

    fetch(`/cursos/${courseId}/clases/crear`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
}

function deleteClass(idClase) {

    console.log("Intentando borrar:", idClase);

    if (!confirm("¿Eliminar esta clase?")) {
        return;
    }

    const idCurso =
        document.getElementById("tab-calendar").dataset.courseId;

    fetch(`/cursos/${idCurso}/clases/${idClase}/eliminar`, {
        method: "DELETE"
    })
    .then(response => {
        console.log("Status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Respuesta:", data);
        location.reload();
    })
    .catch(error => {
        console.error(error);
    });
}