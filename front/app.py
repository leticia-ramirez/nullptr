from flask import Flask, render_template, request, redirect, jsonify, url_for
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/api/v1/"
API_ARG = "https://apis.datos.gob.ar/georef/api/"

#
# Pre: -
# Post: Levanta la vista de home.html.
#
@app.route("/", methods=["GET"])
def home():
    try:
        response = requests.get(API_URL+'reportesNovedades', timeout=3)
        response.raise_for_status()
        reportes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error traer data: {e}")
        reportes = []

    return render_template("home.html", reportes = reportes)

#
# Pre: Recibe la localidad a visualizar.
# Post: Levanta la vista de buscar_zona.html donde se muestran los reportes y ubicacion en mapa.
#
@app.route("/buscarzona", methods=["GET", "POST"])
def buscar():
    if request.method == "GET":
        busqueda = request.args.get("busqueda")
        try:
            response = requests.get(API_URL + "reportes/localidad/" + str(busqueda))
            response.raise_for_status()
            reportes = response.json()

            coordenadas = []
            for reporte in reportes:
                direccion = reporte["direccion_reporte"]
                provincia = reporte["provincia"]
                departamento = reporte["departamento"]

                ubicacion_response = requests.get(
                    f"{API_ARG}direcciones?direccion={direccion}&provincia={provincia}&departamento={departamento}&localidad={busqueda}",
                    timeout=5,
                )
                ubicacion_response.raise_for_status()
                ubicacion = ubicacion_response.json()

                latitud = float(ubicacion["direcciones"][0]["ubicacion"]["lat"])
                longitud = float(ubicacion["direcciones"][0]["ubicacion"]["lon"])
                coordenadas.append({"lat": latitud, "lng": longitud})

            if response:
                return render_template("buscar_zona.html", reportes=reportes, coordenadas=coordenadas)
                
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return render_template("buscar_zona.html", reportes=[], coordenadas=[])

    return render_template("buscar_zona.html")

#
# Pre: Recibe los datos del nuevo reporte a ingresar.
# Post: Levanta la vista de reporte.html y devuelve al backend la informacion recibida.
#
@app.route("/reporte", methods=["GET", "POST"])
def reporte():
    if request.method == "POST":
        provincia = request.form.get("provincia")
        municipio = request.form.get("municipio")
        localidad = request.form.get("localidad")
        direccion = request.form.get("direccion")
        incidente = {
            "tipo_reporte" : request.form.get("tipo_reporte"),
            "direccion_reporte" : direccion,
            "descripcion" : request.form.get("descripcion"),
        }
        id_incidente = requests.post(API_URL+"incidentes", json = incidente, timeout = 5)
        id_incidente.raise_for_status()
        id_incidente = id_incidente.json()
        data = {
            "provincia": provincia,
            "departamento" : municipio,
            "localidad" : localidad,
            "fecha_reporte" : request.form.get("fecha"),
            "horario_reporte" : request.form.get("hora"),
            "ID_incidente" : id_incidente,
            "ID_usuario" : request.form.get("ID_usuario")
        }
        try:
            response = requests.post(API_URL+'reportes', json = data, timeout = 5)
            response.raise_for_status()
            datos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")
            datos = []
        return render_template("reporte.html", datos = datos)
    return render_template("reporte.html")

#
# Pre: Recibe los datos de ubicacion del reporte.
# Post: Devuelve las coordenadas de la ubicacion.
#
@app.route("/get_coordinates", methods=["GET"])
def get_coordinates():
    provincia = request.args.get("provincia")
    municipio = request.args.get("municipio")
    localidad = request.args.get("localidad")
    direccion = request.args.get("direccion")

    try:
        response = requests.get(
            f"{API_ARG}direcciones?direccion={direccion}&provincia={provincia}&departamento={municipio}&localidad={localidad}",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        if data and data.get("direcciones"):
            ubicacion = data["direcciones"][0]["ubicacion"]
            return jsonify({"lat": ubicacion["lat"], "lon": ubicacion["lon"]})
        else:
            return jsonify({"error": "No se encontraron coordenadas"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#
# Pre: -
# Post: Levanta la vista de MisReportes.html.
#
@app.route("/misreportes") 
def mreporte():
    return render_template("MisReportes.html")

#
# Pre: Recibe del id del usuario.
# Post: Devuelve en MisReportes.html la informacion de los reportes de ese usuario.
#
@app.route("/misreportes/usuario/<int:id>")
def mereporteu(id):
    try:
        response = requests.get(API_URL + 'reportes/usuario/' + str(id))
        response.raise_for_status()
        reportes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        reportes = []
    return render_template("MisReportes.html", reportes = reportes)

#
# Pre: Recibe el id del reporte.
# Post: Levanta la vista de modificar.html y devuelve los datos a modificar en el backend.
#
@app.route('/modificar/<int:id>', methods=['GET','POST', 'PUT'])
def modificar(id):
    datos = requests.get(API_URL+'reportes/id/'+str(id)).json()

    if request.method == 'POST':
        data = {
            "ID_reporte": request.form.get('id_reporte'),
            "descripcion": request.form.get('descripcion'),
            "direccion_reporte": request.form.get('direccion_reporte'),
            "fecha_reporte": request.form.get('fecha_reporte'),
            "tipo_reporte": request.form.get('incidencia'),
            "ID_usuario" : request.form.get('id_usuario')
        }
        try:
            response = requests.put(API_URL+"reportes/id/"+str(id), json = data)
            response.raise_for_status()
            if response:
                return redirect(url_for('mreporte'))
                
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")
                
    return render_template('modificar.html', datos=datos[0], id=id)

#
# Pre: Recibe el id del reporte.
# Post: Elimina desde el backend el reporte con ese id.
#
@app.route("/elimacion/<int:id>") 
def eliminar_reporte(id):
    try:
        response = requests.delete(API_URL+'reportes/'+str(id))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return redirect(url_for("mreporte"))

#
# Pre: Recibe el id del reporte.
# Post: Levanta la vista de masinformacion.html y muestra los datos del reporte con ese id.
#
@app.route("/misreportes/<id>")
def mreporte_id(id): 
    try:
        response = requests.get(API_URL+'reportes/id/'+str(id))
        response.raise_for_status()
        datos_reporte = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        datos_reporte = []

    return render_template("masinformacion.html", datos = datos_reporte)

#
# Pre: Recibe el formulario de ingreso de usuario.
# Post: Levanta la vista de signin.html y loggea al usuario que se encuentre en la base de datos.
#
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        nombre_usuario = request.form.get('usuario')
        try:
            response = requests.get(API_URL+"usuarios")
            response.raise_for_status()
            usuarios = response.json()
            intento = {}
            for usuario in usuarios:
                if nombre_usuario == usuario["nombre_usuario"]:
                    intento = usuario
            if intento:
                return render_template("home.html", logged = True, usuario = intento)
            else:
                return render_template("signin.html", logged = False)
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")

    return render_template('signin.html')

#
# Pre: Recibe el formulario de registro de usuario.
# Post: Levanta la vista de signup.html e ingresa al usuario en la base de datos.
#
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = {
            "nombre_usuario" : request.form.get('usuario'),
            "nombre" : request.form.get('nombre'),
            "apellido" : request.form.get('apellido'),
            "email" : request.form.get('email'),
            "telefono" : request.form.get('telefono')
        }
        try:
            requests.post(API_URL+"usuarios", json = data)
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")

    return render_template("signup.html")

#
# Pre: Recibe el id del reporte.
# Post: Devuelve los datos del reporte en una nueva vista.
#
@app.route("/mireportes/<id>")
def mreporte_info(id):
    try:
        response = requests.get(API_URL+'reportes/id/'+str(id))
        response.raise_for_status()
        datos_reporte = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        datos_reporte = []

    return render_template("reportes-masinfo.html", datos = datos_reporte)

#
# Pre: -
# Post: Levanta la vista de download.html.
#
@app.route("/download")
def download():
    return render_template("/download.html")

#
# Pre: Recibe el formulario de contacto.
# Post: Levanta la vista de contacto.html y redirecciona al home.
#
@app.route("/contacto", methods=['POST','GET'])
def contacto():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('contacto.html')

#
# Pre: -
# Post: Levanta la vista de error.html perteneciente al error 404.
#
@app.errorhandler(404)
def error(e):
    return render_template('error.html')

#
# Pre: -
# Post: Levanta la vista de error400.html.
#
@app.errorhandler(400)
def error2(e):
    return render_template('error400.html')

#
# Pre: -
# Post: Levanta la vista de error500.html.
#
@app.errorhandler(500)
def error3(e):
    return render_template('error500.html')

if __name__ == "__main__":
    app.run(debug=True, port="5000")