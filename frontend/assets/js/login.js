import { api } from "./api.js";

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(`${api}/api/v1user/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // Check if the user's role is 'admin'
      if (data.role && data.role === "admin") {
        // Redirect to the admin dashboard
        window.location.href = "/admin/dashboard.html";
      } else {
        window.location.href = "index.html";
      }
    } else {
      alert("Login failed: " + data.message);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during login.");
  }
});
