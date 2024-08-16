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