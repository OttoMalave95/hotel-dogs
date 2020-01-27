import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8004')

nombre = str(input('Ingresar Nombre: '))
tipo = str(input('Ingresar Tipo: '))


print(s.registrar_mascota(nombre, tipo))
