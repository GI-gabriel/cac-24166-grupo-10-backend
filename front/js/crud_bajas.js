const URL = "http://127.0.0.1:5000/"
// const URL = "https://gigabriel.serv00.net/"

// Obtiene el contenido del inventario
function obtenerProp() {
  // Realiza una solicitud GET al servidor y obtener la lista.
  fetch(URL + 'propiedades')
    .then(response => {
      // Si es exitosa (response.ok), convierte los datos de la respuesta
      // de formato JSON a un objeto JavaScript.
      if (response.ok) { return response.json(); }
    })
    // Asigna los datos obtenidos.
    .then(data => {
      const propTable = document.getElementById('prop-table').getElementsByTagName('tbody')[0];
      // Limpia la tabla antes de insertar nuevos datos
      propTable.innerHTML = '';
      data.forEach(propiedad => {
        const row = propTable.insertRow();
        row.innerHTML = `<td>${propiedad.id}</td>
                         <td>${propiedad.descrip_corta}</td>
                         <td>${propiedad.direccion}</td>
                         <td style="text-align: right;">${propiedad.precio}</td>
                         <td><button onclick="eliminarProp('${propiedad.id}')">Eliminar</button></td>`;
      });
    })
    // Captura y maneja errores, mostrando una alerta en caso de error al obtener los productos.
    .catch(error => {
      console.log('Error:', error);
      alert('Error al obtener la lista.');
    });
}

// Se utiliza para eliminar una propiedad.
function eliminarProp(id) {
  // Se muestra un diálogo de confirmación. Si el usuario confirma, se realiza una solicitud
  // DELETE servidor a través de fetch(URL + 'propiedad/${id}', { method: 'DELETE' }).
  if (confirm('¿Estás seguro de que quieres eliminar esta propiedad?')) {
    fetch(URL + `propiedades/${id}`, { method: 'DELETE' })
      .then(response => {
        // Si es exitosa (response.ok), elimina y da mensaje de ok.
        if (response.ok) {          
          // Vuelve a obtener la lista de productos para actualizar la tabla.
          obtenerProp();
          alert('Eliminado correctamente.');
        }
      })
      // En caso de error, mostramos una alerta con un mensaje de error.
      .catch(error => {
        alert(error.message);
      });
  }
}
// Cuando la página se carga, llama a obtenerProp para cargar la lista.
document.addEventListener('DOMContentLoaded', obtenerProp);