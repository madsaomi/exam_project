(async function () {
  const wrap = document.getElementById("about-content");
  try {
    const about = await AboutAPI.get();
    const data = Array.isArray(about) ? about[0] : (about && about.results ? about.results[0] : about);
    if (!data) {
      wrap.innerHTML = `<p>Информация появится здесь позже.</p>`;
      return;
    }
    const title = pick(data, ["title"], "");
    const text = pick(data, ["content", "text", "description", "body"], "");
    const image = pick(data, ["image", "photo", "picture"], "");

    const paragraphs = String(text)
      .split(/\n+/)
      .filter(Boolean)
      .map((p) => `<p>${escapeHtml(p)}</p>`)
      .join("");

    wrap.innerHTML = `
      ${title ? `<h3 style="margin-bottom:20px;">${escapeHtml(title)}</h3>` : ""}
      ${paragraphs || "<p>Описание пока не заполнено.</p>"}
      <img src="${image ? resolveImage(data, "about") : "https://picsum.photos/seed/londongrill-about/900/600"}" alt="О ресторане">
    `;
  } catch (e) {
    wrap.innerHTML = `<p>Не удалось загрузить информацию: ${escapeHtml(e.message)}</p>
      <img src="https://picsum.photos/seed/londongrill-about/900/600" alt="О ресторане">`;
  }
})();
