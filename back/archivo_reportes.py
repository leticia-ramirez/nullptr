from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, URL, text
from sqlalchemy.exc import SQLAlchemyError

#QUERY REPORTES
QUERY_TODOS_LOS_REPORTES = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, DATE_FORMAT(R.fecha_reporte, '%d %b %Y'), R.ID_usuario, R.horario_reporte 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario"""

QUERY_TODOS_LOS_REPORTES_BY_ID="""
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, U.nombre_usuario, R.provincia, R.departamento, R.localidad, R.horario_reporte, R.ID_usuario
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE R.ID_reporte= :ID_reporte"""

QUERY_TODOS_LOS_REPORTESNOVEDADES = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, DATE_FORMAT(R.fecha_reporte, '%d %b %Y'), R.ID_usuario, R.horario_reporte 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
ORDER BY R.fecha_reporte DESC
LIMIT 5
"""

QUERY_REPORTE = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE R.ID_reporte = :ID_reporte"""

QUERY_REPORTE_FECHA = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE R.fecha_reporte = :fecha_reporte"""

QUERY_REPORTE_TIPO = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE I.tipo_reporte = :tipo_reporte """


QUERY_INGRESAR_REPORTE = "INSERT INTO reportes (provincia, departamento, localidad, fecha_reporte, horario_reporte, ID_incidente, ID_usuario) VALUES (:provincia, :departamento, :localidad, :fecha_reporte, :horario_reporte, :ID_incidente, :ID_usuario)"


QUERY_ACTUALIZAR_REPORTE = """
UPDATE reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
SET
R.ID_reporte = :ID_reporte, 
R.fecha_reporte = :fecha_reporte, 
R.ID_usuario = :ID_usuario ,
I.direccion_reporte = :direccion_reporte,
I.descripcion = :descripcion, 
I.tipo_reporte = :tipo_reporte
WHERE R.ID_reporte = :ID_reporte
"""
QUERY_ELIMINAR_REPORTE = "DELETE FROM reportes WHERE ID_reporte = :ID_reporte"

QUERY_LOCALIDAD="""SELECT R.ID_reporte, R.localidad, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
"""

QUERY_BY_LOCALIDAD="""SELECT R.ID_reporte, I.direccion_reporte, R.provincia, R.departamento, R.localidad, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE R.localidad=:localidad"""

#string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/TP_IDS")


def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()

    return result

def todos_los_reportes():
    return run_query(QUERY_TODOS_LOS_REPORTES).fetchall()

def reportes_novedades():
    return run_query(QUERY_TODOS_LOS_REPORTESNOVEDADES).fetchall()

def reporte_por_id(ID_reporte):
    return run_query(QUERY_TODOS_LOS_REPORTES_BY_ID, {'ID_reporte': ID_reporte}).fetchall()

def reporte_localidades():
    return run_query(QUERY_LOCALIDAD).fetchall()

def reporte_por_localidad(localidad):
    return run_query(QUERY_BY_LOCALIDAD, {'localidad':localidad}).fetchall()

def reporte_por_fecha(fecha_reporte):
    return run_query(QUERY_REPORTE_FECHA, {'fecha_reporte': fecha_reporte}).fetchall()

def reporte_por_tipo(tipo_reporte):
    return run_query(QUERY_REPORTE_TIPO, {'tipo_reporte': tipo_reporte}).fetchall()

def insert_reporte(nuevo_reporte):
    run_query(QUERY_INGRESAR_REPORTE, nuevo_reporte)

def chequeo_reporte(ID_reporte):
    return run_query(QUERY_REPORTE, {'ID_reporte': ID_reporte}).fetchall()

def cambiar_reporte(ID_reporte, data):
    run_query(QUERY_ACTUALIZAR_REPORTE, data)

def borra_reporte(ID_reporte):
    run_query(QUERY_ELIMINAR_REPORTE, {'ID_reporte': ID_reporte}).fetchone()



