console.log("?? Warden Dashboard Loaded");

const html  = document.documentElement;
const btn   = document.getElementById("themeBtn");
const icon  = document.getElementById("themeIcon");
const label = document.getElementById("themeLabel");

const saved = localStorage.getItem("hh-theme") || "dark";
html.setAttribute("data-theme", saved);
updateThemeUI(saved);

btn.addEventListener("click", () => {
    const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
    html.setAttribute("data-theme", next);
    localStorage.setItem("hh-theme", next);
    updateThemeUI(next);
});

function updateThemeUI(t) {
    icon.textContent  = t === "dark" ? "??" : "??";
    label.textContent = t === "dark" ? "Light" : "Dark";
}

const svcCards = document.querySelectorAll(".svc-card");

const cardObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (!e.isIntersecting) return;
        const i = parseInt(e.target.dataset.i) || 0;
        setTimeout(() => e.target.classList.add("visible"), i * 100);
        cardObserver.unobserve(e.target);
    });
}, { threshold: 0.08 });

svcCards.forEach(c => cardObserver.observe(c));

setTimeout(() => {
    document.querySelectorAll(".svc-card").forEach(c => c.classList.add("visible"));
}, 800);

svcCards.forEach(card => {
    if (card.classList.contains("svc-sos")) return;

    const arrow = card.querySelector(".card-arrow");

    card.addEventListener("mouseenter", () => {
        if (arrow) { arrow.style.opacity = "1"; arrow.style.transform = "translateX(0)"; }
    });

    card.addEventListener("mousemove", e => {
        const r  = card.getBoundingClientRect();
        const rx = ((e.clientY - r.top  - r.height / 2) / (r.height / 2)) * -3;
        const ry = ((e.clientX - r.left - r.width  / 2) / (r.width  / 2)) *  3;
        card.style.transform  = "translateY(-6px) rotateX(" + rx + "deg) rotateY(" + ry + "deg)";
        card.style.transition = "transform 0.1s linear";
        if (arrow) { arrow.style.opacity = "1"; arrow.style.transform = "translateX(0)"; }
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform  = "";
        card.style.transition = "transform 0.5s ease, background 0.3s, border-color 0.3s, box-shadow 0.3s, opacity 0.5s";
        if (arrow) { arrow.style.opacity = ""; arrow.style.transform = ""; }
    });
});

setTimeout(() => {
    document.querySelectorAll(".msg").forEach(m => {
        m.style.transition = "opacity 0.5s";
        m.style.opacity    = "0";
        setTimeout(() => m.remove(), 500);
    });
}, 3000);
