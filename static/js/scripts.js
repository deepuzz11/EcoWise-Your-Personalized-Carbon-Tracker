document.addEventListener("DOMContentLoaded", () => {
    fetch("/weather-insights?city=Delhi")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("weather-info").textContent = "Error fetching weather data.";
            } else {
                const { city, temperature, description } = data;
                document.getElementById("weather-info").innerHTML =
                    `<b>${city}:</b> ${temperature}°C, ${description}`;
            }
        })
        .catch(err => {
            document.getElementById("weather-info").textContent = "Error fetching weather data.";
        });
});
