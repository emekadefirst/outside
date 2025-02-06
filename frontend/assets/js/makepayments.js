import { api } from "./api.js";

// Use event delegation to handle dynamic ticket button clicks
document.body.addEventListener("click", async (event) => {
  // Check if the clicked element has the class "cop-ticket-btn"
  if (event.target.classList.contains("cop-ticket-btn")) {
    const ticketId = event.target.getAttribute("data-id"); // Get ticket ID from the clicked button
    const userId = sessionStorage.getItem("user_id"); // Get user ID from sessionStorage (you can change to localStorage if needed)

    if (!userId) {
      // Redirect to authentication page if user ID is missing
      window.location.href = "auth.html";
      return;
    }

    try {
      // Prepare request data to send to the API
      const requestData = {
        ticket_id: ticketId,
        user_id: userId,
      };

      // Send the request to the API to initiate payment
      const response = await fetch(`${api}/api/v1/payments/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();

      if (data.authorization_url) {
        // If the response contains the authorization URL, redirect to payment page
        window.location.href = data.authorization_url;
      } else {
        console.error("Payment initiation failed:", data);
        alert("Payment initiation failed. Please try again later.");
      }
    } catch (error) {
      console.error("Error processing payment:", error);
      alert("Error processing payment. Please try again.");
    }
  }
});
