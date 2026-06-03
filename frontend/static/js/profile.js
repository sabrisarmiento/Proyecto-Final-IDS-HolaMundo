document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('profile-modal');
  if (!modal) return;

  // ── Cambio de vista (slide lateral + altura animada) ──────────────────
  const track = modal.querySelector('.profile-track');
  const windowEl = modal.querySelector('.profile-window');
  const perfilPane = document.getElementById('perfil-view');
  const passwordPane = document.getElementById('password-view');
  const title = modal.querySelector('h3');
  let activePane = perfilPane;

  function syncHeight() {
    windowEl.style.height = activePane.scrollHeight + 'px';
  }

  // La altura sigue al panel activo (se reajusta si aparece un mensaje, etc.)
  if (window.ResizeObserver) {
    const ro = new ResizeObserver(syncHeight);
    ro.observe(perfilPane);
    ro.observe(passwordPane);
  }
  syncHeight();

  window.showPasswordView = function () {
    track.classList.add('show-password');
    title.textContent = 'Cambiar mi contraseña';
    activePane = passwordPane;
    syncHeight();
  };

  window.showProfileView = function () {
    track.classList.remove('show-password');
    title.textContent = 'Mi Perfil';
    activePane = perfilPane;
    if (window.resetPasswordForm) window.resetPasswordForm();
    syncHeight();
  };

  // ── "Guardar cambios" solo se habilita si hay cambios ─────────────────
  const perfilSubmit = document.getElementById('perfil-submit');
  const nombre = document.getElementById('perfil-nombre');
  const correo = document.getElementById('perfil-correo');

  function checkProfileDirty() {
    const dirty = nombre.value !== nombre.defaultValue || correo.value !== correo.defaultValue;
    const valid = nombre.value.trim() !== '' && correo.value.trim() !== '';
    perfilSubmit.disabled = !(dirty && valid);
  }
  [nombre, correo].forEach(function (input) {
    input.addEventListener('input', checkProfileDirty);
  });
  checkProfileDirty();

  // ── Form de cambio de contraseña ──────────────────────────────────────
  const form = document.getElementById('password-form');
  const current = document.getElementById('pw-current');
  const newPw = document.getElementById('pw-new');
  const confirm = document.getElementById('pw-confirm');
  const submit = document.getElementById('pw-submit');
  const message = document.getElementById('pw-message');
  const checklist = form.querySelector('.pw-checklist');

  // Toggle mostrar/ocultar de cada input
  form.querySelectorAll('.eye-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = document.getElementById(btn.dataset.target);
      const oculto = input.type === 'password';
      input.type = oculto ? 'text' : 'password';
      btn.classList.toggle('is-on', oculto);
    });
  });

  // Mismas reglas que valida el backend
  const rules = {
    length: function (v) { return v.length >= 8; },
    uppercase: function (v) { return /[A-Z]/.test(v); },
    symbol: function (v) { return /[^A-Za-z0-9]/.test(v); },
  };

  function validate() {
    const v = newPw.value;
    let ok = true;
    Object.keys(rules).forEach(function (key) {
      const valid = rules[key](v);
      checklist.querySelector('[data-rule="' + key + '"]').classList.toggle('valid', valid);
      if (!valid) ok = false;
    });
    const match = v.length > 0 && v === confirm.value;
    checklist.querySelector('[data-rule="match"]').classList.toggle('valid', match);

    submit.disabled = !(ok && match && current.value.length > 0);
    return !submit.disabled;
  }

  [current, newPw, confirm].forEach(function (input) {
    input.addEventListener('input', validate);
  });

  function showMessage(text, ok) {
    message.textContent = text;
    message.hidden = false;
    message.classList.toggle('form-message-ok', ok);
    message.classList.toggle('form-message-error', !ok);
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!validate()) return;
    submit.disabled = true;

    try {
      const resp = await fetch('/perfil/password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_password: current.value,
          new_password: newPw.value,
          confirm_password: confirm.value,
        }),
      });
      const data = await resp.json();

      if (resp.ok && data.ok) {
        showMessage(data.message, true);
        setTimeout(function () { showProfileView(); }, 1500);
      } else {
        showMessage(data.message, false);
        submit.disabled = false;
      }
    } catch (err) {
      showMessage('Error de conexión con el servidor', false);
      submit.disabled = false;
    }
  });

  // Reset al volver a la vista de perfil (limpia campos, mensaje y checklist).
  window.resetPasswordForm = function () {
    form.reset();
    message.hidden = true;
    validate();
  };

  // ── Tras guardar el perfil (?perfil=...): reabrir el modal, limpiar la URL
  //    y auto-descartar el mensaje a los 3s o al cerrar el modal ───────────
  if (new URLSearchParams(window.location.search).has('perfil')) {
    openModal('profile-modal');
    history.replaceState(null, '', window.location.pathname);

    const msg = perfilPane.querySelector('.form-message');
    if (msg) {
      let timer;
      function dismiss() {
        msg.remove();
        clearTimeout(timer);
        observer.disconnect();
      }
      const observer = new MutationObserver(function () {
        if (!modal.classList.contains('active')) dismiss();
      });
      timer = setTimeout(dismiss, 3000);
      observer.observe(modal, { attributes: true, attributeFilter: ['class'] });
    }
  }
});
