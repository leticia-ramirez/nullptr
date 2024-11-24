from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, URL, text
from sqlalchemy.exc import SQLAlchemyError

#QUERY INCIDENTES
QUERY_INGRESAR_INCIDENTE = """
INSERT INTO incidentes (tipo_reporte, direccion_reporte, descripcion) 
VALUES (:tipo_reporte, :direccion_reporte, :descripcion)
"""

QUERY_ULTIMO_INCIDENTE = """
SELECT R.ID_incidente, R.tipo_reporte, R.direccion_reporte, R.descripcion
FROM incidentes R
ORDER BY R.ID_incidente DESC
LIMIT 1
"""

#string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/TP_IDS")


def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()

    return result

def insert_incidente(nuevo_incidente):
    run_query(QUERY_INGRESAR_INCIDENTE, nuevo_incidente)

def ultimo_incidente():
    return run_query(QUERY_ULTIMO_INCIDENTE).fetchall()