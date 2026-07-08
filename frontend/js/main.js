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

  /* ---------- Scroll Reveal Animations ---------- */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

  // Add the class to elements we want to animate, and observe them
  const animatedElements = document.querySelectorAll('.hero-copy, .hero-media, .section-head, .dish-card, .menu-item, .testi-card, .news-card, .insta-grid a, .newsletter');
  animatedElements.forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
  });
  
  // Re-observe dynamically added items (like dishes loaded via API)
  const mutationObserver = new MutationObserver((mutations) => {
    mutations.forEach(m => {
      m.addedNodes.forEach(node => {
        if (node.nodeType === 1 && (node.classList.contains('dish-card') || node.classList.contains('menu-item') || node.classList.contains('news-card'))) {
          node.classList.add('reveal');
          // Short delay to allow CSS to apply before measuring intersection
          setTimeout(() => observer.observe(node), 10);
        }
      });
    });
  });
  
  const grids = document.querySelectorAll('.dish-grid, .menu-grid, .news-grid');
  grids.forEach(grid => mutationObserver.observe(grid, { childList: true }));

  /* ---------- Inline Video ---------- */
  const playBtn = document.getElementById('play-btn');
  const videoBand = document.getElementById('video-band');
  const videoInline = document.getElementById('video-inline');
  if (playBtn && videoBand && videoInline) {
    playBtn.addEventListener('click', () => {
      playBtn.classList.add('hidden');
      videoBand.classList.add('playing');
      videoInline.play();
    });
  }
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
