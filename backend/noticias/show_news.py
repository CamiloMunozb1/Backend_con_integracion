# Importacion de librerias necesarias para la aplicacion junto con la conexion a la base de datos.
from flask import Blueprint,request,jsonify
from backend.data import conexion
from psycopg2 import IntegrityError,InternalError
from dotenv import load_dotenv
import pandas as pd # Uso de pandas para mostrar los datos.

# Creacion del blueprint para su uso como funcion modular.
show_news = Blueprint('mostrar_noticias',__name__)
load_dotenv() # Carga de variables de entorno.

# Retornamos la conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()

# Enrutador para mostrar los datos de la noticia.
@show_news.route('/mostrar_noticias', methods = ['GET'])
def show_new():
    # se devuelve un archivo Json con la informacion.
    data = request.get_json()
    # Se pasa el id de la noticia
    news_id = int(data.get('news_id',''))
    if not news_id:
        return jsonify({'Error' : 'el campo debe estar completo.'}),400
    
    # Uso de la conexion con la base de datos,
    conn = conexion_db()
    if conn is None:
        return jsonify({'Error' : 'no se puedo encontrar la conexion con la base de datos.'}),400
    
    try:
        # creacion del cursor para el manejo de la base de datos.
        cursor = conn.cursor()
        # Seleccionamos el id de la noticia para buscarlo en la base de datos y buscar el usuario.
        cursor.execute('''SELECT * FROM news WHERE news_id = %s''',(news_id))
        if cursor.fetchone() is None:
            return jsonify({'Error' : 'categoria de la noticia no encontrada'}),400
        df = pd.read_sql_query('''
                                SELECT favorite_id, title_news, news_url, news_type
                                FROM news_favorite
                                INNER JOIN 
                                news ON news_favorite.news_id = news.news_id
                                WHERE 
                                news_id = %s
                                ORDER BY 
                                favorite_id DESC;
                                ''', conn,params=[news_id]) # Filtra los ID´s de las noticias para mostrarle al usuario unicamente sus temas de interes.
        # lee la respuesta del dataframe y la convierte a una lista de diccionarios .
        respuesta = df.to_dict(['records'])
        if not respuesta: # Si no se encuentra la respuesta se muestra el mensaje.
            return jsonify({'mensaje' : 'no se encontraron registros.'}),200
        else:
            return jsonify({'respuesta' :  f'{respuesta}'}),200
    # Manejo de errores.
    except IntegrityError:
        return jsonify({'error' : 'error de integridad en la base de datos.'}),400
    except InternalError:
        return jsonify({'error' : 'error interno en la base de datos.'}),400
    except Exception as error:
        return jsonify({'error' : f'error inesperado en el programa : {error}.'}),400
    finally:
        conn.close() # cierre de la conexion con la base de datos.
        
