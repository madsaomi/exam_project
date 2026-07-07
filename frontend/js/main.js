/* ---------- mobile nav toggle ---------- */
document.addEventListener("DOMContentLoaded", () => {
  const burger = document.querySelector(".hamburger");
  const nav = document.querySelector(".main-nav");
  if (burger && nav) {
    burger.addEventListener("click", () => nav.classList.toggle("open"));
    nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => nav.classList.remove("open")));
  }

  /* ---------- swap "Log In" for account state ---------- */
  const loginBtn = document.querySelector("[data-login-btn]");
  if (loginBtn && typeof Auth !== "undefined" && Auth.isLoggedIn()) {
    loginBtn.textContent = __("logout");
    loginBtn.setAttribute("href", "#");
    loginBtn.addEventListener("click", (e) => {
      e.preventDefault();
      Auth.clear();
      window.location.reload();
    });
  }

  /* ---------- newsletter form (any page) ---------- */
  document.querySelectorAll("[data-newsletter-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const emailInput = form.querySelector("input[type=email]");
      const msg = form.querySelector("[data-newsletter-msg]");
      if (!emailInput) return;
      const email = emailInput.value.trim();
      if (!email) return;
      if (msg) {
        msg.textContent = __("newsletterThanks") + email;
      }
      form.reset();
    });
  });

  const yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach((el) => (el.textContent = new Date().getFullYear()));
});

/* ---------- tiny html-escape helper reused by page scripts ---------- */
function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatDate(value) {
  if (!value) return "";
  const d = new Date(value);
  if (isNaN(d)) return value;
  return d.toLocaleDateString("ru-RU", { day: "2-digit", month: "short", year: "numeric" });
}

function formatPrice(value) {
  const n = Number(value);
  if (isNaN(n)) return value || "";
  return `$${n.toFixed(2)}`;
}
