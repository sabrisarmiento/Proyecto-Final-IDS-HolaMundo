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
              CSS("--color-9") || "#111D4A",
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

  function renderAsistenciaClase(d) {
    const select = document.getElementById("dash-asist-clase");
    const countEl = document.getElementById("dash-asist-clase-count");
    const listEl = document.getElementById("dash-asist-clase-lista");
    if (!select || !listEl) return;

    const clases = d.clases_list || [];
    const alumnos = d.alumnos_list || [];
    const presentes = d.presentes || [];

    select.innerHTML = clases
      .map((c) => `<option value="${c.id_clase}">${c.fecha} — ${c.temas || "Clase " + c.id_clase}</option>`)
      .join("");

    function render() {
      const idClase = parseInt(select.value, 10);
      const checked = document.querySelector("input[name='asist-clase-filtro']:checked");
      const filtro = checked ? checked.value : "all";
      const presentSet = new Set(presentes.filter((p) => p[1] === idClase).map((p) => p[0]));

      let presentCount = 0;
      const rows = alumnos.map((a) => {
        const presente = presentSet.has(a.id_alumno);
        if (presente) presentCount += 1;
        return { a, presente };
      });

      countEl.textContent = `${presentCount} / ${alumnos.length} presentes`;

      const visibles = rows.filter((r) =>
        filtro === "all" ? true : filtro === "present" ? r.presente : !r.presente
      );

      listEl.innerHTML = visibles.length
        ? visibles
            .map((r) => {
              const cls = r.presente ? "dash-asist-badge--ok" : "dash-asist-badge--risk";
              const txt = r.presente ? "Presente" : "Ausente";
              return `<li class="dash-attendance-item"><span>${r.a.apellido}, ${r.a.nombre}</span><span class="dash-asist-badge ${cls}">${txt}</span></li>`;
            })
            .join("")
        : `<li class="dash-attendance-empty">Sin alumnos para este filtro</li>`;
    }

    if (clases.length) select.value = clases[clases.length - 1].id_clase;
    select.addEventListener("change", render);
    document
      .querySelectorAll("input[name='asist-clase-filtro']")
      .forEach((el) => el.addEventListener("change", render));
    render();
  }

  function renderAsistenciaAlumno(d) {
    const select = document.getElementById("dash-asist-alumno");
    const canvas = document.getElementById("chart-asist-alumno");
    const pctEl = document.getElementById("dash-asist-alumno-pct");
    const presEl = document.getElementById("dash-asist-alumno-presentes");
    if (!select || !canvas) return;

    const clases = d.clases_list || [];
    const alumnos = d.alumnos_list || [];
    const detalle = d.asistencia_detalle || [];
    const presentSet = new Set((d.presentes || []).map((p) => p[0] + "-" + p[1]));

    select.innerHTML = alumnos
      .map((a) => `<option value="${a.id_alumno}">${a.apellido}, ${a.nombre}</option>`)
      .join("");

    let chart = null;

    function render() {
      const idAlumno = parseInt(select.value, 10);
      const info = detalle.find((x) => x.id_alumno === idAlumno);
      if (pctEl) pctEl.textContent = info ? info.porcentaje + "%" : "—";
      if (presEl) presEl.textContent = info ? `${info.presentes} / ${info.total_clases}` : "—";

      let acumulado = 0;
      const labels = clases.map((c) => c.fecha);
      const data = clases.map((c, i) => {
        if (presentSet.has(idAlumno + "-" + c.id_clase)) acumulado += 1;
        return Math.round((acumulado / (i + 1)) * 100);
      });
      const puntos = clases.map((c) =>
        presentSet.has(idAlumno + "-" + c.id_clase) ? "#16a34a" : CSS("--color-4") || "#C9867E"
      );

      if (chart) chart.destroy();
      chart = new Chart(canvas, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Asistencia acumulada",
              data,
              borderColor: CSS("--color-9") || "#111D4A",
              backgroundColor: "rgba(17,29,74,0.12)",
              fill: true,
              tension: 0.3,
              pointRadius: 4,
              pointBackgroundColor: puntos,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: (ctx) => ` ${ctx.parsed.y}% acumulado` } },
          },
          scales: {
            y: {
              min: 0,
              max: 100,
              ticks: { stepSize: 25, callback: (v) => v + "%" },
              grid: { color: "rgba(0,0,0,0.06)" },
            },
            x: { grid: { display: false } },
          },
        },
      });
    }

    select.addEventListener("change", render);
    if (alumnos.length) render();
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
    renderAsistenciaClase(d);
    renderAsistenciaAlumno(d);

    const loading = document.getElementById("dash-curso-loading");
    const content = document.getElementById("dash-curso-content");
    if (loading) loading.style.display = "none";
    if (content) content.classList.remove("hidden");
  });
})();