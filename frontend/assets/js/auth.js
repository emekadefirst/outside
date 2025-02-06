window.onload = function() {
    // Retrieve session data
    const accessCode = localStorage.getItem('access_token');
    const username = localStorage.getItem('username');
    const email = localStorage.getItem('email');
    const role = localStorage.getItem('role');
    const userId = localStorage.getItem('user_id');

    
    if (!accessCode || !username || !email || !role || !userId || role !== 'admin') {
        window.location.href = "./index.html";
    }
}
