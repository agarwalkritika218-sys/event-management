function registerUser() {
    const name = document.getElementById("name")?.value;
    const email = document.getElementById("email")?.value;
    const password = document.getElementById("password")?.value;

    if (!name || !email || !password) {
        alert("Please fill all fields");
        return;
    }

    fetch("http://127.0.0.1:10000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, password })
    })
    .then(res => {
        if (!res.ok) throw new Error("Server error");
        return res.json();
    })
    .then(data => {
        alert(data.message);
    })
    .catch(err => {
        console.error(err);
        alert("Backend not reachable");
    });
}