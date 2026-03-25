const html  = document.documentElement;
const btn   = document.getElementById('themeBtn');
const icon  = document.getElementById('themeIcon');
const label = document.getElementById('themeLabel');
const saved = localStorage.getItem('hh-theme') || 'dark';
html.setAttribute('data-theme', saved);
updateUI(saved);

if (btn) {
    btn.addEventListener('click', () => {
        const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('hh-theme', next);
        updateUI(next);
    });
}
function updateUI(t) {
    if (icon)  icon.textContent  = t === 'dark' ? '☀️' : '🌙';
    if (label) label.textContent = t === 'dark' ? 'Light' : 'Dark';
}

const cards = document.querySelectorAll('.notice-card');
const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 100);
        obs.unobserve(e.target);
    });
}, { threshold: 0.08 });
cards.forEach(c => obs.observe(c));

setTimeout(() => {
    document.querySelectorAll('.notice-card').forEach(c => {
        c.classList.add('visible');
    });
}, 600);