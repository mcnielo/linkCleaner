function toggleMode() {
  const isSingle = document.querySelector('input[name="mode"]:checked').value === 'single';
  document.getElementById('single-input').style.display = isSingle ? 'block' : 'none';
  document.getElementById('multi-input').style.display = isSingle ? 'none' : 'block';

  const resultSection = document.querySelector('.results');
  if (resultSection) resultSection.remove();
}

function copyResults() {
  const resultItems = document.querySelectorAll('#fullResults li');
  const text = Array.from(resultItems).map(item => item.textContent).join('\n');
  navigator.clipboard.writeText(text).then(() => {
    showToast("All results copied to clipboard");
  });
}

function copyLinksOnly() {
  const resultItems = document.querySelectorAll('#fullResults li');
  const links = Array.from(resultItems).map(item => {
    const parts = item.textContent.split('|');
    return parts.length >= 2 ? parts[1].trim() : '';
  }).filter(Boolean).join('\n');
  navigator.clipboard.writeText(links).then(() => {
    showToast("Links only copied to clipboard");
  });
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add("show"), 100);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 2000);
}

// 🌙 Theme Toggle with LocalStorage
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("themeToggle");

  // Apply saved theme
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
    toggle.textContent = "☀️ Light Mode";
  }

  toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    toggle.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
});
