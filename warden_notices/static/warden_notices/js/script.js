console.log("📢 Warden Notices Loaded");


function updateUI(t) {
    icon.textContent  = t === 'dark' ? '☀️' : '🌙';
    label.textContent = t === 'dark' ? 'Light' : 'Dark';
}

/* NOTICE CARDS REVEAL */
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

/* FALLBACK */
setTimeout(() => {
    document.querySelectorAll('.notice-card').forEach(c => {
        c.classList.add('visible');
    });
}, 600);

/* PRIORITY PREVIEW on add_notice page */
const radios = document.querySelectorAll('input[name="priority"]');
const prevs  = {
    normal:    document.getElementById('prev-normal'),
    important: document.getElementById('prev-important'),
    urgent:    document.getElementById('prev-urgent'),
};
radios.forEach(r => {
    r.addEventListener('change', () => {
        Object.values(prevs).forEach(p => {
            if (p) p.classList.remove('pp-active');
        });
        if (prevs[r.value]) prevs[r.value].classList.add('pp-active');
    });
});

/* AUTO HIDE MESSAGES */
setTimeout(() => {
    document.querySelectorAll('.msg').forEach(m => {
        m.style.transition = 'opacity 0.5s';
        m.style.opacity    = '0';
        setTimeout(() => m.remove(), 500);
    });
}, 3000);


