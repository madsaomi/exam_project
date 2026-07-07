(async function () {
  /* ---------------- Popular dishes (simple carousel: shift 4 at a time) ---------------- */
  const popularWrap = document.getElementById("popular-dishes");
  let popularDishes = [];
  let popularPage = 0;
  const PER_PAGE = 4;

  function renderPopular() {
    if (!popularDishes.length) {
      popularWrap.innerHTML = `<div class="empty-note">Пока нет добавленных блюд. Добавь их через /api/menu/dishes/.</div>`;
      return;
    }
    const start = popularPage * PER_PAGE;
    const slice = popularDishes.slice(start, start + PER_PAGE);
    popularWrap.innerHTML = slice.map((d) => `
      <div class="dish-card">
        <img src="${resolveImage(d, pick(d, ["id"], Math.random()))}" alt="${escapeHtml(pick(d, ["name", "title"], "Блюдо"))}">
        <h4>${escapeHtml(pick(d, ["name", "title"], "Блюдо"))}</h4>
        <div class="dish-stars">&#9733;&#9733;&#9733;&#9733;&#9734;</div>
        <div class="dish-price">${formatPrice(pick(d, ["price"], 0))}</div>
      </div>
    `).join("");
  }

  try {
    popularDishes = await MenuAPI.dishes();
    renderPopular();
  } catch (e) {
    popularWrap.innerHTML = `<div class="empty-note">Не удалось загрузить блюда: ${escapeHtml(e.message)}</div>`;
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
      dishesWrap.innerHTML = `<div class="empty-note">Блюда в этой категории пока не добавлены.</div>`;
      return;
    }
    dishesWrap.innerHTML = list.slice(0, 8).map((d) => `
      <div class="menu-item">
        <img src="${resolveImage(d, pick(d, ["id"], Math.random()))}" alt="${escapeHtml(pick(d, ["name", "title"], "Блюдо"))}">
        <h4>${escapeHtml(pick(d, ["name", "title"], "Блюдо"))}</h4>
        <div class="price">${formatPrice(pick(d, ["price"], 0))}</div>
      </div>
    `).join("");
  }

  async function loadDishes(categoryId) {
    dishesWrap.innerHTML = `<div class="loading-row">Загружаем меню…</div>`;
    try {
      const dishes = await MenuAPI.dishes(categoryId);
      renderDishes(dishes);
    } catch (e) {
      dishesWrap.innerHTML = `<div class="empty-note">Не удалось загрузить меню: ${escapeHtml(e.message)}</div>`;
    }
  }

  try {
    const categories = await MenuAPI.categories();
    categories.slice(0, 8).forEach((c) => {
      const btn = document.createElement("button");
      btn.textContent = pick(c, ["name", "title"], "Категория");
      btn.dataset.cat = pick(c, ["id"], "");
      btn.style.cssText = "border-radius:30px; padding:10px 22px; font-size:13px; border:1.5px solid var(--red); background:transparent; color:var(--red); font-weight:600;";
      catsWrap.appendChild(btn);
    });
  } catch (e) { /* categories are optional for the preview */ }

  catsWrap.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    catsWrap.querySelectorAll("button").forEach((b) => {
      b.classList.remove("btn-primary");
      b.style.background = "transparent";
      b.style.color = "var(--red)";
    });
    btn.classList.add("btn-primary");
    btn.style.background = "var(--red)";
    btn.style.color = "#fff";
    loadDishes(btn.dataset.cat || null);
  });

  loadDishes(null);

  /* ---------------- Latest news ---------------- */
  const newsWrap = document.getElementById("home-news");
  try {
    const news = await NewsAPI.list();
    if (!news.length) {
      newsWrap.innerHTML = `<div class="empty-note">Новостей пока нет. Добавь первую через /api/news/.</div>`;
    } else {
      newsWrap.innerHTML = news.slice(0, 3).map((n) => `
        <div class="news-card">
          <img src="${resolveImage(n, pick(n, ["id"], Math.random()))}" alt="${escapeHtml(pick(n, ["title", "name"], "Новость"))}">
          <div class="news-body">
            <h4>${escapeHtml(pick(n, ["title", "name"], "Новость"))}</h4>
            <p>${escapeHtml(pick(n, ["excerpt", "summary", "content", "body"], "").toString().slice(0, 90))}${pick(n, ["excerpt","summary","content","body"],"").length > 90 ? "…" : ""}</p>
            <div class="news-foot">
              <a href="news.html" class="read-more">Read More</a>
              <span class="date">${formatDate(pick(n, ["created_at", "date", "published_at"], ""))}</span>
            </div>
          </div>
        </div>
      `).join("");
    }
  } catch (e) {
    newsWrap.innerHTML = `<div class="empty-note">Не удалось загрузить новости: ${escapeHtml(e.message)}</div>`;
  }
})();
