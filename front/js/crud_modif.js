const URL = "http://127.0.0.1:5000/"
// const URL = "https://gigabriel.serv00.net/"

// Variables de estado para controlar la visibilidad y los datos del formulario
let id = '';
let descrip_corta = '';
let descrip_larga = '';
let direccion = '';
let nota = '';
let url_foto_1 = '';
let url_foto_2 = '';
let url_foto_3 = '';
let url_maps = '';
let id_broker = '';
let precio = '';
let superf = '';
let superf_total = '';
let baños = '';
let dormitorios = '';
let cocheras = '';
let basicos = '';
let servicios = '';
let amenities = '';

// let imagenSeleccionada = null;
// let imagenUrlTemp = null;
let mostrarDatosProp = false;


// Obtiene el contenido del inventario
function obtenerLista() {
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
                          <td><button title="Editar" onclick="modificarProp('${propiedad.id}')">
                          <svg style="display: block" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                            <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
                          </svg></button></td></button></td>
                          <td><button title="Eliminar" onclick="eliminarProp('${propiedad.id}')">
                          <svg style="display: block" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                          </svg></button></td></button></td>`;
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
          obtenerLista();
          alert('Eliminado correctamente.');
        }
      })
      // En caso de error, mostramos una alerta con un mensaje de error.
      .catch(error => {
        alert(error.message);
      });
  }
}


// Muestra el formulario con los datos del producto, se utiliza para consultar
// sobre una propiedad que se desea modificar
function mostrarFormulario() {
  if (mostrarDatosProp) {
    document.getElementById('descrip_corta').value = descrip_corta;
    document.getElementById('descrip_larga').value = descrip_larga;
    document.getElementById('direccion').value = direccion;
    document.getElementById('nota').value = nota;
    document.getElementById('url_maps').value = url_maps;
    document.getElementById('id_broker').value = id_broker;
    document.getElementById('precio').value = precio;
    document.getElementById('superf').value = superf;
    document.getElementById('superf_tot').value = superf_tot;
    document.getElementById('baños').value = baños;
    document.getElementById('dormitorios').value = dormitorios;
    document.getElementById('cocheras').value = cocheras;
    document.getElementById('basicos').value = basicos;
    document.getElementById('servicios').value = servicios;
    document.getElementById('amenities').value = amenities;

    document.getElementById('datos-prop').style.display = 'block';

    // const imagenActual = document.getElementById('imagen-actual');

    // // Verifica si imagen_url no está vacía y no se ha seleccionado una imagen
    // if (imagen_url && !imagenSeleccionada) {
    //   //imagenActual.src = './static/imagenes/' + imagen_url;
    //   imagenActual.src = 'https://gigabriel.serv00.net/imagenes/' + imagen_url;
    //   //Al subir al servidor, deberá utilizarse la siguiente ruta.USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
    //   //imagenActual.src = 'https://www.pythonanywhere.com/user/USUARIO/files/home/USUARIO/mysite/static / imagenes / ' + imagen_url;

    //   // Muestra la imagen actual
    //   imagenActual.style.display = 'block';
    // } else {
    //   // Oculta la imagen si no hay URL
    //   imagenActual.style.display = 'none';
    // }
  } else {
    document.getElementById('datos-prop').style.display = 'none';
  }
}


// Se utiliza para obtener la tabla de atributos de una propiedad que se desee modificar
function modificarProp(id) {
  fetch(URL + 'propiedades/' + id)
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error('Error al obtener los datos del producto.')
      }
    })
    .then(data => {
      descrip_corta = data.descrip_corta;
      descrip_larga = data.descrip_larga;
      direccion = data.direccion;
      nota = data.nota;
      url_foto_1 = data.url_foto_1;
      url_foto_2 = data.url_foto_2;
      url_foto_3 = data.url_foto_3;
      url_maps = data.url_maps;
      id_broker = data.id_broker;
      precio = data.precio;
      superf = data.superf;
      superf_tot = data.superf_tot;
      baños = data.baños;
      dormitorios = data.dormitorios;
      cocheras = data.cocheras;
      basicos = data.basicos;
      servicios = data.servicios;
      amenities = data.amenities;

      // Activa la vista del segundo formulario
      mostrarDatosProp = true;
      mostrarFormulario();
    })
    .catch(error => {
      alert('Código no encontrado.');
    });
}


// Cuando la página se carga, llama a obtenerProp para cargar la lista.
document.addEventListener('DOMContentLoaded', obtenerLista);


// const URL = "http://127.0.0.1:5000/"
// // const URL = "https://gigabriel.serv00.net/"


// // Variables de estado para controlar la visibilidad y los datos del formulario
// let codigo = '';
// let descripcion = '';
// let cantidad = '';
// let precio = '';
// let proveedor = '';
// let imagen_url = '';
// let imagenSeleccionada = null;
// let imagenUrlTemp = null;
// let mostrarDatosProducto = false;
// document.getElementById('form-obtener-producto').addEventListener('submit', obtenerProducto);
// document.getElementById('form-guardar-cambios').addEventListener('submit', guardarCambios);
// document.getElementById('nuevaImagen').addEventListener('change', seleccionarImagen);


// // Se ejecuta cuando se envía el formulario de consulta. Realiza una solicitud GET a la API y
// // obtiene los datos del producto correspondiente al código ingresado.
// function obtenerProducto(event) {
//   event.preventDefault();
//   codigo = document.getElementById('codigo').value;

//   fetch(URL + 'productos/' + codigo)
//     .then(response => {
//       if (response.ok) {
//         return response.json()
//       } else {
//         throw new Error('Error al obtener los datos del producto.')
//       }
//     })
//     .then(data => {
//       descripcion = data.descripcion;
//       cantidad = data.cantidad;
//       precio = data.precio;
//       proveedor = data.proveedor;
//       imagen_url = data.imagen_url;

//       //Activa la vista del segundo formulario
//       mostrarDatosProducto = true; 
//       mostrarFormulario();
//     })
//     .catch(error => {
//       alert('Código no encontrado.');
//     });
// }


// // Muestra el formulario con los datos del producto
// function mostrarFormulario() {
//   if (mostrarDatosProducto) {
//     document.getElementById('descripcionModificar').value = descripcion;
//     document.getElementById('cantidadModificar').value = cantidad;
//     document.getElementById('precioModificar').value = precio;
//     document.getElementById('proveModificar').value = proveedor;
//     const imagenActual = document.getElementById('imagen-actual');

//     // Verifica si imagen_url no está vacía y no se ha seleccionado una imagen
//     if (imagen_url && !imagenSeleccionada) {
//       //imagenActual.src = './static/imagenes/' + imagen_url;
//       imagenActual.src = 'https://gigabriel.serv00.net/imagenes/' + imagen_url;
//       //Al subir al servidor, deberá utilizarse la siguiente ruta.USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//       //imagenActual.src = 'https://www.pythonanywhere.com/user/USUARIO/files/home/USUARIO/mysite/static / imagenes / ' + imagen_url;
      
//       // Muestra la imagen actual
//       imagenActual.style.display = 'block'; 
//     } else {
//       // Oculta la imagen si no hay URL
//       imagenActual.style.display = 'none'; 
//     }
//     document.getElementById('datos-producto').style.display = 'block';
//   } else {
//     document.getElementById('datos-producto').style.display = 'none';
//   }
// }


// // Se activa cuando el usuario selecciona una imagen para cargar.
// function seleccionarImagen(event) {
//   const file = event.target.files[0];
//   imagenSeleccionada = file;

//   // Crea una URL temporal para la vista previa
//   imagenUrlTemp = URL.createObjectURL(file);
//   const imagenVistaPrevia = document.getElementById('imagen-vista-previa');
//   imagenVistaPrevia.src = imagenUrlTemp;
//   imagenVistaPrevia.style.display = 'block';
// }


// // Se usa para enviar los datos modificados del producto al servidor.
// function guardarCambios(event) {
//   event.preventDefault();
//   const formData = new FormData();
//   formData.append('codigo', codigo);
//   formData.append('descripcion', document.getElementById('descripcionModificar').value);
//   formData.append('cantidad', document.getElementById('cantidadModificar').value);
//   formData.append('proveedor', document.getElementById('proveModificar').value);
//   formData.append('precio', document.getElementById('precioModificar').value);

//   // Si se ha seleccionado una imagen nueva, la añade al formData.
//   if (imagenSeleccionada) {
//     formData.append('imagen', imagenSeleccionada,
//       imagenSeleccionada.name);
//   }

//   fetch(URL + 'productos/' + codigo, {
//     method: 'PUT',
//     body: formData,
//   })
//     .then(response => {
//       if (response.ok) {
//         return response.json()
//       } else {
//         throw new Error('Error al guardar los cambios del producto.')
//       }
//     })
//     .then(data => {
//       alert('Producto actualizado correctamente.');
//       limpiarFormulario();
//     })
//     .catch(error => {
//       console.error('Error:', error);
//       alert('Error al actualizar el producto.');
//     });
// }


// // Restablece todas las variables relacionadas con el formulario a sus valores iniciales,
// // lo que efectivamente "limpia" el formulario.
// function limpiarFormulario() {
//   document.getElementById('codigo').value = '';
//   document.getElementById('descripcionModificar').value = '';
//   document.getElementById('cantidadModificar').value = '';
//   document.getElementById('precioModificar').value = '';
//   document.getElementById('proveModificar').value = '';
//   document.getElementById('nuevaImagen').value = '';
//   const imagenActual = document.getElementById('imagen-actual');
//   imagenActual.style.display = 'none';
//   const imagenVistaPrevia = document.getElementById('imagen-vista-previa');
//   imagenVistaPrevia.style.display = 'none';
//   codigo = '';
//   descripcion = '';
//   cantidad = '';
//   precio = '';
//   proveedor = '';
//   imagen_url = '';
//   imagenSeleccionada = null;
//   imagenUrlTemp = null;
//   mostrarDatosProducto = false;
//   document.getElementById('datos-producto').style.display = 'none';
// }