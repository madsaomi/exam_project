(async function () {
  const catsWrap = document.getElementById("menu-categories");
  const dishesWrap = document.getElementById("menu-dishes");

  function renderDishes(list) {
    if (!list.length) {
      dishesWrap.innerHTML = `<div class="empty-note">Блюда в этой категории пока не добавлены.</div>`;
      return;
    }
    dishesWrap.innerHTML = list.map((d) => `
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
    categories.forEach((c) => {
      const btn = document.createElement("button");
      btn.textContent = pick(c, ["name", "title"], "Категория");
      btn.dataset.cat = pick(c, ["id"], "");
      catsWrap.appendChild(btn);
    });
  } catch (e) {
    const note = document.createElement("p");
    note.style.cssText = "color:rgba(255,255,255,.75); font-size:13px;";
    note.textContent = "Не удалось загрузить категории.";
    catsWrap.appendChild(note);
  }

  catsWrap.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    catsWrap.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    loadDishes(btn.dataset.cat || null);
  });

  loadDishes(null);
})();
