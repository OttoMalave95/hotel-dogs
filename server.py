from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
with SimpleXMLRPCServer(("192.168.1.102", 8004),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def avatar(nombre, apellido, cedula, edad):
        avatar = nombre[0]+apellido+cedula[:2]
        print('¡Hola {} {}! tu cedula es: {}, y tu edad es {}, Hemos creado tu avatar y es {}'.format(
            nombre, apellido, cedula, edad, avatar))
        return '¡Hola {} {}! tu cedula es: {}, y tu edad es {}, Hemos creado tu avatar y es {}'.format(nombre, apellido, cedula, edad, avatar)
    
    server.register_function(avatar, 'avatar')

    # Run the server's main loop
    server.serve_forever()
