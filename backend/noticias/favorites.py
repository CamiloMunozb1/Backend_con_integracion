# Importacion de las librerias necesarias para la aplicacion junto con las funcion de conexion a la base de datos. 
from flask import Blueprint,request,jsonify
from backend.data import conexion
from dotenv import load_dotenv
from psycopg2 import IntegrityError,InternalError

# Creacion del blueprint para usarlo como funcion modular
news_favorites = Blueprint('favorites','__name__')
load_dotenv() # Carga de las variables de entorno.

# Funcion que retorna la conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()

# Enrutador de entrada de a la seccion de noticias favoritas (modular).
@news_favorites.route('/add_favorite',methods = ['POST'])
def ingresar_favoritos():
    # Convierte la informacion recibida en un archivo Json.
    data = request.get_json()
    try:
        # Campos necesarios para identificar la noticia y el usuario.
        news_id = int(data.get('news_id',''))
        title_news = str(data.get('title_news','')).strip()
        news_url = str(data.get('url_news','')).strip()

        # Campo de verificacion de datos.
        if not all([news_id,title_news,news_url]):
            return jsonify({'Error' : 'todos los campos deben estar completos.'}),400
    # Manejo de errores.
    except TypeError:
        return jsonify({'Error' : 'la digitacion de los campos no es la esperada.'}),400
    except ValueError:
        return jsonify({'Error' : 'el tipo de dato no es correcto.'}),400
    
    conn = conexion_db() # Paso de la conexion con la base de datos,
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        # Creacion de un cursor para el manejo de la base de datos.
        cursor = conn.cursor()
        # Consulta para ingresar los campos requeridos a la base de datos.
        cursor.execute('''INSERT INTO news_favorite(titulo,url,news_id) VALUES  (%s,%s,%s)''',(title_news,news_url,news_id))
        conn.commit() # Subida de camvios.
        return jsonify({'Mensaje' : 'se subio el titulo y la url con exito.'}),200
    # Manejo de errores.
    except IntegrityError:
        conn.rollback()
        return jsonify({'Error' : 'integridad de la base de datos comprometida.'}),400
    except InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error interno en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en la base de datos: {error}.'}),400
    finally:
        cursor.close() # Cierre del cursor. 
        conn.close() # Cierre de la conexion con la base de datos.