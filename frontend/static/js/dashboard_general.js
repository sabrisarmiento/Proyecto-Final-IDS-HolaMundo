(function () {
  "use strict";

  const CSS = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

  let barChart;
  let lineChart;

  function cerrarModal(id) {
    document.getElementById(id)?.classList.add("hidden");
  }

  function abrirModal(id) {
    document.getElementById(id)?.classList.remove("hidden");
  }

  document.addEventListener("click", function (e) {
    const cerrar = e.target.closest(".js-cerrar-modal");
    if (cerrar) {
      const target = cerrar.dataset.target;
      if (target) cerrarModal(target);
      return;
    }
    if (e.target.classList.contains("dg-modal-overlay")) {
      e.target.classList.add("hidden");
    }
  });

  document.getElementById("btn-abrir-crear-usuario")?.addEventListener("click", function () {
    abrirModal("modal-crear-usuario");
  });

  document.getElementById("btn-abrir-crear-rol")?.addEventListener("click", function () {
    abrirModal("modal-crear-rol");
  });

  document.getElementById("tabla-usuarios")?.addEventListener("click", function (e) {
    const btnEditar = e.target.closest(".js-editar-usuario");
    if (!btnEditar) return;

    const fila = btnEditar.closest("tr");
    if (!fila) return;
    const { id, nombre, apellido, correo, idRol } = fila.dataset;

    document.getElementById("eu-id").value       = id;
    document.getElementById("eu-nombre").value   = nombre;
    document.getElementById("eu-apellido").value = apellido;
    document.getElementById("eu-correo").value   = correo;
    document.getElementById("eu-nombre-label").textContent = nombre + " " + apellido;

    const sel = document.getElementById("eu-rol");
    if (sel && idRol) sel.value = idRol;

    const form = document.getElementById("form-editar-usuario");
    if (form) form.action = "/dashboard/usuarios/" + id;

    abrirModal("modal-editar-usuario");
  });

  function renderBarCursos() {
    const canvas = document.getElementById("chart-cursos");
    if (!canvas) return;
    let cursos = [];
    try { cursos = JSON.parse(document.getElementById("data-cursos")?.textContent || "[]"); }
    catch (_) { return; }
    if (!cursos.length) return;

    const labels  = cursos.map(function (c) { return c.catedra || c.materia || "Curso " + c.id_curso; });
    const activos = cursos.map(function (c) { return c.activos  || 0; });
    const abandono = cursos.map(function (c) { return c.abandono || 0; });

    barChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          { label: "Activos",  data: activos,  backgroundColor: CSS("--color-secondary") || "#111D4A", borderRadius: 6, borderSkipped: false },
          { label: "Abandono", data: abandono, backgroundColor: CSS("--color-primary") || "#92140C", borderRadius: 6, borderSkipped: false },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom",
          labels: { color: CSS("--color-chart") }
         } },
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 1, color: CSS("--color-chart") } },
          x: { grid: { display: false }, ticks: { color: CSS("--color-chart") } },
        },
      },
    });
  }

  function renderLineHistorico() {
    const canvas = document.getElementById("chart-historico");
    if (!canvas) return;
    let historico = [];
    try { historico = JSON.parse(document.getElementById("data-historico")?.textContent || "[]"); }
    catch (_) { return; }
    if (!historico.length) return;

    lineChart = new Chart(canvas, {
      type: "line",
      data: {
        labels: historico.map(function (h) { return h.anio; }),
        datasets: [{
          label: "Promedio general",
          data: historico.map(function (h) { return h.promedio_notas; }),
          borderColor: CSS("--color-primary") || "#92140C",
          backgroundColor: "rgba(146,20,12,0.1)",
          tension: 0.35,
          pointRadius: 5,
          pointHoverRadius: 7,
          fill: true,
          borderWidth: 2.5,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function (ctx) { return " Promedio: " + ctx.parsed.y.toFixed(2); } } },
        },
        scales: {
          y: { min: 0, max: 10, ticks: { stepSize: 2, color: CSS("--color-chart") }, grid: { color: CSS("--color-chart-border")} },
          x: { grid: { display: false }, ticks: { color: CSS("--color-chart") } },
        },
      },
    });
  }

  window.addEventListener("load", function () {
  renderBarCursos();
  renderLineHistorico();
  });

  window.addEventListener("themeChanged", function () {
    if (barChart) barChart.destroy();
    if (lineChart) lineChart.destroy();

    renderBarCursos();
    renderLineHistorico();
});

})();
