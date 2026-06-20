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
  const message = document.getElementById("import-message");

  const setFile = (file) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".csv")) {
      showMessage(message, "El archivo debe ser .csv", true);
      return;
    }
    input.files = filesFromList(file);
    fileName.textContent = file.name;
    fileName.hidden = false;
    submit.disabled = false;
    hideMessage(message);
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

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!input.files.length) return;

    submit.disabled = true;
    showMessage(message, "Importando…", false);

    try {
      const body = new FormData();
      body.append("file", input.files[0]);
      const res = await fetch(form.dataset.action, { method: "POST", body });
      const data = await res.json();

      if (res.ok && data.creados !== undefined) {
        let msg = `Se importaron ${data.creados} alumno(s).`;
        if (data.errores) msg += ` ${data.errores} fila(s) con error.`;
        showMessage(message, msg, data.errores > 0);
        if (data.creados > 0) {
          setTimeout(() => window.location.reload(), 1200);
        }
      } else {
        const detalle =
          (data.errors && data.errors[0] && data.errors[0].description) ||
          data.error ||
          "No se pudo importar el archivo.";
        showMessage(message, detalle, true);
        submit.disabled = false;
      }
    } catch (err) {
      showMessage(message, "Error de conexión al importar.", true);
      submit.disabled = false;
    }
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

function showMessage(el, text, isError) {
  if (!el) return;
  el.textContent = text;
  el.hidden = false;
  el.classList.toggle("form-message--error", !!isError);
}

function hideMessage(el) {
  if (!el) return;
  el.hidden = true;
}
