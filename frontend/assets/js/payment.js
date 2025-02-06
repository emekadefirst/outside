import { api } from "./api.js";

async function fetchPayments() {
  try {
    const response = await fetch(`${api}/api/v1/payments`);
    const data = await response.json();

    if (data.payments && data.payments.length > 0) {
      const paymentsBody = document.getElementById("tickets-body"); // Ensure correct ID
      paymentsBody.innerHTML = ""; // Clear existing rows

      data.payments.forEach((payment) => {
        const paymentRow = document.createElement("tr");
        paymentRow.classList.add("border-b", "border-zinc-800");

        paymentRow.innerHTML = `
          <td class="py-4">${payment.user}</td>
          <td>${payment.ticket_name || "N/A"}</td>
          <td>${payment.reference_id}</td>
          <td>${payment.status}</td>
          <td>${new Date(payment.created_at).toLocaleString()}</td>
          <td>${payment.amount}</td>
          <td>${payment.ticket_code || "N/A"}</td>
        `;

        paymentsBody.appendChild(paymentRow);
      });
    } else {
      console.error("No payments found in the response");
    }
  } catch (error) {
    console.error("Error fetching payments:", error);
  }
}

window.addEventListener("load", fetchPayments);
