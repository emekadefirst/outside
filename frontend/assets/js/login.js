import { api } from './api.js'

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const loginBtn = document.getElementById("loginBtn");

  // Add a spinner and change button text
  loginBtn.innerHTML =
    'Logging in... <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
  loginBtn.disabled = true;

  try {
    const response = await fetch(`${api}/api/v1user/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    console.log(data);

    if (response.ok) {
      // Store access token and user data
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user_id", data.data.id);
      localStorage.setItem("username", data.data.username);
      localStorage.setItem("email", data.data.email);
      localStorage.setItem("role", data.data.role);

      // Redirect based on role
      if (data.data.role === "admin") {
        window.location.href = "./dashboard.html";
      } else {
        window.location.href = "index.html";
      }
    } else {
      alert("Login failed: " + (data.message || "Invalid credentials"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during login.");
  } finally {
    // Revert button text and enable it again
    loginBtn.innerHTML = "Login";
    loginBtn.disabled = false;
  }
});
