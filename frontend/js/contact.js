(function () {
  const form = document.getElementById("contact-form");
  const msg = document.getElementById("contact-msg");
  const submitBtn = document.getElementById("contact-submit");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.textContent = "";
    msg.className = "form-msg";

    const payload = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      phone: form.phone.value.trim(),
      subject: form.subject.value.trim(),
      message: form.message.value.trim(),
    };

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    try {
      await ContactAPI.send(payload);
      msg.textContent = "Сообщение отправлено! Мы свяжемся с вами в ближайшее время.";
      msg.classList.add("ok");
      form.reset();
    } catch (err) {
      msg.textContent = err.message || "Не удалось отправить сообщение. Попробуй ещё раз.";
      msg.classList.add("err");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Send message";
    }
  });
})();
