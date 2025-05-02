function startClock() {
    function updateClock() {
        // Get the current time
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        let seconds = now.getSeconds();
        let period = hours >= 12 ? "PM" : "AM";

        // Convert 24-hour format to 12-hour format
        hours = hours % 12;
        hours = hours ? hours : 12; // Hour '0' should be '12'

        // Format time as HH:MM:SS AM/PM
        let formattedHours = hours < 10 ? "0" + hours : hours;
        let formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
        let formattedSeconds = seconds < 10 ? "0" + seconds : seconds;

        // Display time
        document.getElementById("clock").textContent = `${formattedHours}:${formattedMinutes}:${formattedSeconds} ${period}`;
    }

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock(); // Initialize clock immediately
}

// Start the clock
startClock();