## Selector de noticias (Flask + NewsData.io)
Este es un proyecto Backend en formato RESTful desarrollado con Flask para el ingreso, gestion y recomendacion de noticias con base a los intereses del usuario. La aplicacion garantiza la division de las operaciones: el genero de interes del usuario, noticias y urls se guardan en una base de datos local (PostgreSQL). Asi mismo, por medio der la API se recomiendan noticias con base a los intereses del usuario.

## Caracteristicas principales
-API REST con Flask: para subir, eliminar y mostrar generos de noticias, noticias y urls favoritas.

-Conexion con PostgreSQL: Persistencia de datos local.

-Uso de la API NewsData.io: Recomendaciones actualizadas de noticias con el tema de interes del usuario.

## Requisitos Para ejecutar este proyecto, necesitas tener instalados:
-Python 3.x

-PostgreSQL (y acceso a una base de datos)

-Acceso a la API de Notion (un token de integración)

-Dependencias de Python Las principales librerías utilizadas se pueden instalar con pip:

     pip install Flask flask-cors psycopg2-binary python-dotenv requests

## Configuración del Entorno
La aplicación utiliza variables de entorno para manejar las credenciales y la configuración de las APIs y la base de datos. Debes crear un archivo llamado .env en la raíz del proyecto.

                # ------------------------------------
                # CONFIGURACIÓN DE POSTGRESQL
                # ------------------------------------
                DB_HOST=localhost
                DB_NAME=mis_peliculas
                DB_USER=postgres
                DB_PASSWORD=mysecretpassword
                DB_PORT=5432
              
                # ------------------------------------
                # CONFIGURACIÓN DE LA API
                # ------------------------------------
                # El Token de Integración de la API de Notion
                API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxx 

## Autor
Proyecto realizado por Juan Camilo Muñoz

## Licencia
Este proyecto esta bajo una licencia MIT.
