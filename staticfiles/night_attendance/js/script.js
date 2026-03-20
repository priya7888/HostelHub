console.log("🌙 Night Attendance Loaded");

/* CURSOR */
/* THEME */
const html  = document.documentElement;
const btn   = document.getElementById('themeBtn');
const icon  = document.getElementById('themeIcon');
const label = document.getElementById('themeLabel');
const saved = localStorage.getItem('hh-theme') || 'dark';
html.setAttribute('data-theme', saved);
updateUI(saved);
btn.addEventListener('click', () => {
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('hh-theme', next);
    updateUI(next);
});
function updateUI(t) {
    icon.textContent  = t === 'dark' ? '☀️' : '🌙';
    label.textContent = t === 'dark' ? 'Light' : 'Dark';
}

/* STAT CARDS REVEAL */
const statCards = document.querySelectorAll('.stat-card');
const obs1 = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 100);
        obs1.unobserve(e.target);
    });
}, { threshold: 0.1 });
statCards.forEach(c => obs1.observe(c));

/* ANIMATED PERCENTAGE BAR */
const fill    = document.getElementById('statFill');
const pctVal  = document.getElementById('pctVal');
const pct     = parseFloat(fill ? fill.dataset.pct : 0) || 0;

setTimeout(() => {
    if (fill) fill.style.width = pct + '%';
    if (pctVal) {
        let current = 0;
        const step = pct / 60;
        const timer = setInterval(() => {
            current += step;
            if (current >= pct) {
                current = pct;
                clearInterval(timer);
            }
            pctVal.textContent = Math.round(current) + '%';
        }, 20);
    }
}, 700);

/* ATTENDANCE ROWS REVEAL */
const rows = document.querySelectorAll('.att-row');
const obs2 = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 60);
        obs2.unobserve(e.target);
    });
}, { threshold: 0.05 });
rows.forEach(r => obs2.observe(r));

/* FALLBACK */
setTimeout(() => {
    document.querySelectorAll('.stat-card, .att-row').forEach(el => {
        el.classList.add('visible');
    });
}, 800);

