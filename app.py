#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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

# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/img/prop'
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

            # Crea tabla de brokers
            cursor.execute('''CREATE TABLE IF NOT EXISTS brokers (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                nombre VARCHAR(255) NOT NULL,
                                mail VARCHAR(255) NOT NULL,
                                telefono VARCHAR(255) NOT NULL,
                                url_foto VARCHAR(255) NOT NULL
            )''')

            # Una vez que la base de datos está establecida
            # Crea tabla de propiedades inmobiliarias
            cursor.execute('''CREATE TABLE IF NOT EXISTS propiedades (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                tipo_oper VARCHAR(255) NOT NULL,
                                tipo_prop VARCHAR(255) NOT NULL,
                                descrip_corta VARCHAR(255) NOT NULL,
                                descrip_larga VARCHAR(2048) NOT NULL,
                                direccion VARCHAR(255) NOT NULL,
                                nota VARCHAR(255) NOT NULL,
                                url_foto_1 VARCHAR(255) NOT NULL,
                                url_foto_2 VARCHAR(255) NOT NULL,
                                url_foto_3 VARCHAR(255) NOT NULL,
                                url_maps VARCHAR(512) NOT NULL,
                                id_broker INT,
                                precio INT NOT NULL,
                                superf INT,
                                superf_tot INT,
                                baños INT,
                                dormitorios INT,
                                cocheras INT,
                                basicos VARCHAR(1024) NOT NULL,
                                servicios VARCHAR(1024) NOT NULL,
                                amenities VARCHAR(1024) NOT NULL,
                                FOREIGN KEY (id_broker) REFERENCES brokers(id) ON DELETE CASCADE ON UPDATE CASCADE
            )''')

            # Se completa la tabla de brokers de forma estática,
            # no se va a utilizar un CRUD para esta tabla
            brokers = [
                {'name': 'John Doe', 'phone': '123-456-7890', 'email': 'john.doe@example.com', 'url_img': 'm1' + '.jpg'},
                {'name': 'Jane Smith', 'phone': '987-654-3210', 'email': 'jane.smith@example.com', 'url_img': 'f1' + '.jpg'},
                {'name': 'Alice Johnson', 'phone': '555-123-4567', 'email': 'alice.johnson@example.com', 'url_img': 'f2' + '.jpg'},
                {'name': 'Bob Brown', 'phone': '555-987-6543', 'email': 'bob.brown@example.com', 'url_img': 'm2' + '.jpg'},
                {'name': 'Carol White', 'phone': '555-555-5555', 'email': 'carol.white@example.com', 'url_img': 'f3' + '.jpg'},
                {'name': 'David Black', 'phone': '555-444-3333', 'email': 'david.black@example.com', 'url_img': 'm3' + '.jpg'},
                {'name': 'Eva Green', 'phone': '555-222-1111', 'email': 'eva.green@example.com', 'url_img': 'f4' + '.jpg'},
                {'name': 'Frank Blue', 'phone': '555-666-7777', 'email': 'frank.blue@example.com', 'url_img': 'm4' + '.jpg'},
                {'name': 'Grace Yellow', 'phone': '555-888-9999', 'email': 'grace.yellow@example.com', 'url_img': 'f5' + '.jpg'},
                {'name': 'Hank Red', 'phone': '555-000-1111', 'email': 'hank.red@example.com', 'url_img': 'm5' + '.jpg'}
            ]

            cursor.execute("SELECT COUNT(*) FROM brokers")
            # Si el resultado es mayor a 0, la tabla existe
            # Entonces no es necesario llenarla nuevamente       
            if not (cursor.fetchone()[0]) > 0:
                for broker in brokers:
                    cursor.execute(f'''INSERT INTO brokers (nombre, mail, telefono, url_foto)
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


    #----------------------------------------------------------------
    def agregar_prop(self,
                     tipo_oper, tipo_prop,
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
                        tipo_oper, tipo_prop,
                        descrip_corta, descrip_larga, direccion,
                        nota, url_foto_1, url_foto_2, url_foto_3,
                        url_maps, id_broker, precio, superf,
                        superf_tot, baños, dormitorios, cocheras,
                        basicos, servicios, amenities )
                    VALUES ( %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            valores = (tipo_oper, tipo_prop,
                    descrip_corta, descrip_larga, direccion,
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
            query = "SELECT * FROM propiedades WHERE id = %s"
            cursor.execute(query, (id,))
  
            ret_val = cursor.fetchone()
        
        except ValueError as e:
            print(f"Error al ejecutar la consulta: {e}")

        finally:
            if cursor:
                cursor.close()
            close_db_connection(conn)
    
        return ret_val
    

    #----------------------------------------------------------------
    def consultar_ficha(self, id):
        conn = None
        cursor = None
        try:        
            conn = open_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Consultamos a partir de su id
            query = '''SELECT p.id,
                        p.tipo_oper,
                        p.tipo_prop,
                        p.descrip_corta,
                        p.descrip_larga,
                        p.direccion,
                        p.nota,
                        p.url_foto_1,
                        p.url_foto_2,
                        p.url_foto_3,
                        p.url_maps,
                        p.id_broker,
                        p.precio,
                        p.superf,
                        p.superf_tot,
                        p.baños,
                        p.dormitorios,
                        p.cocheras,
                        p.basicos,
                        p.servicios,
                        p.amenities,
                        b.id AS broker_id,
                        b.nombre AS broker_nombre,
                        b.mail AS broker_mail,
                        b.telefono AS broker_telefono,
                        b.url_foto AS broker_url_foto
                    FROM propiedades p
                    JOIN brokers b ON p.id_broker = b.id
                    WHERE p.id = %s;
                    '''
            
            cursor.execute(query, (id,))
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
                       tipo_oper, tipo_prop,
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
                        tipo_oper = %s, tipo_prop = %s,
                        descrip_corta = %s, descrip_larga = %s, direccion = %s,
                        nota = %s, url_foto_1 = %s, url_foto_2 = %s, url_foto_3 = %s,
                        url_maps = %s, id_broker = %s, precio = %s, superf = %s,
                        superf_tot = %s, baños = %s, dormitorios = %s, cocheras = %s,
                        basicos = %s, servicios = %s, amenities = %s
                    WHERE id = %s'''
            
            valores = (tipo_oper, tipo_prop,
                    descrip_corta, descrip_larga, direccion,
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
            ret_val = cursor.fetchall()

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
            query = "DELETE FROM propiedades WHERE id = %s"
            cursor.execute(query, (id,))

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
    def filtrar_prop(self, tipo_prop, tipo_oper, precio):
        # Conexión a la base de datos
        conn = open_db_connection()
        cursor = conn.cursor(dictionary=True) 

        try:
            #------------------------------------------------------------------------------
            #
            # Crear la consulta SQL
            query = "SELECT * FROM propiedades WHERE "
            conditions = []
            values = []

            if tipo_prop:
                placeholders = ','.join(['%s'] * len(tipo_prop))
                conditions.append(f"tipo_prop IN ({placeholders})")
                values.extend(tipo_prop)

            if tipo_oper:
                placeholders = ','.join(['%s'] * len(tipo_oper))
                conditions.append(f"tipo_oper IN ({placeholders})")
                values.extend(tipo_oper)

            # Construir la parte de la consulta para el campo precio
            if precio:
                subqueries = []
                for p in precio:
                    if p == '1':
                        subqueries.append("precio < 30")
                    elif p == '2':
                        subqueries.append("precio >= 30 AND precio < 50")
                    elif p == '3':
                        subqueries.append("precio > 50")

                if subqueries:
                    conditions.append("(" + " OR ".join(subqueries) + ")")

            if conditions:
                query += " AND ".join(conditions)
            else:
                query = query[:-7]  # Eliminar el 'WHERE' final si no hay condiciones
            #
            #------------------------------------------------------------------------------
            # Crear la consulta completa con los valores para imprimirla
            # query_with_values = query % tuple([f"'{v}'" for v in values])
            # print(f"Consulta SQL: {query_with_values}")

            # Ejecutar la consulta
            cursor.execute(query, values)
            ret_val = cursor.fetchall()

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
    tipo_oper = request.form['tipo_oper']
    tipo_prop = request.form['tipo_prop']
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
    nuevo_id = catalogo.agregar_prop(tipo_oper, tipo_prop,
                                        descrip_corta, descrip_larga, direccion,
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
    tipo_oper = request.form['tipo_oper']
    tipo_prop = request.form['tipo_prop']
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
                                tipo_oper, tipo_prop,
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


# index.html
@app.route('/')
def index():
    return redirect('static/index.html')

#--------------------------------------------------------------------
# Generar lista de propiedades según criterio de búsqueda
#--------------------------------------------------------------------
@app.route("/consulta", methods=["POST"])
def filtrar_prop():
    tipo_prop = request.form.getlist('tipo_prop')
    tipo_oper = request.form.getlist('tipo_oper')
    precio = request.form.getlist('precio')

    # Realiza la búsqueda en la base de datos
    listaProp = catalogo.filtrar_prop(tipo_prop=tipo_prop, tipo_oper=tipo_oper, precio=precio)

    return render_template('main_propiedades.html', listaProp=listaProp)


@app.route("/buscar", methods=["GET"])
def buscar_prop():
    # Realiza la búsqueda en la base de datos
    listaProp = catalogo.filtrar_prop(None, None, None)

    return render_template('main_propiedades.html', listaProp=listaProp)

#-------------------------------------------------------------------------------------
@app.route("/buscar/casa", methods=["GET"])
def buscar_propCasa():
    listaProp = catalogo.filtrar_prop(tipo_prop=['Casa',], tipo_oper=[], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)

@app.route("/buscar/departamento", methods=["GET"])
def buscar_propDepto():
    listaProp = catalogo.filtrar_prop(tipo_prop=['Departamento',], tipo_oper=[], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)

@app.route("/buscar/local", methods=["GET"])
def buscar_propLocal():
    listaProp = catalogo.filtrar_prop(tipo_prop=['Local',], tipo_oper=[], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)

@app.route("/buscar/otro-prop", methods=["GET"])
def buscar_propOtroProp():
    listaProp = catalogo.filtrar_prop(tipo_prop=['Otro',], tipo_oper=[], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)
#-----------------------------------------------------------------------------------------
@app.route("/buscar/venta", methods=["GET"])
def buscar_propVenta():
    listaProp = catalogo.filtrar_prop(tipo_prop=[], tipo_oper=['Venta',], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)

@app.route("/buscar/alquiler", methods=["GET"])
def buscar_propAlquiler():
    listaProp = catalogo.filtrar_prop(tipo_prop=[], tipo_oper=['Alquiler',], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)

@app.route("/buscar/otro-oper", methods=["GET"])
def buscar_propOtroOper():
    listaProp = catalogo.filtrar_prop(tipo_prop=[], tipo_oper=['Otro',], precio=[])
    return render_template('main_propiedades.html', listaProp=listaProp)

#--------------------------------------------------------------------
# Generar ficha de propiedad según id
#--------------------------------------------------------------------
@app.route("/buscar/<int:id>", methods=["GET"])
def buscar_ficha(id):
    # Realiza la búsqueda en la base de datos
    propiedad = catalogo.consultar_ficha(id)

    return render_template('main_ficha.html', propiedad=propiedad)
 

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
        return redirect('static/crud_menu.html')
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
            return redirect('static/crud_menu.html')
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