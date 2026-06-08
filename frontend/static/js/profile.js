document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('profile-modal');
  if (!modal) return;

  // ── Helpers compartidos ───────────────────────────────────────────────
  const postJSON = async (url, body) => {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await resp.json();
    return { ok: resp.ok && data.ok, data };
  };

  const setMessage = (el, text, ok) => {
    el.textContent = text;
    el.hidden = false;
    el.classList.toggle('form-message-ok', ok);
    el.classList.toggle('form-message-error', !ok);
  };

  // ── Cambio de vista (slide lateral + altura animada) ──────────────────
  const initViewSwitcher = () => {
    const track = modal.querySelector('.profile-track');
    const windowEl = modal.querySelector('.profile-window');
    const perfilPane = document.getElementById('perfil-view');
    const passwordPane = document.getElementById('password-view');
    const title = modal.querySelector('h3');
    let activePane = perfilPane;

    const syncHeight = () => {
      windowEl.style.height = activePane.scrollHeight + 'px';
    };

    // La altura sigue al panel activo (se reajusta si aparece un mensaje, etc.)
    if (window.ResizeObserver) {
      const ro = new ResizeObserver(syncHeight);
      ro.observe(perfilPane);
      ro.observe(passwordPane);
    }
    syncHeight();

    window.showPasswordView = () => {
      track.classList.add('show-password');
      title.textContent = 'Cambiar mi contraseña';
      activePane = passwordPane;
      syncHeight();
    };

    window.showProfileView = () => {
      track.classList.remove('show-password');
      title.textContent = 'Mi Perfil';
      activePane = perfilPane;
      if (window.resetPasswordForm) window.resetPasswordForm();
      syncHeight();
    };

    return { syncHeight };
  };

  // ── Form de perfil (AJAX): "Guardar cambios" solo si hay cambios ──────
  const initProfileForm = ({ syncHeight }) => {
    const form = document.getElementById('perfil-form');
    const submit = document.getElementById('perfil-submit');
    const message = document.getElementById('perfil-message');
    const nombre = document.getElementById('perfil-nombre');
    const correo = document.getElementById('perfil-correo');

    const checkDirty = () => {
      const dirty = nombre.value !== nombre.defaultValue || correo.value !== correo.defaultValue;
      const valid = nombre.value.trim() !== '' && correo.value.trim() !== '';
      submit.disabled = !(dirty && valid);
    };

    [nombre, correo].forEach((input) => input.addEventListener('input', checkDirty));

    checkDirty();

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (submit.disabled) return;
      submit.disabled = true;

      try {
        const { ok, data } = await postJSON('/perfil', { 
          nombre: nombre.value, correo: correo.value 
        });
        
        if (ok) {
          // Los valores guardados pasan a ser los nuevos "defaults" para el dirty-check.
          nombre.defaultValue = nombre.value;
          correo.defaultValue = correo.value;
          setMessage(message, data.message, true);
        } else {
          setMessage(message, data.message, false);
          checkDirty();
        }
      } catch (err) {
        setMessage(message, 'Error de conexión con el servidor', false);
        checkDirty();
      }
      syncHeight();
    });
  };

  // ── Form de cambio de contraseña (AJAX) ───────────────────────────────
  const initPasswordForm = ({ syncHeight }) => {
    const form = document.getElementById('password-form');
    const current = document.getElementById('pw-current');
    const newPw = document.getElementById('pw-new');
    const confirm = document.getElementById('pw-confirm');
    const submit = document.getElementById('pw-submit');
    const message = document.getElementById('pw-message');
    const checklist = form.querySelector('.pw-checklist');

    // Toggle mostrar/ocultar de cada input
    form.querySelectorAll('.eye-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        const oculto = input.type === 'password';
        input.type = oculto ? 'text' : 'password';
        btn.classList.toggle('is-on', oculto);
      });
    });

    // Mismas reglas que valida el backend
    const rules = {
      length: (value) => value.length >= 8,
      uppercase: (value) => /[A-Z]/.test(value),
      symbol: (value) => /[^A-Za-z0-9]/.test(value),
    };

    const validate = () => {
      const v = newPw.value;
      let ok = true;

      Object.keys(rules).forEach((key) => {
        const valid = rules[key](v);
        checklist.querySelector('[data-rule="' + key + '"]').classList.toggle('valid', valid);
        if (!valid) ok = false;
      });

      const match = v.length > 0 && v === confirm.value;
      checklist.querySelector('[data-rule="match"]').classList.toggle('valid', match);

      submit.disabled = !(ok && match && current.value.length > 0);
      return !submit.disabled;
    };

    [current, newPw, confirm].forEach((input) => input.addEventListener('input', validate));

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!validate()) return;
      submit.disabled = true;

      try {
        const { ok, data } = await postJSON('/perfil/password', {
          current_password: current.value,
          new_password: newPw.value,
          confirm_password: confirm.value,
        });
        if (ok) {
          setMessage(message, data.message, true);
          setTimeout(() => showProfileView(), 1500);
        } else {
          setMessage(message, data.message, false);
          submit.disabled = false;
        }
      } catch (err) {
        setMessage(message, 'Error de conexión con el servidor', false);
        submit.disabled = false;
      }
      syncHeight();
    });

    // Reset al volver a la vista de perfil (limpia campos, mensaje y checklist).
    window.resetPasswordForm = () => {
      form.reset();
      message.hidden = true;
      validate();
    };
  };

  const views = initViewSwitcher();
  initProfileForm(views);
  initPasswordForm(views);
});
