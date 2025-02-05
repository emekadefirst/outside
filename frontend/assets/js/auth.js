
document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("access_token");
  const username = localStorage.getItem("username");

  if (!token || !username) {
    window.location.href = "/";
  }
});