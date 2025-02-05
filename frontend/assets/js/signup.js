import { api } from "./api.js";

document.getElementById("signup-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  try {
    const response = await fetch(`${api}/api/v1user/auth/signup`, {
      // Fixed URL
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      alert("Signup successful! You can now log in.");
      window.location.href = "auth.html"; // Redirect to login page after signup
    } else {
      alert("Signup failed: " + (data.message || "Unknown error"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred during signup");
  }
});
