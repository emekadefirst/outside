import { api } from "./api.js";

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(`${api}/api/v1user/auth/login`, {
      // Fixed URL
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    console.log(data);

    if (response.ok) {
      // Store access token
      localStorage.setItem("access_token", data.access_token); // Fixed key name

      // Store user data properly
      localStorage.setItem("user_id", data.data.id);
      localStorage.setItem("username", data.data.username);
      localStorage.setItem("email", data.data.email);
      localStorage.setItem("role", data.data.role);

      // Redirect based on role
      if (data.data.role === "admin") {
        window.location.href = "/admin/dashboard.html";
      } else {
        window.location.href = "index.html";
      }
    } else {
      alert("Login failed: " + (data.message || "Invalid credentials"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during login.");
  }
});
