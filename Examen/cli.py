"""Interfaz simple de texto para interactuar con el zoológico."""

from __future__ import annotations

from typing import List

from .zoo import Zoologico


def mostrar_menu() -> None:
    print("\n Zoologico interactivo")
    print("1) Listar animales por clase")
    print("2) Listar animales por caracteristica")
    print("3) Agregar animal")
    print("4) Guardar y salir")
    print("0) Salir sin guardar")


def solicitar_opcion() -> str:
    return input("Seleccione una opcion: ").strip()


def seleccionar_clase(zoo: Zoologico) -> str:
    clases = zoo.obtener_clases()
    if not clases:
        print("No hay clases definidas en el zoologico.")
        return ""

    print("Clases disponibles:")
    for i, clase in enumerate(clases, start=1):
        print(f"  {i}) {clase}")

    seleccion = input("Ingrese el numero de la clase o escriba el nombre: ").strip()
    if not seleccion:
        return ""

    if seleccion.isdigit():
        idx = int(seleccion) - 1
        if 0 <= idx < len(clases):
            return clases[idx]
        print("Seleccion invalida.")
        return ""

    return seleccion


def seleccionar_caracteristica(zoo: Zoologico) -> str:
    caracts = zoo.obtener_caracteristicas()
    if not caracts:
        print("No se encontraron características en los animales.")
        return ""

    print("Características disponibles (parciales):")
    for i, c in enumerate(caracts[:30], start=1):
        print(f"  {i}) {c}")
    if len(caracts) > 30:
        print(f"  ... (y {len(caracts) - 30} más)")

    return input("Escriba el texto de la característica (o un fragmento): ").strip()


def listar_por_clase(zoo: Zoologico) -> None:
    clase = seleccionar_clase(zoo)
    if not clase:
        return

    resultado = zoo.listar_por_clase(clase)
    if not resultado:
        print(f"No se encontraron animales en la clase '{clase}'.")
        return

    print(f"\nAnimales de la clase '{clase}':")
    for animal in resultado:
        print(f"- {animal}")


def listar_por_caracteristica(zoo: Zoologico) -> None:
    caracteristica = seleccionar_caracteristica(zoo)
    if not caracteristica:
        return

    resultado = zoo.listar_por_caracteristica(caracteristica)
    if not resultado:
        print(f"No se encontraron animales con la característica '{caracteristica}'.")
        return

    print(f"\nAnimales con característica '{caracteristica}':")
    for animal in resultado:
        print(f"- {animal}")


def agregar_animal(zoo: Zoologico) -> None:
    print("\n--- Agregar nuevo animal ---")
    nombre = input("Nombre: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    if nombre in zoo.animales:
        print(f"Ya existe un animal con nombre '{nombre}'.")
        return

    clase = input("Clase (por ejemplo 'Mamifero'): ").strip()
    if not clase:
        print("La clase no puede estar vacía.")
        return

    caracteristicas = input(
        "Características (separadas por ';', ex: plumas;vuela;diurno): "
    ).strip()
    car_list = [c.strip() for c in caracteristicas.split(";") if c.strip()]
    zoo.agregar_animal(nombre=nombre, clase=clase, caracteristicas=car_list, persist=False)
    print(f"Animal '{nombre}' agregado (se guardará al salir).")


def loop_principal() -> None:
    zoo = Zoologico()
    guardado = False

    while True:
        mostrar_menu()
        opcion = solicitar_opcion()

        if opcion == "1":
            listar_por_clase(zoo)
        elif opcion == "2":
            listar_por_caracteristica(zoo)
        elif opcion == "3":
            agregar_animal(zoo)
            guardado = False
        elif opcion == "4":
            zoo.save_animals()
            print("Cambios guardados. Saliendo...")
            return
        elif opcion == "0":
            if not guardado:
                respuesta = input(
                    "No se han guardado los cambios. ¿Desea salir sin guardar? (s/n): "
                ).strip().lower()
                if respuesta != "s":
                    continue
            print("Saliendo sin guardar.")
            return
        else:
            print("Opción inválida. Intente nuevamente.")
