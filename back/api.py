from flask import Flask, render_template, request, redirect, jsonify

import archivo_reportes
import archivo_incidentes
import archivo_usuarios

app = Flask(__name__)


"""----------------------------------"""
"""------- ENDPOINTS REPORTES -------"""
"""----------------------------------"""

#
# Pre: Recibe desde la base de datos todos los reportes existentes.
# Post: Devuelve los reportes con sus elementos en formato JSON.
#
@app.route('/api/v1/reportes', methods=['GET'])                                  
def reportes():
    try: 
        result = archivo_reportes.todos_los_reportes()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5], 'horario_reporte': str(row[6])})
    return jsonify(response), 200

#
# Pre: Recibe desde la base de datos los ultimos cinco reportes ordenados por fecha descendiente.
# Post: Devuelve los reportes con sus elementos en formato JSON.
#
@app.route('/api/v1/reportesNovedades', methods=['GET'])                         
def reportesNovedades():
    try: 
        result = archivo_reportes.reportes_novedades()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5], 'horario_reporte': str(row[6])})
    return jsonify(response), 200

#
# Pre: Recibe por parametro el ID del reporte y toma desde la base el reporte que coincida con ese ID.
# Post: Devuelve el reporte, que coincidió, con sus elementos en formato JSON.
#
@app.route('/api/v1/reportes/id/<int:ID_reporte>', methods=['GET'])             
def reporte_ID(ID_reporte):    
    try: 
        result = archivo_reportes.reporte_por_id(ID_reporte)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID_reporte': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'nombre_usuario': row[5], 'provincia': row[6], 'departamento': row[7], 'localidad': row[8], "horario_reporte": str(row[9]), "ID_usuario": row[10]})
    return jsonify(response), 200


#
# Pre: Recibe por parametro la localidad del reporte y toma desde la base todos los reportes que coincidan con esa localidad.
# Post: Devuelve los reportes, que coincidieron, con sus elementos en formato JSON.
#
@app.route('/api/v1/reportes/localidad/<localidad>', methods=['GET'])         
def reporte_by_localidad(localidad):    
    try: 
        result = archivo_reportes.reporte_por_localidad(localidad)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID_reporte': row[0], 'direccion_reporte': row[1], 'provincia': row[2], 'departamento': row[3], 'localidad': row[4], 'descripcion': row[5], 'tipo_reporte': row[6], 'fecha_reporte': row[7], 'ID_usuario': row[8]})
    return jsonify(response), 200

#
# Pre: Recibe por parametro el ID del usuario y toma desde la base todos los reportes que coincidan con ese ID de usuario.
# Post: Devuelve los reportes, que coincidieron, con sus elementos en formato JSON.
#
@app.route('/api/v1/reportes/usuario/<ID_usuario>', methods=['GET'])                     
def reporte_usuario(ID_usuario):    
    try:
        result = archivo_reportes.reporte_por_usuario(ID_usuario)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'ID': row[0], 'direccion_reporte': row[1], 'descripcion': row[2], 'tipo_reporte': row[3], 'fecha_reporte': row[4], 'ID_usuario': row[5], 'horario_reporte': str(row[6])})
    return jsonify(response), 200

#
# Pre: Recibe desde un formulario los datos de las keys solicitadas.
# Post: Devuelve los reportes con sus elementos en formato JSON al metodo insert_reporte y genera un codigo 201 si fue exitoso.
#
@app.route('/api/v1/reportes', methods=['POST'])   
def ingresar_reporte():    
    nuevo_reporte = request.get_json()

    keys = ('provincia', 'departamento', 'localidad', 'fecha_reporte', 'horario_reporte', 'ID_incidente', 'ID_usuario')
    for key in keys:
        if key not in nuevo_reporte:
            return jsonify({'message': f"Falta el dato {key}"}), 400    

    try:
        archivo_reportes.insert_reporte(nuevo_reporte)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(nuevo_reporte), 201

#
# Pre: Recibe por parametro el ID del reporte y toma desde un formulario los datos de las keys solicitadas, a su vez busca en 
#      la base de datos los reportes que coincida con el ID.
# Post: Devuelve los reportes con sus elementos en formato JSON al metodo cambiar_reporte y genera un codigo 200 si fue exitoso.
#
@app.route('/api/v1/reportes/id/<int:ID_reporte>', methods=['PUT'])   
def actualizar_reporte(ID_reporte):    
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

#
# Pre: Recibe por parametro el ID del reporte y toma desde la base el reporte que coincidan con ese ID.
# Post: Elimina en la base de datos el reporte que coincidió.
#
@app.route('/api/v1/reportes/<int:ID_reporte>', methods=['DELETE'])  
def eliminar_reporte(ID_reporte):   
    try:
        result = archivo_reportes.reporte_por_id(ID_reporte)
        if not result:
            return jsonify({'error': 'No se encontro el reporte'}), 400
        archivo_reportes.borra_reporte(ID_reporte)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    result = result[0]
    return jsonify({'ID_reporte': result[0], 'direccion_reporte': result[1], 'descripcion': result[2], 'tipo_reporte': result[3], 'fecha_reporte': result[4], 'ID_usuario': result[5]}), 200


"""----------------------------------"""
"""------ ENDPOINTS INCIDENTES ------"""
"""----------------------------------"""

#
# Pre: Recibe desde un formulario los datos de las keys solicitadas.
# Post: Devuelve los incidentes con sus elementos en formato JSON al metodo insert_incidente y genera un codigo 201 si fue exitoso.
#
@app.route('/api/v1/incidentes', methods=['POST'])                              
def ingresar_incidente():    
    nuevo_incidente = request.get_json()

    keys = ('tipo_reporte', 'direccion_reporte', 'descripcion')
    for key in keys:
        if key not in nuevo_incidente:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        archivo_incidentes.insert_incidente(nuevo_incidente)
        incidente = archivo_incidentes.ultimo_incidente()
        incidente = incidente[0][0]

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(str(incidente)), 201


"""----------------------------------"""
"""------- ENDPOINTS USUARIOS -------"""
"""----------------------------------"""

#
# Pre: Recibe desde la base de datos todos los usuarios existentes.
# Post: Devuelve los usuarios con sus elementos en formato JSON.
#
@app.route('/api/v1/usuarios', methods=['GET'])                                            
def usuarios():
    try: 
        result = archivo_usuarios.todos_los_usuarios()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response=[]
    for row in result:
        response.append({'ID_usuario': row[0],'nombre_usuario': row[1], 'nombre': row[2], 'apellido': row[3], 'email': row[4], 'telefono': row[5]})
    return jsonify(response), 200

#
# Pre: Recibe por parametro el ID del usuario y toma desde la base de datos al usuario que coincida con ese ID.
# Post: Devuelve el usuario, que coincide, con sus elementos en formato JSON.
#
@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['GET'])                    
def usuario(ID_usuario):    
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

#
# Pre: Recibe desde un formulario los datos de las keys solicitadas.
# Post: Devuelve los usuarios con sus elementos en formato JSON al metodo insert_usuario y genera un codigo 201 si fue exitoso.
#
@app.route('/api/v1/usuarios', methods=['POST'])  
def ingresar_usuario():    
    nuevo_usuario = request.get_json()

    keys = ('nombre_usuario', 'nombre', 'apellido', 'email', 'telefono')
    for key in keys:
        if key not in nuevo_usuario:
            return jsonify({'message': f"Falta el dato {key}"}), 400

    try:
        archivo_usuarios.insert_usuario(nuevo_usuario)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(nuevo_usuario), 201

#
# Pre: Recibe por parametro el ID del usuario y toma desde un formulario los datos de las keys solicitadas, a su vez busca en 
#      la base de datos el usuario que coincida con el ID.
# Post: Devuelve el usuario con sus elementos en formato JSON al metodo cambiar_usuario y genera un codigo 200 si fue exitoso.
#
@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['PUT']) 
def actualizar_usuario(ID_usuario):    
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

#
# Pre: Recibe por parametro el ID del usuario y toma desde la base el usuario que coincidan con ese ID.
# Post: Elimina en la base de datos el usuario que coincidió.
#
@app.route('/api/v1/usuarios/<int:ID_usuario>', methods=['DELETE'])  
def eliminar_usuario(ID_usuario):    
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