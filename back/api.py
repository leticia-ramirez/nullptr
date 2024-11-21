from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker, scoped_session

#NO OLVIDAR las pre y post

#QUERY REPORTES
QUERY_TODOS_LOS_REPORTES = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario"""

QUERY_TODOS_LOS_REPORTES_BY_ID="""
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, U.nombre, U.apellido, R.provincia, R.departamento, R.localidad, R.horario_reporte, R.ID_usuario
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE R.ID_reporte= :ID_reporte"""

QUERY_TODOS_LOS_REPORTESNOVEDADES = """
SELECT R.ID_reporte, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
ORDER BY R.fecha_reporte DESC
LIMIT 3
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

#QUERY USUARIOS
QUERY_TODOS_LOS_USUARIOS = "SELECT ID_usuario, nombre_usuario, nombre, apellido, email, telefono FROM usuarios"

QUERY_USUARIO = "SELECT ID_usuario, nombre_usuario, nombre, apellido, email, telefono FROM usuarios WHERE ID_usuario = :ID_usuario"

QUERY_INGRESAR_USUARIO = "INSERT INTO usuarios (ID_usuario, nombre_usuario, nombre, apellido, email, telefono) VALUES (:ID_usuario, :nombre_usuario, :nombre, :apellido, :email, :telefono)"

QUERY_ACTUALIZAR_USUARIO = "UPDATE usuarios SET nombre_usuario = :nombre_usuario, nombre = :nombre, apellido = :apellido, email = :email, telefono = :telefono WHERE ID_usuario = :ID_usuario"

QUERY_ELIMINAR_USUARIO = "DELETE FROM usuarios WHERE ID_usuario = :ID_usuario"

QUERY_LOCALIDAD="""SELECT R.ID_reporte, R.localidad, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
"""

QUERY_BY_LOCALIDAD="""SELECT R.ID_reporte, R.localidad, I.direccion_reporte, I.descripcion, I.tipo_reporte, R.fecha_reporte, R.ID_usuario 
FROM reportes R
INNER JOIN incidentes I on I.ID_incidente = R.ID_incidente
INNER JOIN usuarios U on U.ID_usuario = R.ID_usuario
WHERE R.localidad=:localidad"""

#string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
engine = create_engine("mysql+mysqlconnector://root:tucontraseña@localhost:3306/TP_IDS")

Session = scoped_session(sessionmaker(bind=engine)) #para empezar a tomar consultas

app = Flask(__name__)


#ENDPOINTS REPORTES
@app.route('/api/v1/reportes', methods=['GET'])     #Endpoint: /reportes
def reportes():
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_TODOS_LOS_REPORTES)).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5]})
    return jsonify(response), 200

@app.route('/api/v1/reportesNovedades', methods=['GET'])     #Endpoint: /reportes Novedades
def reportesNovedades():
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_TODOS_LOS_REPORTESNOVEDADES)).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/id/<int:ID_reporte>', methods=['GET'])   #Endpoint: /reportes/porID
def reporte_ID(ID_reporte):    #metodo reporte_ID
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_TODOS_LOS_REPORTES_BY_ID), {'ID_reporte':ID_reporte}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response = []
    for row in result:
        response.append({'ID_reporte': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'nombre': row[5], 'apellido': row[6], 'provincia': row[7], 'departamento': row[8], 'localidad': row[9], "horario_reporte": str(row[10]), "ID_usuario": row[11]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/localidad', methods=['GET'])   #Endpoint: /reportes/todaslocalidades
def reporte_localidad():    #metodo reporte_todas_localidad
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_LOCALIDAD)).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response = []
    for row in result:
        response.append({'ID': row[0], 'localidad':row[1], 'direccion_reporte': row[2], 'descripcion': row[3], 'tipo_reporte': row[4], 'fecha_reporte': row[5], 'ID_usuario': row[6]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/localidad/<localidad>', methods=['GET'])   #Endpoint: /filtro por localidades
def reporte_by_localidad(localidad):    
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_BY_LOCALIDAD), {'localidad':localidad}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response = []
    for row in result:
        response.append({'ID': row[0], 'localidad':row[1], 'direccion_reporte': row[2], 'descripcion': row[3], 'tipo_reporte': row[4], 'fecha_reporte': row[5], 'ID_usuario': row[6]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/fecha/<fecha_reporte>', methods=['GET'])   #Endpoint: /reportes/porFecha
def reporte_fecha(fecha_reporte):    #metodo reporte_fecha
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE_FECHA), {'fecha_reporte': fecha_reporte}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    response = []
    for row in result:
        response.append({'ID': row [0], 'direccion_reporte': row [1], 'descripcion': row [2], 'tipo_reporte': row [3], 'fecha_reporte': row [4], 'ID_usuario': row [5]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/tipo/<tipo_reporte>', methods=['GET'])   #Endpoint: /reportes/porTipoDeReporte
def reporte_tipo(tipo_reporte):    #metodo reporte_tipo
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE_TIPO), {'tipo_reporte': tipo_reporte}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    response = []
    for row in result:
        response.append({'ID': row [0], 'direccion_reporte': row [1], 'descripcion': row [2], 'tipo_reporte': row [3], 'fecha_reporte': row [4], 'ID_usuario': row [5]})
    return jsonify(response), 200


@app.route('/api/v1/reportes', methods=['POST'])   #Endpoint: /reportes
def ingresar_reporte():    #metodo ingresar
    nuevo_reporte = request.get_json()

    keys = ('provincia', 'departamento', 'localidad', 'fecha_reporte', 'horario_reporte', 'ID_incidente', 'ID_usuario')
    for key in keys:
        if key not in nuevo_reporte:
            return jsonify({'message': f"Falta el dato {key}"}), 400    

    try:
        conn = Session()
        conn.execute(text(QUERY_INGRESAR_REPORTE), params=nuevo_reporte)
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify(nuevo_reporte), 201

@app.route('/api/v1/incidentes', methods=['POST'])   #Endpoint: /incidentes
def ingresar_incidente():    #metodo ingresar
    nuevo_reporte = request.get_json()

    keys = ('tipo_reporte', 'direccion_reporte', 'descripcion')
    for key in keys:
        if key not in nuevo_reporte:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        conn.execute(text(QUERY_INGRESAR_INCIDENTE), params = nuevo_reporte)
        nashei = conn.execute(text(QUERY_ULTIMO_INCIDENTE)).fetchall()
        nashei = nashei[0][0]
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify(str(nashei)), 201

@app.route('/api/v1/reportes/id/<int:ID_reporte>', methods=['PUT'])   #Endpoint: /reportes
def actualizar_reporte(ID_reporte):    #metodo actualizar
    data = request.get_json()

    keys = ('ID_reporte', 'ID_usuario', 'descripcion', 'direccion_reporte', 'fecha_reporte', 'tipo_reporte')
    for key in keys:
        if key not in data:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'ID_reporte': ID_reporte}).fetchall()
        if not result:
            return jsonify({'error': 'No se encontro el usuario'}), 400
        conn.execute(text(QUERY_ACTUALIZAR_REPORTE), params = data)
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'ID_reporte': ID_reporte, **data}), 200

@app.route('/api/v1/reportes/<int:ID_reporte>', methods=['DELETE'])   #Endpoint: /reportes/porID
def eliminar_reporte(ID_reporte):    #metodo eliminar
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'ID_reporte': ID_reporte}).fetchone()
        if not result:
            return jsonify({'error': 'No se encontro el reporte'}), 400
        conn.execute(text(QUERY_ELIMINAR_REPORTE), params={'ID_reporte': ID_reporte})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'ID_reporte': result[0], 'direccion_reporte': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'ID_usuario': result[5]}), 200


#ENDPOINTS USUARIOS
@app.route('/api/v1/usuarios', methods=['GET'])     #Endpoint: /usuarios
def usuarios():
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_TODOS_LOS_USUARIOS)).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response=[]
    for row in result:
        response.append({'ID_usuario': row[0],'nombre_usuario': row[1], 'nombre': row[2], 'apellido': row[3], 'email': row[4], 'telefono': row[5]})
    return jsonify(response), 200


@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['GET'])   #Endpoint: /usuarios/porID
def usuario(ID_usuario):    #metodo usuario
    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), {'ID_usuario': ID_usuario}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    if not result:
        return jsonify({'message': f"No se puede encontrar el usuario con ID {ID_usuario}"}), 404
    
    response=[]
    for row in result:
        response.append({'ID_usuario': row[0],'nombre_usuario': row[1], 'nombre': row[2], 'apellido': row[3], 'email': row[4], 'telefono': row[5]})
    return jsonify(response), 200

@app.route('/api/v1/usuarios', methods=['POST'])   #Endpoint: /usuarios
def ingresar_usuario():    #metodo ingresar
    nuevo_usuario = request.get_json()
    keys = ('ID_usuario', 'nombre_usuario', 'nombre', 'apellido', 'email', 'telefono')
    for key in keys:
        if key not in nuevo_usuario:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), params={'ID_usuario': nuevo_usuario['ID_usuario']}).fetchone()
        if result is not None:
            return jsonify({'error': 'El usuario ya existe'}), 400
        conn.execute(text(QUERY_INGRESAR_USUARIO), params=nuevo_usuario)
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify(nuevo_usuario), 201

@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['PUT'])   #Endpoint: /usuarios/porID
def actualizar_usuario(ID_usuario):    #metodo actualizar
    data = request.get_json()

    keys = ('nombre_usuario', 'nombre', 'apellido', 'email', 'telefono')
    for key in keys:
        if key not in data:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), {'ID_usuario': ID_usuario}).fetchall()
        if not result:
            return jsonify({'error': 'No se encontro el usuario'}), 400
        conn.execute(text(QUERY_ACTUALIZAR_USUARIO), params={'ID_usuario': ID_usuario, **data})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'ID_usuario': ID_usuario, **data}), 200


@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['DELETE'])   #Endpoint: /usuarios/porID
def eliminar_usuario(ID_usuario):    #metodo eliminar
    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), {'ID_usuario': ID_usuario}).fetchone()
        if not result:
            return jsonify({'error': 'No se encontro el usuario'}), 400
        conn.execute(text(QUERY_ELIMINAR_USUARIO), params={'ID_usuario': ID_usuario})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'nombre_usuario': result[0], 'nombre': result[1], 'apellido': result[2], 'email': result[3], 'telefono': result[4], 'ID_usuario': result[5]}), 200

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)