const forms = document.querySelectorAll('.js-form');

forms.forEach(form => {
  form.addEventListener('submit', e => {
    e.preventDefault();

    const password = form.querySelector('.js-password');
    const passwordRepeat = form.querySelector('.js-password-repeat');

    password.classList.remove('is-invalid');
    passwordRepeat.classList.remove('is-invalid');

    if (password.value === '') {
      password.classList.add('is-invalid');
    } else if (password.value !== passwordRepeat.value) {
      passwordRepeat.classList.add('is-invalid');
    } else {
      form.submit();
    }
  });
});
