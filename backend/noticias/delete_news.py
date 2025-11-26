# Importacion de las librerias necesarias para la aplicacion y la conexion con la base de datos.
from flask import Blueprint, request, jsonify
from backend.data import conexion
from dotenv import load_dotenv
from psycopg2 import IntegrityError,InternalError

# Generamos un blueprint para el uso de esta como funcion modular.
delete_new = Blueprint('delete',__name__)
load_dotenv() # Carga de las variables de entorno.

# Retorno de la conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()

# Enrutador del Blueprint para la eliminacion de informacion.
@delete_new.route('delete',methods = ['POST'])
def delete_news():
    # Convierte la informacion pasada a un archivo Json.
    data = request.get_json()

    try:
        # Pasamos el id de la noticia que se quiere eliminar.
        delete_news = int(data.get('news_id',''))
        # Validador de campo.
        if not delete_news:
            return jsonify({'Error' : 'El campo debe estar completo.'}),400
    # Manejo de errores.
    except TypeError:
        return jsonify({'Error' : 'la digitacion del campo es incorrecta.'}),400
    except ValueError:
        return jsonify({'Error' : 'el tipo de dato no es correcto.'}),400
    
    # Pasamos la conexion a la base de datos.
    conn = conexion_db()
    if conn is None: # Validador de campo.
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor() # Creacion del cursor para manejo de la base de datos.
        # Consulta para la seleccion del ID del genero de la noticia.
        cursor.execute('''SELECT * FROM news WHERE news_id = ?''',(delete_news,))
        if cursor.fetchone() is None: # Validador de campo.
            return jsonify({'Error' : 'noticia no encontrada.'}),400
        # Consulta de eliminacion en cascada donde se elimina el ID del genero de la noticia, por ende se eliminan los datos.
        cursor.execute('''DELETE FROM news WHERE news_id = %s''',(delete_news,))
        cursor.execute('''DELETE FROM news_favorite WHERE news_id = %s''')(delete_news,)
        if cursor.rowcount == 0: # Se busca el ID de la review.
            return jsonify({'Error' : 'no se encontro el id de la categoria de interes.'}),400
        conn.commit() # Se suben los cambios a la base de datos.
        return jsonify({'Mensaje' : 'se elimino la noticia de manera correcta.'}),200
    # Manejo de errores.
    except IntegrityError:
        conn.rollback()
        return jsonify({'Error' : 'error de integridad en la base de datos.'})
    except InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error en la integridad de la base de datos.'})
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en la aplicacion: {error}.'}) 
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion con la base de datos.
