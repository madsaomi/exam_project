(async function () {
  /* ---------------- Popular dishes (simple carousel: shift 4 at a time) ---------------- */
  const popularWrap = document.getElementById("popular-dishes");
  let popularDishes = [];
  let popularPage = 0;
  const PER_PAGE = 4;
  const MAX_PREVIEW = 8;

  function renderPopular() {
    if (!popularDishes.length) {
      popularWrap.innerHTML = `<div class="empty-note">${__("noDishes")}</div>`;
      return;
    }
    const start = popularPage * PER_PAGE;
    const slice = popularDishes.slice(start, start + PER_PAGE);
    popularWrap.innerHTML = slice.map((d) => `
      <div class="dish-card">
        <img src="${resolveImage(d, seed(d))}" alt="${escapeHtml(pick(d, ["name", "title"], "Dish"))}">
        <h4>${escapeHtml(pick(d, ["name", "title"], "Dish"))}</h4>
        <div class="dish-stars">&#9733;&#9733;&#9733;&#9733;&#9734;</div>
        <div class="dish-price">${formatPrice(pick(d, ["price"], 0))}</div>
      </div>
    `).join("");
  }

  try {
    popularDishes = await MenuAPI.dishes();
    renderPopular();
  } catch (e) {
    popularWrap.innerHTML = `<div class="empty-note">${__("loading")}: ${escapeHtml(e.message)}</div>`;
  }

  document.getElementById("popular-next").addEventListener("click", () => {
    if (!popularDishes.length) return;
    const maxPage = Math.ceil(popularDishes.length / PER_PAGE) - 1;
    popularPage = popularPage >= maxPage ? 0 : popularPage + 1;
    renderPopular();
  });
  document.getElementById("popular-prev").addEventListener("click", () => {
    if (!popularDishes.length) return;
    const maxPage = Math.ceil(popularDishes.length / PER_PAGE) - 1;
    popularPage = popularPage <= 0 ? maxPage : popularPage - 1;
    renderPopular();
  });

  /* ---------------- Menu preview with category filter ---------------- */
  const catsWrap = document.getElementById("home-categories");
  const dishesWrap = document.getElementById("home-dishes");

  function renderDishes(list) {
    if (!list.length) {
      dishesWrap.innerHTML = `<div class="empty-note">${__("noDishes")}</div>`;
      return;
    }
    dishesWrap.innerHTML = list.slice(0, MAX_PREVIEW).map((d) => `
      <div class="menu-item">
        <img src="${resolveImage(d, seed(d))}" alt="${escapeHtml(pick(d, ["name", "title"], "Dish"))}">
        <h4>${escapeHtml(pick(d, ["name", "title"], "Dish"))}</h4>
        <div class="price">${formatPrice(pick(d, ["price"], 0))}</div>
      </div>
    `).join("");
  }

  async function loadDishes(categoryId) {
    dishesWrap.innerHTML = `<div class="loading-row">${__("loading")}</div>`;
    try {
      const dishes = await MenuAPI.dishes(categoryId);
      renderDishes(dishes);
    } catch (e) {
      dishesWrap.innerHTML = `<div class="empty-note">${__("loading")}: ${escapeHtml(e.message)}</div>`;
    }
  }

  try {
    const categories = await MenuAPI.categories();
    categories.slice(0, MAX_PREVIEW).forEach((c) => {
      const btn = document.createElement("button");
      btn.textContent = pick(c, ["name", "title"], __("categories").slice(0,-1));
      btn.dataset.cat = pick(c, ["id"], "");
      btn.className = "cat-btn";
      catsWrap.appendChild(btn);
    });
  } catch (e) { console.warn("Failed to load categories:", e); }

  catsWrap.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    catsWrap.querySelectorAll("button").forEach((b) => {
      b.classList.remove("cat-btn-active");
    });
    btn.classList.add("cat-btn-active");
    loadDishes(btn.dataset.cat || null);
  });

  loadDishes(null);

  /* ---------------- Latest news ---------------- */
  const newsWrap = document.getElementById("home-news");
  try {
    const news = await NewsAPI.list();
    if (!news.length) {
      newsWrap.innerHTML = `<div class="empty-note">${__("noNews")}</div>`;
    } else {
      newsWrap.innerHTML = news.slice(0, 3).map((n) => `
        <div class="news-card">
          <img src="${resolveImage(n, seed(n))}" alt="${escapeHtml(pick(n, ["title", "name"], "News"))}">
          <div class="news-body">
            <h4>${escapeHtml(pick(n, ["title", "name"], "News"))}</h4>
            <p>${escapeHtml(pick(n, ["excerpt", "summary", "content", "body"], "").toString().slice(0, 90))}${pick(n, ["excerpt","summary","content","body"],"").length > 90 ? "…" : ""}</p>
            <div class="news-foot">
              <a href="news.html" class="read-more">${__("readMore")}</a>
              <span class="date">${formatDate(pick(n, ["created_at", "date", "published_at"], ""))}</span>
            </div>
          </div>
        </div>
      `).join("");
    }
  } catch (e) {
    newsWrap.innerHTML = `<div class="empty-note">${__("loading")}: ${escapeHtml(e.message)}</div>`;
  }
})();
