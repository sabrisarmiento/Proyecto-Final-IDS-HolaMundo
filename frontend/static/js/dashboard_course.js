(function () {
  "use strict";

  const CSS = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

  function setInner(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
  }

  function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function renderStats(d) {
    setText("dash-total-alumnos",   d.alumnos.total);
    setText("dash-activos",         d.alumnos.activos);
    setText("dash-abandonaron",     d.alumnos.abandonaron);
    setText("dash-equipos",         d.equipos);
    setText("dash-promedio",        d.promedio_general !== null ? d.promedio_general : "—");

    const c = d.clasificacion;
    setText("dash-promocionados", c.promocionados);
    setText("dash-van-final",     c.van_a_final);
    setText("dash-recursantes",   c.recursantes);
  }

// rendimiento por evaluacion (barritas)

  function renderBarChart(evaluaciones) {
    const canvas = document.getElementById("chart-rendimiento");
    if (!canvas) return;

    const labels  = evaluaciones.map((e) => e.nombre || `Eval ${e.id}`);
    const data    = evaluaciones.map((e) => e.promedio ?? 0);
    const hasData = data.some((v) => v > 0);

    if (!hasData) {
      canvas.closest(".dash-chart-card").querySelector(".dash-chart-empty")
        ?.classList.remove("hidden");
      canvas.classList.add("hidden");
      return;
    }

    const colorOk  = CSS("--color-3")  || "#92140C";
    const colorLow = CSS("--color-4")  || "#C9867E";
    const barColors = data.map((v) => (v >= 4 ? colorOk : colorLow));

    new Chart(canvas, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Promedio",
            data,
            backgroundColor: barColors,
            borderRadius: 8,
            borderSkipped: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` Promedio: ${ctx.parsed.y.toFixed(1)}`,
            },
          },
        },
        scales: {
          y: {
            min: 0,
            max: 10,
            ticks: { stepSize: 2 },
            grid: { color: "rgba(0,0,0,0.06)" },
          },
          x: { grid: { display: false } },
        },
      },
    });
  }

// asistencia (torta)

  function renderAsistenciaChart(asistencia) {
    const canvas = document.getElementById("chart-asistencia");
    if (!canvas) return;

    const { regulares = 0, en_riesgo = 0, sin_datos = 0 } = asistencia;
    const total = regulares + en_riesgo + sin_datos;

    if (total === 0) {
      canvas.closest(".dash-chart-card").querySelector(".dash-chart-empty")
        ?.classList.remove("hidden");
      canvas.classList.add("hidden");
      return;
    }

    setText("dash-asist-regulares",  regulares);
    setText("dash-asist-en-riesgo",  en_riesgo);
    if (total > 0) {
      setText("dash-asist-pct", Math.round((regulares / total) * 100) + "%");
    }

    new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: ["Regular", "En riesgo", "Sin datos"],
        datasets: [
          {
            data: [regulares, en_riesgo, sin_datos],
            backgroundColor: [
              CSS("--color-3") || "#92140C",
              CSS("--color-4") || "#C9867E",
              CSS("--color-6") || "#FFE4C5",
            ],
            borderWidth: 0,
            hoverOffset: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "68%",
        plugins: {
          legend: {
            position: "bottom",
            labels: { padding: 16, font: { size: 12 } },
          },
        },
      },
    });
  }

// estado cursada (torta)

  function renderEstadoChart(clasificacion, esPromocionable) {
    const canvas = document.getElementById("chart-estado");
    if (!canvas) return;

    const { promocionados, van_a_final, recursantes, abandonaron } = clasificacion;
    const total = promocionados + van_a_final + recursantes + abandonaron;

    if (total === 0) {
      canvas.closest(".dash-chart-card").querySelector(".dash-chart-empty")
        ?.classList.remove("hidden");
      canvas.classList.add("hidden");
      return;
    }

    const labels = esPromocionable
      ? ["Promociona", "Van a final", "Recursantes", "Abandonaron"]
      : ["Aprobados", "Van a final", "Recursantes", "Abandonaron"];

    new Chart(canvas, {
      type: "doughnut",
      data: {
        labels,
        datasets: [
          {
            data: [promocionados, van_a_final, recursantes, abandonaron],
            backgroundColor: [
              "#22c55e",
              CSS("--color-9")  || "#111D4A",
              CSS("--color-3")  || "#92140C",
              CSS("--color-8")  || "#887672",
            ],
            borderWidth: 0,
            hoverOffset: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "68%",
        plugins: {
          legend: {
            position: "bottom",
            labels: { padding: 16, font: { size: 12 } },
          },
        },
      },
    });
  }

  function showError(msg) {
    const el = document.getElementById("dash-curso-error");
    if (el) {
      el.textContent = msg;
      el.classList.remove("hidden");
    }
    document.getElementById("dash-curso-loading")?.classList.add("hidden");
    document.getElementById("dash-curso-content")?.classList.add("hidden");
  }

  function hideLoading() {
    const loading = document.getElementById("dash-curso-loading");
    const content = document.getElementById("dash-curso-content");
    if (loading) loading.style.display = "none";
    if (content) content.classList.remove("hidden");
  }

  async function loadDashboard(courseId) {
    try {
      const res  = await fetch(`/cursos/${courseId}/dashboard-data`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      const d    = json.dashboard;

      renderStats(d);
      renderBarChart(d.evaluaciones);
      renderAsistenciaChart(d.asistencia);
      renderEstadoChart(d.clasificacion, d.es_promocionable);
      hideLoading();
    } catch (err) {
      showError("No se pudieron cargar las estadísticas del curso.");
      console.error(err);
    }
  }

  window.addEventListener("DOMContentLoaded", function () {
    const courseId = document.getElementById("dash-curso-root")?.dataset.courseId;
    if (!courseId) return;

    if (typeof Chart !== "undefined") {
      loadDashboard(courseId);
    } else {
      window.addEventListener("load", () => loadDashboard(courseId));
    }
  });
})();