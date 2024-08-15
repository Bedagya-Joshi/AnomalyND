const profileImage = document.getElementById("profile");
const dropdown = document.getElementById("profileDropdownContent");

profileImage.addEventListener("mouseover", () => {
  dropdown.classList.add("show");
});

profileImage.addEventListener("mouseout", () => {
  dropdown.classList.remove("show");
});
