const profileImage = document.getElementById("profile");
const dropdown = document.getElementById("profileDropdownContent");
let timeoutId;

document.getElementById("profile").addEventListener("mouseover", function (event) {
    event.stopPropagation();
    dropdown.classList.toggle("show");
});

document
    .getElementById("profileDropdownContent")
    .addEventListener("mouseover", function () {
        dropdown.classList.add("show");
        clearTimeout(timeoutId);
});

document.getElementById("profile").addEventListener("mouseleave", function (event) {
    timeoutId = setTimeout(() => {
        event.stopPropagation();
        dropdown.classList.toggle("show");
    }, 100); 
});

document
    .getElementById("profileDropdownContent")
    .addEventListener("mouseleave", function () {
        timeoutId = setTimeout(() => {
        dropdown.classList.remove("show");
        }, 100); 
});