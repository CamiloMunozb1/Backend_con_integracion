# Importacion de las librerias necesarias para la conexion con la base de datos.
from flask import Flask,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

# Identificador de la aplicacion para la conexion.
app = Flask(__name__)
# Se genera la conexion con el fronted para el paso de informacion.
CORS(app,origins='www.paginaejemplo.com',supports_credentials=True)
load_dotenv() # Carga de las variables de entorno-

def conexion_db():
    try:
        '''
        Conexion con la base de datos junto con el cargue de las variables
        de entorno donde se encuentra la informacion de la base de datos.
        '''
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
        )
        return conn
    # Manejo de errores.
    except psycopg2.errors.InternalError:
        return jsonify({'Error' : 'error interno en la base de datos.'}),400
    except Exception as error:
        print(f'Error en el programa: {error}.')
    finally:
        conn.close() # Cerrar la conexion.