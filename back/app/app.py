#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
# from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app) # Esto habilitará CORS para todas las rutas

# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/img/'
# RUTA_DESTINO = '/home/GIgabriel/mysite/static/imagenes'

#--------------------------------------------------------------------
class Catalogo:
#----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        self.cursor = self.conn.cursor()
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
            
        # Una vez que la base de datos está establecida
        # Crea tabla de propiedades inmobiliarias
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS propiedades (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            descrip_corta VARCHAR(255) NOT NULL,
                            descrip_larga VARCHAR(2048) NOT NULL,
                            direccion VARCHAR(255) NOT NULL,
                            nota VARCHAR(255) NOT NULL,
                            url_foto_1 VARCHAR(255) NOT NULL,
                            url_foto_2 VARCHAR(255) NOT NULL,
                            url_foto_3 VARCHAR(255) NOT NULL,
                            url_maps VARCHAR(255) NOT NULL,
                            id_broker INT,
                            precio DECIMAL(10, 2) NOT NULL,
                            superf INT,
                            superf_tot INT,
                            baños INT,
                            dormitorios INT,
                            cocheras INT,
                            basicos VARCHAR(1024) NOT NULL,
                            servicios VARCHAR(1024) NOT NULL,
                            amenities VARCHAR(1024) NOT NULL
        )''')
        # Crea tabla de brokers
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS brokers (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(255) NOT NULL,
                            mail VARCHAR(255) NOT NULL,
                            telefono VARCHAR(255) NOT NULL,
                            url_foto VARCHAR(255) NOT NULL
        )''')

        # Se completa la tabla de brokers de forma estática,
        # no se va a utilizar un CRUD para esta tabla
        # url_img_path = "./static/img/brokers/"
        url_img_path = RUTA_DESTINO + 'brokers/'
        brokers = [
            {'name': 'John Doe', 'phone': '123-456-7890', 'email': 'john.doe@example.com', 'url_img': url_img_path + 'm1' + '.jpg'},
            {'name': 'Jane Smith', 'phone': '987-654-3210', 'email': 'jane.smith@example.com', 'url_img': url_img_path + 'f1' + '.jpg'},
            {'name': 'Alice Johnson', 'phone': '555-123-4567', 'email': 'alice.johnson@example.com', 'url_img': url_img_path + 'f2' + '.jpg'},
            {'name': 'Bob Brown', 'phone': '555-987-6543', 'email': 'bob.brown@example.com', 'url_img': url_img_path + 'm2' + '.jpg'},
            {'name': 'Carol White', 'phone': '555-555-5555', 'email': 'carol.white@example.com', 'url_img': url_img_path + 'f3' + '.jpg'},
            {'name': 'David Black', 'phone': '555-444-3333', 'email': 'david.black@example.com', 'url_img': url_img_path + 'm3' + '.jpg'},
            {'name': 'Eva Green', 'phone': '555-222-1111', 'email': 'eva.green@example.com', 'url_img': url_img_path + 'f4' + '.jpg'},
            {'name': 'Frank Blue', 'phone': '555-666-7777', 'email': 'frank.blue@example.com', 'url_img': url_img_path + 'm4' + '.jpg'},
            {'name': 'Grace Yellow', 'phone': '555-888-9999', 'email': 'grace.yellow@example.com', 'url_img': url_img_path + 'f5' + '.jpg'},
            {'name': 'Hank Red', 'phone': '555-000-1111', 'email': 'hank.red@example.com', 'url_img': url_img_path + 'm5' + '.jpg'}
        ]

        self.cursor.execute("SELECT COUNT(*) FROM brokers")
        # Si el resultado es mayor a 0, la tabla existe
        # Entonces no es necesario llenarla nuevamente       
        if not (self.cursor.fetchone()[0]) > 0:
            for broker in brokers:
                self.cursor.execute(f'''INSERT INTO brokers (nombre, mail, telefono, url_foto)
                                        VALUES ('{broker['name']}',
                                                '{broker['email']}',
                                                '{broker['phone']}',
                                                '{broker['url_img']}')
                                    ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


    #----------------------------------------------------------------
    def agregar_prop(self,
                     descrip_corta, descrip_larga, direccion,
                     nota, url_foto_1, url_foto_2, url_foto_3,
                     url_maps, id_broker, precio, superf,
                     superf_tot, baños, dormitorios, cocheras,
                     basicos, servicios, amenities):
        sql = '''INSERT INTO propiedades (
                    descrip_corta, descrip_larga, direccion,
                    nota, url_foto_1, url_foto_2, url_foto_3,
                    url_maps, id_broker, precio, superf,
                    superf_tot, baños, dormitorios, cocheras,
                    basicos, servicios, amenities )
                 VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        valores = (descrip_corta, descrip_larga, direccion,
                   nota, url_foto_1, url_foto_2, url_foto_3,
                   url_maps, id_broker, precio, superf,
                   superf_tot, baños, dormitorios, cocheras,
                   basicos, servicios, amenities)
        
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid
    
    
    #----------------------------------------------------------------
    def consultar_prop(self, id):
        # Consultamos a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {id}")
        return self.cursor.fetchone()
    

    #----------------------------------------------------------------
    def modificar_prop(self, id,
                       descrip_corta, descrip_larga, direccion,
                       nota, url_foto_1, url_foto_2, url_foto_3,
                       url_maps, id_broker, precio, superf,
                       superf_tot, baños, dormitorios, cocheras,
                       basicos, servicios, amenities):
        
        # CUIDADO! - Tienen el mismo nombre, pero no son los argumentos de la función
        # Son los parámetros de la consulta
        sql = '''UPDATE productos SET 
                    descrip_corta = %s, descrip_larga = %s, direccion = %s,
                    nota = %s, url_foto_1 = %s, url_foto_2 = %s, url_foto_3 = %s,
                    url_maps = %s, id_broker = %s, precio = %s, superf = %s,
                    superf_tot = %s, baños = %s, dormitorios = %s, cocheras = %s,
                    basicos = %s, servicios = %s, amenities = %s
                WHERE id = %s'''
        
        valores = (descrip_corta, descrip_larga, direccion,
                   nota, url_foto_1, url_foto_2, url_foto_3,
                   url_maps, id_broker, precio, superf,
                   superf_tot, baños, dormitorios, cocheras,
                   basicos, servicios, amenities, id)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0


    #----------------------------------------------------------------
    def listar_prop(self):
        self.cursor.execute("SELECT * FROM propiedades")
        propiedades = self.cursor.fetchall()
        return propiedades
    

    #----------------------------------------------------------------
    def eliminar_prop(self, id):
        # Eliminamos de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0


    #----------------------------------------------------------------
    # def mostrar_producto(self, id):
    #     # Mostramos los datos a partir de su código
    #     propiedad = self.consultar_producto(id)
    #     if propiedad:
    #         print("-" * 40)
    #         print(f"Código.....: {producto['codigo']}")
    #         print(f"Descripción: {producto['descripcion']}")
    #         print(f"Cantidad...: {producto['cantidad']}")
    #         print(f"Precio.....: {producto['precio']}")
    #         print(f"Imagen.....: {producto['imagen_url']}")
    #         print(f"Proveedor..: {producto['proveedor']}")
    #         print("-" * 40)
    #     else:
    #         print("Producto no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='', database='miapp')
# catalogo = Catalogo(host='mysql4.serv00.com',
#                     user='m10808_gigabriel',
#                     password="",
#                     database='m10808_miapp')


#--------------------------------------------------------------------
# Listar todos
#--------------------------------------------------------------------
# El método devuelve una lista con todas las propiedades en formato JSON.
@app.route("/propiedades", methods=["GET"])
def listar_prop():
    propiedades = catalogo.listar_prop()
    return jsonify(propiedades)


#--------------------------------------------------------------------
# Mostrar uno sólo, según su id
#--------------------------------------------------------------------
# El método busca en la base de datos la propiedad con el id especificado y 
# devuelve un JSON con los detalles si lo encuentra, o None si no lo encuentra.
@app.route("/propiedades/<int:codigo>", methods=["GET"])
def mostrar_prop(id):
    propiedad = catalogo.consultar_prop(id)
    if propiedad:
        return jsonify(propiedad), 201
    else:
        return "Propiedad no encontrada", 404
    

#--------------------------------------------------------------------
# Agregar uno
#--------------------------------------------------------------------
@app.route("/propiedades", methods=["POST"])
# La función agregar_prop se asocia con esta URL y es llamada cuando se hace
# una solicitud POST a /propiedades.
def agregar_prop():
    descrip_corta = request.form['descrip_corta']
    descrip_larga = request.form['descrip_larga']
    direccion = request.form['direccion']
    nota = request.form['nota']
    foto_1 = request.files['url_foto_1']
    foto_2 = request.files['url_foto_2']
    foto_3 = request.files['url_foto_3']
    url_maps = request.form['url_maps']
    id_broker = request.form['id_broker']
    precio = request.form['precio']
    superf = request.form['superf']
    superf_tot = request.form['superf_tot']
    baños = request.form['baños']
    dormitorios = request.form['dormitorios']
    cocheras = request.form['cocheras']
    basicos = request.form['basicos']
    servicios = request.form['servicios']
    amenities = request.form['amenities']
    
    ########################################################################
    # Genera nombres de imagenes con un timestamp para evitar conflictos si
    # se cargan imagenes con el mismo nombre base
    imgs = [foto_1, foto_2, foto_3]
    img_urls = []

    i = 0
    for img in imgs:
        # Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro
        # para guardar en el sistema de archivos
        img_name = secure_filename(img.filename)
        # Separa el nombre del archivo de su extensión
        nombre_base, extension = os.path.splitext(img_name)     
        # Nombre guión bajo timestamp
        img_urls.append(f"{nombre_base}_{int(time.time())}_{i}{extension}")
        i = i + 1
    #
    # 
    ########################################################################
    
    #Agrega propiedad a una fila de la tabla
    nuevo_id = catalogo.agregar_prop(descrip_corta, descrip_larga, direccion,
                                     nota, img_urls[0], img_urls[1], img_urls[2],
                                     url_maps, id_broker, precio, superf,
                                     superf_tot, baños, dormitorios, cocheras,
                                     basicos, servicios, amenities)
    # Si el guardado en base de datos fue exitoso, guarda los archivos de imagenes
    # en el sistema de archivos    
    if nuevo_id:
        # Guarda archivos de imagenes
        i = 0
        for img in imgs:
            img.save(os.path.join(RUTA_DESTINO, img_urls[i]))
            i = i + 1

        # Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito
        # y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Producto agregado correctamente.", "codigo": nuevo_id}), 201
    else:
        # Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error
        # y un código de estado HTTP 500 (Internal Server Error).
        print ('316')
        return jsonify({"mensaje": "Error al agregar el producto."}), 500


#--------------------------------------------------------------------
# Modificar uno, según su id
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["PUT"])
# La función modificar_producto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /productos/ seguido de un número (el código del producto).
def modificar_producto(codigo):
    #Se recuperan los nuevos datos del formulario
    nueva_descripcion = request.form.get("descripcion")
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")

    nuevo_proveedor = request.form.get("proveedor")
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        # Busco el producto guardado
        producto = catalogo.consultar_producto(codigo)
        if producto: # Si existe el producto...
            imagen_vieja = producto["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)
            
            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del producto
        producto = catalogo.consultar_producto(codigo)
        if producto:
            nombre_imagen = producto["imagen_url"]
        
    # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos.
    if catalogo.modificar_producto(codigo, nueva_descripcion,
    nueva_cantidad, nuevo_precio, nombre_imagen, nuevo_proveedor):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        #Si el producto no se encuentra (por ejemplo, si no hay ningún producto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Producto no encontrado"}), 403
    
    
#--------------------------------------------------------------------
# Eliminar un producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:codigo>", methods=["DELETE"])
# La función eliminar_producto se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /productos/ seguido de un número (el código del producto).
def eliminar_producto(codigo):
    # Busco el producto en la base de datos
    producto = catalogo.consultar_producto(codigo)
    if producto: # Si el producto existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = producto["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)
        
        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
        
        # Luego, elimina el producto del catálogo
        if catalogo.eliminar_producto(codigo):
            #Si el producto se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Producto eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el producto no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    else:
        #Si el producto no se encuentra (por ejemplo, si no existe un producto con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Producto no encontrado"}), 404

    
#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
