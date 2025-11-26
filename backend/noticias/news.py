# Importacion de librerias para el funcionamiento de la aplicacion junto con las funciones modulares de la alplicacion.
from flask import Flask,request,jsonify
from backend.data import conexion
from backend.noticias import favorites
from backend.noticias import delete_news
from backend.noticias import show_news
from flask_cors import CORS
from dotenv import load_dotenv
from psycopg2 import IntegrityError,InternalError # Importacion de errores comunes en la base de datos.
import requests
import os

# Identificador de la aplicacion.
app = Flask(__name__)
# Conexion con el fronted para el ingreso de la informacion.
CORS(app,origins='www.paginaejemplo.com',supports_credentials=True)
load_dotenv() # Carga de las variables de entorno.

# Funcion que retorna la conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()

# Funciones modulares de la aplicacion.
app.register_blueprint(favorites)
app.register_blueprint(delete_news)
app.register_blueprint(show_news)

# Funcion de la api de donde se van a traer las noticias.
def api_news(news_type): # se pasa 'New_type' donde se especifica el genero de la noticia.
    try:
        # Se traen de las variables de entorno la api_key.
        api_key = os.getenv('API_KEY')
        # Se usa la url de la api junto con el genero dado por el usuario.
        url = f'https://newsdata.io/api/1/news?apikey={api_key}&q={news_type}&language=es'
        # Validador de campo para la api_key.
        if not api_key:
            return jsonify({'Error' : 'el campo de la API KEY es necesario para la autentificacion.'}),400
        # solicitud a la API y guarda la respuesta en la variable.
        respuesta = requests.get(url)
        # status de la respuesta de la API.
        if respuesta.status_code == 200:
            # Convertimos la respuesta a formato JSON.
            data = respuesta.json()
            # Se recoje la informacion solicitada (link,title y date).
            link = data['results'][0]['link']
            title = data['results'][0]['title']
            date = data['results'][0]['pubDate']
            # Se muestra la informacion seleccionada.
            print(f'Link de la noticia : {link}')
            print(f'El titulo de la notica es : {title}')
            print(f'La fecha de emision del articulo es : {date}')
        else: 
            return jsonify({'Error' : f'respuesta de la API invalida : {respuesta.status_code}'}),400
        # Manejo de errores.
    except Exception as error:
        return jsonify({'Error' : f'error de manejo en la base de datos : {error}.'}),400

'''
Enrutador para el ingreso del genero de noticias 
con el metodo POST que para el envio de informacion 
a la base de datos.
'''
@app.route('/news',methods = ['POST'])
def search_news():
    # La informacion que se genere desde el fronted se transforma en un archivo Json.
    data = request.get_json()

    try:
        # Se pasa el tipo o genero de las noticias de la preferencia del usuario.
        news_type = str(data.get('news_type','')).strip()
        # Validador de campo.
        if not news_type:
            return jsonify({'Error' : 'El campo debe estar completo.'}),400
    # Manejo de errores.
    except TypeError:
        return jsonify({'Error' : 'La digitacion del campo no es compatible con el tipo de cadena de texto.'}),400
    
    # Paso de la conexion de la base de datos.
    conn = conexion_db()
    # Validador de la conexion de la base de datos.
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        # Creacion de un cursor para manejo de la base de datos.
        cursor = conn.cursor()
        # Consulta de ingreso de informacion a la base de datos.
        cursor.execute('''
                        INSERT INTO
                        news(news_user) 
                        VALUES (%s) RETURNING ID''',
                        (news_type,))
        # se devuelve el id generado en el genero de la noticia.
        news_id = cursor.fetchone()[0]
        # Se suben los datos.
        conn.commit()
        # Se pasa el genero de la noticia de la base de datos a la API.
        news_search_unit = api_news(news_type)
        # Campo de validacion si no se encuentra el campo del genero de la noticia.
        if news_search_unit:
            conn.rollback()
            return jsonify({'Error' : f'no se pudo hacer la integracion con la API : {news_search_unit}.'}),400
        return jsonify({'Mensaje' : 'el tema de interes de noticas subido con exito.', 'ID' : news_id}),200
    # Manejo de errores.
    except IntegrityError:
        conn.rollback()
        return jsonify({'Error' : 'integridad de la base de datos comprometida.'}),400
    except InternalError:
        conn.rollback()
        return jsonify({'Error' : 'error interno en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error inesperado en el programa : {error}.'})
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.



