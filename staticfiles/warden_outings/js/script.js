console.log("🚪 Warden Outings Loaded");


function updateUI(t) {
    icon.textContent  = t === 'dark' ? '☀️' : '🌙';
    label.textContent = t === 'dark' ? 'Light' : 'Dark';
}

/* OUTING CARDS */
const cards = document.querySelectorAll('.outing-card');
const obs1  = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 80);
        obs1.unobserve(e.target);
    });
}, { threshold: 0.08 });
cards.forEach(c => obs1.observe(c));

/* ALL ROWS */
const rows = document.querySelectorAll('.all-row');
const obs2 = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 50);
        obs2.unobserve(e.target);
    });
}, { threshold: 0.05 });
rows.forEach(r => obs2.observe(r));

/* FALLBACK */
setTimeout(() => {
    document.querySelectorAll('.outing-card, .all-row').forEach(el => {
        el.classList.add('visible');
    });
}, 700);

/* AUTO HIDE MESSAGES */
setTimeout(() => {
    document.querySelectorAll('.msg').forEach(m => {
        m.style.transition = 'opacity 0.5s';
        m.style.opacity    = '0';
        setTimeout(() => m.remove(), 500);
    });
}, 3000);


