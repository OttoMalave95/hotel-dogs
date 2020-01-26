import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://192.168.1.102:8004')

nombre = str(input('Ingresar Nombre: '))
apellido = str(input('Ingresar Apellido: '))
cedula = str(input('Ingresar Cedula: '))
edad = str(input('Ingresar Edad: '))


print(s.avatar(nombre,apellido,cedula,edad)) 
