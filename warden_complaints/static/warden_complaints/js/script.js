console.log("📝 Warden Complaints Loaded");


function updateUI(t) {
    icon.textContent  = t === 'dark' ? '☀️' : '🌙';
    label.textContent = t === 'dark' ? 'Light' : 'Dark';
}

/* CARD REVEAL */
const cards = document.querySelectorAll('.complaint-card');
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
    document.querySelectorAll('.complaint-card').forEach(c => {
        c.classList.add('visible');
    });
}, 600);

/* AUTO HIDE MESSAGES */
setTimeout(() => {
    document.querySelectorAll('.msg').forEach(m => {
        m.style.transition = 'opacity 0.5s';
        m.style.opacity    = '0';
        setTimeout(() => m.remove(), 500);
    });
}, 3000);


