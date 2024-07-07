const URL = "/"

// Variables de estado para controlar la visibilidad y los datos del formulario
let id_ = '';
let tipo_oper = ''
let tipo_prop = ''
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
let superf_tot = '';
let baños = '';
let dormitorios = '';
let cocheras = '';
let basicos = '';
let servicios = '';
let amenities = '';

let foto_1_Seleccionada = null;
let foto_2_Seleccionada = null;
let foto_3_Seleccionada = null;
let foto_1_UrlTemp = null;
let foto_2_UrlTemp = null;
let foto_3_UrlTemp = null;
let mostrarDatosProp = false;

document.getElementById('form-guardar-cambios').addEventListener('submit', guardarCambios);
document.getElementById('btn-cancelar').addEventListener('click', limpiarFormulario);
document.getElementById('url-foto-1').addEventListener('change', seleccionarFoto_1);
document.getElementById('url-foto-2').addEventListener('change', seleccionarFoto_2);
document.getElementById('url-foto-3').addEventListener('change', seleccionarFoto_3);


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
                          <td>${propiedad.tipo_oper}</td>
                          <td>${propiedad.tipo_prop}</td>
                          <td>${propiedad.direccion}</td>
                          <td class="sqrbtn"><button title="Editar" onclick="modificarProp('${propiedad.id}')">
                          <svg style="display: block" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                            <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001m-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708z"/>
                          </svg></button></td></button></td>
                          <td class="sqrbtn"><button title="Eliminar" onclick="eliminarProp('${propiedad.id}')">
                          <svg class="2col style="display: block" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
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
    // fetch(URL + `propiedades/${id}`, { method: 'DELETE', credentials: 'include' })
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
    document.getElementById('tipo_oper').value = tipo_oper;
    document.getElementById('tipo_prop').value = tipo_prop;
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

    const foto_1_actual = document.getElementById('foto-1-actual');
    const foto_2_actual = document.getElementById('foto-2-actual');
    const foto_3_actual = document.getElementById('foto-3-actual');

    // #1 Verifica si imagen_url no está vacía y no se ha seleccionado una imagen
    if (url_foto_1 && !foto_1_Seleccionada) {
      foto_1_actual.src = '/static/img/prop/' + url_foto_1;
      // imagenActual.src = 'https://gigabriel.serv00.net/imagenes/' + imagen_url;
      
      // Muestra la imagen actual
      foto_1_actual.style.display = 'block';
    } else {
      // Oculta la imagen si no hay URL
      foto_1_actual.style.display = 'none';
    }

    // #2 Verifica si imagen_url no está vacía y no se ha seleccionado una imagen
    if (url_foto_2 && !foto_2_Seleccionada) {
      foto_2_actual.src = '/static/img/prop/' + url_foto_2;
      // imagenActual.src = 'https://gigabriel.serv00.net/imagenes/' + imagen_url;
      
      // Muestra la imagen actual
      foto_2_actual.style.display = 'block';
    } else {
      // Oculta la imagen si no hay URL
      foto_2_actual.style.display = 'none';
    }

    // #3 Verifica si imagen_url no está vacía y no se ha seleccionado una imagen
    if (url_foto_3 && !foto_3_Seleccionada) {
      foto_3_actual.src = '/static/img/prop/' + url_foto_3;
      // imagenActual.src = 'https://gigabriel.serv00.net/imagenes/' + imagen_url;
      
      // Muestra la imagen actual
      foto_3_actual.style.display = 'block';
    } else {
      // Oculta la imagen si no hay URL
      foto_3_actual.style.display = 'none';
    }
    
  } else {
    document.getElementById('datos-prop').style.display = 'none';
  }
}


// Se activa cuando el usuario selecciona una imagen para cargar.
function seleccionarFoto_1(event) {
  const file = event.target.files[0];
  if (file) {
    foto_1_Seleccionada = file;
    // Crea una URL temporal para la vista previa
    const foto_1_UrlTemp = window.URL.createObjectURL(file);
    const imagenVistaPrevia = document.getElementById('foto-1-vista-previa');
    imagenVistaPrevia.src = foto_1_UrlTemp;
    imagenVistaPrevia.style.display = 'block';

    // Oculta la imagen reemplazada
    const foto_1_Actual = document.getElementById('foto-1-actual');
    foto_1_Actual.style.display = 'none';

    imagenVistaPrevia.onload = function() {
      window.URL.revokeObjectURL(foto_1_UrlTemp);
    }
  }
}


// Se activa cuando el usuario selecciona una imagen para cargar.
function seleccionarFoto_2(event) {
  const file = event.target.files[0];
  if (file) {
    foto_2_Seleccionada = file;
    // Crea una URL temporal para la vista previa
    const foto_2_UrlTemp = window.URL.createObjectURL(file);
    const imagenVistaPrevia = document.getElementById('foto-2-vista-previa');
    imagenVistaPrevia.src = foto_2_UrlTemp;
    imagenVistaPrevia.style.display = 'block';

    // Oculta la imagen reemplazada
    const foto_2_Actual = document.getElementById('foto-2-actual');
    foto_2_Actual.style.display = 'none';

    imagenVistaPrevia.onload = function() {
      window.URL.revokeObjectURL(foto_2_UrlTemp);
    }
  }
}


// Se activa cuando el usuario selecciona una imagen para cargar.
function seleccionarFoto_3(event) {
  const file = event.target.files[0];
  if (file) {
    foto_3_Seleccionada = file;
    // Crea una URL temporal para la vista previa
    const foto_3_UrlTemp = window.URL.createObjectURL(file);
    const imagenVistaPrevia = document.getElementById('foto-3-vista-previa');
    imagenVistaPrevia.src = foto_3_UrlTemp;
    imagenVistaPrevia.style.display = 'block';

    // Oculta la imagen reemplazada
    const foto_3_Actual = document.getElementById('foto-3-actual');
    foto_3_Actual.style.display = 'none';

    imagenVistaPrevia.onload = function() {
      window.URL.revokeObjectURL(foto_3_UrlTemp);
    }
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
      tipo_oper = data.tipo_oper;
      tipo_prop = data.tipo_prop;
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
      id_ = id;
      mostrarFormulario();
    })
    .catch(error => {
      alert('Código no encontrado.');
    });
}


// Se usa para enviar los datos modificados del producto al servidor.
function guardarCambios(event) {
  event.preventDefault();

  const formData = new FormData();
  formData.append('id', id_);
  formData.append('tipo_oper', document.getElementById('tipo_oper').value);
  formData.append('tipo_prop', document.getElementById('tipo_prop').value);
  formData.append('descrip_corta', document.getElementById('descrip_corta').value);
  formData.append('descrip_larga', document.getElementById('descrip_larga').value);
  formData.append('direccion', document.getElementById('direccion').value);
  formData.append('nota', document.getElementById('nota').value);
  formData.append('url_maps', document.getElementById('url_maps').value);
  formData.append('id_broker', document.getElementById('id_broker').value);
  formData.append('precio', document.getElementById('precio').value);
  formData.append('superf', document.getElementById('superf').value);
  formData.append('superf_tot', document.getElementById('superf_tot').value);
  formData.append('baños', document.getElementById('baños').value);
  formData.append('dormitorios', document.getElementById('dormitorios').value);
  formData.append('cocheras', document.getElementById('cocheras').value);
  formData.append('basicos', document.getElementById('basicos').value);
  formData.append('servicios', document.getElementById('servicios').value);
  formData.append('amenities', document.getElementById('amenities').value);

  // Si se ha seleccionado una imagen nueva, la añade al formData.
  if (foto_1_Seleccionada) {
    formData.append('url_foto_1', foto_1_Seleccionada,
      foto_1_Seleccionada.name);
  }

  if (foto_2_Seleccionada) {
    formData.append('url_foto_2', foto_2_Seleccionada,
      foto_2_Seleccionada.name);
  }

  if (foto_3_Seleccionada) {
    formData.append('url_foto_3', foto_3_Seleccionada,
      foto_3_Seleccionada.name);
  }

  fetch(URL + 'propiedades/' + id_, {
    method: 'PUT',
    // credentials: 'include',
    body: formData,
  })
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error('Error al guardar los cambios del producto.')
      }
    })
    .then(data => {
      alert('Producto actualizado correctamente.');
      limpiarFormulario();
      obtenerLista();
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al actualizar el producto.');
    });
}


// Restablece todas las variables relacionadas con el formulario a sus valores iniciales,
// lo que efectivamente "limpia" el formulario.
function limpiarFormulario() {
  elems = document.querySelectorAll('#form-guardar-cambios > input');

  elems.forEach(elem => {
    elem.value = "";
  });
  
  const foto_1_Actual = document.getElementById('foto-1-actual');
  foto_1_Actual.style.display = 'none';
  const foto_1_VistaPrevia = document.getElementById('foto-1-vista-previa');
  foto_1_VistaPrevia.style.display = 'none';

  const foto_2_Actual = document.getElementById('foto-2-actual');
  foto_2_Actual.style.display = 'none';
  const foto_2_VistaPrevia = document.getElementById('foto-2-vista-previa');
  foto_2_VistaPrevia.style.display = 'none';

  const foto_3_Actual = document.getElementById('foto-3-actual');
  foto_3_Actual.style.display = 'none';
  const foto_3_VistaPrevia = document.getElementById('foto-3-vista-previa');
  foto_3_VistaPrevia.style.display = 'none';

  id_ = '';
  tipo_oper = ''
  tipo_prop = ''
  descrip_corta = '';
  descrip_larga = '';
  direccion = '';
  nota = '';
  url_foto_1 = '';
  url_foto_2 = '';
  url_foto_3 = '';
  url_maps = '';
  id_broker = '';
  precio = '';
  superf = '';
  superf_tot = '';
  baños = '';
  dormitorios = '';
  cocheras = '';
  basicos = '';
  servicios = '';
  amenities = '';

  foto_1_Seleccionada = null;
  foto_1_UrlTemp = null;
  foto_2_Seleccionada = null;
  foto_2_UrlTemp = null;
  foto_3_Seleccionada = null;
  foto_3_UrlTemp = null;

  mostrarDatosProducto = false;

  document.getElementById('datos-prop').style.display = 'none';
}


// Cuando la página se carga, llama a obtenerProp para cargar la lista.
document.addEventListener('DOMContentLoaded', obtenerLista);