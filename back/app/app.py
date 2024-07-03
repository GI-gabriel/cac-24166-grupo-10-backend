#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

# Importa claves
from keys import keys

app = Flask(__name__)
app.secret_key = keys['secret_key']
CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}}, supports_credentials=True)

# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/img/'
# RUTA_DESTINO = '/home/GIgabriel/mysite/static/imagenes'

# Funciones para abrir y cerrar la base de datos en cada consulta
def open_db_connection():
    try:
        cnx = mysql.connector.connect(
            user=keys['sql_user'],
            password=keys['sql_pass'],
            host='localhost',
            database='miapp'
        )
        if cnx.is_connected():
            # print("Conexión a la base de datos establecida.")
            return cnx
    except Error as e:
        raise ValueError(f"Error al conectar a la base de datos: {e}")

def close_db_connection(cnx):
    if cnx.is_connected():
        cnx.close()
        # print("Conexión a la base de datos cerrada.")


#--------------------------------------------------------------------
class Catalogo:
#--------------------------------------------------------------------
    # Constructor de la clase
    def __init__(self):        
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor()

            # Una vez que la base de datos está establecida
            # Crea tabla de propiedades inmobiliarias
            cursor.execute('''CREATE TABLE IF NOT EXISTS propiedades (
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
            cursor.execute('''CREATE TABLE IF NOT EXISTS brokers (
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

            cursor.execute("SELECT COUNT(*) FROM brokers")
            # Si el resultado es mayor a 0, la tabla existe
            # Entonces no es necesario llenarla nuevamente       
            if not (cursor.fetchone()[0]) > 0:
                for broker in brokers:
                    self.cursor.execute(f'''INSERT INTO brokers (nombre, mail, telefono, url_foto)
                                            VALUES ('{broker['name']}',
                                                    '{broker['email']}',
                                                    '{broker['phone']}',
                                                    '{broker['url_img']}')
                                        ''')
            conn.commit()
        
        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)

        # self.cursor = self.conn.cursor(dictionary=True)


    #----------------------------------------------------------------
    def agregar_prop(self,
                     descrip_corta, descrip_larga, direccion,
                     nota, url_foto_1, url_foto_2, url_foto_3,
                     url_maps, id_broker, precio, superf,
                     superf_tot, baños, dormitorios, cocheras,
                     basicos, servicios, amenities):
        
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor(dictionary=True)
        
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
            
            cursor.execute(sql, valores)
            conn.commit()
            ret_val = cursor.lastrowid

        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)

        return ret_val
    
    #----------------------------------------------------------------
    def consultar_prop(self, id):
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Consultamos a partir de su id
            cursor.execute(f"SELECT * FROM propiedades WHERE id = {id}")
            ret_val = cursor.fetchone()
        
        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)
    
        return ret_val
    #----------------------------------------------------------------
    def modificar_prop(self, id,
                       descrip_corta, descrip_larga, direccion,
                       nota, url_foto_1, url_foto_2, url_foto_3,
                       url_maps, id_broker, precio, superf,
                       superf_tot, baños, dormitorios, cocheras,
                       basicos, servicios, amenities):
        
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor(dictionary=True)

            # CUIDADO! - Tienen el mismo nombre, pero no son los argumentos de la función
            # Son los parámetros de la consulta
            sql = '''UPDATE propiedades SET 
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

            cursor.execute(sql, valores)
            conn.commit()
            ret_val = cursor.rowcount > 0

        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)
    
        return ret_val


    #----------------------------------------------------------------
    def listar_prop(self):
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM propiedades")
            propiedades = cursor.fetchall()
            ret_val = propiedades

        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)
    
        return ret_val    

    #----------------------------------------------------------------
    def eliminar_prop(self, id):
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor(dictionary=True)    

            # Eliminamos de la tabla a partir de su código
            cursor.execute(f"DELETE FROM propiedades WHERE id = {id}")
            conn.commit()
            ret_val = cursor.rowcount > 0
            
        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)
    
        return ret_val 


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------

# Crear una instancia de la clase Catalogo
catalogo = Catalogo()
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
@app.route("/propiedades/<int:id>", methods=["GET"])
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
@login_required
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
        return jsonify({"mensaje": "Agregado correctamente.", "id": nuevo_id}), 201
    else:
        # Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error
        # y un código de estado HTTP 500 (Internal Server Error).
        print ('316')
        return jsonify({"mensaje": "Error al agregar."}), 500


#--------------------------------------------------------------------
# Modificar uno, según su id
#--------------------------------------------------------------------
@app.route("/propiedades/<int:id>", methods=["PUT"])
@login_required
# La función modificar_producto se asocia con esta URL y es invocada cuando se
# realiza una solicitud PUT a /productos/ seguido de un número (el código del producto).
def modificar_prop(id):
    #Se recuperan los nuevos datos del formulario
    descrip_corta = request.form.get("descrip_corta")
    descrip_larga = request.form.get("descrip_larga")
    direccion = request.form.get("direccion")
    nota = request.form.get("nota")
    url_maps = request.form.get("url_maps")
    id_broker = request.form.get("id_broker")
    precio = request.form.get("precio")
    superf = request.form.get("superf")
    superf_tot = request.form.get("superf_tot")
    baños = request.form.get("baños")
    dormitorios = request.form.get("dormitorios")
    cocheras = request.form.get("cocheras")
    basicos = request.form.get("basicos")
    servicios = request.form.get("servicios")
    amenities = request.form.get("amenities")

    ######################################################################################
    #
    imgs = [None, None, None]
    urls = ['url_foto_1', 'url_foto_2', 'url_foto_3']
    img_urls = [None, None, None]

    for i in range(3):
        # Verifica si se proporcionó una nueva imagen
        if urls[i] in request.files:
            imgs[i] = request.files[urls[i]]

            # Procesamiento de la imagen
            # Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro
            # para guardar en el sistema de archivos
            img_urls[i] = secure_filename(imgs[i].filename)

            # Separa el nombre del archivo de su extensión.
            nombre_base, extension = os.path.splitext(img_urls[i])

            # Genera un nuevo nombre para la imagen usando un timestamp, para evitar
            # sobreescrituras y conflictos de nombres.
            img_urls[i] = f"{nombre_base}_{int(time.time())}_{i}{extension}"

            # Guardar la imagen en el servidor
            imgs[i].save(os.path.join(RUTA_DESTINO, img_urls[i]))

            # Busco el producto guardado
            propiedad = catalogo.consultar_prop(id)
            # Si existe el producto...
            if propiedad:
                imagen_vieja = propiedad[urls[i]]
                # Armo la ruta a la imagen
                ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)            
                # Y si existe la borro.
                if os.path.exists(ruta_imagen):
                    os.remove(ruta_imagen)

        else:
            # Si no se proporciona una nueva imagen, simplemente usa la imagen existente
            propiedad = catalogo.consultar_prop(id)
            if propiedad:
                img_urls[i] = propiedad[urls[i]]
        
        i = i + 1
    #
    ######################################################################################

        
    # Se llama al método modificar_producto pasando el id y los nuevos datos.
    if catalogo.modificar_prop(id,
                                descrip_corta, descrip_larga, direccion,
                                nota, img_urls[0], img_urls[1], img_urls[2],
                                url_maps, id_broker, precio, superf,
                                superf_tot, baños, dormitorios, cocheras,
                                basicos, servicios, amenities):
        
        # Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito
        # y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Modificado"}), 200
    else:
        # Si la propiedad no se encuentra (por ejemplo, si no hay ninguna con ese id),
        # se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "No encontrado"}), 403
    
    
#--------------------------------------------------------------------
# Eliminar una propiedad según su id
#--------------------------------------------------------------------
@app.route("/propiedades/<int:id>", methods=["DELETE"])
@login_required
# La función eliminar_prop se asocia con esta URL y es llamada cuando se realiza una solicitud
# DELETE a /propiedades/ seguido de un número (el id de la propiedad).
def eliminar_prop(id):
    # Busca en la base de datos
    propiedad = catalogo.consultar_prop(id)

    # Si el producto existe... 
    if propiedad:
        ###################################################################
        # Verifica si hay imagenes asociadas en el servidor.
        #
        imgs_viejas = [propiedad["url_foto_1"],
                       propiedad["url_foto_2"],
                       propiedad["url_foto_3"]]

        for img in imgs_viejas:
            # Ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, img)
            
            # Y si existe, la elimina del sistema de archivos.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
        #
        #
        ###################################################################

        # Luego, elimina la propiedad del catálogo
        if catalogo.eliminar_prop(id):
            # Si el producto se elimina correctamente, se devuelve una respuesta JSON con un mensaje
            # de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Eliminado"}), 200
        else:
            # Si ocurre un error durante la eliminación (por ejemplo, si la propiedad no se puede
            # eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un
            # código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar"}), 500
    else:
        # Si la propiedad no se encuentra (por ejemplo, si no existe el id proporcionado), se devuelve
        # un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "No encontrado"}), 404


#--------------------------------------------------------------------
# Control de acceso
# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Simulación de una base de datos de usuarios
users = {'1': User(id='1', username=keys['admin_user'], password=generate_password_hash(keys['admin_pass'])),
         '2': User(id='2', username=keys['guest_user'], password=generate_password_hash(keys['guest_pass']))
        }


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/menu')
def menu():
    if current_user.is_authenticated:
        return redirect('http://localhost:5500/front/crud_menu.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users.values() if u.username == username), None)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('http://localhost:5500/front/crud_menu.html')
        else:
            flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

