console.log("🚪 Outing Request Loaded");

/* CURSOR */

/* THEME */
const html  = document.documentElement;
const btn   = document.getElementById('themeBtn');
const icon  = document.getElementById('themeIcon');
const label = document.getElementById('themeLabel');
if (btn) {
    const saved = localStorage.getItem('hh-theme') || 'dark';
    html.setAttribute('data-theme', saved);
    updateUI(saved);
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

/* CARD REVEAL */
const cards = document.querySelectorAll('.outing-card');
const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 100);
        obs.unobserve(e.target);
    });
}, { threshold: 0.08 });
cards.forEach(c => obs.observe(c));

/* FALLBACK */
setTimeout(() => {
    document.querySelectorAll('.outing-card').forEach(c => {
        c.classList.add('visible');
    });
}, 600);

/* COPY PARENT LINK */
function copyLink(id) {
    const el   = document.getElementById(id);
    const text = el ? el.textContent.trim() : '';
    navigator.clipboard.writeText(text).then(() => {
        const copyBtn = el.nextElementSibling;
        if (copyBtn) {
            copyBtn.textContent = '✓ Copied!';
            setTimeout(() => copyBtn.textContent = 'Copy Link', 2000);
        }
    });
}

/* AUTO HIDE MESSAGES */
setTimeout(() => {
    document.querySelectorAll('.msg').forEach(m => {
        m.style.transition = 'opacity 0.5s';
        m.style.opacity    = '0';
        setTimeout(() => m.remove(), 500);
    });
}, 3000);
