/* IDBC Salary Guide — the shared header menu (every page). Below 1200 px the links and the
   button group fold behind the toggle, as on idbc.hu. */
(() => {
  const nav = document.querySelector('.sg-nav');
  const toggle = document.querySelector('.sg-toggle');
  if (!nav || !toggle) return;
  const icon = toggle.querySelector('i');
  const set = open => {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    if (icon) icon.className = open ? 'bi bi-x-lg' : 'bi bi-list';
  };
  toggle.addEventListener('click', () => set(!nav.classList.contains('is-open')));
  nav.querySelectorAll('.sg-links a, .sg-actions a').forEach(a => a.addEventListener('click', () => set(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { set(false); toggle.focus(); } });
})();
