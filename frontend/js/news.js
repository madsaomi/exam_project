(async function () {
  const listWrap = document.getElementById("news-list");
  const loadMoreBtn = document.getElementById("load-more-btn");
  const PAGE_SIZE = 6;
  let allNews = [];
  let shown = 0;

  function renderMore() {
    const next = allNews.slice(shown, shown + PAGE_SIZE);
    listWrap.insertAdjacentHTML("beforeend", next.map((n) => `
      <div class="news-card">
        <img src="${resolveImage(n, pick(n, ["id"], Math.random()))}" alt="${escapeHtml(pick(n, ["title", "name"], "Новость"))}">
        <div class="news-body">
          <h4>${escapeHtml(pick(n, ["title", "name"], "Новость"))}</h4>
          <p>${escapeHtml(pick(n, ["excerpt", "summary", "content", "body"], "").toString().slice(0, 110))}${pick(n, ["excerpt","summary","content","body"],"").length > 110 ? "…" : ""}</p>
          <div class="news-foot">
            <a href="#" class="read-more">Read More</a>
            <span class="date">${formatDate(pick(n, ["created_at", "date", "published_at"], ""))}</span>
          </div>
        </div>
      </div>
    `).join(""));
    shown += next.length;
    loadMoreBtn.style.display = shown >= allNews.length ? "none" : "inline-flex";
  }

  try {
    allNews = await NewsAPI.list();
    listWrap.innerHTML = "";
    if (!allNews.length) {
      listWrap.innerHTML = `<div class="empty-note">Новостей пока нет. Добавь первую через /api/news/.</div>`;
      loadMoreBtn.style.display = "none";
    } else {
      renderMore();
    }
  } catch (e) {
    listWrap.innerHTML = `<div class="empty-note">Не удалось загрузить новости: ${escapeHtml(e.message)}</div>`;
    loadMoreBtn.style.display = "none";
  }

  loadMoreBtn.addEventListener("click", renderMore);
})();
