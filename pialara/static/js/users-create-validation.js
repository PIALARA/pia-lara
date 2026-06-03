const forms = document.querySelectorAll('.js-form');

forms.forEach(form => {
  form.addEventListener('submit', e => {
    e.preventDefault();

    const password = form.querySelector('.js-password');
    const passwordRepeat = form.querySelector('.js-password-repeat');

    // Primero limpiamos cualquier error anterior
    password.classList.remove('is-invalid');
    passwordRepeat.classList.remove('is-invalid');
    
    // Si tienes un contenedor para forzar un mensaje personalizado, se actualiza aquí:
    const invalidFeedback = password.nextElementSibling;
    if (invalidFeedback && invalidFeedback.classList.contains('invalid-feedback')) {
        invalidFeedback.textContent = "La contraseña no puede estar vacía.";
    }

    if (password.value === '') {
      password.classList.add('is-invalid');
    } else if (password.value.length < 8) {
      // Validar longitud mínima de 8 caracteres
      if (invalidFeedback && invalidFeedback.classList.contains('invalid-feedback')) {
        invalidFeedback.textContent = "La contraseña debe tener al menos 8 caracteres.";
      }
      password.classList.add('is-invalid');
    } else if (password.value !== passwordRepeat.value) {
      passwordRepeat.classList.add('is-invalid');
    } else {
      form.submit();
    }
  });
});
