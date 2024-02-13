"""
===================================
Panel de administración de usuarios
===================================

Introducción
============

Este proyecto implementa un backend Flask con un sistema de login y
operaciones CRUD (Crear, Leer, Actualizar y Borrar) en los usuarios de la
base de datos.
En el frontend, la aplicación es renderizada utilizando React y se proporciona
todos los formularios correspondientes para interactuar con la API del backend.

Notas sobre los formularios
---------------------------

Los formularios con los que trabajan tanto frontend como backend para
interactuar, tienen la siguiente estructura:

:param email:    str
:param name:     str
:param lastname: str
:param password: str
:param phone:    int
:param age:      int

Excepto para la creación y actualización de usuarios, donde además se agrega el
campo 'id' a la estructura del formulario de arriba; y para el borrado de
usuarios, donde el único campo recibido es el campo 'id'.

:param id: int
    Número de identificación del usuario en cuestión.

Rutas
=====

- "/"                               : Es el punto de entrada a la aplicación.
- "/server/new_user"                : (C) Crear un usuario.
- "/server/list_of_users"           : (R) Leer los usuarios.
- "/server/edit_user/"              : (U) Actualizar datos de un usuario.
- "/server/delete_user/<int:id>"    : (D) Borrar un usuario.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from types import SimpleNamespace
import json

app = Flask("server", static_folder="dist/assets/", template_folder="dist")
CORS(app)

@app.route("/")
def index():
    """
    Renderiza la página pricipal de la aplicación.

    Esta ruta sirve como punto de entrada a la aplicación React retornando
    el archivo index.html que renderizará la aplicación.

    Returns:
        str: Contenido HTML de la página principal.
    """

    return render_template("index.html")

@app.post("/server/new_user")
def new_user():
    """
    Recibe la información para la creación de un usuario nuevo.

    Esta ruta recibe los datos de un formulario que serán usados para la
    creación de un objeto 'new_user' que contendrá los datos de un usuario
    nuevo y los guardará en la base de datos.
    """
    form = request.get_json()
    
    new_user = {
        "email" : form["email"],
        "name" : form["name"],
        "lastname" : form["lastname"],
        "password" : form["password"],
        "phone" : form["phone"],
        "age": form["age"]
    }

    try:
        with open("users.json", "r+") as file:
            user_list = json.load(file)
            new_user = {"id": len(user_list), **new_user}
            user_list.append(new_user)
            file.seek(0)
            json.dump(user_list, file, indent=2)
    except FileNotFoundError:
        with open("users.json", "w") as file:
            new_user = {"id": 0, **new_user}
            json.dump([new_user], file, indent=2)

    return "", 200

@app.get("/server/list_of_users")
def list_of_users():
    """
    Envía la lista de usuarios creados y sus datos.

    Esta ruta toma todos los usuarios guardados en la base de datos y su
    información y la envía al cliente como una lista serializada en formato
    JSON.

    Returns:
        list: Una lista de diccionarios que representan a cada usuario.
              Se devuelve una lista vacía si no hay usuarios o si la base
              de datos no existe.
    """
    try:
        with open("users.json", "r") as file:
            user_list = json.load(
                file,
                object_hook = lambda d: SimpleNamespace(**d)
            )
            return jsonify([vars(user) for user in user_list])
    except FileNotFoundError:
        return jsonify([])

@app.get("/server/edit_user/")
def edit_user():
    """
    Actualiza los datos de un usuario ya creado usando los datos recibidos.

    Esta ruta recibe un formulario donde se especifica el usuario que debe
    ser actualizado, y los nuevos datos del usuario a guardar.
    """
    args = request.args.get("user_data")
    user_data = json.loads(args)
    id = user_data["id"]

    with open("users.json", "r") as file:
        user_list = json.load(file)

    user_list[id]["email"] = user_data["email"]
    user_list[id]["name"] = user_data["name"]
    user_list[id]["lastname"] = user_data["lastname"]
    user_list[id]["password"] = user_data["password"]
    user_list[id]["phone"] = user_data["phone"]
    user_list[id]["age"] = user_data["age"]

    with open("users.json", "w") as file:
        json.dump(user_list, file, indent=2)

    return "", 200

@app.get("/server/delete_user/<int:id>")
def delete_user(id):
    """
    Borra el usuario especificado.

    Esta ruta recibe una identificación de usuario y se usará para borrar
    el usuario correspondiente en la base de datos.

    Args:
        int: ID del usuario a ser borrado.
    """
    with open("users.json", "r") as file:
        user_list = json.load(file)
        del user_list[id]
        for i in range(0, len(user_list)):
            user_list[i]["id"] = i
    with open("users.json", "w") as file:
        json.dump(user_list, file, indent=2)

    return "", 200