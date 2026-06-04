function openSignupModal() {
    document.getElementById("signupModal").style.display = "block";
}

function closeSignupModal() {
    document.getElementById("signupModal").style.display = "none";
}

function openLoginModal() {
    document.getElementById("loginModal").style.display = "block";
}

function closeLoginModal() {
    document.getElementById("loginModal").style.display = "none";
}

function signup() {
    let username = document.getElementById("signupUsername").value;
    let password = document.getElementById("signupPassword").value;

    fetch("https://soulsync-rosy.vercel.app/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("signupResult").innerHTML = data.message;
    })
    .catch(error => {
        console.log(error);
        document.getElementById("signupResult").innerHTML = "Signup failed";
    });
}

function login() {
    let username = document.getElementById("loginUsername").value;
    let password = document.getElementById("loginPassword").value;

    fetch("https://soulsync-rosy.vercel.app/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loginResult").innerHTML = data.message;

        if (data.user_id) {
            localStorage.setItem("soulsync_user_id", data.user_id);
            localStorage.setItem("soulsync_username", data.username);
           document.getElementById("welcomeUser").innerText =
"Logged in as " + username;
            closeLoginModal();
            location.reload();
        }
    })
    .catch(error => {
        console.log(error);
        document.getElementById("loginResult").innerHTML = "Login failed";
    });
}

function logout() {
    localStorage.removeItem("soulsync_user_id");
    localStorage.removeItem("soulsync_username");
    document.getElementById("welcomeUser").innerHTML = "Logged out successfully";
    location.reload();
}

function analyzeMood() {
    let mood = document.querySelector('input[name="mood"]:checked');
    let userId = localStorage.getItem("soulsync_user_id");

    if (mood == null) {
        document.getElementById("result").innerHTML = "Please choose one option";
        return;
    }

    if (!userId) {
        document.getElementById("result").innerHTML = "Please login first";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/mood", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mood: mood.value,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = data.response;
    })
    .catch(error => {
        console.log(error);
        document.getElementById("result").innerHTML = "Could not connect to backend.";
    });
}

function loadHistory() {
    let userId = localStorage.getItem("soulsync_user_id");

    if (!userId) {
        document.getElementById("history").innerHTML = "<p>Please login first.</p>";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/history?user_id=" + userId)
        .then(response => response.json())
        .then(data => {
            let historyDiv = document.getElementById("history");
            historyDiv.innerHTML = "";

            if (data.length === 0) {
                historyDiv.innerHTML = "<p>No mood history yet.</p>";
                return;
            }

            data.forEach(item => {
                historyDiv.innerHTML += `<p>${item.mood} - ${item.created_at}</p>`;
            });
        })
        .catch(error => {
            console.log(error);
            document.getElementById("history").innerHTML = "<p>Could not load history.</p>";
        });
}

function loadStats() {
    let userId = localStorage.getItem("soulsync_user_id");

    if (!userId) {
        document.getElementById("stats").innerHTML = "<p>Please login first.</p>";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/stats?user_id=" + userId)
        .then(response => response.json())
        .then(data => {
            let statsDiv = document.getElementById("stats");
            statsDiv.innerHTML = "";

            if (data.length === 0) {
                statsDiv.innerHTML = "<p>No mood data yet.</p>";
                return;
            }

            data.forEach(item => {
                let emoji = "🤔";

                if (item.mood == "happy") {
                    emoji = "😊";
                } else if (item.mood == "sad") {
                    emoji = "💙";
                } else if (item.mood == "lonely") {
                    emoji = "🤍";
                } else if (item.mood == "confused") {
                    emoji = "😕";
                }

                statsDiv.innerHTML += `<p>${emoji} ${item.mood} : ${item.count}</p>`;
            });
        })
        .catch(error => {
            console.log(error);
            document.getElementById("stats").innerHTML = "<p>Could not load analytics.</p>";
        });
}

window.onload = function() {
    let username = localStorage.getItem("soulsync_username");

    if (username) {
        document.getElementById("welcomeUser").innerHTML = "👋 Welcome, " + username;
    }
};
function saveJournal() {
    let entry = document.getElementById("journalText").value;
    let userId = localStorage.getItem("soulsync_user_id");

    if (!entry) {
        document.getElementById("journals").innerHTML = "<p>Please write something first.</p>";
        return;
    }

    if (!userId) {
        document.getElementById("journals").innerHTML = "<p>Please login first.</p>";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/journal", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            entry: entry,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("journals").innerHTML = data.message;
        document.getElementById("journalText").value = "";
    })
    .catch(error => {
        console.log(error);
        document.getElementById("journals").innerHTML = "<p>Could not save journal.</p>";
    });
}

function loadJournals() {
    let userId = localStorage.getItem("soulsync_user_id");

    if (!userId) {
        document.getElementById("journals").innerHTML = "<p>Please login first.</p>";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/journals?user_id=" + userId)
        .then(response => response.json())
        .then(data => {
            let journalsDiv = document.getElementById("journals");
            journalsDiv.innerHTML = "";

            if (data.length === 0) {
                journalsDiv.innerHTML = "<p>No journal entries yet.</p>";
                return;
            }

            data.forEach(item => {
                journalsDiv.innerHTML += `<p>${item.entry} <br><small>${item.created_at}</small></p>`;
            });
        })
        .catch(error => {
            console.log(error);
            document.getElementById("journals").innerHTML = "<p>Could not load journals.</p>";
        });
}function openJournalModal() {
    document.getElementById("journalModal").style.display = "block";
}

function closeJournalModal() {
    document.getElementById("journalModal").style.display = "none";
}

function saveJournal() {
    let entry = document.getElementById("journalText").value;
    let userId = localStorage.getItem("soulsync_user_id");

    if (!entry) {
        document.getElementById("journals").innerHTML = "<p>Please write something first.</p>";
        return;
    }

    if (!userId) {
        document.getElementById("journals").innerHTML = "<p>Please login first.</p>";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/journal", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            entry: entry,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("journals").innerHTML = data.message;
        document.getElementById("journalText").value = "";
    })
    .catch(error => {
        console.log(error);
        document.getElementById("journals").innerHTML = "<p>Could not save journal.</p>";
    });
}

function loadJournals() {
    let userId = localStorage.getItem("soulsync_user_id");

    if (!userId) {
        document.getElementById("journals").innerHTML = "<p>Please login first.</p>";
        return;
    }

    fetch("https://soulsync-rosy.vercel.app/journals?user_id=" + userId)
        .then(response => response.json())
        .then(data => {
            let journalsDiv = document.getElementById("journals");
            journalsDiv.innerHTML = "";

            if (data.length === 0) {
                journalsDiv.innerHTML = "<p>No journal entries yet.</p>";
                return;
            }

            data.forEach(item => {
                journalsDiv.innerHTML += `<p>${item.entry}<br><small>${item.created_at}</small></p>`;
            });
        })
        .catch(error => {
            console.log(error);
            document.getElementById("journals").innerHTML = "<p>Could not load journals.</p>";
        });
}