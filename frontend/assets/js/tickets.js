import { api } from "./api.js";

async function fetchTickets() {
  // Show loading state and hide ticket content
  const loadingDiv = document.getElementById("loading-div");
  const ticketDiv = document.getElementById("ticket-div");

  loadingDiv.style.display = "flex"; // Show loading state
  ticketDiv.style.display = "none"; // Hide ticket content

  try {
    const response = await fetch(`${api}/api/v1/tickets/`);
    const data = await response.json();

    if (data.tickets && data.tickets.length > 0) {
      const ticketBody = document.getElementById("ticket-div");
      ticketBody.innerHTML = ""; // Clear existing content

      data.tickets.forEach((ticket) => {
        const ticketDiv = document.createElement("div");
        ticketDiv.classList.add(
          "bg-white/5",
          "rounded-xl",
          "overflow-hidden",
          "hover:bg-white/10",
          "transition-colors"
        );

        ticketDiv.innerHTML = `
          <div class="flex flex-col md:flex-row">
              <div class="md:w-1/4">
                  <img src="${ticket.banner}" alt="${ticket.name}" class="w-full h-48 md:h-full object-cover" />
              </div>
              <div class="flex-1 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                  <div>
                      <div class="flex items-center gap-4 mb-2">
                          <span class="text-orange-500 text-sm font-semibold">${ticket.date}</span>
                          <span class="text-white/50 text-sm">${ticket.time}</span>
                      </div>
                      <h3 class="text-white text-xl font-bold mb-2">${ticket.name}</h3>
                      <p class="text-white/70 mb-4">${ticket.venue}</p>
                      <div class="flex items-center gap-4">
                       <span class="text-white/50 text-sm">Available: ${ticket.quantity}</span>
                       <span class="text-white/50 text-sm">₦${ticket.unit_price}</span>
                      </div>
                  </div>
                  <div class="flex gap-3 w-full md:w-auto">
                      <button class="flex-1 md:flex-none bg-white/10 hover:bg-white/20 text-white px-6 py-3 rounded-full text-sm font-semibold transition-colors">
                          Add to Watchlist
                      </button>
                      <button class="flex-1 md:flex-none bg-white text-black px-6 py-3 rounded-full text-sm font-semibold hover:scale-105 transition-transform">
                          Cop Tickets
                      </button>
                  </div>
              </div>
          </div>
        `;

        ticketBody.appendChild(ticketDiv);
      });

      // Hide loading and show ticket content once data is available
      loadingDiv.style.display = "none"; // Hide loading state
      ticketDiv.style.display = "grid"; // Show ticket content
    } else {
      console.error("No tickets found in the response");
    }
  } catch (error) {
    console.error("Error fetching tickets:", error);
    // Handle error (optional)
  }
}

window.onload = fetchTickets;