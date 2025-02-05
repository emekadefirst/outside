import { api } from "./api.js";

async function fetchTickets() {
  try {
    const response = await fetch(`${api}/api/v1/tickets/`); // Fixed backticks
    const data = await response.json();

    if (data.tickets && data.tickets.length > 0) {
      const ticketsBody = document.getElementById("tickets-body"); // Fixed ID
      ticketsBody.innerHTML = ""; // Clear any existing rows

      // Loop through tickets and insert rows into the table
      data.tickets.forEach((ticket) => {
        // Fixed "data.ticket" to "data.tickets"
        const ticketRow = document.createElement("tr");
        ticketRow.classList.add("border-b", "border-zinc-800");

        ticketRow.innerHTML = `
          <td class="py-4 px-4">${ticket._id}</td>
          <td>${ticket.name}</td>
          <td>${ticket.date}</td>
          <td>${ticket.venue}</td>
          <td>${new Date(ticket.created_at).toLocaleString()}</td>
        `; // Fixed template literal usage

        ticketsBody.appendChild(ticketRow);
      });
    } else {
      console.error("No tickets found in the response"); // Fixed "users" to "tickets"
    }
  } catch (error) {
    console.error("Error fetching tickets:", error); // Fixed "users" to "tickets"
  }
}

// Call the function to load tickets when the page loads
window.onload = fetchTickets;


async function fetchRecentEvent() {
  try {
    const response = await fetch(`${api}/api/v1/tickets/`); // Adjust API endpoint if needed
    const data = await response.json();

    if (data.tickets && data.tickets.length > 0) {
      // Sort events by date (most recent first)
      data.tickets.sort((a, b) => new Date(b.date) - new Date(a.date));

      // Get the most recent event
      const recentEvent = data.tickets[0];

      // Select the table body
      const eventBody = document.querySelector("tbody"); // Adjust if you have multiple tables

      // Clear existing rows
      eventBody.innerHTML = "";

      // Create a new row for the recent event
      const eventRow = document.createElement("tr");
      eventRow.classList.add("border-b", "border-zinc-800");

      eventRow.innerHTML = `
        <td class="py-4">${recentEvent.name}</td>
        <td>${new Date(recentEvent.date).toLocaleDateString()}</td>
        <td>${recentEvent.venue}</td>
        <td>${recentEvent.quantity}</td>
        <td>${recentEvent.unit_price}</td>
      `;

      // Append the row
      eventBody.appendChild(eventRow);
    } else {
      console.error("No events found");
    }
  } catch (error) {
    console.error("Error fetching events:", error);
  }
}

// Call the function on page load
window.onload = fetchRecentEvent;

