const profileImage = document.getElementById("profile");
const dropdown = document.getElementById("profileDropdownContent");
const notif = document.getElementById("notification");
const notiDropdown = document.getElementById("notifDropdownContent");

let timeoutId;

//Dropdown show for profilePic
document.getElementById("profile").addEventListener("mouseover", function (event) {
    event.stopPropagation();
    dropdown.classList.toggle("show");
});

//dropdown show for profileDropdown
document
    .getElementById("profileDropdownContent")
    .addEventListener("mouseover", function () {
        dropdown.classList.add("show");
        clearTimeout(timeoutId);
});

//dropdown hide for profilePic
document.getElementById("profile").addEventListener("mouseleave", function (event) {
    timeoutId = setTimeout(() => {
        event.stopPropagation();
        dropdown.classList.toggle("show");
    }, 100); 
});

//dropdown hide for profileDropdown
document
    .getElementById("profileDropdownContent")
    .addEventListener("mouseleave", function () {
        timeoutId = setTimeout(() => {
        dropdown.classList.remove("show");
        }, 100); 
});

//toggle on off switch on dashboard
const toggleBtn = document.getElementById("toggleBtn");
const offImg = document.getElementById("off");
const onImg = document.getElementById("on");
const statusText = document.getElementById("status");

toggleBtn.addEventListener("click", () => {
  offImg.classList.toggle("active");
  onImg.classList.toggle("active");

  if (offImg.classList.contains("active")) {
    statusText.textContent = "Start Capturing";
  } else {
    statusText.textContent = "Stop Capturing";
  }
});