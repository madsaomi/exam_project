(function () {
  const form = document.getElementById("contact-form");
  const msg = document.getElementById("contact-msg");
  const submitBtn = document.getElementById("contact-submit");
  if (!form || !msg || !submitBtn) return;

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
    submitBtn.textContent = __("loading");

    try {
      await ContactAPI.send(payload);
      msg.textContent = __("contactSuccess");
      msg.classList.add("ok");
      form.reset();
    } catch (err) {
      msg.textContent = err.message || __("contactError");
      msg.classList.add("err");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = __("send");
    }
  });
})();
