# -*- coding: utf-8 -*-
import xmlrpc.client
import getch, sys, os

s = xmlrpc.client.ServerProxy('http://localhost:8004')


def registrar_mascota():
    os.system("clear") 
    print("*------ Registrar Mascota ------* \n")

    print("* Ingrese los siguientes Datos del Dueno: \n")
    cedula = str(input("Cedula: "))

    print("\n* Ingrese los siguientes Datos de la Mascota: \n")
    nombre = str(input("Nombre: "))
    especie = str(input("Especie: "))
    sexo = str(input("Sexo: "))
    raza = str(input("Raza: "))
    color = str(input("Color: "))

    return print("\n", s.registrar_mascota(cedula, nombre, especie, sexo, raza, color))


def asignar_mascota():
    os.system("clear")
    print("*------ Retirar Mascota ------* \n")

    print("* Ingrese los siguientes Datos del Dueno: \n")
    cedula = str(input("Cedula: "))

    print("\n* Ingrese los siguientes Datos de la Mascota: \n")
    nombre = str(input("Nombre: "))

    return print("\n", s.asignar_mascota(cedula, nombre))


def retirar_mascota():
    os.system("clear")
    print("*------ Retirar Mascota ------* \n")

    print("* Ingrese los siguientes Datos del Dueno: \n")
    cedula = str(input("Cedula: "))

    print("\n* Ingrese los siguientes Datos de la Mascota: \n")
    nombre = str(input("Nombre: "))

    return print("\n", s.retirar_mascota(cedula, nombre))


def habitaciones_ocupadas():
    os.system("clear")
    print("*------ Habitaciones Ocupadas ------* \n")

    return print("\n", s.habitaciones_ocupadas())


def listado_mascotas():
    os.system("clear")
    print("*------ listado de Mascotas Albergadas ------* \n")

    lista = s.listado_mascotas()
    for l in lista:
        print(l)
    return True


def cantidad_registros():
    os.system("clear")
    print("*------ Registros Mascota ------* \n")

    print("* Ingrese los siguientes Datos del Dueno: \n")
    cedula = str(input("Cedula: "))

    print("\n* Ingrese los siguientes Datos de la Mascota: \n")
    nombre = str(input("Nombre: "))

    return print("\n", s.cantidad_registros(cedula, nombre))


def menu():
    menu = """ 
        1 - Registrar Mascota
        2 - Asignar Cuarto a una Mascota
        3 - Retirar Mascota
        4 - Cantidad de cuartos ocupados
        5 - Listado de mascotas albergadas
        6 - Cantidad de registro de una mascota
        7 - Salir
    """
    eleccion = None

    while eleccion is not 7:
        os.system("clear") 

        print(menu)
        sys.stdin.flush()
        eleccion = int(input("Elige: "))

        if eleccion == 1:
            registrar_mascota()
        elif eleccion == 2:
            asignar_mascota()
        elif eleccion == 3:
            retirar_mascota()
        elif eleccion == 4:
            habitaciones_ocupadas()
        elif eleccion == 5:
            listado_mascotas()
        elif eleccion == 6:
            cantidad_registros()
        elif eleccion == 7:
            print("\n Saliendo del programa... \n")
            break
        else:
            print("\n Ha introducido una opcion invalida.. \n")

        sys.stdin.flush()
        getch.getch()

menu()
