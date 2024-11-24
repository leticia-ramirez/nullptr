from flask import Flask, render_template, request, redirect, jsonify

import archivo_reportes
import archivo_incidentes
import archivo_usuarios

#NO OLVIDAR las pre y post

app = Flask(__name__)


#ENDPOINTS REPORTES
@app.route('/api/v1/reportes', methods=['GET'])     #Endpoint: /reportes
def reportes():
    try: 
        result = archivo_reportes.todos_los_reportes()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5], 'horario_reporte': str(row[6])})
    return jsonify(response), 200

@app.route('/api/v1/reportesNovedades', methods=['GET'])     #Endpoint: /reportes Novedades
def reportesNovedades():
    try: 
        result = archivo_reportes.reportes_novedades()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5], 'horario_reporte': str(row[6])})
    return jsonify(response), 200

@app.route('/api/v1/reportes/id/<int:ID_reporte>', methods=['GET'])   #Endpoint: /reportes/porID
def reporte_ID(ID_reporte):    #metodo reporte_ID
    try: 
        result = archivo_reportes.reporte_por_id(ID_reporte)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID_reporte': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'nombre_usuario': row[5], 'provincia': row[6], 'departamento': row[7], 'localidad': row[8], "horario_reporte": str(row[9]), "ID_usuario": row[10]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/localidad', methods=['GET'])   #Endpoint: /reportes/todaslocalidades
def reporte_localidad():    #metodo reporte_todas_localidad
    try: 
        result = archivo_reportes.reporte_localidades()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row[0], 'localidad':row[1], 'direccion_reporte': row[2], 'descripcion': row[3], 'tipo_reporte': row[4], 'fecha_reporte': row[5], 'ID_usuario': row[6]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/localidad/<localidad>', methods=['GET'])   #Endpoint: /filtro por localidades
def reporte_by_localidad(localidad):    
    try: 
        result = archivo_reportes.reporte_por_localidad(localidad)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID_reporte': row[0], 'direccion_reporte': row[1], 'provincia': row[2], 'departamento': row[3], 'localidad': row[4], 'descripcion': row[5], 'tipo_reporte': row[6], 'fecha_reporte': row[7], 'ID_usuario': row[8]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/fecha/<fecha_reporte>', methods=['GET'])   #Endpoint: /reportes/porFecha
def reporte_fecha(fecha_reporte):    #metodo reporte_fecha
    try:
        result = archivo_reportes.reporte_por_fecha(fecha_reporte)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row [0], 'direccion_reporte': row [1], 'descripcion': row [2], 'tipo_reporte': row [3], 'fecha_reporte': row [4], 'ID_usuario': row [5]})
    return jsonify(response), 200

@app.route('/api/v1/reportes/tipo/<tipo_reporte>', methods=['GET'])   #Endpoint: /reportes/porTipoDeReporte
def reporte_tipo(tipo_reporte):    #metodo reporte_tipo
    try:
        result = archivo_reportes.reporte_por_tipo(tipo_reporte)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        result = archivo_reportes.insert_reporte(nuevo_reporte)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(nuevo_reporte), 201


@app.route('/api/v1/reportes/id/<int:ID_reporte>', methods=['PUT'])   #Endpoint: /reportes
def actualizar_reporte(ID_reporte):    #metodo actualizar
    data = request.get_json()

    keys = ('ID_reporte', 'ID_usuario', 'descripcion', 'direccion_reporte', 'fecha_reporte', 'tipo_reporte')
    for key in keys:
        if key not in data:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        result = archivo_reportes.reporte_por_id(ID_reporte)
        if not result:
            return jsonify({'error': 'No se encontro el usuario'}), 400
        archivo_reportes.cambiar_reporte(ID_reporte, data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'ID_reporte': ID_reporte, **data}), 200

@app.route('/api/v1/reportes/<int:ID_reporte>', methods=['DELETE'])   #Endpoint: /reportes/porID
def eliminar_reporte(ID_reporte):    #metodo eliminar
    try:
        result = archivo_reportes.reporte_por_id(ID_reporte)
        if not result:
            return jsonify({'error': 'No se encontro el reporte'}), 400
        archivo_reportes.borra_reporte(ID_reporte)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    result = result[0]
    return jsonify({'ID_reporte': result[0], 'direccion_reporte': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'ID_usuario': result[5]}), 200


#ENDPOINTS INCIDENTES
@app.route('/api/v1/incidentes', methods=['POST'])   #Endpoint: /incidentes
def ingresar_incidente():    #metodo ingresar
    nuevo_incidente = request.get_json()

    keys = ('tipo_reporte', 'direccion_reporte', 'descripcion')
    for key in keys:
        if key not in nuevo_incidente:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        result = archivo_incidentes.insert_incidente(nuevo_incidente)
        nashei = archivo_incidentes.ultimo_incidente()
        nashei = nashei[0][0]

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(str(nashei)), 201


#ENDPOINTS USUARIOS
@app.route('/api/v1/usuarios', methods=['GET'])     #Endpoint: /usuarios
def usuarios():
    try: 
        result = archivo_usuarios.todos_los_usuarios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response=[]
    for row in result:
        response.append({'ID_usuario': row[0],'nombre_usuario': row[1], 'nombre': row[2], 'apellido': row[3], 'email': row[4], 'telefono': row[5]})
    return jsonify(response), 200


@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['GET'])   #Endpoint: /usuarios/porID
def usuario(ID_usuario):    #metodo usuario
    try:
        result = archivo_usuarios.usuarios_por_id(ID_usuario)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        result = archivo_usuarios.usuarios_por_id(nuevo_usuario['ID_usuario'])
        if result is not None:
            return jsonify({'error': 'El usuario ya existe'}), 400
        archivo_usuarios.insert_usuario(nuevo_usuario)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(nuevo_usuario), 201

@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['PUT'])   #Endpoint: /usuarios/porID
def actualizar_usuario(ID_usuario):    #metodo actualizar
    data = request.get_json()

    keys = ('nombre_usuario', 'nombre', 'apellido', 'email', 'telefono')
    for key in keys:
        if key not in data:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        result = archivo_usuarios.usuarios_por_id(ID_usuario)
        if not result:
            return jsonify({'error': 'No se encontro el usuario'}), 400
        archivo_usuarios.cambiar_usuario(ID_usuario, data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'ID_usuario': ID_usuario, **data}), 200


@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['DELETE'])   #Endpoint: /usuarios/porID
def eliminar_usuario(ID_usuario):    #metodo eliminar
    try:
        result = archivo_usuarios.usuarios_por_id(ID_usuario)
        if not result:
            return jsonify({'error': 'No se encontro el usuario'}), 400
        archivo_usuarios.borra_usuario(ID_usuario)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'nombre_usuario': result[0], 'nombre': result[1], 'apellido': result[2], 'email': result[3], 'telefono': result[4], 'ID_usuario': result[5]}), 200

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)