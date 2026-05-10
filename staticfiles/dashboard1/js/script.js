console.log("🏠 Dashboard Loaded");
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
const cards = document.querySelectorAll('.svc-card');
const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add('visible'), i * 100);
        obs.unobserve(e.target);
    });
}, { threshold: 0.1 });
cards.forEach(c => obs.observe(c));
cards.forEach(card => {
    card.addEventListener('mousemove', e => {
        const r  = card.getBoundingClientRect();
        const rx = ((e.clientY - r.top  - r.height/2) / (r.height/2)) * -3.5;
        const ry = ((e.clientX - r.left - r.width /2) / (r.width /2)) *  3.5;
        card.style.transform  =
            `translateY(-6px) rotateX(${rx}deg) rotateY(${ry}deg)`;
        card.style.transition = 'transform 0.1s linear';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform  = '';
        card.style.transition =
            'transform 0.5s ease, background 0.3s, border-color 0.3s, box-shadow 0.3s, opacity 0.5s';
    });
});
