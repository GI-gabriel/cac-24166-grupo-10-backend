const URL = "http://localhost:5000/"
// const URL = "https://gigabriel.serv00.net/"

// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function (event) {
  event.preventDefault(); // Evitamos que se envie el form

  var formData = new FormData(this);
  // Realizamos la solicitud POST al servidor
    fetch(URL + 'propiedades', {
    // Aquí enviamos formData. Dado que formData puede contener archivos,
    // no se utiliza JSON.
    method: 'POST',
    credentials: 'include',
    body: formData
  })
    // Después de realizar la solicitud POST, se utiliza el método then()
    // para manejar la respuesta del servidor.
    .then(function (response) {
      if (response.ok) {
        // Si la respuesta es exitosa, convierte respuesta a JSON.
        return response.json();
      } else {
        // Si hubo un error, lanzar explícitamente una excepción
        // para ser "catcheada" más adelante
        throw new Error('Error al agregar.');
      }
    })
    // Respuesta OK, muestra una alerta informando que el producto se agregó
    // correctamente y limpia los campos del formulario para que puedan ser
    // utilizados para un nuevo producto.
    .then(function (data) {
      alert('Agregado correctamente.');
    })
    // En caso de error, mostramos una alerta con un mensaje de error.
    .catch(function (error) {
      alert('Error al agregar.');
    })
    // Limpiar el formulario en ambos casos (éxito o error)
    .finally(function () {
      elems = document.querySelectorAll('#formulario > input');

      elems.forEach(elem => {
        elem.value = "";
      });
    });
})