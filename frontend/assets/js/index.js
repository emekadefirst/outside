import { api } from "./api.js";

async function fetchRecentEvent() {
  try {
    const response = await fetch(`${api}/api/v1/tickets/`);
    const data = await response.json();

    if (data.tickets && data.tickets.length > 0) {
      // Sort events by date (most recent first)
      data.tickets.sort((a, b) => new Date(b.date) - new Date(a.date));

      // Get the most recent event
      const recentEvent = data.tickets[0];

      // Select the container for the event
      const eventBody = document.getElementById("recent");

      // Clear existing content
      eventBody.innerHTML = "";

      // Fallback for missing banner
      const bannerImage = recentEvent.banner || "assets/img/default-event.jpg";

      // Format date properly
      const eventDate = new Date(recentEvent.date).toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
      });

      // Create a new event card
      const eventRow = document.createElement("div");
      eventRow.classList.add(
        "group",
        "relative",
        "rounded-xl",
        "overflow-hidden",
        "hover:scale-[1.02]",
        "transition-transform"
      );

      eventRow.innerHTML = `
        <div class="absolute inset-0 bg-gradient-to-t from-black/90 to-transparent z-10"></div>
        <img src="${bannerImage}" alt="Event" class="w-full h-[400px] object-cover" />
        <div class="absolute bottom-0 left-0 right-0 p-6 z-20">
          <span class="text-white/70 text-sm mb-2 block">${eventDate}</span>
          <h3 class="text-white text-xl font-bold mb-2">${recentEvent.name}</h3>
          <p class="text-white/70 text-sm">${recentEvent.venue}</p>
        </div>
      `;

      // Append the event card
      eventBody.appendChild(eventRow);
    } else {
      console.warn("No events found");
    }
  } catch (error) {
    console.error("Error fetching events:", error);
  }
}

// Fetch on page load
document.addEventListener("DOMContentLoaded", fetchRecentEvent);
