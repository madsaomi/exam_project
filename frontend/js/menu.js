(async function () {
  const catsWrap = document.getElementById("menu-categories");
  const dishesWrap = document.getElementById("menu-dishes");

  function renderDishes(list) {
    if (!list.length) {
      dishesWrap.innerHTML = `<div class="empty-note">No dishes in this category yet.</div>`;
      return;
    }
    dishesWrap.innerHTML = list.map((d) => `
      <div class="menu-item">
        <img src="${resolveImage(d, seed(d))}" alt="${escapeHtml(pick(d, ["name", "title"], "Dish"))}">
        <h4>${escapeHtml(pick(d, ["name", "title"], "Dish"))}</h4>
        <div class="price">${formatPrice(pick(d, ["price"], 0))}</div>
      </div>
    `).join("");
  }

  async function loadDishes(categoryId) {
    dishesWrap.innerHTML = `<div class="loading-row">Loading menu…</div>`;
    try {
      const dishes = await MenuAPI.dishes(categoryId);
      renderDishes(dishes);
    } catch (e) {
      dishesWrap.innerHTML = `<div class="empty-note">Failed to load menu: ${escapeHtml(e.message)}</div>`;
    }
  }

  try {
    const categories = await MenuAPI.categories();
    categories.forEach((c) => {
      const btn = document.createElement("button");
      btn.textContent = pick(c, ["name", "title"], "Category");
      btn.dataset.cat = pick(c, ["id"], "");
      catsWrap.appendChild(btn);
    });
  } catch (e) {
    const note = document.createElement("p");
    note.style.cssText = "color:rgba(255,255,255,.75); font-size:13px;";
    note.textContent = "Failed to load categories.";
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
