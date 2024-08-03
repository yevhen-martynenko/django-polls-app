let darkMode = localStorage.getItem("darkMode");

document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".themes-checkbox");
    const checkboxContainer = document.querySelectorAll(".themes-checkbox__container");
    const logoSvg = document.querySelectorAll(".header__logo, .header__logo--mobile, .footer__logo");

    const enableDarkMode = () => {
        document.body.classList.add("darkmode");
        logoSvg.forEach(function(logo) {
            logo.classList.add("logo-svg");
        });
        localStorage.setItem("darkMode", "enabled");
    };
    const disableDarkMode = () => {
        document.body.classList.remove("darkmode");
        logoSvg.forEach(function(logo) {
            logo.classList.remove("logo-svg");
        });
        localStorage.setItem("darkMode", null);
    };
    const updateCheckboxState = () => {
        darkMode = localStorage.getItem("darkMode");
        if (darkMode === "enabled") {
            enableDarkMode();
        } else {
            disableDarkMode();
        }
    };

    const handleCheckboxClick = (checkbox) => {
        const input = checkbox.querySelector("input");
        if (checkbox.classList.contains("active")) {
            input.checked = false;
            disableDarkMode();
        } else {
            input.checked = true;
            enableDarkMode();
        }
        checkbox.classList.toggle("active");
    };

    // checkboxes.forEach(function (checkbox) {
    //     checkbox.addEventListener("click", function (event) {
    //         handleCheckboxClick(this);
    //         event.preventDefault();
    //     });
    // });

    checkboxContainer.forEach(function (container) {
        container.addEventListener("click", function (event) {
            checkboxes.forEach(function (checkbox) {
                handleCheckboxClick(checkbox);
            });
            event.preventDefault();
        });
    });

    updateCheckboxState();
});
