from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker, scoped_session

#QUERY REPORTES
QUERY_TODOS_LOS_REPORTES = "SELECT ID, ubicacion, descripcion, tipo_reporte, fecha_reporte, id_user FROM reportes"

QUERY_REPORTE = "SELECT ID, ubicacion, descripcion, tipo_reporte, fecha_reporte, id_user FROM reportes WHERE ID = :ID"

QUERY_INGRESAR_REPORTE = "INSERT INTO reportes (ID, ubicacion, descripcion, tipo_reporte, fecha_reporte, id_user) VALUES (:ID, :ubicacion, :descripcion, :tipo_reporte, :fecha_reporte, :id_user)"

QUERY_ACTUALIZAR_REPORTE = "UPDATE reportes SET ID = :ID, ubicacion = :ubicacion, descripcion = :descripcion, tipo_reporte = :tipo_reporte, fecha_reporte = :fecha_reporte, id_user = :id_user WHERE ID = :ID"

QUERY_ELIMINAR_REPORTE = "DELETE FROM reportes WHERE ID = :ID"

#QUERY USUARIOS
QUERY_TODOS_LOS_USUARIOS = "SELECT username, nombre, email, telefono FROM usuarios"

QUERY_USUARIO = "SELECT username, nombre, email, telefono FROM usuarios WHERE id_usuario = :id_usuario"

QUERY_INGRESAR_USUARIO = "INSERT INTO usuarios (username, nombre, email, telefono) VALUES (:username, :nombre, :email, :telefono)"

QUERY_ACTUALIZAR_USUARIO = "UPDATE usuarios SET username = :username, nombre = :nombre, email = :email, telefono = :telefono WHERE id_usuario = :id_usuario"

QUERY_ELIMINAR_USUARIO = "DELETE FROM usuarios WHERE id_usuario = :id_usuario"

#string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
engine = create_engine("mysql://root:root@localhost:3306/TP_IDS")

Session = scoped_session(sessionmaker(bind=engine)) #para empezar a tomar consultas

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/reporte")
def reporte():
    return render_template("reporte.html")

@app.route("/misreportes")
def mreporte():
    return render_template("MisReportes.html")

@app.route("/download")
def download():
    return render_template("/download.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


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
        response.append({'ID': row[0], 'ubicacion': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'id_user': row[5]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/<int:ID>', methods=['GET'])   #Endpoint: /reportes/porID
def reporte(ID):    #metodo reporte
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'ID': ID}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    if len(result) == 0:
        return jsonify({'message': f"No se encontró el reporte nro {ID}"}), 404
    
    result = result[0]
    return jsonify({'ID': result[0], 'ubicacion': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'id_user': result[5]}), 200

@app.route('/api/v1/reportes/<fecha_reporte>', methods=['GET'])   #Endpoint: /reportes/porFecha
def reporte_fecha(fecha_reporte):    #metodo reporte_fecha
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'fecha_reporte': fecha_reporte}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    if len(result) == 0:
        return jsonify({'message': f"No se encontró el reporte con fecha {fecha_reporte}"}), 404
    
    result = result[0]
    return jsonify({'ID': result[0], 'ubicacion': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'id_user': result[5]}), 200

@app.route('/api/v1/reportes/<tipo_reporte>', methods=['GET'])   #Endpoint: /reportes/porTipoDeReporte
def reporte_tipo(tipo_reporte):    #metodo reporte_tipo
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'tipo_reporte': tipo_reporte}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    if len(result) == 0:
        return jsonify({'message': f"No se encontró reporte con el tipo de reporte {tipo_reporte}"}), 404
    
    result = result[0]
    return jsonify({'ID': result[0], 'ubicacion': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'id_user': result[5]}), 200


@app.route('/api/v1/reportes', methods=['POST'])   #Endpoint: /reportes
def ingresar_reporte():    #metodo ingresar
    nuevo_reporte = request.get_json()

    keys = ('ID', 'ubicacion', 'descripcion', 'tipo_reporte', 'fecha_reporte', 'id_user')
    for key in keys:
        if key not in nuevo_reporte:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_INGRESAR_REPORTE), params={'ID': nuevo_reporte['ID']})
        if len(result) > 0:
            return jsonify({'error': 'Ya existe un reporte con ese ID'}), 400
        conn.execute(text(QUERY_INGRESAR_REPORTE), params=nuevo_reporte)
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify(nuevo_reporte), 201


@app.route('/api/v1/reportes/<int:ID>', methods=['PUT'])   #Endpoint: /reportes
def actualizar_reporte(ID):    #metodo actualizar
    data = request.get_json()

    keys = ('ID', 'ubicacion', 'descripcion', 'tipo_reporte', 'fecha_reporte', 'id_user')
    for key in keys:
        if key not in data:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'ID': ID})
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el reporte'}), 400
        conn.execute(text(QUERY_ACTUALIZAR_REPORTE), params={'ID': ID, **data})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'ID': ID, **data}), 200

@app.route('/api/v1/reportes/<int:ID>', methods=['DELETE'])   #Endpoint: /reportes/porID
def eliminar_reporte(ID):    #metodo eliminar
    try:
        conn = Session()
        result = conn.execute(text(QUERY_REPORTE), {'ID': ID})
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el reporte'}), 400
        conn.execute(text(QUERY_ELIMINAR_REPORTE), params={'ID': ID, **data})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'ID': result[0], 'ubicacion': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'id_user': result[5]}), 200


#ENDPOINTS USUARIOS
@app.route('/api/v1/usuarios', methods=['GET'])     #Endpoint: /usuarios
def usuarios():
    try: 
        conn = Session()
        result = conn.execute(text(QUERY_TODOS_LOS_USUARIOS)).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    conn.close()

    response = []
    for row in result:
        response.append({'username': row[0], 'nombre': row[1], 'email': row[2], 'telefono': row[3]})
    return jsonify(response), 200


@app.route('/api/v1/usuarios/<int:id_usuario>', methods=['GET'])   #Endpoint: /usuarios/porID
def usuario(id_usuario):    #metodo usuario
    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), {'id_usuario': id_usuario}).fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    if len(result) == 0:
        return jsonify({'message': f"Could not find user with username {username}"}), 404
    
    result = result[0]
    return jsonify({'username': result[0], 'nombre': result[1], 'email': result[2], 'telefono': result[3]}), 200


@app.route('/api/v1/usuarios', methods=['POST'])   #Endpoint: /usuarios
def ingresar_usuario():    #metodo ingresar
    nuevo_usuario = request.get_json()

    keys = ('username', 'nombre', 'email', 'telefono')
    for key in keys:
        if key not in nuevo_usuario:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_INGRESAR_USUARIO), params={'id_usuario': nuevo_usuario['id_usuario']})
        if len(result) > 0:
            return jsonify({'error': 'El usuario ya existe'}), 400
        conn.execute(text(QUERY_INGRESAR_USUARIO), params=nuevo_usuario)
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify(nuevo_usuario), 201

@app.route('/api/v1/usuarios/<int:id_usuario>', methods=['PUT'])   #Endpoint: /usuarios/porID
def actualizar_usuario(id_usuario):    #metodo actualizar
    data = request.get_json()

    keys = ('username', 'nombre', 'email', 'telefono')
    for key in keys:
        if key not in data:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), {'id_usuario': id_usuario})
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el usuario'}), 400
        conn.execute(text(QUERY_ACTUALIZAR_USUARIO), params={'id_usuario': id_usuario, **data})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'id_usuario': id_usuario, **data}), 200


@app.route('/api/v1/usuarios/<int:id_usuario>', methods=['DELETE'])   #Endpoint: /usuarios/porID
def eliminar_usuario(id_usuario):    #metodo eliminar
    try:
        conn = Session()
        result = conn.execute(text(QUERY_USUARIO), {'id_usuario': id_usuario})
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el usuario'}), 400
        conn.execute(text(QUERY_ELIMINAR_USUARIO), params={'id_usuario': id_usuario, **data})
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    conn.close()

    return jsonify({'username': result[0], 'nombre': result[1], 'email': result[2], 'telefono': result[3]}), 200



if __name__ == "__main__":
    app.run(debug=True)