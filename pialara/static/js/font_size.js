var selectedButton = null; 

function changeSize(size) {
      var textoEjemplo = document.getElementById("textoEjemplo");
      textoEjemplo.style.fontSize = size + "em";
      document.getElementById('font_size').value = size;

  if (selectedButton) {
    selectedButton.classList.remove("btn-primary");
    selectedButton.classList.add("btn-secondary");
  }

  var currentButton = event.target;
  currentButton.classList.remove("btn-secondary");
  currentButton.classList.add("btn-primary");
  selectedButton = currentButton;

    }


function habilitarActualizar() {
  var botonActualizar = document.getElementById('actualizarBtn');
  botonActualizar.disabled = false;
}

// Añadir manejadores de eventos 'change' para los campos de entrada
document.getElementById('nombre').addEventListener('change', habilitarActualizar);
document.getElementById('email').addEventListener('change', habilitarActualizar);

// Añadir manejadores de eventos 'click' para los botones de tamaño de fuente
document.querySelectorAll('.btn.btn-secondary').forEach(button => {
  button.addEventListener('click', habilitarActualizar);
});