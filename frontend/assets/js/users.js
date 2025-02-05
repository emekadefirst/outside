import { api } from "./api.js";

async function fetchUsers() {
  try {
    const response = await fetch(`${api}/api/v1/users`);
    const data = await response.json();

    if (data.users && data.users.length > 0) {
      const usersBody = document.getElementById("users-body");
      usersBody.innerHTML = ""; // Clear any existing rows

      // Loop through users and insert rows into the table
      data.users.forEach((user) => {
        const userRow = document.createElement("tr");
        userRow.classList.add("border-b", "border-zinc-800");

        userRow.innerHTML = `
                   
                        <td class="py-4 px-4">${user._id}</td>
                        <td>${user.username}</td>
                        <td>${user.email}</td>
                        <td>${user.role}</td>
                        <td>${new Date(user.created_at).toLocaleString()}</td>
                    
                    `;

        usersBody.appendChild(userRow);
      });
    } else {
      console.error("No users found in the response");
    }
  } catch (error) {
    console.error("Error fetching users:", error);
  }
}

// Call the function to load users when the page loads
window.onload = fetchUsers;
