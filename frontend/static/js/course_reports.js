// Importación de alumnos (CSV) y exportación de informes (PDF) del curso.

document.addEventListener("DOMContentLoaded", () => {
  setupImportStudents();
  setupExportReports();
});

// ---------- Parte 2: Importar alumnos desde CSV ----------
function setupImportStudents() {
  const form = document.getElementById("import-students-form");
  if (!form) return;

  const dropzone = document.getElementById("csv-dropzone");
  const input = document.getElementById("csv-file-input");
  const fileName = document.getElementById("csv-file-name");
  const submit = document.getElementById("csv-submit");

  const setFile = (file) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".csv")) return;
    input.files = filesFromList(file);
    fileName.textContent = file.name;
    fileName.hidden = false;
    submit.disabled = false;
  };

  dropzone.addEventListener("click", () => input.click());
  input.addEventListener("change", () => setFile(input.files[0]));

  ["dragover", "dragenter"].forEach((ev) =>
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.classList.add("csv-dropzone--active");
    })
  );
  ["dragleave", "dragend", "drop"].forEach((ev) =>
    dropzone.addEventListener(ev, () =>
      dropzone.classList.remove("csv-dropzone--active")
    )
  );
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    setFile(e.dataTransfer.files[0]);
  });
}

// ---------- Parte 4: Exportar informes (PDF) ----------
function setupExportReports() {
  const form = document.getElementById("export-reports-form");
  if (!form) return;

  const notasCheck = document.getElementById("export-notas-check");
  const evalsBox = document.getElementById("export-evaluaciones");
  const message = document.getElementById("export-message");

  if (notasCheck && evalsBox) {
    notasCheck.addEventListener("change", () => {
      evalsBox.hidden = !notasCheck.checked;
    });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const alumnos = form.querySelector('input[name="alumnos"]').checked;
    const equipos = form.querySelector('input[name="equipos"]').checked;
    const notas = notasCheck && notasCheck.checked;
    const asistencia = form.querySelector('input[name="asistencia"]')?.checked;

    if (!alumnos && !equipos && !notas && !asistencia) {
      showMessage(message, "Seleccioná al menos una sección.", true);
      return;
    }

    const params = new URLSearchParams();
    if (alumnos) params.append("alumnos", "1");
    if (asistencia) params.append("asistencia", "1");
    if (equipos) params.append("equipos", "1");
    if (notas) {
      params.append("notas", "1");
      form
        .querySelectorAll('input[name="evaluaciones[]"]:checked')
        .forEach((cb) => params.append("evaluaciones[]", cb.value));
      if (form.querySelector('input[name="mostrar_corrector"]')?.checked)
        params.append("mostrar_corrector", "1");
      if (form.querySelector('input[name="incluir_estado_final"]')?.checked)
        params.append("incluir_estado_final", "1");
    }

    for (const field of ['materia', 'catedra', 'cuatrimestre', 'anio']) {
      const val = form.querySelector(`input[name="${field}"]`)?.value;
      if (val) params.append(field, val);
    }

    hideMessage(message);
    window.open(`${form.dataset.base}?${params.toString()}`, "_blank");
  });
}

// ---------- Helpers ----------
function filesFromList(file) {
  const dt = new DataTransfer();
  dt.items.add(file);
  return dt.files;
}

function showMessage(el, text, isError = false) {
  el.textContent = text;
  el.classList.toggle("form-message--error", isError);
  el.hidden = false;
}

function hideMessage(el) {
  el.hidden = true;
  el.textContent = "";
}
