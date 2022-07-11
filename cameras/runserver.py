from waitress import serve
from cameras.wsgi import application
from cameras.settings import HOST, PORT

if __name__ == "__main__":
    serve(application, host=HOST, port=PORT)