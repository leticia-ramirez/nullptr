from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, URL, text
from sqlalchemy.exc import SQLAlchemyError

#QUERY USUARIOS
QUERY_TODOS_LOS_USUARIOS = "SELECT ID_usuario, nombre_usuario, nombre, apellido, email, telefono FROM usuarios"

QUERY_USUARIO = "SELECT ID_usuario, nombre_usuario, nombre, apellido, email, telefono FROM usuarios WHERE ID_usuario = :ID_usuario"

QUERY_INGRESAR_USUARIO = "INSERT INTO usuarios (ID_usuario, nombre_usuario, nombre, apellido, email, telefono) VALUES (:ID_usuario, :nombre_usuario, :nombre, :apellido, :email, :telefono)"

QUERY_ACTUALIZAR_USUARIO = "UPDATE usuarios SET nombre_usuario = :nombre_usuario, nombre = :nombre, apellido = :apellido, email = :email, telefono = :telefono WHERE ID_usuario = :ID_usuario"

QUERY_ELIMINAR_USUARIO = "DELETE FROM usuarios WHERE ID_usuario = :ID_usuario"


#string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/TP_IDS")


def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()

    return result

def todos_los_usuarios():
    return run_query(QUERY_TODOS_LOS_USUARIOS).fetchall()

def usuarios_por_id(ID_usuario):
    return run_query(QUERY_USUARIO, {'ID_usuario': ID_usuario}).fetchall()

def insert_usuario(nuevo_usuario):
    run_query(QUERY_INGRESAR_USUARIO, nuevo_usuario)

def cambiar_usuario(ID_usuario, data):
    run_query(text(QUERY_ACTUALIZAR_USUARIO), {'ID_usuario': ID_usuario, **data})

def borra_usuario(ID_usuario):
    run_query(QUERY_ELIMINAR_USUARIO, {'ID_usuario': ID_usuario}).fetchone()