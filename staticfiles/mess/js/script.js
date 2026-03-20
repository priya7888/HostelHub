/* ══════════════════════════════════════════
   HOSTELHUB — MESS FOOD VOTING SCRIPT
══════════════════════════════════════════ */

console.log("🍽️ Mess Food Voting Loaded");

/* ── CURSOR ─────────────────────────────── */

/* ── THEME ──────────────────────────────── */
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

/* ── CARD SCROLL REVEAL ─────────────────── */
const cards = document.querySelectorAll('.food-card');

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const card = entry.target;
        const idx  = parseInt(card.dataset.i) || 0;
        setTimeout(() => card.classList.add('visible'), idx * 100);
        observer.unobserve(card);
    });
}, { threshold: 0.1 });

cards.forEach(c => observer.observe(c));

/* ── VOTE BARS ──────────────────────────── */
const MAX_VOTES = 10;

cards.forEach(card => {
    const votes = parseInt(card.dataset.votes) || 0;
    const pct   = Math.min((votes / MAX_VOTES) * 100, 100);
    const fill  = card.querySelector('.vote-bar-fill');
    if (fill) {
        setTimeout(() => {
            fill.style.width = pct + '%';
        }, 700);
    }
});

/* ── CARD TILT ──────────────────────────── */
cards.forEach(card => {
    card.addEventListener('mousemove', e => {
        const r  = card.getBoundingClientRect();
        const rx = ((e.clientY - r.top  - r.height/2) / (r.height/2)) * -3;
        const ry = ((e.clientX - r.left - r.width /2) / (r.width /2)) *  3;
        card.style.transform  =
            `translateY(-5px) rotateX(${rx}deg) rotateY(${ry}deg)`;
        card.style.transition = 'transform 0.1s linear';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform  = '';
        card.style.transition =
            'transform 0.5s ease, background 0.3s, border-color 0.3s, box-shadow 0.3s, opacity 0.5s';
    });
});

/* ── AUTO HIDE MESSAGES ─────────────────── */
setTimeout(() => {
    document.querySelectorAll('.msg').forEach(m => {
        m.style.transition = 'opacity 0.5s';
        m.style.opacity    = '0';
        setTimeout(() => m.remove(), 500);
    });
}, 3000);
