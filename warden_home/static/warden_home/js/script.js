console.log("👮 Warden Home Loaded");

/* THEME */
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

