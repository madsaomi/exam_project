(function () {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    const msg = document.getElementById("login-msg");
    const btn = document.getElementById("login-submit");
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      msg.textContent = "";
      msg.className = "form-msg";
      btn.disabled = true;
      btn.textContent = "Входим…";
      try {
        const data = await AuthAPI.login({
          username: loginForm.username.value.trim(),
          password: loginForm.password.value,
        });
        Auth.set(data.access, data.refresh);
        msg.textContent = "Вход выполнен! Перенаправляем…";
        msg.classList.add("ok");
        setTimeout(() => (window.location.href = "index.html"), 700);
      } catch (err) {
        msg.textContent = err.message || "Неверный логин или пароль.";
        msg.classList.add("err");
      } finally {
        btn.disabled = false;
        btn.textContent = "Log In";
      }
    });
  }

  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    const msg = document.getElementById("register-msg");
    const btn = document.getElementById("register-submit");
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      msg.textContent = "";
      msg.className = "form-msg";

      if (registerForm.password.value !== registerForm.password2.value) {
        msg.textContent = "Пароли не совпадают.";
        msg.classList.add("err");
        return;
      }

      btn.disabled = true;
      btn.textContent = "Создаём аккаунт…";
      try {
        await AuthAPI.register({
          username: registerForm.username.value.trim(),
          email: registerForm.email.value.trim(),
          password: registerForm.password.value,
        });
        msg.textContent = "Аккаунт создан! Теперь можно войти.";
        msg.classList.add("ok");
        setTimeout(() => (window.location.href = "login.html"), 900);
      } catch (err) {
        msg.textContent = err.message || "Не удалось зарегистрироваться.";
        msg.classList.add("err");
      } finally {
        btn.disabled = false;
        btn.textContent = "Create Account";
      }
    });
  }
})();
