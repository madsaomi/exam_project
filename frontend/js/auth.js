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
      btn.textContent = __("loading");
      try {
        const data = await AuthAPI.login({
          username: loginForm.username.value.trim(),
          password: loginForm.password.value,
        });
        Auth.set(data.access, data.refresh);
        msg.textContent = __("login") + "...";
        msg.classList.add("ok");
        setTimeout(() => (window.location.href = "index.html"), 700);
      } catch (err) {
        msg.textContent = err.message || "Login failed";
        msg.classList.add("err");
      } finally {
        btn.disabled = false;
        btn.textContent = __("signIn");
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

      const pw = registerForm.password.value;
      if (pw !== registerForm.password2.value) {
        msg.textContent = "Passwords do not match";
        msg.classList.add("err");
        return;
      }
      if (pw.length < 8) {
        msg.textContent = "Password must be at least 8 characters";
        msg.classList.add("err");
        return;
      }

      btn.disabled = true;
      btn.textContent = __("loading");
      try {
        await AuthAPI.register({
          username: registerForm.username.value.trim(),
          email: registerForm.email.value.trim(),
          password: registerForm.password.value,
        });
        msg.textContent = __("registerSuccess");
        msg.classList.add("ok");
        setTimeout(() => (window.location.href = "login.html"), 900);
      } catch (err) {
        msg.textContent = err.message || "Registration failed";
        msg.classList.add("err");
      } finally {
        btn.disabled = false;
        btn.textContent = __("signUp");
      }
    });
  }
})();
