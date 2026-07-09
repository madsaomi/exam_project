(async function () {
  const listWrap = document.getElementById("news-list");
  const loadMoreBtn = document.getElementById("load-more-btn");
  const modal = document.getElementById("news-modal");
  const modalImg = document.getElementById("modal-img");
  const modalTitle = document.getElementById("modal-title");
  const modalDate = document.getElementById("modal-date");
  const modalBody = document.getElementById("modal-body");
  const PAGE_SIZE = 6;
  let allNews = [];
  let shown = 0;

  function openModal(item) {
    const img = resolveImage(item, seed(item));
    const title = escapeHtml(pick(item, ["title", "name"], "News"));
    const date = formatDate(pick(item, ["created_at", "date", "published_at"], ""));
    const full = escapeHtml(pick(item, ["content", "body", "excerpt", "summary"], ""));
    modalImg.src = img;
    modalImg.alt = title;
    modalTitle.textContent = title;
    modalDate.textContent = date;
    modalBody.innerHTML = full.split("\n").filter(Boolean).map(p => `<p>${p}</p>`).join("");
    modal.classList.add("open");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.classList.remove("open");
    document.body.style.overflow = "";
  }

  function renderMore() {
    const next = allNews.slice(shown, shown + PAGE_SIZE);
    next.forEach((n) => {
      const card = document.createElement("div");
      card.className = "news-card";
      const img = resolveImage(n, seed(n));
      const title = escapeHtml(pick(n, ["title", "name"], "News"));
      const excerpt = escapeHtml(pick(n, ["excerpt", "summary", "content", "body"], "").toString().slice(0, 110));
      const hasMore = pick(n, ["excerpt", "summary", "content", "body"], "").length > 110;
      const date = formatDate(pick(n, ["created_at", "date", "published_at"], ""));
      card.innerHTML = `
        <img src="${img}" alt="${title}">
        <div class="news-body">
          <h4>${title}</h4>
          <p>${excerpt}${hasMore ? "…" : ""}</p>
          <div class="news-foot">
            <a href="#" class="read-more">${__("readMore")}</a>
            <span class="date">${date}</span>
          </div>
        </div>
      `;
      card.querySelector(".read-more").addEventListener("click", (e) => {
        e.preventDefault();
        openModal(n);
      });
      listWrap.appendChild(card);
    });
    shown += next.length;
    loadMoreBtn.style.display = shown >= allNews.length ? "none" : "inline-flex";
  }

  try {
    allNews = await NewsAPI.list();
    listWrap.innerHTML = "";
    if (!allNews.length) {
      listWrap.innerHTML = `<div class="empty-note">${__("noNews")}</div>`;
      loadMoreBtn.style.display = "none";
    } else {
      renderMore();
    }
  } catch (e) {
    listWrap.innerHTML = `<div class="empty-note">${__("loading")}: ${escapeHtml(e.message)}</div>`;
    loadMoreBtn.style.display = "none";
  }

  loadMoreBtn.addEventListener("click", renderMore);

  document.getElementById("modal-close").addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => { if (e.target === modal) closeModal(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });
})();
