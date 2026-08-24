document.addEventListener('DOMContentLoaded', function () {
    const togglePassword1 = document.querySelector('#togglePassword1');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password1 = document.querySelector('#id_password1');
    const password2 = document.querySelector('#id_password2');

    function setUpToggle(button, password) {
        button.addEventListener('click', function () {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.textContent = this.textContent === '👁️' ? '🙈' : '👁️';
        });
    }

    setUpToggle(togglePassword1, password1);
    setUpToggle(togglePassword2, password2);
});