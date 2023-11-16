// Aplicar las preferencias de accesibilidad al cargar la página
document.addEventListener('DOMContentLoaded', (event) => {
    const savedColorScheme = localStorage.getItem('preferredColorScheme');
    const savedTextSize = localStorage.getItem('preferredTextSize');
  
    if (savedColorScheme) {
      changeColorScheme(savedColorScheme);
    }
  
    if (savedTextSize) {
      changeTextSize(savedTextSize);
    }
  });
  