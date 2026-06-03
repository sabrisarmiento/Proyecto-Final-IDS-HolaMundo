// Cambio entre la vista de perfil y la de cambiar contraseña dentro del modal.
function showPasswordView() {
  const modal = document.getElementById('profile-modal');
  modal.querySelector('#perfil-view').classList.add('is-hidden');
  modal.querySelector('#password-view').classList.remove('is-hidden');
  modal.querySelector('h3').textContent = 'Cambiar mi contraseña';
}

function showProfileView() {
  const modal = document.getElementById('profile-modal');
  modal.querySelector('#password-view').classList.add('is-hidden');
  modal.querySelector('#perfil-view').classList.remove('is-hidden');
  modal.querySelector('h3').textContent = 'Mi Perfil';
  if (window.resetPasswordForm) window.resetPasswordForm();
}

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('password-form');
  if (!form) return;

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
});

// Tras guardar el perfil (?perfil=...): reabrir el modal, limpiar la URL y
// auto-descartar el mensaje a los 3s o al cerrar el modal.
document.addEventListener('DOMContentLoaded', function () {
  if (!new URLSearchParams(window.location.search).has('perfil')) return;

  const modalEl = document.getElementById('profile-modal');
  if (!modalEl) return;

  openModal('profile-modal');
  history.replaceState(null, '', window.location.pathname);

  const msg = modalEl.querySelector('.form-message');
  if (!msg) return;

  let timer;
  function dismiss() {
    msg.remove();
    clearTimeout(timer);
    observer.disconnect();
  }

  const observer = new MutationObserver(function () {
    if (!modalEl.classList.contains('active')) dismiss();
  });

  timer = setTimeout(dismiss, 3000);
  observer.observe(modalEl, { attributes: true, attributeFilter: ['class'] });
});
