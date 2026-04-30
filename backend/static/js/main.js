document.addEventListener("DOMContentLoaded", () => {
    const dateTimeElement = document.getElementById("dateTime");

    // Update the top bar with the current local date and time.
    function updateDateTime() {
        const now = new Date();
        const formattedDate = now.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "long",
            year: "numeric"
        });
        const formattedTime = now.toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        });

        if (dateTimeElement) {
            dateTimeElement.textContent = `${formattedDate} | ${formattedTime}`;
        }
    }

    updateDateTime();
    setInterval(updateDateTime, 1000);
});
