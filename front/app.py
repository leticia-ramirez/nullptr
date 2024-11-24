from flask import Flask, render_template, request, redirect, jsonify, url_for
import requests
import pprint
app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/api/v1/"
API_ARG = "https://apis.datos.gob.ar/georef/api/"

@app.route("/", methods=["GET", "POST"]) #endpoint reporte
def home():
    try:
        response = requests.get(API_URL+'reportesNovedades', timeout=3)
        response.raise_for_status()
        reportes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error traer data: {e}")
        reportes = []

    return render_template("home.html", reportes = reportes)

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


@app.route("/reporte", methods=["GET", "POST"])
def reporte():
    if request.method == "POST":
        provincia = request.form.get("provincia")
        municipio = request.form.get("municipio")
        localidad = request.form.get("localidad")
        direccion = request.form.get("direccion")
#       Lo vamos a necesitar para el mapa, no borrar
        ubicacion = requests.get(f"{API_ARG}direcciones?direccion={direccion}&provincia={provincia}&departamento={municipio}&localidad={localidad}", timeout = 5)
        ubicacion.raise_for_status()
        ubicacion = ubicacion.json()
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
            "ubicacion" : f'{ubicacion["direcciones"][0]["ubicacion"]["lat"]} {ubicacion["direcciones"][0]["ubicacion"]["lon"]}',
            "fecha_reporte" : request.form.get("fecha"),
            "horario_reporte" : request.form.get("hora"),
            "ID_incidente" : id_incidente,
            "ID_usuario" : request.form.get("ID_usuario")
        }
        print(data)
        try:
            response = requests.post(API_URL+'reportes', json = data, timeout = 5)
            response.raise_for_status()
            datos = response.json()
            print(datos)
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")
            datos = []
            return render_template("reporte.html", datos = datos)
    return render_template("reporte.html")

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

@app.route("/misreportes") 
def mreporte():
    try:
        response = requests.get(API_URL+'reportes')
        response.raise_for_status()
        reportes = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        reportes = []
    return render_template("MisReportes.html", reportes = reportes)

@app.route('/modificar/<int:id>', methods=['GET','POST', 'PUT'])#endpoint modificar reporte (aun no funciona)
def modificar(id):
    datos = requests.get(API_URL+'reportes/id/'+str(id)).json()

    if request.method == 'POST':
        data = {
            "ID_reporte": request.form.get('id_reporte'),
            "descripcion": request.form.get('descripcion'),
            "direccion_reporte": request.form.get('direccion_reporte'),
            "fecha_reporte": request.form.get('fecha_reporte'),
            "tipo_reporte": request.form.get('incidencia'),
            "ID_usuario" : 1
        }
        try:
            response = requests.put(API_URL+"reportes/id/"+str(id), json = data)
            response.raise_for_status()
            if response:
                return redirect(url_for('mreporte'))
                
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")
                
    return render_template('modificar.html', datos=datos[0], id=id)

@app.route("/elimacion/<int:id>") #endpoint eliminar reportes de mreporte
def eliminar_reporte(id):
    try:
        response = requests.delete(API_URL+'reportes/'+str(id))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return redirect(url_for("mreporte"))

@app.route("/misreportes/<id>")
def mreporte_id(id): #endpoint para mostrar todos los reportes
    try:
        response = requests.get(API_URL+'reportes/id/'+str(id))
        response.raise_for_status()
        datos_reporte = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        datos_reporte = []

    return render_template("masinformacion.html", datos = datos_reporte)

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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = {
            "nombre_usuario" : request.form.get('usuario'),
            "nombre" : request.form.get('usuario'),
            "apellido" : request.form.get('apellido'),
            "email" : request.form.get('email'),
            "telefono" : request.form.get('telefono')
        }
        try:
            requests.post(API_URL+"usuarios", json = data)
        except requests.exceptions.RequestException as e:
            print(f"Error pushing data: {e}")

    return render_template("signup.html")

@app.route("/download")
def download():
    return render_template("/download.html")

@app.route("/contacto", methods=['POST','GET'])
def contacto():
    return render_template("contacto.html")

@app.errorhandler(404)
def error(e):
    return render_template('error.html')

@app.errorhandler(400)
def error2(e):
    return render_template('error400.html')

@app.errorhandler(500)
def error3(e):
    return render_template('error500.html')

if __name__ == "__main__":
    app.run(debug=True, port="5001")