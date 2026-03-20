/* ══════════════════════════════════════════
   HOSTELHUB — CLEAN + LIGHT/DARK SCRIPTS
══════════════════════════════════════════ */

console.log("🏠 HostelHub — Clean with Themes");

/* ─────────────────────────────────────────
   1. THEME TOGGLE
────────────────────────────────────────── */
const html       = document.documentElement;
const themeBtn   = document.getElementById('themeBtn');
const themeIcon  = document.getElementById('themeIcon');
const themeLabel = document.getElementById('themeLabel');

// Restore saved theme
const saved = localStorage.getItem('hh-theme') || 'dark';
html.setAttribute('data-theme', saved);
applyThemeUI(saved);

themeBtn.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next    = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('hh-theme', next);
    applyThemeUI(next);
});

function applyThemeUI(theme) {
    if (theme === 'dark') {
        themeIcon.textContent  = '☀️';
        themeLabel.textContent = 'Light';
    } else {
        themeIcon.textContent  = '🌙';
        themeLabel.textContent = 'Dark';
    }
}

/* ─────────────────────────────────────────
   2. AMBER DOT CURSOR
────────────────────────────────────────── */


/* ─────────────────────────────────────────
   3. CARD SCROLL REVEAL — staggered
────────────────────────────────────────── */
const cards = document.querySelectorAll('.svc-card');

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

/* ─────────────────────────────────────────
   4. CARD SUBTLE TILT
────────────────────────────────────────── */
/* ─────────────────────────────────────────
   4. CARD SUBTLE TILT (FIXED)
────────────────────────────────────────── */
cards.forEach(card => {

    card.addEventListener('mousemove', e => {
        const r  = card.getBoundingClientRect();
        const rx = ((e.clientY - r.top  - r.height/2) / (r.height/2)) * -3.5;
        const ry = ((e.clientX - r.left - r.width /2) / (r.width /2)) *  3.5;

        // ✅ combine hover + tilt (IMPORTANT FIX)
        card.style.transform =
            `translateY(-6px) rotateX(${rx}deg) rotateY(${ry}deg)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
    });

});
/* ─────────────────────────────────────────
   5. TYPEWRITER on hero name
────────────────────────────────────────── */
const nameEl = document.getElementById('heroName');
if (nameEl) {
    const full = nameEl.textContent.trim();
    nameEl.textContent = '';

    const blink = document.createElement('span');
    blink.textContent = '|';
    blink.style.cssText =
        'color:var(--amber);animation:blink .85s step-end infinite;font-style:normal;font-weight:300;margin-left:1px;';
    document.head.insertAdjacentHTML('beforeend',
        '<style>@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}</style>');
    nameEl.appendChild(blink);

    let i = 0;
    setTimeout(() => {
        const tick = () => {
            if (i < full.length) {
                nameEl.insertBefore(document.createTextNode(full[i]), blink);
                i++;
                setTimeout(tick, 72 + Math.random() * 40);
            } else {
                setTimeout(() => {
                    blink.style.transition = 'opacity .4s';
                    blink.style.opacity    = '0';
                }, 1400);
            }
        };
        tick();
    }, 600);
}

/* ─────────────────────────────────────────
   6. LOGOUT graceful fade
────────────────────────────────────────── */
document.querySelectorAll('.nav-exit, .foot-logout').forEach(el => {
    el.addEventListener('click', () => {
        el.style.opacity       = '0.3';
        el.style.pointerEvents = 'none';
    });
});
