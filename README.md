# Sitio web para empresa de servicios inmobiliarios  
[https://gigabriel.pythonanywhere.com](https://gigabriel.pythonanywhere.com)  
[https://gigabriel.alwaysdata.net](https://gigabriel.alwaysdata.net)  

Trabajo práctico integrador Back-End
Codo a Codo 4.0, comisión 24166, grupo 10  

## Público objetivo
Personas interesadas en comprar, vender o realizar inversiones en el mercado de bienes raíces.

## Estructura del sitio
[Home](https://gigabriel.pythonanywhere.com/)  
&emsp;|  
&emsp;|---- [Búsqueda y filtrado de Propiedades](https://gigabriel.pythonanywhere.com/buscar) - Template dinámico  
&emsp;|&emsp;&emsp;|  
&emsp;|&emsp;&emsp;|---- [Ficha de la propiedad](https://gigabriel.pythonanywhere.com/buscar/3) - Template dinámico  
&emsp;|  
&emsp;|---- [Tasaciones](https://gigabriel.pythonanywhere.com/static/tasaciones.html)  
&emsp;|---- [Nosotros](https://gigabriel.pythonanywhere.com/static/nosotros.html)  
&emsp;|---- [Formulario de contacto](https://gigabriel.pythonanywhere.com/static/contacto.html)  
&emsp;|  
&emsp;|---- [Panel de administración](https://gigabriel.pythonanywhere.com/menu)  
&emsp;&emsp;&emsp;&emsp;|  
&emsp;&emsp;&emsp;&emsp;|---- Agregar propiedad - (requiere ingreso con credenciales)  
&emsp;&emsp;&emsp;&emsp;|---- Modificar/Eliminar propiedad - (requiere ingreso con credenciales)  

# Front-End
Los detalles del front-end pueden consultarse en la [documentación](https://github.com/GI-gabriel/cac-24166-grupo-10-frontend/blob/main/README.md) del proyecto correspondiente.

---

# Back-End

## Modelo de datos
Se utilizó el siguiente modelo datos, con dos tablas:
- Propiedades: datos de la propiedad a vender, alquilar, etc.
- Brokers: datos del broker inmobiliario responsable de esa propiedad.
![Screenshot from 2024-07-08 16-46-51](https://github.com/GI-gabriel/cac-24166-grupo-10-backend/assets/161953323/8b70ca97-5084-44be-a755-8ce56a1eda05)

## Recursos utilizados
#### mySQL
El modelo de datos fue implementado en mySQL, utilizando las herrmaientas XAMPP/WAMP para desarrollo en local.
El deploy se hizo a servidores que soporten este sistema de DB (pythonanwhere, alwaysdata).

#### Javascript
Se utilizó la API Fetch de JS, para realizar las solicitudes HTTP (GET, POST, PUT, DELETE) en modo asíncrono al back-end.
En un principio se alojaron front-end y back-end en servidores distintos, pero después se simplificó el diseño de la app, alojando todo en mismo servidor. Como las solicitudes HTTP se realizan dentro del mismo dominio, se puede prescindir de librerías para el manejo de CORS (flask-cors) y el envío de credenciales.

#### Flask / Python
Para desarrollar el back-end, atendiendo las solicitudes HTTP desde el front a través de rutas @app.route.

#### mysql-connector
Se utilizó el módulo mySQL-connector-python para realizar las consultas a BD. Se realizan todas las consultas utilizando parámetros, a fin de mitigar el efecto de ataques por inyección SQL desde el front-end.

#### flask-login
Se empleó el módulo flask-login para el Menú de administración, de forma que la modificación de los datos de la base de datos y la subida de archivos de imágenes al servidor sólo pueda realizarse con credenciales de acceso.

#### Herramientas de desarrollador de Firefox / Chrome
Se utilizó la consola JS, el Debugger y especialmente el Network Monitor para depurar las consultas HTTP desde el front-end al back-end.

#### Herramientas AI
Se utilizaron herramientas de AI para generar contenido de imagenes [(Perchance)](https://perchance.org/ai-text-to-image-generator) y texto [(ChatGPT)](https://chatgpt.com)

#### VSCode
Para editar el código.

#### Git/Github
Para el control de versiones y trabajo colaborativo se utilizó.

#### GIMP
Para escalar y recortar imágenes.

#### Alojamiento
Toda la aplicación (front, back y base de datos) se alojó en dos servidores gratuitos:
[PythonAnywhere](https://www.pythonanywhere.com/)  
[Alwaysdata](https://www.alwaysdata.com) - Este tiene la ventaja para el desarrollador de ofrecer FTP/SFTP para gestión de archivos y phpmyAdmin para gestión de la base de datos.

---

## Equipo
- [Claudia Miranda](https://github.com/claumiranda) - (Validaciones Front, Backend)
- [Michel Diamant](https://github.com/mikeowl) - (Estilos, Backend)
- [Gabriel Iarussi](https://github.com/GI-gabriel) - (SQL, Backend)
- [Victoria G. Curzi](https://github.com/vixcurzi) - (Estilos, Backend)

## Etapas del proyecto
- **Diseño modelo de datos y consultas:** 1 semana
- **Desarrollo back-end (clases, rutas flask):** 5 días
- **Desarrollo front-end (solicitudes HTTP en JS):** 5 días

## A futuro...
- Ampliar el modelo de datos para incluír datos de propietario, sucursales inmobiliarias, transacciones de compra/venta/alquiler/etc.
- Utilizar un framework JS reactivo (React, Vue) para que al refrescar el filtrado de propiedades no cargue toda la página

---

## Criterios de evaluación
![pautas](https://github.com/GI-gabriel/cac-24166-grupo-10-be/assets/161953323/4cd66354-065d-417f-b36b-1a648712c8f4)

---

## Agradecimientos
- Al programa [Codo a Codo 4.0 de la Agencia de Habilidades para el Futuro, de la Ciudad de Buenos Aires](https://agenciadeaprendizaje.bue.edu.ar/), por poner a disposición la plataforma, los docentes y el material educativo que permitió generar este proyecto.
- Al docente [Guido Santigo Varela Coletta](https://www.linkedin.com/in/guidovarelacoletta/), por su gran dedicación y paciencia.
- Al grupo de docentes y alumnos que realizaron y facilitaron el Modelo para Proyecto TPO 2024, CRUD, el cual fue utilizado como referencia para el código de este proyecto.

