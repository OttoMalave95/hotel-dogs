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


def listado_mascotas():
    os.system("clear")

    print("*------ listado de Mascotas Albergadas ------* \n")

    return print("\n", s.listado_mascotas())

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

        # print("eleccion ", eleccion)
        # getch.getch()

        if eleccion == 1:
            registrar_mascota()
        elif eleccion == 2:
            # registrar_mascota()
            pass
        elif eleccion == 3:
            # registrar_mascota()
            pass
        elif eleccion == 4:
            # registrar_mascota()
            pass
        elif eleccion == 5:
            listado_mascotas()
        elif eleccion == 6:
            # registrar_mascota()
            pass
        else:
            print("\n Ha introducido una opcion invalida.. \n")

        sys.stdin.flush()
        getch.getch()

menu()
