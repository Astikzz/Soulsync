function analyzeMood() {

    let mood = document.querySelector('input[name="mood"]:checked');

    if (mood == null) {

        document.getElementById("result").innerHTML =
        "Please choose one option";

        return;
    }

    if (mood.value == "sad") {

        document.getElementById("result").innerHTML =
        "You seem sad 💙";

    }

    else if (mood.value == "happy") {

        document.getElementById("result").innerHTML =
        "You seem happy 🌟";

    }

    else if (mood.value == "lonely") {

        document.getElementById("result").innerHTML =
        "You seem lonely 🤍";

    }

    else if (mood.value == "confused") {

        document.getElementById("result").innerHTML =
        "You seem confused 😕";

    }


}