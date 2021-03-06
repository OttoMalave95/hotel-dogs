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
                    "registros": 1,
                }).inserted_id
            result = 'Ocurrio un error al registrar la mascota'
            if id:
                result = 'Mascota registrada con exito'
            return result
        else:
            db.mascotas.update_one({ "cedula": cedula, "nombre": nombre }, {
                "$set": {
                    "registros": mascota['registros'] + 1
                }
            })
            return 'Mascota ya registrada'

    def asignar_mascota(cedula, nombre):
        db = conexion_db()
        mascota = db.mascotas.find_one({ "cedula": cedula, "nombre": nombre })
        if mascota:
            if not db.hotel.find_one({}):
                id_hotel = db.hotel.insert_one({
                    "nombre": "Hotel de Perros",
                    "rif": "1234",
                    "habitaciones": []
                }).inserted_id

            hotel = db.hotel.find_one({})
            habitaciones = hotel['habitaciones']

            if len(habitaciones):
                for h in habitaciones:
                    if h['mascota'] and h['mascota']['cedula'] == cedula and h['mascota']['nombre'] == nombre:
                        return 'La mascota ya tiene una habitación asignada'
                for h in habitaciones:
                    if h['disponible'] == True:
                        h['mascota'] = mascota
                        h['disponible'] = False
                        break
                    else:
                        habitaciones.append({
                            "mascota": mascota,
                            "disponible": False,
                            "numero": len(habitaciones) + 1
                        })
                        break
            else:
                habitaciones.append({
                    "mascota": mascota,
                    "disponible": False,
                    "numero": 1
                })

            db.hotel.update_one({ "rif": "1234" }, {
                "$set": {
                    "habitaciones": habitaciones
                }
            })

            return 'Mascota asginada a una habitación'
        else:
            return 'Mascota no registrada'

    def retirar_mascota(cedula, nombre):
        db = conexion_db()
        mascota = db.mascotas.find_one({ "cedula": cedula, "nombre": nombre })
        if not mascota:
            return 'Mascota no registrada'
        hotel = db.hotel.find_one({})
        if hotel:
            habitaciones = hotel['habitaciones']
            if len(habitaciones):
                mascota_retirada = False
                for h in habitaciones:
                    if h['mascota'] and h['mascota']['cedula'] == cedula and h['mascota']['nombre'] == nombre:
                        h['mascota'] = None
                        h['disponible'] = True
                        mascota_retirada = True

                if mascota_retirada:
                    db.hotel.update_one({ "rif": "1234" }, {
                        "$set": {
                            "habitaciones": habitaciones
                        }
                    })

                    return 'Mascota retirada del hotel'
                else:
                    return 'La mascota no esta registrada en el hotel'
                
            else:
                return 'No hay mascotas registradas en el hotel'
        else:
            return 'No hay mascotas registradas en el hotel'

    def habitaciones_ocupadas():
        db = conexion_db()
        hotel = db.hotel.find_one({})
        if hotel:
            habitaciones = hotel['habitaciones']
            if len(habitaciones):
                cantidad = 0
                for h in habitaciones:
                    if not h['disponible']:
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
            return 'Numero de veces registrada: ' + str(mascota['registros'])
        else:
            return 'Mascota no registrada'

    def listado_mascotas():
        db = conexion_db()
        hotel = db.hotel.find_one({})
        if hotel:
            habitaciones = hotel['habitaciones']
            if len(habitaciones):
                lista_mascotas = []
                for h in habitaciones:
                    if not h['disponible']:
                        informacion = 'dueño: ' + h['mascota']['cedula'] + ', mascota: ' + h['mascota']['nombre'] + ', habitación: ' + str(h['numero'])
                        lista_mascotas.append(informacion)

                if lista_mascotas:
                    return lista_mascotas
                else:
                    return 'No hay mascotas en el hotel'
            else:
                return 'No hay mascotas registradas'
        else:
            return 'No hay mascotas registradas'


    server.register_function(registrar_mascota, 'registrar_mascota')
    server.register_function(asignar_mascota, 'asignar_mascota')
    server.register_function(retirar_mascota, 'retirar_mascota')
    server.register_function(habitaciones_ocupadas, 'habitaciones_ocupadas')
    server.register_function(cantidad_registros, 'cantidad_registros')
    server.register_function(listado_mascotas, 'listado_mascotas')

    # Run the server's main loop
    server.serve_forever()
