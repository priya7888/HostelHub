const role = document.querySelector("select");
const room = document.querySelector("input[name='room']");

role.addEventListener("change", function() {
    if (this.value === "student") {
        room.style.display = "block";
    } else {
        room.style.display = "none";
    }
});
