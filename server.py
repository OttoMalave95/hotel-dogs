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

    def registrar_mascota(cedula, nombre, especie, sexo, raza, color):
        db = conexion_db()
        mascota = db.mascotas.find_one({ "cedula": cedula, "nombre": nombre })

        if not mascota:
            id = db.mascotas.insert_one({
                    "cedula": cedula,
                    "nombre": nombre,
                    "especie": especie,
                    "sexo": sexo,
                    "raza": raza,
                    "color": color,
                    "registros": 0,
                }).inserted_id
            result = 'Ocurrio un error al registrar la mascota'
            if id:
                result = 'Mascota registrada con exito'
            return result
        else:
            n = mascota.registros + 1
            db.mascotas.update_one({ "cedula": cedula, "nombre": nombre }, {
                "$set": {
                    "registros": n
                }
            })
            result = 'Mascota ya registrada'

    def asignar_mascota(cedula, nombre):
        db = conexion_db()
        mascota = db.mascotas.find_one({ "cedula": cedula, "nombre": nombre })
        if mascota:
            hotel = db.hotel.find_one({})
            if not hotel:
                hotel.insert_one({
                    "nombre": "Hotel de Perros",
                    "rif": "1234",
                    "habitaciones": []
                }).inserted_id

            habitaciones = hotel.habitaciones

            if len(habitaciones):
                for h in habitaciones:
                    if h.disponible == True:
                        h.mascota = mascota
                        h.disponible = False
                        break
                    else:
                        habitaciones.append({
                            "mascota": mascota,
                            "disponible": False
                            "numero": len(habitaciones)
                        })
                        break
            else:
                habitaciones.append({
                    "mascota": mascota,
                    "disponible": False,
                    "numero": len(habitaciones)
                })

            db.hotel.update_one({ "rif": "1234" }, {
                "$set": {
                    "habitaciones": habitaciones
                }
            })

            return 'Mascota asginada a una habitación'
        else:
            result = 'Mascota no registrada'

    def retirar_mascota(cedula, nombre):
        db = conexion_db()
        mascota = db.mascotas.find_one({ "cedula": cedula, "nombre": nombre })
        if not mascota:
            return 'Mascota no registrada'
        hotel = db.hotel.find_one({})
        if hotel:
            habitaciones = hotel.habitaciones
            if len(habitaciones):
                for h in habitaciones
                    if h.mascota.cedula == cedula and h.mascota.nombre == nombre:
                        h.mascota = None
                        h.disponible = True
                        break
                    else:
                        return 'La mascota no esta registrada en el hotel'
                
                db.hotel.update_one({ "rif": "1234" }, {
                    "$set": {
                        "habitaciones": habitaciones
                    }
                })

                return 'Mascota retirada del hotel'
            else:
                return 'No hay mascotas registradas en el hotel'
        else:
            return 'No hay mascotas registradas en el hotel'

    def habitaciones_ocupadas():
        db = conexion_db()
        hotel = db.hotel.find_one({})
        if hotel:
            habitaciones = hotel.habitaciones
            if len(habitaciones):
                cantidad = 0
                for h in habitaciones:
                    if not h.disponible:
                        cantidad = cantidad + 1
                return 'cantidad de habitaciones ocupadas: ' + str(cantidad)
            else:
                return 'No hay mascotas registradas'
        else:
            return 'No hay mascotas registradas'

    def cantidad_registros(cedula, nombre):
        db = conexion_db()
        mascota = db.mascotas.find_one({ "cedula": cedula, "nombre": nombre })

        if mascota:
            return 'Numero de veces registrada: ' + str(mascota.registros)
        else:
            return 'Mascota no registrada'

    def listado_mascotas():
        db = conexion_db()
        hotel = db.hotel.find_one({})
        if hotel:
            habitaciones = hotel.habitaciones
            if len(habitaciones):
                lista_mascotas = []
                for h in habitaciones:
                    if h.disponible:
                        informacion = 'dueño: ' + h.mascota.cedula + ' mascota: ' + h.mascota.nombre + ' habitación: ' + str(h.numero)
                        lista_mascotas.append(informacion)
                return lista_mascotas
            else:
                return 'No hay mascotas registradas'
        else:
            return 'No hay mascotas registradas'


    server.register_function(registrar_mascota, 'registrar_mascota')
    server.register_function(asignar_mascota, 'asignar_mascota')
    server.register_function(retirar_mascota, 'retirar_mascota')
    server.register_function(habitaciones_ocupadas, 'habitaciones_ocupadas')
    server.register_function(cantidad_registros, 'cantidad_registros')

    # Run the server's main loop
    server.serve_forever()
