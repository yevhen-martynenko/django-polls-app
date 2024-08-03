const burger_menu = document.querySelector('.header__burger');

if (burger_menu) {
    const burger = document.querySelector('.header__container');

    // ! error: when the menu is opened and then the screen extension is changed to breakpoint2-, the header breaks
    burger_menu.addEventListener('click', function () {
        document.body.classList.toggle('lock');
        burger_menu.classList.toggle('active');
        burger.classList.toggle('active');
    });
}