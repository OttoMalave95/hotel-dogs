from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pymongo import MongoClient
from bson.objectid import ObjectId


def conexion_db():
    host = "localhost"
    puerto = "27017"
    base_de_datos = "hotel_perros"
    cliente = MongoClient("mongodb://{}:{}".format(host, puerto))
    return cliente[base_de_datos]


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
with SimpleXMLRPCServer(("localhost", 8004),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def registrar_mascota(nombre, tipo):
        db = conexion_db()
        mascotas = db.mascotas
        return mascotas.insert_one({
                "nombre": nombre,
                "tipo": tipo,
            }).inserted_id

    server.register_function(registrar_mascota, 'registrar_mascota')

    # Run the server's main loop
    server.serve_forever()
