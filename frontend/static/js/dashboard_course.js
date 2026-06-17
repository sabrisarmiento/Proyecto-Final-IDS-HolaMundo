(function () {
  "use strict";

  const CSS = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

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
    setText("dash-promocionados", d.es_promocionable ? c.promocionados : "—");
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

    const { regulares = 0, en_riesgo = 0, sin_datos = 0, umbral = 75 } = asistencia;
    const total = regulares + en_riesgo + sin_datos;

    if (total === 0) {
      canvas.closest(".dash-chart-card").querySelector(".dash-chart-empty")
        ?.classList.remove("hidden");
      canvas.classList.add("hidden");
      return;
    }

    setText("dash-asist-regulares", regulares);
    setText("dash-asist-en-riesgo", en_riesgo);
    if (total > 0) {
      setText("dash-asist-pct", Math.round((regulares / total) * 100) + "%");
    }

    const umbralEl = document.getElementById("dash-asist-umbral");
    if (umbralEl) {
      umbralEl.textContent = `Umbral: ${umbral}% de asistencia`;
    }

    new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: [`Regular (≥${umbral}%)`, `En riesgo (<${umbral}%)`, "Sin datos"],
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
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: ${ctx.parsed} alumnos`,
            },
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
              CSS("--color-9") || "#111D4A",
              CSS("--color-3") || "#92140C",
              CSS("--color-8") || "#887672",
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

  window.addEventListener("DOMContentLoaded", function () {
    const dataEl = document.getElementById("dash-curso-data");
    if (!dataEl) return;

    let d;
    try {
      d = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.error("Error al leer dash-curso-data:", e);
      return;
    }

    renderStats(d);
    renderBarChart(d.evaluaciones);
    renderAsistenciaChart(d.asistencia);
    renderEstadoChart(d.clasificacion, d.es_promocionable);

    const loading = document.getElementById("dash-curso-loading");
    const content = document.getElementById("dash-curso-content");
    if (loading) loading.style.display = "none";
    if (content) content.classList.remove("hidden");
  });
})();