document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('profile-modal');
  if (!modal) return;

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

  // ── Form de perfil: habilitar "Guardar" solo si hay cambios ──────────
  const initProfileForm = () => {
    const submit = document.getElementById('perfil-submit');
    const nombre = document.getElementById('perfil-nombre');
    const correo = document.getElementById('perfil-correo');

    const checkDirty = () => {
      const dirty = nombre.value !== nombre.defaultValue || correo.value !== correo.defaultValue;
      const valid = nombre.value.trim() !== '' && correo.value.trim() !== '';
      submit.disabled = !(dirty && valid);
    };

    [nombre, correo].forEach((input) => input.addEventListener('input', checkDirty));
    checkDirty();
  };

  // ── Form de cambio de contraseña: validación client-side ─────────────
  const initPasswordForm = () => {
    const form = document.getElementById('password-form');
    const current = document.getElementById('pw-current');
    const newPw = document.getElementById('pw-new');
    const confirm = document.getElementById('pw-confirm');
    const submit = document.getElementById('pw-submit');
    const checklist = form.querySelector('.pw-checklist');

    form.querySelectorAll('.eye-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        const oculto = input.type === 'password';
        input.type = oculto ? 'text' : 'password';
        btn.classList.toggle('is-on', oculto);
      });
    });

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

    window.resetPasswordForm = () => {
      form.reset();
      validate();
    };
  };

  const views = initViewSwitcher();
  initProfileForm();
  initPasswordForm();

  // ── Reabrir modal si venimos de un redirect con ?open=perfil ─────────
  const params = new URLSearchParams(window.location.search);
  if (params.get('open') === 'perfil') {
    openModal('profile-modal');
    if (params.get('pane') === 'password' && window.showPasswordView) {
      window.showPasswordView();
    }
    views.syncHeight();
    params.delete('open');
    params.delete('pane');
    const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    history.replaceState({}, '', newUrl);
  }
});
