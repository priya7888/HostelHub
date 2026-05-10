console.log("🚨 Emergency SOS Loaded");
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
const sosForm = document.getElementById('sosForm');
const sosBtn  = document.getElementById('sosBtn');
if (sosForm && sosBtn) {
    sosForm.addEventListener('submit', e => {
        e.preventDefault();
        sosBtn.style.transform = 'scale(0.94)';
        sosBtn.style.transition = 'transform 0.1s ease';
        setTimeout(() => {
            sosBtn.style.transform = 'scale(1.08)';
        }, 100);
        setTimeout(() => {
            sosBtn.innerHTML = `
                <span class="sos-icon">✅</span>
                <span class="sos-text">SENT!</span>
                <span class="sos-sub">Help is coming</span>
            `;
            sosBtn.style.background = '#2a8c5a';
            sosBtn.style.transform  = 'scale(1)';
            sosBtn.style.animation  = 'none';
        }, 200);
        setTimeout(() => {
            sosForm.submit();
        }, 800);
    });
}
const rows = document.querySelectorAll('.alert-row');
const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 80);
        obs.unobserve(e.target);
    });
}, { threshold: 0.1 });
rows.forEach(r => obs.observe(r));
setTimeout(() => {
    document.querySelectorAll('.alert-row').forEach(r => {
        r.classList.add('visible');
    });
}, 600);
setTimeout(() => {
    document.querySelectorAll('.msg').forEach(m => {
        m.style.transition = 'opacity 0.5s';
        m.style.opacity    = '0';
        setTimeout(() => m.remove(), 500);
    });
}, 4000);

