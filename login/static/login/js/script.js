console.log("🏠 HostelHub Login");

/* BACKGROUND SLIDESHOW */
const slides = document.querySelectorAll('.bg-slide');
let current  = 0;

function nextSlide() {
    slides[current].classList.remove('active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('active');
}

setInterval(nextSlide, 4000);

/* FEATURE ITEMS REVEAL */
setTimeout(() => {
    document.querySelectorAll('.feature-item').forEach((el, i) => {
        setTimeout(() => el.classList.add('visible'), i * 120);
    });
}, 400);

/* ROLE SELECTOR */
const radios    = document.querySelectorAll('input[name="role"]');
const roomGroup = document.getElementById('roomGroup');
const roomInput = document.getElementById('roomInput');

radios.forEach(r => {
    r.addEventListener('change', () => {
        if (r.value === 'student') {
            roomGroup.style.display = 'block';
            roomInput.required = true;
        } else {
            roomGroup.style.display = 'none';
            roomInput.required = false;
            roomInput.value   = '';
        }
    });
});

/* PASSWORD TOGGLE */
const eyeBtn    = document.getElementById('eyeBtn');
const passInput = document.getElementById('passInput');
if (eyeBtn) {
    eyeBtn.addEventListener('click', () => {
        if (passInput.type === 'password') {
            passInput.type     = 'text';
            eyeBtn.textContent = '🙈';
        } else {
            passInput.type     = 'password';
            eyeBtn.textContent = '👁';
        }
    });
}

/* LOGIN BUTTON LOADING */
const form     = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const btnText  = document.getElementById('btnText');
if (form) {
    form.addEventListener('submit', () => {
        loginBtn.classList.add('loading');
        btnText.textContent = 'Logging in...';
    });
}
