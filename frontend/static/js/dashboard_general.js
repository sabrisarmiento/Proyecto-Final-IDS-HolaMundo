(function () {
  "use strict";

  const CSS = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

  function showMsg(elId, text, ok) {
    const el = document.getElementById(elId);
    if (!el) return;
    el.textContent = text;
    el.className = "dg-modal-msg " + (ok ? "ok" : "error");
    el.classList.remove("hidden");
  }

  function hideMsg(elId) {
    const el = document.getElementById(elId);
    if (el) { el.textContent = ""; el.classList.add("hidden"); }
  }

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
    hideMsg("msg-crear-usuario");
    ["cu-nombre", "cu-apellido", "cu-correo", "cu-password"].forEach(function (id) {
      const el = document.getElementById(id);
      if (el) el.value = "";
    });
    abrirModal("modal-crear-usuario");
  });

  document.getElementById("btn-abrir-crear-rol")?.addEventListener("click", function () {
    hideMsg("msg-crear-rol");
    const el = document.getElementById("cr-nombre");
    if (el) el.value = "";
    abrirModal("modal-crear-rol");
  });

  document.getElementById("tabla-usuarios")?.addEventListener("click", function (e) {
    const btnEditar = e.target.closest(".js-editar-usuario");
    const btnEliminar = e.target.closest(".js-eliminar-usuario");

    if (btnEditar) {
      const fila = btnEditar.closest("tr");
      if (!fila) return;
      const { id, nombre, apellido, correo, idRol } = fila.dataset;

      hideMsg("msg-editar-usuario");
      document.getElementById("eu-id").value = id;
      document.getElementById("eu-nombre").value = nombre;
      document.getElementById("eu-apellido").value = apellido;
      document.getElementById("eu-correo").value = correo;
      document.getElementById("eu-nombre-label").textContent = nombre + " " + apellido;

      const sel = document.getElementById("eu-rol");
      if (sel && idRol) sel.value = idRol;

      abrirModal("modal-editar-usuario");
    }

    if (btnEliminar) {
      const fila = btnEliminar.closest("tr");
      if (!fila) return;
      const { id, nombre, apellido } = fila.dataset;
      const nombreCompleto = nombre + " " + apellido;

      document.getElementById("modal-confirmar-msg").textContent =
        "¿Estás seguro de que querés eliminar al usuario \"" + nombreCompleto + "\"? Esta acción no se puede deshacer.";

      const btn = document.getElementById("modal-confirmar-btn");
      btn.onclick = async function () {
        await eliminarUsuario(id);
        cerrarModal("modal-confirmar");
      };
      abrirModal("modal-confirmar");
    }
  });

  document.getElementById("lista-roles")?.addEventListener("click", function (e) {
    const btn = e.target.closest(".js-eliminar-rol");
    if (!btn) return;
    const fila = btn.closest(".dg-rol-row");
    if (!fila) return;
    const { id, nombre } = fila.dataset;

    document.getElementById("modal-confirmar-msg").textContent =
      "¿Estás seguro de que querés eliminar el rol \"" + nombre + "\"? Los usuarios con este rol pueden quedar sin asignación.";

    const confirmBtn = document.getElementById("modal-confirmar-btn");
    confirmBtn.onclick = async function () {
      await eliminarRol(id);
      cerrarModal("modal-confirmar");
    };
    abrirModal("modal-confirmar");
  });

  document.getElementById("btn-crear-usuario")?.addEventListener("click", async function () {
    const payload = {
      nombre:     document.getElementById("cu-nombre")?.value.trim(),
      apellido:   document.getElementById("cu-apellido")?.value.trim(),
      correo:     document.getElementById("cu-correo")?.value.trim(),
      contraseña: document.getElementById("cu-password")?.value,
      id_rol:     parseInt(document.getElementById("cu-rol")?.value, 10),
    };

    if (!payload.nombre || !payload.apellido || !payload.correo || !payload.contraseña) {
      showMsg("msg-crear-usuario", "Completá todos los campos obligatorios.", false);
      return;
    }

    try {
      const res = await fetch("/dashboard/usuarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok && data.ok !== false) {
        showMsg("msg-crear-usuario", "Usuario creado correctamente. Recargando...", true);
        setTimeout(function () { location.reload(); }, 1200);
      } else {
        const desc = data.errors?.[0]?.description || data.message || "Error al crear usuario";
        showMsg("msg-crear-usuario", desc, false);
      }
    } catch (_) {
      showMsg("msg-crear-usuario", "Error de conexión.", false);
    }
  });

  document.getElementById("btn-editar-usuario")?.addEventListener("click", async function () {
    const id = document.getElementById("eu-id")?.value;
    const payload = {
      nombre:   document.getElementById("eu-nombre")?.value.trim(),
      apellido: document.getElementById("eu-apellido")?.value.trim(),
      correo:   document.getElementById("eu-correo")?.value.trim(),
      id_rol:   parseInt(document.getElementById("eu-rol")?.value, 10),
    };

    try {
      const res = await fetch("/dashboard/usuarios/" + id, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok && data.ok !== false) {
        showMsg("msg-editar-usuario", "Cambios guardados. Recargando...", true);
        setTimeout(function () { location.reload(); }, 1200);
      } else {
        const desc = data.errors?.[0]?.description || data.message || "Error al actualizar";
        showMsg("msg-editar-usuario", desc, false);
      }
    } catch (_) {
      showMsg("msg-editar-usuario", "Error de conexión.", false);
    }
  });

  async function eliminarUsuario(id) {
    try {
      const res = await fetch("/dashboard/usuarios/" + id, { method: "DELETE" });
      if (res.ok) {
        document.getElementById("fila-usuario-" + id)?.remove();
      } else {
        alert("No se pudo eliminar el usuario.");
      }
    } catch (_) {
      alert("Error de conexión.");
    }
  }

  document.getElementById("btn-crear-rol")?.addEventListener("click", async function () {
    const nombre = document.getElementById("cr-nombre")?.value.trim();
    const nivel  = parseInt(document.getElementById("cr-nivel")?.value, 10);

    if (!nombre) {
      showMsg("msg-crear-rol", "El nombre del rol es obligatorio.", false);
      return;
    }

    try {
      const res = await fetch("/dashboard/roles", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, nivel_administracion: nivel }),
      });
      const data = await res.json();
      if (res.ok && data.ok !== false) {
        showMsg("msg-crear-rol", "Rol creado. Recargando...", true);
        setTimeout(function () { location.reload(); }, 1200);
      } else {
        const desc = data.errors?.[0]?.description || data.message || "Error al crear rol";
        showMsg("msg-crear-rol", desc, false);
      }
    } catch (_) {
      showMsg("msg-crear-rol", "Error de conexión.", false);
    }
  });

  async function eliminarRol(id) {
    try {
      const res = await fetch("/dashboard/roles/" + id, { method: "DELETE" });
      if (res.ok || res.status === 204) {
        document.getElementById("rol-row-" + id)?.remove();
      } else {
        alert("No se pudo eliminar el rol.");
      }
    } catch (_) {
      alert("Error de conexión.");
    }
  }

  function renderBarCursos() {
    const canvas = document.getElementById("chart-cursos");
    if (!canvas) return;
    let cursos = [];
    try { cursos = JSON.parse(document.getElementById("data-cursos")?.textContent || "[]"); }
    catch (_) { return; }
    if (!cursos.length) return;

    const labels   = cursos.map(function (c) { return c.catedra || c.materia || "Curso " + c.id_curso; });
    const activos  = cursos.map(function (c) { return c.activos   || 0; });
    const abandono   = cursos.map(function (c) { return c.abandono || 0; });

    new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          { label: "Activos",    data: activos, backgroundColor: CSS("--color-9") || "#111D4A", borderRadius: 6, borderSkipped: false },
          { label: "Abandono", data: abandono,  backgroundColor: CSS("--color-3") || "#92140C", borderRadius: 6, borderSkipped: false },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom" } },
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 1 } },
          x: { grid: { display: false } },
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

    new Chart(canvas, {
      type: "line",
      data: {
        labels: historico.map(function (h) { return h.anio; }),
        datasets: [{
          label: "Promedio general",
          data: historico.map(function (h) { return h.promedio_notas; }),
          borderColor: CSS("--color-3") || "#92140C",
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
          y: { min: 0, max: 10, ticks: { stepSize: 2 }, grid: { color: "rgba(0,0,0,0.06)" } },
          x: { grid: { display: false } },
        },
      },
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderBarCursos();
    renderLineHistorico();
  });

})();