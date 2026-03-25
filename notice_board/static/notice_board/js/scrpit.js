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

/* FORCE ALL CARDS VISIBLE IMMEDIATELY */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.notice-card').forEach((c, i) => {
        setTimeout(() => c.classList.add('visible'), i * 150);
    });
});

/* FALLBACK */
setTimeout(() => {
    document.querySelectorAll('.notice-card').forEach(c => {
        c.classList.add('visible');
    });
}, 300);