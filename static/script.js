let countdown;

function startTimer() {

    clearInterval(countdown);

    let totalSeconds = parseInt(
        document.getElementById("seconds").value
    );

    if (isNaN(totalSeconds) || totalSeconds <= 0) {

        alert("Please enter a valid number.");

        return;

    }

    document.getElementById("message").innerHTML = "";

    updateDisplay(totalSeconds);

    countdown = setInterval(function () {

        totalSeconds--;

        updateDisplay(totalSeconds);

        if (totalSeconds <= 0) {

            clearInterval(countdown);

            document.getElementById("message").innerHTML =
                "🎉 Time is Up!";

        }

    }, 1000);

}

function updateDisplay(seconds) {

    let minutes = Math.floor(seconds / 60);

    let remainingSeconds = seconds % 60;

    minutes = String(minutes).padStart(2, "0");

    remainingSeconds = String(remainingSeconds).padStart(2, "0");

    document.getElementById("timer").innerHTML =
        minutes + ":" + remainingSeconds;

}
